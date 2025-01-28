import csv
from typing import List, Dict, Tuple

def get_node_data(csv_path: str) -> Tuple[
    List[Dict[str, str]],
    List[Dict[str, str]],
    List[Dict[str, str]],
    List[Dict[str, str]],
    List[Dict[str, str]]
]:
    """
    Returns (root_nodes, common_factors, intervention_concepts, therapeutic_skills, examples).

    1) The root node, CFs, and ICs, and skills are hardcoded/fixed.
    2) The examples are loaded from the CSV at 'csv_path'.

    The CSV must have at least:
      - 'text'
      - 'factor_id'
      - 'ic_id'
      - 'skill_id'
    plus any other columns you want to include or parse.

    Adjust as needed if your CSV or naming conventions differ.
    """
    
    # Root node (not used for prediction but kept for graph structure)
    root_node = [{
        'id': 0,
        'type': 'root',
        'name': 'Therapeutic Relationship',
        'description': "A therapist relates to their client empathically to form a discernible bond and an attitude of working together on tasks to move toward agreed-upon goals that help the client remoralize. Therapists attend to potential ruptures with the intention to repair."
    }]
    
    # Common factors (these are our target classes for prediction)
    common_factors = [
        {
            'id': 1,
            'type': 'common_factor',
            'name': 'Bond',
            'description': "Therapists orient to the client in order to work on a therapeutic bond by taking a stance of empathy, compassion, and acceptance, with the aims of understanding and of helping the client feel understood and supported in a true partnership."
        },
        {
            'id': 2,
            'type': 'common_factor',
            'name': 'Goal alignment',
            'description': "Therapists work to understand their client's desires for change, conceptualize their client's demoralization, and facilitate conversation about the goals they will work on together to address to bring about remoralization. They do this with an attitude of collaboration to negotiate these goals."
        },
        {
            'id': 3,
            'type': 'common_factor',
            'name': 'Task agreement',
            'description': "Therapists facilitate client engagement by clarifying how therapist and client work together and focusing their in-session attention on agreed-upon content and concomitant therapeutic actions that will lead to change. This involves clarifying roles, processes, settings, and session agendas, and ensuring that both therapist and client are aligned on these aspects. The therapist seeks feedback on alignment of session agenda with treatment goals and on therapist in-session procedures."
        }
    ]
    
    # Intervention concepts
    intervention_concepts = [
        {
            'id': 4,
            'type': 'intervention_concept',
            'name': "Empathy, Acceptance and Positive Regard",
            'description': "The therapist shows the capacity to understand, share, and genuinely connect with the patient's thoughts, feelings, and experiences by listening attentively to the patient's concerns without judgment; understanding and validating the patient's emotions and experiences; demonstrating compassion, warmth, and genuine care for the patient's well-being; communicating understanding and support, helping the patient feel heard and valued. Acceptance includes that the therapist sees the client's inherent absolute worth and potential, honors their autonomy, and affirms their personal strengths and efforts. (Bailey & Ogles, p. 48). Positive regard involves prizing and acknowledging what is positive in your clients (Miller & Moyers, p. 46)."
        },
        {
            'id': 5,
            'type': 'intervention_concept',
            'name': "Collaboration and Partnership",
            'description': "The therapist is open to conversations and opportunities to explore client values, goals, and needs and to accept their differences and respect their autonomy. The therapist expresses to the client that he sees the client as an equal who brings strengths, talents, and personal expertise to the relationship. The therapist expresses directly or indirectly that they view the client as a partner in resolving the client's challenges. Therapist attempts to create we-ness, e.g. by using we and together instead  of you, asking questions about the fit of interpretations, conclusions, goals, etc."
        }
    ]
    
    # Therapeutic skills (used as intermediate representations)
    therapeutic_skills = [
        {
            'id': 6,
            'type': 'skill',
            'name': 'Reflective Listening',
            'description': 'Actively listening and reflecting to demonstrate understanding.'
        },
        {
            'id': 7,
            'type': 'skill',
            'name': 'Genuineness',
            'description': 'Being authentic, sincere, and transparent in interactions.'
        },
        {
            'id': 8,
            'type': 'skill',
            'name': 'Validation',
            'description': 'Recognizing and affirming the client\'s experiences and feelings.'
        },
        {
            'id': 9,
            'type': 'skill',
            'name': 'Affirmation',
            'description': 'Highlighting the client\'s strengths and efforts.'
        },
        {
            'id': 10,
            'type': 'skill',
            'name': 'Respect for Autonomy',
            'description': 'Honoring the client\'s independence and choices.'
        },
        {
            'id': 11,
            'type': 'skill',
            'name': 'Asking for Permission',
            'description': 'Seeking the client\'s consent before offering suggestions.'
        },
        {
            'id': 12,
            'type': 'skill',
            'name': 'Open-ended Question',
            'description': 'Inviting deeper, more expansive client responses.'
        }
    ]
    
    examples: List[Dict[str, str]] = []
    
    with open(csv_path, mode='r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        for idx, row in enumerate(reader):
            # Example node ID can start after all above nodes (0..12 used)
            # If you'd like to simply enumerate from 13 onward:
            # example_id = 13 + idx  # or use row.get('id') if your CSV has an explicit 'id'
            example_id = row.get('id')
            
            # Safely parse the factor_id
            factor_id_str = row.get("CF_id", "").strip()
            factor_id = int(factor_id_str) if factor_id_str else 0

            # Safely parse the ic_id
            ic_id_str = row.get("IC_id", "").strip()
            ic_id = int(ic_id_str) if ic_id_str else 0

            # Safely parse the skill_id
            skill_id_str = row.get("skill_id", "").strip()
            skill_id = int(skill_id_str) if skill_id_str else 0
            
            # Build a dictionary for this example node
            example_node = {
                "id": example_id,
                "type": "example",
                "text": row.get("text", ""),
                "CF_id": factor_id,
                "IC_id": ic_id,
                "skill_id": skill_id
            }
            
            examples.append(example_node)
    
    return (
        root_node,
        common_factors,
        intervention_concepts,
        therapeutic_skills,
        examples
    )

def get_edge_indices(csv_path: str) -> List[Tuple[int, int]]:
    """
    Read cf_id, ic_id, skill_id, and each example's own 'id' directly from CSV
    and build graph edges. Also demonstrates root->CF edges and
    skill->CF edges, similar to the original design.
    """
    # Track unique IDs for CF, IC, and skill, and store each example row
    cf_ids = set()
    ic_ids = set()
    skill_ids = set()
    examples = []

    # 1. Read the CSV file to gather all IDs
    with open(csv_path, mode='r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            # Convert to int as needed, assuming columns are named exactly:
            #   id, CF_id, IC_id, skill_id
            example_id = int(row['id'])
            
             # Safely parse the factor_id
            factor_id_str = row.get("CF_id", "").strip()
            cf_id = int(factor_id_str) if factor_id_str else -1

            # Safely parse the ic_id
            ic_id_str = row.get("IC_id", "").strip()
            ic_id = int(ic_id_str) if ic_id_str else -1

            # Safely parse the skill_id
            skill_id_str = row.get("skill_id", "").strip()
            skill_id = int(skill_id_str) if skill_id_str else -1

            # Add to sets
            cf_ids.add(cf_id)
            ic_ids.add(ic_id)
            skill_ids.add(skill_id)

            # Keep the row info for building edges later
            examples.append({
                'example_id': example_id,
                'cf_id': cf_id,
                'ic_id': ic_id,
                'skill_id': skill_id
            })
            
    print(f"examples before edge building: {examples}")

    # 2. Build edges
    edges: List[Tuple[int, int]] = []

    # (a) Root node (ID=0) -> each unique CF
    for cf_id in cf_ids:
        edges.append((0, cf_id))

    # (b) Skills -> CFs
    # for skill_id in skill_ids:
    #     for cf_id in cf_ids:
    #         edges.append((skill_id, cf_id))

    # (c) Example -> skill, CF, IC
    for ex in examples:
        ex_id = ex['example_id']
        cf_id = ex['cf_id']
        ic_id = ex['ic_id']
        skill_id = ex['skill_id']
        
        # 1) If there's a skill, connect Example -> Skill
        if skill_id != -1:
            edges.append((ex_id, skill_id))

        # 2) If there's an IC:
        if ic_id != -1:
            edges.append((ex_id, ic_id))  # Example -> IC
            edges.append((ic_id, cf_id))  # IC -> CF

            # If there's also a skill, connect Skill -> IC
            if skill_id != -1:
                edges.append((skill_id, ic_id))
        else:
            # 3) If no IC, connect Example -> CF
            edges.append((ex_id, cf_id))

            # If there's a skill, connect Skill -> CF
            if skill_id != -1:
                edges.append((skill_id, cf_id))

    # 3. Make edges bidirectional (TODO)
    # print(f"Original edges: {edges}")
    bidirectional_edges = edges + [(dest, src) for (src, dest) in edges]
    
    # 4. Remove duplicates (set() of tuples) and convert back to list
    unique_edges = list(set(bidirectional_edges))

    # Optional: sort them if you need a deterministic order
    unique_edges.sort()

    print(f"Final unique edges: {unique_edges}")
    
    return bidirectional_edges