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
    # 1. Reflective Listening (Skill ID: 4)
    # Bond
    {'id': 1, 'type': 'example', 'text': 'Therapist: "It sounds like you’re worried about sharing too much because you’re unsure how I’ll respond. Is that right?"', 'skill_id': 4, 'factor_id': 1},
    {'id': 2, 'type': 'example', 'text': 'Therapist: "So, you feel like no one really understands how you’re feeling right now?"', 'skill_id': 4, 'factor_id': 1},
    {'id': 3, 'type': 'example', 'text': 'Therapist: "You mentioned feeling disconnected from your partner. Can you tell me if I’m understanding that correctly?"', 'skill_id': 4, 'factor_id': 1},
    {'id': 4, 'type': 'example', 'text': 'Therapist: "I hear that you’re feeling overwhelmed by the situation and unsure about what to do next."', 'skill_id': 4, 'factor_id': 1},
    {'id': 5, 'type': 'example', 'text': 'Therapist: "It seems like you feel unsupported by your friends and family. Did I get that right?"', 'skill_id': 4, 'factor_id': 1},
    {'id': 6, 'type': 'example', 'text': 'Therapist: "You said you feel stuck in your job. Is that how you’d describe it?"', 'skill_id': 4, 'factor_id': 1},
    {'id': 7, 'type': 'example', 'text': 'Therapist: "If I’m understanding you correctly, you’re saying that you feel like nobody is listening to your concerns."', 'skill_id': 4, 'factor_id': 1},

    # Goal alignment
    {'id': 8, 'type': 'example', 'text': 'Therapist: "So, achieving more balance in your life is your main priority right now. Is that correct?"', 'skill_id': 4, 'factor_id': 2},
    {'id': 9, 'type': 'example', 'text': 'Therapist: "You mentioned that resolving conflicts with your family is something you’d like to work on. Am I getting that right?"', 'skill_id': 4, 'factor_id': 2},
    {'id': 10, 'type': 'example', 'text': 'Therapist: "If I’m following you, it sounds like finding more time for self-care is a major goal for you."', 'skill_id': 4, 'factor_id': 2},
    {'id': 11, 'type': 'example', 'text': 'Therapist: "So you’re saying that improving your ability to communicate at work is important to you. Did I capture that right?"', 'skill_id': 4, 'factor_id': 2},
    {'id': 12, 'type': 'example', 'text': 'Therapist: "You said you’d like to strengthen your relationship with your kids. Is that something we should focus on together?"', 'skill_id': 4, 'factor_id': 2},
    {'id': 13, 'type': 'example', 'text': 'Therapist: "It sounds like your ultimate goal is to feel more confident in social situations. Is that what you mean?"', 'skill_id': 4, 'factor_id': 2},
    {'id': 14, 'type': 'example', 'text': 'Therapist: "So your goal is to reduce your anxiety in group settings. Does that sound accurate?"', 'skill_id': 4, 'factor_id': 2},

    # Task agreement
    {'id': 15, 'type': 'example', 'text': 'Therapist: "Let me make sure I understand: You’re planning to try journaling every evening to process your emotions. Correct?"', 'skill_id': 4, 'factor_id': 3},
    {'id': 16, 'type': 'example', 'text': 'Therapist: "You’re suggesting that a daily walk might help clear your mind. Is that right?"', 'skill_id': 4, 'factor_id': 3},
    {'id': 17, 'type': 'example', 'text': 'Therapist: "To confirm, you’d like to start setting aside time each week to practice mindfulness. Does that align with what you want?"', 'skill_id': 4, 'factor_id': 3},
    {'id': 18, 'type': 'example', 'text': 'Therapist: "It sounds like you’re committed to limiting your screen time before bed. Is that correct?"', 'skill_id': 4, 'factor_id': 3},
    {'id': 19, 'type': 'example', 'text': 'Therapist: "If I understand you correctly, you’d like to focus on practicing assertiveness in conversations at work."', 'skill_id': 4, 'factor_id': 3},
    {'id': 20, 'type': 'example', 'text': 'Therapist: "You mentioned wanting to prioritize getting enough sleep every night. Does that reflect your current plan?"', 'skill_id': 4, 'factor_id': 3},
    {'id': 21, 'type': 'example', 'text': 'Therapist: "So you’re aiming to practice deep breathing exercises every morning. Is that your plan?"', 'skill_id': 4, 'factor_id': 3},


    # 2. Genuineness (Skill ID: 5)
    # Bond
    {'id': 22, 'type': 'example', 'text': 'Therapist: "I want to be honest with you. I can see this is really difficult, and I appreciate you trusting me with it."', 'skill_id': 5, 'factor_id': 1},
    {'id': 23, 'type': 'example', 'text': 'Therapist: "I value your openness, and I want to make sure I’m understanding you fully."', 'skill_id': 5, 'factor_id': 1},
    {'id': 24, 'type': 'example', 'text': 'Therapist: "This is a safe space for you to share your feelings. I mean that sincerely."', 'skill_id': 5, 'factor_id': 1},
    {'id': 25, 'type': 'example', 'text': 'Therapist: "I appreciate your willingness to share, and I want you to know I’m here to support you."', 'skill_id': 5, 'factor_id': 1},
    {'id': 26, 'type': 'example', 'text': 'Therapist: "I can see how vulnerable this makes you feel, and I respect that you’ve chosen to share it."', 'skill_id': 5, 'factor_id': 1},
    {'id': 27, 'type': 'example', 'text': 'Therapist: "Being here and talking about this shows a lot of courage, and I want to acknowledge that."', 'skill_id': 5, 'factor_id': 1},
    {'id': 28, 'type': 'example', 'text': 'Therapist: "I want to let you know that I’m here to listen, and I truly care about what you’re going through."', 'skill_id': 5, 'factor_id': 1},

    # Goal alignment
    {'id': 29, 'type': 'example', 'text': 'Therapist: "It’s important for me to be upfront: tackling too many goals at once might feel overwhelming."', 'skill_id': 5, 'factor_id': 2},
    {'id': 30, 'type': 'example', 'text': 'Therapist: "I genuinely believe we can work together to achieve what matters most to you."', 'skill_id': 5, 'factor_id': 2},
    {'id': 31, 'type': 'example', 'text': 'Therapist: "Your goals are important to me, and I want to make sure we’re on the same page."', 'skill_id': 5, 'factor_id': 2},
    {'id': 32, 'type': 'example', 'text': 'Therapist: "I’m being honest when I say that breaking this into smaller goals could make it more manageable."', 'skill_id': 5, 'factor_id': 2},
    {'id': 33, 'type': 'example', 'text': 'Therapist: "It’s okay if your goals change along the way. I want to work with what feels right for you."', 'skill_id': 5, 'factor_id': 2},
    {'id': 34, 'type': 'example', 'text': 'Therapist: "I want to be clear that this is your journey, and I’ll support you in setting priorities."', 'skill_id': 5, 'factor_id': 2},
    {'id': 35, 'type': 'example', 'text': 'Therapist: "It’s great that you’ve identified your main goals, and I’m committed to helping you achieve them."', 'skill_id': 5, 'factor_id': 2},
    
    # Task Agreement
    {'id': 36, 'type': 'example', 'text': 'Therapist: "I want to be transparent: sticking to this plan might feel challenging, but we’ll adjust as needed."', 'skill_id': 5, 'factor_id': 3},
    {'id': 37, 'type': 'example', 'text': 'Therapist: "I think we’re heading in the right direction, but let’s revisit your plan to ensure it works for you."', 'skill_id': 5, 'factor_id': 3},
    {'id': 38, 'type': 'example', 'text': 'Therapist: "I truly believe that starting small will help us build momentum toward your bigger goals."', 'skill_id': 5, 'factor_id': 3},
    {'id': 39, 'type': 'example', 'text': 'Therapist: "I’ll be honest: this is a structured plan, but we can be flexible if something feels off."', 'skill_id': 5, 'factor_id': 3},
    {'id': 40, 'type': 'example', 'text': 'Therapist: "I want to make sure this plan aligns with your needs and feels realistic."', 'skill_id': 5, 'factor_id': 3},
    {'id': 41, 'type': 'example', 'text': 'Therapist: "I believe this task could be helpful, but it’s your call on how to proceed."', 'skill_id': 5, 'factor_id': 3},
    {'id': 42, 'type': 'example', 'text': 'Therapist: "Let’s make this plan together so it reflects your goals and what feels doable."', 'skill_id': 5, 'factor_id': 3},
    
    # 3. Validation (Skill ID: 6)
    # Bond
    {'id': 43, 'type': 'example', 'text': 'Therapist: "I hear how difficult this has been for you, and it makes sense to feel this way."', 'skill_id': 6, 'factor_id': 1},
    {'id': 44, 'type': 'example', 'text': 'Therapist: "Feeling overwhelmed is a natural reaction to everything you’ve been dealing with."', 'skill_id': 6, 'factor_id': 1},
    {'id': 45, 'type': 'example', 'text': 'Therapist: "It’s understandable that you’d feel hesitant after everything that’s happened."', 'skill_id': 6, 'factor_id': 1},
    {'id': 46, 'type': 'example', 'text': 'Therapist: "I can see how much this situation has affected you. Your feelings are valid."', 'skill_id': 6, 'factor_id': 1},
    {'id': 47, 'type': 'example', 'text': 'Therapist: "Given what you’ve experienced, it makes complete sense to feel this way."', 'skill_id': 6, 'factor_id': 1},
    {'id': 48, 'type': 'example', 'text': 'Therapist: "Your reaction is completely normal given the challenges you’re facing."', 'skill_id': 6, 'factor_id': 1},
    {'id': 49, 'type': 'example', 'text': 'Therapist: "I hear what you’re saying, and it’s valid to feel this way."', 'skill_id': 6, 'factor_id': 1},
    
    # Goal alignment
    {'id': 50, 'type': 'example', 'text': 'Therapist: "It’s completely valid to feel uncertain about prioritizing your goals. Let’s break them down together."', 'skill_id': 6, 'factor_id': 2},
    {'id': 51, 'type': 'example', 'text': 'Therapist: "Feeling overwhelmed by your goals makes sense, especially since you have so much on your plate."', 'skill_id': 6, 'factor_id': 2},
    {'id': 52, 'type': 'example', 'text': 'Therapist: "Your focus on wanting to build stronger relationships shows how much you care, and that’s important."', 'skill_id': 6, 'factor_id': 2},
    {'id': 53, 'type': 'example', 'text': 'Therapist: "It’s understandable that you feel conflicted about which goal to prioritize. That’s a common challenge."', 'skill_id': 6, 'factor_id': 2},
    {'id': 54, 'type': 'example', 'text': 'Therapist: "Wanting to feel more confident in achieving your goals is a valid and important desire."', 'skill_id': 6, 'factor_id': 2},
    {'id': 55, 'type': 'example', 'text': 'Therapist: "It makes sense to feel cautious about taking on too much at once. That’s a healthy approach."', 'skill_id': 6, 'factor_id': 2},
    {'id': 56, 'type': 'example', 'text': 'Therapist: "Your desire to align your goals with your values is completely understandable."', 'skill_id': 6, 'factor_id': 2},
    
    # Task Agreement
    {'id': 57, 'type': 'example', 'text': 'Therapist: "It’s valid to feel uncertain about starting this task. It’s a new step, and that can feel challenging."', 'skill_id': 6, 'factor_id': 3},
    {'id': 58, 'type': 'example', 'text': 'Therapist: "Feeling hesitant about following through on this plan is normal. Let’s talk about what feels manageable."', 'skill_id': 6, 'factor_id': 3},
    {'id': 59, 'type': 'example', 'text': 'Therapist: "Your reaction to wanting more clarity about the task is completely valid. Let’s break it down."', 'skill_id': 6, 'factor_id': 3},
    {'id': 60, 'type': 'example', 'text': 'Therapist: "It makes sense to feel nervous about committing to this task. Let’s work together to adjust it if needed."', 'skill_id': 6, 'factor_id': 3},
    {'id': 61, 'type': 'example', 'text': 'Therapist: "You’ve expressed doubts about sticking to the plan, and that’s understandable. It’s a big change."', 'skill_id': 6, 'factor_id': 3},
    {'id': 62, 'type': 'example', 'text': 'Therapist: "It’s completely valid to feel unsure about the first step. That’s why we’re working on this together."', 'skill_id': 6, 'factor_id': 3},
    {'id': 63, 'type': 'example', 'text': 'Therapist: "Wanting to revisit the task and make adjustments shows how thoughtful you are about the process."', 'skill_id': 6, 'factor_id': 3},
    
    # 4. Affirmation (Skill ID: 7)
    # Bond
    {'id': 64, 'type': 'example', 'text': 'Therapist: "It’s impressive how much effort you’ve put into building connections with those around you."', 'skill_id': 7, 'factor_id': 1},
    {'id': 65, 'type': 'example', 'text': 'Therapist: "Your willingness to share such personal details shows incredible strength."', 'skill_id': 7, 'factor_id': 1},
    {'id': 66, 'type': 'example', 'text': 'Therapist: "The way you’ve described your relationships shows how much you value them, and that’s admirable."', 'skill_id': 7, 'factor_id': 1},
    {'id': 67, 'type': 'example', 'text': 'Therapist: "Your courage in opening up about these feelings is truly inspiring."', 'skill_id': 7, 'factor_id': 1},
    {'id': 68, 'type': 'example', 'text': 'Therapist: "Your persistence in working on this relationship demonstrates how much you care."', 'skill_id': 7, 'factor_id': 1},
    {'id': 69, 'type': 'example', 'text': 'Therapist: "I can tell you’ve put a lot of thought into improving your relationships, and that’s something to be proud of."', 'skill_id': 7, 'factor_id': 1},
    {'id': 70, 'type': 'example', 'text': 'Therapist: "It’s inspiring to see how committed you are to building stronger connections."', 'skill_id': 7, 'factor_id': 1},

    # Goal alignment
    {'id': 71, 'type': 'example', 'text': 'Therapist: "The fact that you’ve identified these goals shows how determined you are to make positive changes."', 'skill_id': 7, 'factor_id': 2},
    {'id': 72, 'type': 'example', 'text': 'Therapist: "Your ability to focus on what matters most is a real strength."', 'skill_id': 7, 'factor_id': 2},
    {'id': 73, 'type': 'example', 'text': 'Therapist: "You’ve done an amazing job of outlining what’s most important to you."', 'skill_id': 7, 'factor_id': 2},
    {'id': 74, 'type': 'example', 'text': 'Therapist: "Your determination to achieve these goals is truly commendable."', 'skill_id': 7, 'factor_id': 2},
    {'id': 75, 'type': 'example', 'text': 'Therapist: "You’ve made incredible progress just by defining your goals so clearly."', 'skill_id': 7, 'factor_id': 2},
    {'id': 76, 'type': 'example', 'text': 'Therapist: "Your thoughtfulness in aligning your goals with your values is very impressive."', 'skill_id': 7, 'factor_id': 2},
    {'id': 77, 'type': 'example', 'text': 'Therapist: "You’ve shown so much insight into what matters most to you, and that’s worth celebrating."', 'skill_id': 7, 'factor_id': 2},

    # Task Agreement
    {'id': 78, 'type': 'example', 'text': 'Therapist: "Your commitment to sticking to this task is really admirable."', 'skill_id': 7, 'factor_id': 3},
    {'id': 79, 'type': 'example', 'text': 'Therapist: "The way you’re approaching this plan shows a lot of thoughtfulness."', 'skill_id': 7, 'factor_id': 3},
    {'id': 80, 'type': 'example', 'text': 'Therapist: "Your willingness to try something new is an incredible strength."', 'skill_id': 7, 'factor_id': 3},
    {'id': 81, 'type': 'example', 'text': 'Therapist: "Your effort to stay consistent with this task is something to be really proud of."', 'skill_id': 7, 'factor_id': 3},
    {'id': 82, 'type': 'example', 'text': 'Therapist: "Your openness to experimenting with new approaches is impressive."', 'skill_id': 7, 'factor_id': 3},
    {'id': 83, 'type': 'example', 'text': 'Therapist: "It’s inspiring to see how proactive you’re being about following through."', 'skill_id': 7, 'factor_id': 3},
    {'id': 84, 'type': 'example', 'text': 'Therapist: "The dedication you’ve shown to this task is truly remarkable."', 'skill_id': 7, 'factor_id': 3},

    # 5. Respect for Autonomy (Skill ID: 8)
    # Bond
    {'id': 85, 'type': 'example', 'text': 'Therapist: "I trust that you know what’s best for yourself. Let’s explore what feels right for you."', 'skill_id': 8, 'factor_id': 1},
    {'id': 86, 'type': 'example', 'text': 'Therapist: "You have the right to set your own boundaries, and I respect that."', 'skill_id': 8, 'factor_id': 1},
    {'id': 87, 'type': 'example', 'text': 'Therapist: "It’s your choice how much you want to share, and I’ll follow your lead."', 'skill_id': 8, 'factor_id': 1},
    {'id': 88, 'type': 'example', 'text': 'Therapist: "Your decisions about your relationships are entirely yours to make, and I support that."', 'skill_id': 8, 'factor_id': 1},
    {'id': 89, 'type': 'example', 'text': 'Therapist: "I appreciate how thoughtfully you’re approaching this. It’s your call on how to proceed."', 'skill_id': 8, 'factor_id': 1},
    {'id': 90, 'type': 'example', 'text': 'Therapist: "You know yourself best, and I want to honor that."', 'skill_id': 8, 'factor_id': 1},
    {'id': 91, 'type': 'example', 'text': 'Therapist: "Your willingness to take ownership of your decisions is something I respect deeply."', 'skill_id': 8, 'factor_id': 1},

    # Goal alignment
    {'id': 92, 'type': 'example', 'text': 'Therapist: "It’s up to you to decide which goals feel most important to you right now."', 'skill_id': 8, 'factor_id': 2},
    {'id': 93, 'type': 'example', 'text': 'Therapist: "You’re in charge of how we approach these goals. What feels like the right place to start?"', 'skill_id': 8, 'factor_id': 2},
    {'id': 94, 'type': 'example', 'text': 'Therapist: "You have the freedom to prioritize your goals however you like, and I’ll support you."', 'skill_id': 8, 'factor_id': 2},
    {'id': 95, 'type': 'example', 'text': 'Therapist: "This is your journey, and I want to help you define it in a way that works for you."', 'skill_id': 8, 'factor_id': 2},
    {'id': 96, 'type': 'example', 'text': 'Therapist: "Your goals are personal to you, and only you can decide what’s most important."', 'skill_id': 8, 'factor_id': 2},
    {'id': 97, 'type': 'example', 'text': 'Therapist: "Let’s focus on what aligns most closely with your values. What feels like the right direction for you?"', 'skill_id': 8, 'factor_id': 2},
    {'id': 98, 'type': 'example', 'text': 'Therapist: "It’s entirely your decision how we move forward with your goals."', 'skill_id': 8, 'factor_id': 2},

    # Task Agreement
    {'id': 99, 'type': 'example', 'text': 'Therapist: "It’s your call whether or not to take on this task. Let me know what feels right."', 'skill_id': 8, 'factor_id': 3},
    {'id': 100, 'type': 'example', 'text': 'Therapist: "You’re in charge of deciding how to approach this task. I’ll offer guidance if you’d like."', 'skill_id': 8, 'factor_id': 3},
    {'id': 101, 'type': 'example', 'text': 'Therapist: "You have complete control over whether to stick with this plan or make adjustments."', 'skill_id': 8, 'factor_id': 3},
    {'id': 102, 'type': 'example', 'text': 'Therapist: "Let’s collaborate on this task in a way that feels manageable for you."', 'skill_id': 8, 'factor_id': 3},
    {'id': 103, 'type': 'example', 'text': 'Therapist: "I trust your judgment on how to proceed with this task."', 'skill_id': 8, 'factor_id': 3},
    {'id': 104, 'type': 'example', 'text': 'Therapist: "You’re the one who decides whether this plan feels right for you."', 'skill_id': 8, 'factor_id': 3},
    {'id': 105, 'type': 'example', 'text': 'Therapist: "If this task doesn’t feel like a good fit, we can adjust it. It’s entirely up to you."', 'skill_id': 8, 'factor_id': 3},

    # 6. Asking for Permission (Skill ID: 9)
    # Bond
    {'id': 106, 'type': 'example', 'text': 'Therapist: "Would it be okay if we talk about how your relationships have been affecting you lately?"', 'skill_id': 9, 'factor_id': 1},
    {'id': 107, 'type': 'example', 'text': 'Therapist: "Is it alright if we explore your feelings about trust in relationships?"', 'skill_id': 9, 'factor_id': 1},
    {'id': 108, 'type': 'example', 'text': 'Therapist: "Can we spend some time discussing what makes you feel supported?"', 'skill_id': 9, 'factor_id': 1},
    {'id': 109, 'type': 'example', 'text': 'Therapist: "Would you be comfortable sharing more about how you’ve been feeling emotionally?"', 'skill_id': 9, 'factor_id': 1},
    {'id': 110, 'type': 'example', 'text': 'Therapist: "Is it okay if we focus on understanding your needs in your relationships?"', 'skill_id': 9, 'factor_id': 1},
    {'id': 111, 'type': 'example', 'text': 'Therapist: "Can I ask how your experiences have shaped the way you connect with others?"', 'skill_id': 9, 'factor_id': 1},
    {'id': 112, 'type': 'example', 'text': 'Therapist: "Would you feel comfortable talking about what makes you feel most connected to others?"', 'skill_id': 9, 'factor_id': 1},

    # Goal alignment
    {'id': 113, 'type': 'example', 'text': 'Therapist: "Would it be alright if we clarify your goals for the next few sessions?"', 'skill_id': 9, 'factor_id': 2},
    {'id': 114, 'type': 'example', 'text': 'Therapist: "Is it okay if we talk about which goals feel most urgent to you right now?"', 'skill_id': 9, 'factor_id': 2},
    {'id': 115, 'type': 'example', 'text': 'Therapist: "Can we focus on how your goals align with your values?"', 'skill_id': 9, 'factor_id': 2},
    {'id': 116, 'type': 'example', 'text': 'Therapist: "Would you feel comfortable prioritizing one goal to work on first?"', 'skill_id': 9, 'factor_id': 2},
    {'id': 117, 'type': 'example', 'text': 'Therapist: "Is it alright if we spend time defining what success looks like for you?"', 'skill_id': 9, 'factor_id': 2},
    {'id': 118, 'type': 'example', 'text': 'Therapist: "Can I ask if you’d like to explore smaller steps toward your larger goals?"', 'skill_id': 9, 'factor_id': 2},
    {'id': 119, 'type': 'example', 'text': 'Therapist: "Would it be okay if we revisit your goals to make sure they still feel relevant?"', 'skill_id': 9, 'factor_id': 2},

    # Task Agreement
    {'id': 120, 'type': 'example', 'text': 'Therapist: "Would it be alright if we break this task into smaller, actionable steps to make it more manageable?"', 'skill_id': 9, 'factor_id': 3},
    {'id': 121, 'type': 'example', 'text': 'Therapist: "Is it okay if we review your progress on this task next week to see how it’s going?"', 'skill_id': 9, 'factor_id': 3},
    {'id': 122, 'type': 'example', 'text': 'Therapist: "Can I ask if you’d like to adjust the pace of this task to fit your schedule better?"', 'skill_id': 9, 'factor_id': 3},
    {'id': 123, 'type': 'example', 'text': 'Therapist: "Would you feel comfortable focusing on this one part of the task for now?"', 'skill_id': 9, 'factor_id': 3},
    {'id': 124, 'type': 'example', 'text': 'Therapist: "Is it alright if we take some time today to discuss how this task feels for you so far?"', 'skill_id': 9, 'factor_id': 3},
    {'id': 125, 'type': 'example', 'text': 'Therapist: "Would you like to explore alternative ways to accomplish this task that might feel easier?"', 'skill_id': 9, 'factor_id': 3},
    {'id': 126, 'type': 'example', 'text': 'Therapist: "Can we talk about what adjustments might make this task feel more aligned with your needs?"', 'skill_id': 9, 'factor_id': 3},

    # 7. Open-ended Questions (Skill ID: 10)
    # Bond
    {'id': 127, 'type': 'example', 'text': 'Therapist: "How do you feel about the support you’re getting from those closest to you?"', 'skill_id': 10, 'factor_id': 1},
    {'id': 128, 'type': 'example', 'text': 'Therapist: "What does a strong relationship mean to you?"', 'skill_id': 10, 'factor_id': 1},
    {'id': 129, 'type': 'example', 'text': 'Therapist: "Can you tell me more about how you’ve been feeling about your partner lately?"', 'skill_id': 10, 'factor_id': 1},
    {'id': 130, 'type': 'example', 'text': 'Therapist: "How do you typically respond when you feel unsupported?"', 'skill_id': 10, 'factor_id': 1},
    {'id': 131, 'type': 'example', 'text': 'Therapist: "What does trust in a relationship look like for you?"', 'skill_id': 10, 'factor_id': 1},
    {'id': 132, 'type': 'example', 'text': 'Therapist: "What kinds of conversations make you feel most connected to others?"', 'skill_id': 10, 'factor_id': 1},
    {'id': 133, 'type': 'example', 'text': 'Therapist: "Can you describe a time when you felt truly supported?"', 'skill_id': 10, 'factor_id': 1},

    # Goal alignment
    {'id': 134, 'type': 'example', 'text': 'Therapist: "You mentioned wanting to improve your work-life balance. Can you elaborate on what that would look like for you?"', 'skill_id': 10, 'factor_id': 2},
    {'id': 135, 'type': 'example', 'text': 'Therapist: "What would achieving that goal mean for your day-to-day life?"', 'skill_id': 10, 'factor_id': 2},
    {'id': 136, 'type': 'example', 'text': 'Therapist: "How would you prioritize your goals if we focused on the most important ones first?"', 'skill_id': 10, 'factor_id': 2},
    {'id': 137, 'type': 'example', 'text': 'Therapist: "What do you think would change if you were able to improve your communication skills?"', 'skill_id': 10, 'factor_id': 2},
    {'id': 138, 'type': 'example', 'text': 'Therapist: "What outcome would make you feel like therapy has been successful?"', 'skill_id': 10, 'factor_id': 2},
    {'id': 139, 'type': 'example', 'text': 'Therapist: "Can you think of one specific thing you’d like to accomplish by next month?"', 'skill_id': 10, 'factor_id': 2},
    {'id': 140, 'type': 'example', 'text': 'Therapist: "How do you envision your life looking if we focus on this particular goal?"', 'skill_id': 10, 'factor_id': 2},

    # Task Agreement
    {'id': 141, 'type': 'example', 'text': 'Therapist: "What do you think would help you stick to a plan for practicing mindfulness?"', 'skill_id': 10, 'factor_id': 3},
    {'id': 142, 'type': 'example', 'text': 'Therapist: "How do you feel about setting a schedule for daily journaling?"', 'skill_id': 10, 'factor_id': 3},
    {'id': 143, 'type': 'example', 'text': 'Therapist: "Can you describe what success looks like if we implement this approach?"', 'skill_id': 10, 'factor_id': 3},
    {'id': 144, 'type': 'example', 'text': 'Therapist: "What small changes could we make to make this plan easier for you to follow?"', 'skill_id': 10, 'factor_id': 3},
    {'id': 145, 'type': 'example', 'text': 'Therapist: "What do you think is a reasonable first step to start practicing this skill?"', 'skill_id': 10, 'factor_id': 3},
    {'id': 146, 'type': 'example', 'text': 'Therapist: "How would you like to track your progress for this activity?"', 'skill_id': 10, 'factor_id': 3},
    {'id': 147, 'type': 'example', 'text': 'Therapist: "What adjustments could we make to make sure this plan works for you?"', 'skill_id': 10, 'factor_id': 3},
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