# data_loading.py

import sys

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
            # print(f"### {node['name']}: {node['description']}")
            text = f"{node['name']}: {node['description']}"
            node_features.append(self._encode_text(text))
        
        # 2. Process examples (which primarily have a 'text' field)
        for example in self.examples:
            node_features.append(self._encode_text(example['text']))
            
        return torch.stack(node_features)
    
    def _create_labels(self) -> torch.Tensor:
        """
        Create a combined labels tensor for:
        - 3 Common Factors (IDs 1..3)
        - 2 Intervention Concepts (IDs 4..5)
        - 7 Skills (IDs 6..12)
        Total columns = 3 + 2 + 7 = 12

        If an example row has factor_id=1, that sets column 0 to 1.
        If factor_id=2 => col 1 = 1, factor_id=3 => col 2 = 1
        If ic_id=4 => col 3=1, ic_id=5 => col 4=1
        If skill_id=6 => col 5=1, 7 => col 6=1, ... 12 => col 11=1
        """
        num_examples = len(self.examples)

        # We hardcode that there are 3 CF, 2 IC, 7 skills => total 12 columns
        num_factors = 3
        num_intervention_concepts = 2
        num_skills = 7
        total_cols = num_factors + num_intervention_concepts + num_skills  # 12

        labels = torch.zeros((num_examples, total_cols), dtype=torch.float)
        # print(f"Examples\n{self.examples}")
        for i, example in enumerate(self.examples):
            # Factor ID in [1..3]
            factor_id = int(example.get('CF_id', 0))
            if 1 <= factor_id <= 3:
                factor_idx = factor_id - 1        # CF 1->col0, 2->col1, 3->col2
                labels[i, factor_idx] = 1.0

            # IC ID in [4..5]
            ic_id = int(example.get('IC_id', 0))
            if 4 <= ic_id <= 5:
                # e.g. ID=4 => index=0 => column=3; ID=5 => index=1 => column=4
                ic_idx = (ic_id - 4) + num_factors
                labels[i, ic_idx] = 1.0

            # Skill ID in [6..12]
            skill_id = int(example.get('skill_id', 0))
            if 6 <= skill_id <= 12:
                # e.g. ID=6 => index=0 => column=5; ID=12 => index=6 => column=11
                skill_offset = num_factors + num_intervention_concepts  # 3 + 2 = 5
                skill_idx = (skill_id - 6) + skill_offset
                labels[i, skill_idx] = 1.0
                   
            # print(f"Example {i}: factor={factor_id}, ic={ic_id}, skill={skill_id}")

        # print("Final label tensor shape:", labels.shape)
        # print(labels)
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


def main():
    # 1) Get filepath from command-line or hardcode
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        # Provide a default CSV if none is passed
        filepath = "data/htc_examples_ids.csv"
    
    print(f"Using CSV: {filepath}")
    
    # 2) Instantiate the dataset
    dataset = TherapeuticDataset(filepath)
    
    # 3) Call _create_labels() to test label creation
    print("Testing _create_labels()...")
    labels = dataset._create_labels()
    print("Labels Tensor Shape:", labels.shape)
    print("Labels Tensor:")
    print(labels)
    
    # 4) Optionally, create the full PyG Data object to verify the entire pipeline
    print("\nTesting create_pyg_data()...")
    pyg_data = dataset.create_pyg_data()
    print("PyG Data object created.")
    print("x shape:", pyg_data.x.shape)
    print("y shape:", pyg_data.y.shape)
    print("edge_index shape:", pyg_data.edge_index.shape)
    print("train_mask sum:", pyg_data.train_mask.sum())
    print("val_mask sum:", pyg_data.val_mask.sum())
    print("test_mask sum:", pyg_data.test_mask.sum())
    
    print("\nDone.")

if __name__ == "__main__":
    main()