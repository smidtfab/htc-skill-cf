# example_data.py
from typing import Dict, List, Tuple

def get_node_data() -> Tuple[List[Dict], List[Dict], List[Dict], List[Dict]]:
    # Root node (not used for prediction but kept for graph structure)
    root_node = [{
        'id': 0,
        'type': 'root',
        'name': 'Therapeutic Relationship',
        'description': 'Root factor representing the overall therapeutic relationship.'
    }]
    
    # Common factors (these are our target classes for prediction)
    common_factors = [
        {
            'id': 1,
            'type': 'common_factor',
            'name': 'Bond',
            'description': 'Emotional/interpersonal connection between therapist and client.'
        },
        {
            'id': 2,
            'type': 'common_factor',
            'name': 'Goal alignment',
            'description': 'Shared understanding and agreement on therapy goals.'
        },
        {
            'id': 3,
            'type': 'common_factor',
            'name': 'Task agreement',
            'description': 'Clear agreement on tasks and methods to reach therapeutic goals.'
        }
    ]
    
    # Therapeutic skills (used as intermediate representations)
    therapeutic_skills = [
        {
            'id': 4,
            'type': 'skill',
            'name': 'Reflective Listening',
            'description': 'Actively listening and reflecting to demonstrate understanding.'
        },
        {
            'id': 5,
            'type': 'skill',
            'name': 'Genuineness',
            'description': 'Being authentic, sincere, and transparent in interactions.'
        },
        {
            'id': 6,
            'type': 'skill',
            'name': 'Validation',
            'description': 'Recognizing and affirming the client\'s experiences and feelings.'
        },
        {
            'id': 7,
            'type': 'skill',
            'name': 'Affirmation',
            'description': 'Highlighting the client\'s strengths and efforts.'
        },
        {
            'id': 8,
            'type': 'skill',
            'name': 'Respect for Autonomy',
            'description': 'Honoring the client\'s independence and choices.'
        },
        {
            'id': 9,
            'type': 'skill',
            'name': 'Asking for Permission',
            'description': 'Seeking the client\'s consent before offering suggestions.'
        },
        {
            'id': 10,
            'type': 'skill',
            'name': 'Open-ended Question',
            'description': 'Inviting deeper, more expansive client responses.'
        }
    ]
    
    # Training examples with labels
    examples = [
        # Existing examples
        {
            'id': 11,
            'type': 'example',
            'text': 'Therapist: "It sounds like you\'re feeling hesitant to open up because you\'re not sure how I\'ll react. Is that right?"',
            'skill_id': 4,  # Reflective Listening
            'factor_id': 1  # Bond
        },
        {
            'id': 12,
            'type': 'example',
            'text': 'Therapist: "You mentioned wanting to improve communication with your partner. Could you share more about your ideal outcome?"',
            'skill_id': 10,  # Open-ended Question
            'factor_id': 2  # Goal alignment
        },
        {
            'id': 13,
            'type': 'example',
            'text': 'Therapist: "Would it be okay if we try a short role-play exercise to help you practice assertiveness?"',
            'skill_id': 9,  # Asking for Permission
            'factor_id': 3  # Task agreement
        },
        {
            'id': 14,
            'type': 'example',
            'text': 'Therapist: "It sounds like you\'re under a lot of pressure, and it\'s completely understandable to feel overwhelmed."',
            'skill_id': 6,  # Validation
            'factor_id': 1  # Bond
        },
        {
            'id': 15,
            'type': 'example',
            'text': 'Therapist: "I appreciate your honesty. I also want to be genuine with you: if we try to tackle too many goals at once, we might lose focus."',
            'skill_id': 5,  # Genuineness
            'factor_id': 2  # Goal alignment
        },

        # New examples
        {
            'id': 16,
            'type': 'example',
            'text': 'Therapist: "I can see that you’ve been making great efforts to practice mindfulness, and it’s starting to pay off."',
            'skill_id': 7,  # Affirmation
            'factor_id': 1  # Bond
        },
        {
            'id': 17,
            'type': 'example',
            'text': 'Therapist: "Let’s focus on the smaller goals first, as that’s entirely up to you. What feels most manageable right now?"',
            'skill_id': 8,  # Respect for Autonomy
            'factor_id': 2  # Goal alignment
        },
        {
            'id': 18,
            'type': 'example',
            'text': 'Therapist: "Let’s work together to make sure this plan feels realistic. Is there any part you’d like to modify?"',
            'skill_id': 9,  # Asking for Permission
            'factor_id': 2  # Goal alignment
        },
        {
            'id': 19,
            'type': 'example',
            'text': 'Therapist: "It’s important to me that this process respects your priorities. What do you think we should focus on in today’s session?"',
            'skill_id': 8,  # Respect for Autonomy
            'factor_id': 3  # Task agreement
        },
        {
            'id': 20,
            'type': 'example',
            'text': 'Therapist: "Let’s summarize the key steps we’ve outlined: you plan to start by journaling your thoughts each evening, correct?"',
            'skill_id': 10,  # Open-ended Question
            'factor_id': 3  # Task agreement
        },
        {
            'id': 21,
            'type': 'example',
            'text': 'Therapist: "It sounds like rebuilding trust with your family is important to you. Can you tell me more about how you envision that process?"',
            'skill_id': 10,  # Open-ended Question
            'factor_id': 1  # Bond
        },
        {
            'id': 22,
            'type': 'example',
            'text': 'Therapist: "You’ve shown incredible strength by continuing to work on this even when it feels challenging."',
            'skill_id': 7,  # Affirmation
            'factor_id': 3  # Task agreement
        },
        {
            'id': 23,
            'type': 'example',
            'text': 'Therapist: "It sounds like staying consistent with your goals is something you value deeply, and that’s really admirable."',
            'skill_id': 7,  # Affirmation
            'factor_id': 2  # Goal alignment
        },
        {
            'id': 24,
            'type': 'example',
            'text': 'Therapist: "I understand how hard this has been for you, and I really appreciate your willingness to share this with me."',
            'skill_id': 6,  # Validation
            'factor_id': 2  # Goal alignment
        },
        {
            'id': 25,
            'type': 'example',
            'text': 'Therapist: "Your decision to take responsibility for these actions shows a lot of courage."',
            'skill_id': 7,  # Affirmation
            'factor_id': 1  # Bond
        },
        {
            'id': 26,
            'type': 'example',
            'text': 'Therapist: "I believe that setting realistic expectations together will make this process more effective for you."',
            'skill_id': 5,  # Genuineness
            'factor_id': 3  # Task agreement
        },
        {
            'id': 27,
            'type': 'example',
            'text': 'Therapist: "Thank you for being open about what you’re feeling. It helps me better understand how we can proceed together."',
            'skill_id': 5,  # Genuineness
            'factor_id': 1  # Bond
        }
    ]
    
    return root_node, common_factors, therapeutic_skills, examples

def get_edge_indices() -> List[Tuple[int, int]]:
    edges = []
    
    # Root to Common Factors (kept for graph structure)
    for cf_id in range(1, 4):
        edges.append((0, cf_id))
    
    # Skills to Common Factors
    for skill_id in range(4, 11):
        for cf_id in range(1, 4):
            edges.append((skill_id, cf_id))
    
    # Examples to Skills and Factors
    for example in range(11, 16):
        # Example to Skill
        edges.append((example, get_node_data()[3][example-11]['skill_id']))
        # Example to Factor
        edges.append((example, get_node_data()[3][example-11]['factor_id']))
    
    # Make edges bidirectional
    bidirectional_edges = edges + [(j, i) for i, j in edges]
    
    return bidirectional_edges

def get_example_labels() -> List[int]:
    """Get factor labels for examples"""
    _, _, _, examples = get_node_data()
    return [example['factor_id'] - 1 for example in examples]  # -1 for 0-based indexing