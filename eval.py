# eval.py
import torch
import torch.nn.functional as F
from sklearn.metrics import classification_report, confusion_matrix, multilabel_confusion_matrix
import numpy as np
from data_loading import load_data
from model import EnhancedTherapeuticGNN
from typing import Dict, Any, List, Tuple

def evaluate_model(model: EnhancedTherapeuticGNN, data) -> Dict[str, Any]:
    """Evaluate the trained model on test set for both factors and skills"""
    model.eval()
    
    with torch.no_grad():
        # Get predictions
        factors_logits, skills_logits = model(data.x, data.edge_index)
        
        # Get predictions for test examples only
        test_indices = data.test_mask.nonzero().squeeze()
        
        # Handle case where there's only one test example
        if test_indices.dim() == 0:
            test_indices = test_indices.unsqueeze(0)
            
        # Get test predictions and labels
        test_labels = data.y[test_indices]  # Adjust for example node indices
        factor_labels = test_labels[:, :3]  # First 3 columns for factors
        skill_labels = test_labels[:, 3:]   # Remaining columns for skills
        
        # Process factor predictions
        factor_predictions = factors_logits[test_indices]
        factor_pred_classes = factor_predictions.max(dim=1)[1]
        factor_true_classes = factor_labels.max(dim=1)[1]
        
        # Process skill predictions
        skill_predictions = torch.sigmoid(skills_logits[test_indices])
        skill_pred_classes = (skill_predictions > 0.5).float()
        
        # Calculate metrics for factors
        factor_accuracy = factor_pred_classes.eq(factor_true_classes).float().mean().item()
        
        # Calculate metrics for skills
        skill_accuracy = (skill_pred_classes == skill_labels).float().mean().item()
        
        # Convert to numpy arrays for sklearn metrics
        y_true_factors = factor_true_classes.cpu().numpy()
        y_pred_factors = factor_pred_classes.cpu().numpy()
        y_true_skills = skill_labels.cpu().numpy()
        y_pred_skills = skill_pred_classes.cpu().numpy()
        
        # Create classification reports
        factor_names = ['Bond', 'Goal Alignment', 'Task Agreement']
        skill_names = [
            'Reflective Listening', 'Genuineness', 'Validation', 
            'Affirmation', 'Respect for Autonomy', 'Asking for Permission', 
            'Open-ended Question'
        ]
        
        try:
            # Factor classification report
            factor_report = classification_report(
                y_true_factors,
                y_pred_factors,
                target_names=factor_names,
                output_dict=True,
                zero_division=0
            )
            
            # Skills classification report (multilabel)
            skill_report = classification_report(
                y_true_skills,
                y_pred_skills,
                target_names=skill_names,
                output_dict=True,
                zero_division=0
            )
        except ValueError as e:
            print(f"Warning: Could not generate classification report: {e}")
            factor_report = {}
            skill_report = {}
        
        # Generate confusion matrices
        try:
            factor_conf_matrix = confusion_matrix(y_true_factors, y_pred_factors)
            skill_conf_matrices = multilabel_confusion_matrix(y_true_skills, y_pred_skills)
        except ValueError as e:
            print(f"Warning: Could not generate confusion matrix: {e}")
            factor_conf_matrix = np.array([[0]])
            skill_conf_matrices = np.array([[[0, 0], [0, 0]]] * len(skill_names))
        
        return {
            'factor_accuracy': factor_accuracy,
            'skill_accuracy': skill_accuracy,
            'factor_classification_report': factor_report,
            'skill_classification_report': skill_report,
            'factor_confusion_matrix': factor_conf_matrix,
            'skill_confusion_matrices': skill_conf_matrices,
            'num_test_examples': len(test_indices)
        }

