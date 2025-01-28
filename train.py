# train.py
import torch
import torch.nn.functional as F
from torch.optim import Adam
from data_loading import load_data
from model import EnhancedTherapeuticGNN
import numpy as np
from typing import Tuple

def compute_losses(
    factors_logits: torch.Tensor,
    intervention_concept_logits: torch.Tensor,
    skills_logits: torch.Tensor,
    labels: torch.Tensor,  # Combined labels
    example_indices: torch.Tensor
) -> Tuple[torch.Tensor, torch.Tensor]:
    """Compute losses for both tasks"""
    # print(f"Labels shape: {labels.shape}")
    # print(f"Factors logits shape: {factors_logits.shape}")
    # print(f"Skills logits shape: {skills_logits.shape}")
    # print(f"Example indices shape: {example_indices.shape}")
    # print(f"labels:\n{labels}")
    # Assuming labels are combined: first 3 columns for factors (one-hot), next two are the intervention concepts, and next 7 for skills (multi-label)
    factors_labels = labels[:, :3]  # First 3 columns for factors
    ic_labels = labels[:, 3:5]     # Next 8 columns for ICs
    skills_labels = labels[:, 5:]   # Remaining columns for skills
    
    # print("Factors labels:", factors_labels)
    # print("Skills labels:", skills_labels)
    
    # print("Factors logits:", factors_logits)
    # print("factor preds:", factors_logits[example_indices])
    # print("factor labels in loss", factors_labels[example_indices].argmax(dim=1))
    
    factors_loss = F.cross_entropy(
        factors_logits[example_indices],
        factors_labels[example_indices].argmax(dim=1)  # Convert one-hot to class index
    )
    
    intervention_concept_loss = F.cross_entropy(
        intervention_concept_logits[example_indices],
        ic_labels[example_indices].argmax(dim=1)  # Convert one-hot to class index
    )
    
    # print("Skills logits:", skills_logits)
    # print("skills_labels:", skills_labels[example_indices])
    # print("skills labels before loss", skills_labels[example_indices].argmax(dim=1))
    # print("skills labels in loss", skills_labels[example_indices - 11].argmax(dim=1))
    # print(f"Skill preds\n{skills_labels[example_indices]}")
    # print(f"Skill labels\n{skills_labels[example_indices].argmax(dim=1)}")
    # print(f"Skills logits shape: {skills_logits[example_indices].shape}")
    # print(f"Skills labels shape: {skills_labels[example_indices].argmax(dim=1).shape}")
    skills_loss = F.cross_entropy(
        skills_logits[example_indices],
        skills_labels[example_indices].argmax(dim=1)  # Convert one-hot to class index
    )
    
    return factors_loss, intervention_concept_loss, skills_loss

def train_model(
    model: EnhancedTherapeuticGNN,
    data,
    optimizer: torch.optim.Optimizer,
    epochs: int = 200,
    task_weights: Tuple[float, float] = (1.0, 1.0)  # Weights for factors and skills losses
) -> Tuple[list, list]:
    """Train the enhanced GNN model"""
    train_losses = []
    val_losses = []
    
    # Get example node indices
    train_example_indices = data.train_mask.nonzero().squeeze()
    val_example_indices = data.val_mask.nonzero().squeeze()
    
    # Check if we have any training and validation examples
    if train_example_indices.dim() == 0:
        train_example_indices = train_example_indices.unsqueeze(0)
    if val_example_indices.dim() == 0:
        val_example_indices = val_example_indices.unsqueeze(0)
        
    for epoch in range(epochs):
        # Training
        model.train()
        optimizer.zero_grad()
        factors_logits, intervention_concept_logits, skills_logits = model(data.x, data.edge_index)
        
        # Only compute loss if we have training examples
        if len(train_example_indices) > 0:
            factors_loss, intervention_concept_loss, skills_loss = compute_losses(
                factors_logits, intervention_concept_logits, skills_logits,
                data.y,  # Using combined labels
                train_example_indices
            )
            
            # Weighted sum of losses
            total_loss = (
                task_weights[0] * factors_loss +
                task_weights[1] * intervention_concept_loss +
                task_weights[1] * skills_loss
            )
            
            total_loss.backward()
            optimizer.step()
            train_losses.append(total_loss.item())
        else:
            print("No training examples found!")
            return [], []
        
        # Validation
        model.eval()
        with torch.no_grad():
            if len(val_example_indices) > 0:
                val_factors_logits, val_intervention_concepts_logits, val_skills_logits = model(data.x, data.edge_index)
                val_factors_loss, val_intervention_concepts_loss, val_skills_loss = compute_losses(
                    val_factors_logits, val_intervention_concepts_logits, val_skills_logits,
                    data.y,  # Using combined labels (first three cols are the CFs and the rest are the skills)
                    val_example_indices
                )
                val_total_loss = (
                    task_weights[0] * val_factors_loss +
                    task_weights[1] * val_intervention_concepts_loss +
                    task_weights[1] * val_skills_loss
                )
                val_losses.append(val_total_loss.item())
            else:
                val_total_loss = torch.tensor(0.0)
                val_losses.append(0.0)
        
        if (epoch + 1) % 10 == 0:
            print(f'Epoch {epoch+1:03d}, Train Loss: {total_loss:.4f}, Val Loss: {val_total_loss:.4f}')
    
    return train_losses, val_losses

def main():
    # Set random seed for reproducibility
    # torch.manual_seed(42)
    
    # Settings for now
    FILEPATH = 'data/htc_examples_ids.csv'
    
    # Load data
    data, _ = load_data(FILEPATH)
    
    # Print dataset statistics
    n_train = data.train_mask.sum().item()
    n_val = data.val_mask.sum().item()
    n_test = data.test_mask.sum().item()
    
    print(f"Number of training examples: {n_train}")
    print(f"Number of validation examples: {n_val}")
    print(f"Number of test examples: {n_test}")
    
    # Check label dimensions
    print(f"Label shape: {data.y.shape}")
    print(f"Number of features: {data.x.size(1)}")
    
    # Initialize enhanced model
    model = EnhancedTherapeuticGNN(
        in_channels=data.x.size(1),
        hidden_channels=64,
        num_common_factors=3,
        num_intervention_concepts=2,
        num_skills=7,
        num_layers=2,
        dropout=0.5
    )
    
    # Setup optimizer
    optimizer = Adam(model.parameters(), lr=0.01, weight_decay=5e-4)
    
    # Train model only if we have training examples
    if n_train > 0:
        train_losses, val_losses = train_model(
            model, data, optimizer,
            task_weights=(1.0, 1.0),  # Equal weights for both tasks,
            epochs=300
        )
        
        # Save model
        torch.save(model.state_dict(), 'enhanced_therapeutic_gnn.pth')
        print("Training completed!")
    else:
        print("Error: No training examples available!")

if __name__ == '__main__':
    main()