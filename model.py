# model.py
import torch
import torch.nn.functional as F
from torch_geometric.nn import GATConv
from torch.nn import Linear, ModuleList
from typing import Tuple

class EnhancedTherapeuticGNN(torch.nn.Module):
    def __init__(
        self,
        in_channels: int,
        hidden_channels: int,
        num_common_factors: int = 3,
        num_skills: int = 7,
        num_layers: int = 2,
        dropout: float = 0.5
    ):
        super().__init__()
        
        self.num_layers = num_layers
        self.dropout = dropout
        
        # GAT layers for feature learning
        self.conv_layers = ModuleList()
        self.conv_layers.append(GATConv(in_channels, hidden_channels))
        for _ in range(num_layers - 1):
            self.conv_layers.append(GATConv(hidden_channels, hidden_channels))
        
        # Task-specific layers
        self.factors_classifier = Linear(hidden_channels, num_common_factors)
        self.skills_classifier = Linear(hidden_channels, num_skills)
    
    def forward(
        self,
        x: torch.Tensor,
        edge_index: torch.Tensor = None,
        return_logits: bool = True
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Forward pass handling both training and inference.
        
        Args:
            x: Node features
            edge_index: Optional edge indices for message passing. If None, processes each node independently.
            return_logits: If True, returns raw logits. If False, returns probabilities.
            
        Returns:
            Tuple of (factors_output, skills_output), either as logits or probabilities
        """
        # Process through GAT layers
        for i in range(self.num_layers):
            if edge_index is None:
                # Process features independently without message passing
                x = F.linear(x, self.conv_layers[i].lin.weight, self.conv_layers[i].lin.bias)
            else:
                # Full GAT operation with message passing
                x = self.conv_layers[i](x, edge_index)
            
            x = F.relu(x)
            x = F.dropout(x, p=self.dropout, training=self.training)
        
        # Get predictions
        factors_output = self.factors_classifier(x)
        skills_output = self.skills_classifier(x)
        
        # Return logits or probabilities based on flag
        if not return_logits:
            factors_output = F.softmax(factors_output, dim=-1)
            skills_output = F.softmax(skills_output, dim=-1)
            
        return factors_output, skills_output