# eval.py
def predict_new_text(
    model: EnhancedTherapeuticGNN,
    dataset,
    text: str
) -> Tuple[Dict[str, float], Dict[str, float]]:
    """
    Predict common factors and skills for new therapeutic text example
    """
    model.eval()
    with torch.no_grad():
        # Encode new text and ensure it's 2D (batch dimension)
        text_features = dataset.encode_new_text(text)
        if text_features.dim() == 1:
            text_features = text_features.unsqueeze(0)
        
        # Get predictions using the unified forward pass
        factor_probs, skill_probs = model(
            text_features,
            edge_index=None,  # Process independently
            return_logits=False  # Get probabilities directly
        )
        
        # Create probability dictionaries
        factor_names = ['Bond', 'Goal Alignment', 'Task Agreement']
        skill_names = [
            'Reflective Listening', 'Genuineness', 'Validation', 
            'Affirmation', 'Respect for Autonomy', 'Asking for Permission', 
            'Open-ended Question'
        ]
        
        # Ensure we're working with the first (and only) prediction
        factor_probs = factor_probs.squeeze(0)
        skill_probs = skill_probs.squeeze(0)
        
        factor_predictions = {
            name: prob.item() for name, prob in zip(factor_names, factor_probs)
        }
        
        skill_predictions = {
            name: prob.item() for name, prob in zip(skill_names, skill_probs)
        }
        
        return factor_predictions, skill_predictions

def main():
    # Load data and model
    data, dataset = load_data()
    
    model = EnhancedTherapeuticGNN(
        in_channels=data.x.size(1),
        hidden_channels=64,
        num_common_factors=3,
        num_skills=7
    )
    
    try:
        # Load trained model weights
        model.load_state_dict(torch.load('enhanced_therapeutic_gnn.pth'))
        
        # Print dataset statistics
        n_test = data.test_mask.sum().item()
        print(f"\nNumber of test examples: {n_test}")
        
        if n_test > 0:
            # Evaluate on test set
            metrics = evaluate_model(model, data)
            
            print("\nModel Evaluation Results:")
            print(f"Factor Accuracy: {metrics['factor_accuracy']:.4f}")
            print(f"Skill Accuracy: {metrics['skill_accuracy']:.4f}")
            print(f"Number of test examples: {metrics['num_test_examples']}")
            
            print("\nCommon Factors Classification Report:")
            for class_name, metrics_dict in metrics['factor_classification_report'].items():
                if isinstance(metrics_dict, dict):
                    print(f"\n{class_name}:")
                    print(f"Precision: {metrics_dict['precision']:.4f}")
                    print(f"Recall: {metrics_dict['recall']:.4f}")
                    print(f"F1-score: {metrics_dict['f1-score']:.4f}")
            
            print("\nSkills Classification Report:")
            for class_name, metrics_dict in metrics['skill_classification_report'].items():
                if isinstance(metrics_dict, dict):
                    print(f"\n{class_name}:")
                    print(f"Precision: {metrics_dict['precision']:.4f}")
                    print(f"Recall: {metrics_dict['recall']:.4f}")
                    print(f"F1-score: {metrics_dict['f1-score']:.4f}")
            
            print("\nCommon Factors Confusion Matrix:")
            print(metrics['factor_confusion_matrix'])
            
            print("\nSkills Confusion Matrices (one per skill):")
            for skill_name, conf_matrix in zip(
                ['Reflective Listening', 'Genuineness', 'Validation', 
                 'Affirmation', 'Respect for Autonomy', 'Asking for Permission', 
                 'Open-ended Question'],
                metrics['skill_confusion_matrices']
            ):
                print(f"\n{skill_name}:")
                print(conf_matrix)
        else:
            print("No test examples available for evaluation.")
        
        # Example of predicting new text
        print("\nPredicting New Examples:")
        example_texts = [
            "Therapist: 'You mentioned wanting to improve your communication with your partner. Can you tell me more about what that would look like for you?'",
            "Therapist: 'What specific changes would you like to see in your relationship by the end of therapy?'",
            "Therapist: 'Let's break down this new communication technique into smaller steps we can practice.'"
        ]
        
        for text in example_texts:
            factor_preds, skill_preds = predict_new_text(model, dataset, text)
            print(f"\nText: {text}")
            print("\nPredicted Common Factors:")
            for factor, prob in factor_preds.items():
                print(f"{factor}: {prob:.4f}")
            print("\nPredicted Skills:")
            for skill, prob in skill_preds.items():
                print(f"{skill}: {prob:.4f}")
                
    except FileNotFoundError:
        print("Error: Could not find trained model file (enhanced_therapeutic_gnn.pth)")
        print("Please train the model first using train.py")

if __name__ == '__main__':
    main()