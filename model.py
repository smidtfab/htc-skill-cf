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
        
        # GAT layers for shared feature learning
        self.conv_layers = ModuleList()
        self.conv_layers.append(GATConv(in_channels, hidden_channels))
        for _ in range(num_layers - 1):
            self.conv_layers.append(GATConv(hidden_channels, hidden_channels))
        
        # Separate task-specific layers
        self.factors_classifier = Linear(hidden_channels, num_common_factors)
        self.skills_classifier = Linear(hidden_channels, num_skills)
        
    def forward(self, x, edge_index):
        # Shared feature learning through GAT layers
        for i in range(self.num_layers):
            x = self.conv_layers[i](x, edge_index)
            x = F.relu(x)
            x = F.dropout(x, p=self.dropout, training=self.training)
        
        # Task-specific predictions
        factors_logits = self.factors_classifier(x)
        skills_logits = self.skills_classifier(x)
        
        return factors_logits, skills_logits
    
    def predict_text(self, data, new_text_features: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """Predict common factors and skills for new text"""
        self.eval()
        with torch.no_grad():
            # Add new text features to existing graph
            x = torch.cat([data.x, new_text_features.unsqueeze(0)], dim=0)
            
            # Add edges connecting new node to all skill nodes
            num_existing_nodes = data.x.size(0)
            new_edges = []
            for skill_id in range(4, 11):  # skill node IDs
                new_edges.extend([
                    [num_existing_nodes, skill_id],
                    [skill_id, num_existing_nodes]
                ])
            new_edge_index = torch.cat([
                data.edge_index,
                torch.tensor(new_edges, dtype=torch.long).t()
            ], dim=1)
            
            print(f"Edge index:\n{new_edge_index}")
            
            # Get predictions
            factors_logits, skills_logits = self.forward(x, new_edge_index)
            
            # Return predictions for new node only
            return (
                F.softmax(factors_logits[-1], dim=0),
                # torch.sigmoid(skills_logits[-1])  # Multi-label prediction for skills
                F.softmax(skills_logits[-1], dim=0)  # Multi-class prediction for skills
            )