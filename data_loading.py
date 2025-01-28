# data_loading.py

import torch
from torch_geometric.data import Data
from transformers import AutoTokenizer, AutoModel
from example_data import get_node_data, get_edge_indices
from typing import Tuple
import numpy as np

class TherapeuticDataset:
    def __init__(self, filepath: str):
        """
        Initialize the dataset with a given CSV filepath.
        - Loads all node data (root, factors, ICs, skills, examples) at once.
        - Instantiates tokenizer and BERT model for text encoding.
        """
        self.filepath = filepath
        
        # Load node data once and store it
        (self.root,
         self.factors,
         self.intervention_concepts,
         self.skills,
         self.examples) = get_node_data(self.filepath)

        self.tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
        self.bert_model = AutoModel.from_pretrained('bert-base-uncased')
        self.hidden_size = 768  # BERT base hidden size
    
    def _encode_text(self, text: str) -> torch.Tensor:
        """Encode text using BERT (average-pooled last hidden state)."""
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=128
        )
        with torch.no_grad():
            outputs = self.bert_model(**inputs)
        # Average-pool across the sequence length (dim=1)
        return outputs.last_hidden_state.mean(dim=1).squeeze()
    
    def _create_node_features(self) -> torch.Tensor:
        """Create node features from text descriptions."""
        node_features = []
        
        # 1. Process root, factors, ICs, skills
        for node in self.root + self.factors + self.intervention_concepts + self.skills:
            text = f"{node['name']} {node['description']}"
            node_features.append(self._encode_text(text))
        
        # 2. Process examples (which primarily have a 'text' field)
        for example in self.examples:
            node_features.append(self._encode_text(example['text']))
        print(node_features)
        return torch.stack(node_features)
    
    def _create_labels(self) -> torch.Tensor:
        """
        Create a combined labels tensor for factors + intervention_concepts + skills.
        Each example can have multiple active labels (one-hot or multi-hot).
        """
        num_examples = len(self.examples)
        num_factors = len(self.factors)
        num_intervention_concepts = len(self.intervention_concepts)
        num_skills = len(self.skills)
        
        # Shape: [num_examples, num_factors + num_intervention_concepts + num_skills]
        labels = torch.zeros((num_examples, num_factors + num_intervention_concepts + num_skills))
        print(f"labels shape: {labels.shape}")
        
        for i, example in enumerate(self.examples):
            # Convert string IDs to int if necessary (depending on how example data is loaded)
            factor_id = int(example['factor_id'])
            ic_id = int(example['ic_id'])
            skill_id = int(example['skill_id'])
            
            # Factors are indexed from 1..N, so shift to 0-based
            factor_idx = factor_id - 1
            labels[i, factor_idx] = 1
            
            # Intervention Concepts: offset by num_factors
            ic_idx = (ic_id - 1) + num_factors
            labels[i, ic_idx] = 1
            
            # Skills: offset by num_factors + num_intervention_concepts
            # If your skill IDs also start at 1, then offset it the same way
            # (But in your original code, skill_id started at 4, so adjust accordingly)
            # For example, if your skill IDs are 4..10, shift them down by 4 to be zero-based.
            skill_offset = num_factors + num_intervention_concepts
            # skill_id (4..10) -> (0..6) after subtracting 4
            print(f"skill_id: {skill_id}, skill_offset: {skill_offset}")
            skill_idx = (skill_id - 6) + skill_offset
            labels[i, skill_idx] = 1
        print(f"New labels shape: {labels.shape}")
        return labels
    
    def encode_new_text(self, text: str) -> torch.Tensor:
        """Public method to encode arbitrary new text for inference."""
        return self._encode_text(text)
    
    def create_pyg_data(self) -> Data:
        """
        Create a PyG (PyTorch Geometric) Data object:
         - x: node features
         - edge_index: graph edges
         - y: multi-hot labels (factors, ICs, skills)
         - train_mask, val_mask, test_mask: boolean masks for splitting
        """
        # 1. Node features
        x = self._create_node_features()
        
        # 2. Edge indices
        # Pass the same filepath to get_edge_indices
        edge_index = torch.tensor(get_edge_indices(self.filepath), dtype=torch.long).t()
        
        # 3. Labels
        labels = self._create_labels()
        
        # 4. Create train/val/test masks for example nodes only
        num_examples = len(self.examples)
        indices = torch.randperm(num_examples)
        
        train_mask = torch.zeros(x.size(0), dtype=torch.bool)
        val_mask = torch.zeros(x.size(0), dtype=torch.bool)
        test_mask = torch.zeros(x.size(0), dtype=torch.bool)
        
        # The examples are appended after root, factors, ICs, skills in _create_node_features
        # so we find the offset index where examples start:
        example_start_idx = (
            len(self.root)
            + len(self.factors)
            + len(self.intervention_concepts)
            + len(self.skills)
        )
        
        # Split examples into 60% train, 20% val, 20% test
        train_end = int(0.6 * num_examples)
        val_end = int(0.8 * num_examples)
        
        train_idx = indices[:train_end]
        val_idx = indices[train_end:val_end]
        test_idx = indices[val_end:]
        
        train_mask[example_start_idx + train_idx] = True
        val_mask[example_start_idx + val_idx] = True
        test_mask[example_start_idx + test_idx] = True
        
        # Create a full label matrix for all nodes (non-examples remain zero)
        full_labels = torch.zeros((x.size(0), labels.size(1)))
        full_labels[example_start_idx:example_start_idx + num_examples] = labels
        
        return Data(
            x=x,
            edge_index=edge_index,
            y=full_labels,  # Combined factor+IC+skill labels
            train_mask=train_mask,
            val_mask=val_mask,
            test_mask=test_mask
        )


def load_data(filepath: str) -> Tuple[Data, TherapeuticDataset]:
    """
    Helper function: 
      1) Instantiates the dataset with the given filepath
      2) Creates the PyG Data object
      3) Returns (Data, dataset) so you can use `dataset.encode_new_text(...)` for inference.
    """
    dataset = TherapeuticDataset(filepath=filepath)
    data = dataset.create_pyg_data()
    return data, dataset