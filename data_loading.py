# data_loading.py
import torch
from torch_geometric.data import Data, Dataset
from transformers import AutoTokenizer, AutoModel
from example_data import get_node_data, get_edge_indices, get_example_labels
from typing import Tuple, List, Optional
import numpy as np

class TherapeuticDataset:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
        self.bert_model = AutoModel.from_pretrained('bert-base-uncased')
        self.hidden_size = 768  # BERT base hidden size
        
    def _encode_text(self, text: str) -> torch.Tensor:
        """Encode text using BERT"""
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=128)
        with torch.no_grad():
            outputs = self.bert_model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).squeeze()
    
    def _create_node_features(self) -> torch.Tensor:
        """Create node features from text descriptions"""
        root, factors, skills, examples = get_node_data()
        node_features = []
        
        # Process each type of node
        for node in root + factors + skills:
            text = f"{node['name']} {node['description']}"
            node_features.append(self._encode_text(text))
            
        # Process examples
        for example in examples:
            node_features.append(self._encode_text(example['text']))
            
        return torch.stack(node_features)
    
    def _create_labels(self) -> torch.Tensor:
        """Create combined labels tensor for factors and skills"""
        _, _, skills, examples = get_node_data()
        num_examples = len(examples)
        num_factors = 3  # Number of common factors
        num_skills = len(skills)
        
        # Create combined labels tensor: [num_examples, num_factors + num_skills]
        labels = torch.zeros((num_examples, num_factors + num_skills))
        
        for i, example in enumerate(examples):
            # One-hot encoding for factors
            factor_idx = example['factor_id'] - 1  # Convert to 0-based index
            labels[i, factor_idx] = 1
            
            # Binary label for skills
            skill_idx = example['skill_id'] - 4 + num_factors  # Adjust skill index
            labels[i, skill_idx] = 1
            
        return labels
    
    def encode_new_text(self, text: str) -> torch.Tensor:
        """Encode new text for prediction"""
        return self._encode_text(text)
    
    def create_pyg_data(self) -> Data:
        """Create PyG Data object"""
        x = self._create_node_features()
        edge_index = torch.tensor(get_edge_indices(), dtype=torch.long).t()
        
        # Get combined labels for factors and skills
        labels = self._create_labels()
        
        # Create masks for train/val/test split of examples
        num_examples = len(get_node_data()[3])  # Number of examples
        indices = torch.randperm(num_examples)
        
        train_mask = torch.zeros(x.size(0), dtype=torch.bool)
        val_mask = torch.zeros(x.size(0), dtype=torch.bool)
        test_mask = torch.zeros(x.size(0), dtype=torch.bool)
        
        # Only apply masks to example nodes
        example_start_idx = 11  # First example node index
        
        # Split examples: 60% train, 20% val, 20% test
        train_idx = indices[:int(0.6 * num_examples)]
        val_idx = indices[int(0.6 * num_examples):int(0.8 * num_examples)]
        test_idx = indices[int(0.8 * num_examples):]
        
        train_mask[example_start_idx + train_idx] = True
        val_mask[example_start_idx + val_idx] = True
        test_mask[example_start_idx + test_idx] = True
        
        # Create dummy labels for non-example nodes (will not be used in training)
        full_labels = torch.zeros((x.size(0), labels.size(1)))
        full_labels[example_start_idx:example_start_idx + num_examples] = labels
        
        return Data(
            x=x,
            edge_index=edge_index,
            y=full_labels,  # Combined labels for factors and skills
            train_mask=train_mask,
            val_mask=val_mask,
            test_mask=test_mask
        )

def load_data() -> Tuple[Data, TherapeuticDataset]:
    """Helper function to load the dataset and return the dataset object for encoding new text"""
    dataset = TherapeuticDataset()
    data = dataset.create_pyg_data()
    return data, dataset