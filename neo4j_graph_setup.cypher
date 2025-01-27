////////////////////////////////////////////////////////////////////////
// 1. CREATE OR MERGE THE ROOT NODE (UPDATED DESCRIPTION AND NAME ATTRIBUTE)
////////////////////////////////////////////////////////////////////////
MERGE (tr:ChangePrinciple {
  name: "TR",
  full_label: "Therapeutic Relationship",
  description: "A therapist relates to their client empathically to form a discernible bond and an attitude of working together on tasks to move toward agreed-upon goals that help the client remoralize. Therapists attend to potential ruptures with the intention to repair."
})

////////////////////////////////////////////////////////////////////////
// 2. CREATE COMMON FACTORS (UPDATED DESCRIPTION AND NAME ATTRIBUTE)
////////////////////////////////////////////////////////////////////////
MERGE (bond:CommonFactor {
  name: "B",
  full_label: "Bond",
  description: "Therapists orient to the client in order to work on a therapeutic bond by taking a stance of empathy, compassion, and acceptance, with the aims of understanding and of helping the client feel understood and supported in a true partnership."
})
MERGE (ga:CommonFactor {
  name: "GA",
  full_label: "Goal alignment",
  description: "Therapists work to understand their client's desires for change, conceptualize their client's demoralization, and facilitate conversation about the goals they will work on together to address to bring about remoralization. They do this with an attitude of collaboration to negotiate these goals."
})
MERGE (ta:CommonFactor {
  name: "TA",
  full_label: "Task agreement",
  description: "Therapists facilitate client engagement by clarifying how therapist and client work together and focusing their in-session attention on agreed-upon content and concomitant therapeutic actions that will lead to change. This involves clarifying roles, processes, settings, and session agendas, and ensuring that both therapist and client are aligned on these aspects. The therapist seeks feedback on alignment of session agenda with treatment goals and on therapist in-session procedures."
})

////////////////////////////////////////////////////////////////////////
// 3. LINK THE ROOT NODE TO EACH COMMON FACTOR
////////////////////////////////////////////////////////////////////////
MERGE (tr)-[:INCLUDES]->(bond)
MERGE (tr)-[:INCLUDES]->(ga)
MERGE (tr)-[:INCLUDES]->(task)

////////////////////////////////////////////////////////////////////////
// 4. CREATE INTERVENTION CONCEPTS (UPDATED DESCRIPTION AND NAME ATTRIBUTE)
////////////////////////////////////////////////////////////////////////
MERGE (ear:InterventionConcept {
  name: "EAR",
  full_label: "Empathy, Acceptance and Positive Regard",
  description: "The therapist shows the capacity to understand, share, and genuinely connect with the patient's thoughts, feelings, and experiences by listening attentively to the patient's concerns without judgment; understanding and validating the patient's emotions and experiences; demonstrating compassion, warmth, and genuine care for the patient's well-being; communicating understanding and support, helping the patient feel heard and valued. Acceptance includes that the therapist sees the client's inherent absolute worth and potential, honors their autonomy, and affirms their personal strengths and efforts. (Bailey & Ogles, p. 48). Positive regard involves prizing and acknowledging what is positive in your clients (Miller & Moyers, p. 46)."
})
MERGE (cp:InterventionConcept {
  name: "CP",
  full_label: "Collaboration and Partnership",
  description: "The therapist is open to conversations and opportunities to explore client values, goals, and needs and to accept their differences and respect their autonomy. The therapist expresses to the client that he sees the client as an equal who brings strengths, talents, and personal expertise to the relationship. The therapist expresses directly or indirectly that they view the client as a partner in resolving the client's challenges. Therapist attempts to create we-ness, e.g. by using we and together instead  of you, asking questions about the fit of interpretations, conclusions, goals, etc."
})

MERGE (bond)-[:INCLUDES]->(ear)
MERGE (bond)-[:INCLUDES]->(CP)

////////////////////////////////////////////////////////////////////////
// 5. CREATE THERAPEUTIC SKILLS (UPDATED NAME AND ADDED FULL_LABEL ATTRIBUTE)
////////////////////////////////////////////////////////////////////////
MERGE (rl:TherapeuticSkill {
  name: "RL",
  full_label: "Reflective Listening",
  description: "Actively listening and reflecting to demonstrate understanding."
})
MERGE (gn:TherapeuticSkill {
  name: "G",
  full_label: "Genuineness",
  description: "Being authentic, sincere, and transparent in interactions."
})
MERGE (v:TherapeuticSkill {
  name: "V",
  full_label: "Validation",
  description: "Recognizing and affirming the client's experiences and feelings."
})
MERGE (af:TherapeuticSkill {
  name: "A",
  full_label: "Affirmation",
  description: "Highlighting the client's strengths and efforts."
})
MERGE (ra:TherapeuticSkill {
  name: "RA",
  full_label: "Respect for Autonomy",
  description: "Honoring the client’s independence and choices."
})
MERGE (ap:TherapeuticSkill {
  name: "AP",
  full_label: "Asking for Permission",
  description: "Seeking the client's consent before offering suggestions."
})
MERGE (oq:TherapeuticSkill {
  name: "OQ",
  full_label: "Open-ended Question",
  description: "Inviting deeper, more expansive client responses."
})

////////////////////////////////////////////////////////////////////////
// 6. LINK INTERVENTION CONCEPTS TO ALL THERAPEUTIC SKILLS WITH "EXPRESSES"
////////////////////////////////////////////////////////////////////////
MERGE (ear)<-[:EXPRESSES]-(rl)
MERGE (ear)<-[:EXPRESSES]-(gn)
MERGE (ear)<-[:EXPRESSES]-(v)
MERGE (ear)<-[:EXPRESSES]-(af)
MERGE (ear)<-[:EXPRESSES]-(ra)
MERGE (ear)<-[:EXPRESSES]-(ap)
MERGE (ear)<-[:EXPRESSES]-(oq)

MERGE (cp)-[:EXPRESSES]->(rl)
MERGE (cp)-[:EXPRESSES]->(gn)
MERGE (cp)-[:EXPRESSES]->(v)
MERGE (cp)-[:EXPRESSES]->(af)
MERGE (cp)-[:EXPRESSES]->(ra)
MERGE (cp)-[:EXPRESSES]->(ap)
MERGE (cp)-[:EXPRESSES]->(oq)

////////////////////////////////////////////////////////////////////////
// 7. LINK SKILLS TO OTHER COMMON FACTORS
////////////////////////////////////////////////////////////////////////
MERGE (rl)-[:SUPPORTS]->(ga)
MERGE (rl)-[:SUPPORTS]->(task)

MERGE (gn)-[:SUPPORTS]->(ga)
MERGE (gn)-[:SUPPORTS]->(task)

MERGE (v)-[:SUPPORTS]->(ga)
MERGE (v)-[:SUPPORTS]->(task)

MERGE (af)-[:SUPPORTS]->(ga)
MERGE (af)-[:SUPPORTS]->(task)

MERGE (ra)-[:SUPPORTS]->(ga)
MERGE (ra)-[:SUPPORTS]->(task)

MERGE (ap)-[:SUPPORTS]->(ga)
MERGE (ap)-[:SUPPORTS]->(task)

MERGE (oq)-[:SUPPORTS]->(ga)
MERGE (oq)-[:SUPPORTS]->(task)

////////////////////////////////////////////////////////////////////////
// 8. CREATE EXAMPLE NODES WITH THE TRIADIC PATTERN
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
// EAR/V Examples
////////////////////////////////////////////////////////////////////////
MERGE (ex1:Example {
  text: "I hear you, and it must feel awful to be criticized in that way."
})
MERGE (ex1)-[:DEMONSTRATES]->(v)  // Links to Validation (V)
MERGE (ex1)-[:EXPRESSES]->(ear)  // Links to EAR

MERGE (ex2:Example {
  text: "It sounds like you’re feeling really overwhelmed right now. That’s completely understandable given what you’re going through."
})
MERGE (ex2)-[:DEMONSTRATES]->(v)
MERGE (ex2)-[:EXPRESSES]->(ear)

MERGE (ex3:Example {
  text: "I can hear the pain in your voice when you talk about that experience. It must have been incredibly hard for you."
})
MERGE (ex3)-[:DEMONSTRATES]->(v)
MERGE (ex3)-[:EXPRESSES]->(ear)

////////////////////////////////////////////////////////////////////////
// EAR/RL Examples
////////////////////////////////////////////////////////////////////////
MERGE (ex4:Example {
  text: "And yet, as you say, you do have these desires and you do have your feelings, but- but you don't feel good about them?"
})
MERGE (ex4)-[:DEMONSTRATES]->(rl)  // Links to Reflective Listening (RL)
MERGE (ex4)-[:EXPRESSES]->(ear)

MERGE (ex5:Example {
  text: "Yeah, I get the disappointment - that here, a lot of these things you’d thought you'd worked through, and now the guilts and the feeling that only a part of you is acceptable to anybody else."
})
MERGE (ex5)-[:DEMONSTRATES]->(rl)
MERGE (ex5)-[:EXPRESSES]->(ear)

MERGE (ex6:Example {
  text: "I guess I do catch the real deep puzzlement that you feel as to What the hell shall I do? What can I do?"
})
MERGE (ex6)-[:DEMONSTRATES]->(rl)
MERGE (ex6)-[:EXPRESSES]->(ear)

////////////////////////////////////////////////////////////////////////
// EAR/G Examples
////////////////////////////////////////////////////////////////////////
MERGE (ex7:Example {
  text: "Hearing about your experience made me feel a deep sense of empathy for what you’ve gone through. It’s incredibly impactful."
})
MERGE (ex7)-[:DEMONSTRATES]->(gn)  // Links to Genuineness (G)
MERGE (ex7)-[:EXPRESSES]->(ear)

////////////////////////////////////////////////////////////////////////
// EAR/A Examples
////////////////////////////////////////////////////////////////////////
MERGE (ex8:Example {
  text: "You have a great deal of patience and courage, I admire that."
})
MERGE (ex8)-[:DEMONSTRATES]->(af)  // Links to Affirmation (A)
MERGE (ex8)-[:EXPRESSES]->(ear)

MERGE (ex9:Example {
  text: "As you talk about all of the troubles you've been through, do you know what strikes me? You are a real survivor. You've taken a lot of hard knocks, and you're still here."
})
MERGE (ex9)-[:DEMONSTRATES]->(af)
MERGE (ex9)-[:EXPRESSES]->(ear)

MERGE (ex10:Example {
  text: "Thank you for being willing to discuss our relationship. It is very helpful."
})
MERGE (ex10)-[:DEMONSTRATES]->(af)
MERGE (ex10)-[:EXPRESSES]->(ear)

MERGE (ex11:Example {
  text: "You intended not to drink at all this week, and you had five days with no alcohol at all. That's amazing! How did you do that?"
})
MERGE (ex11)-[:DEMONSTRATES]->(af)
MERGE (ex11)-[:EXPRESSES]->(ear)

MERGE (ex12:Example {
  text: "You deeply love your children and want to do all you can to protect them."
})
MERGE (ex12)-[:DEMONSTRATES]->(af)
MERGE (ex12)-[:EXPRESSES]->(ear)

MERGE (ex13:Example {
  text: "I appreciate you being so open and forthright about what is going through your mind here."
})
MERGE (ex13)-[:DEMONSTRATES]->(af)
MERGE (ex13)-[:EXPRESSES]->(ear)

////////////////////////////////////////////////////////////////////////
// EAR/RA Examples
////////////////////////////////////////////////////////////////////////
MERGE (ex14:Example {
  text: "I support your decision to set boundaries in that relationship. It sounds like it’s what you need for your well-being."
})
MERGE (ex14)-[:DEMONSTRATES]->(ra)  // Links to Respect for Autonomy (RA)
MERGE (ex14)-[:EXPRESSES]->(ear)

MERGE (ex15:Example {
  text: "This is just my opinion of course, and you might disagree, but from my perspective, it seems that you have a number of qualities that make you a good candidate for this treatment."
})
MERGE (ex15)-[:DEMONSTRATES]->(ra)
MERGE (ex15)-[:EXPRESSES]->(ear)

MERGE (ex16:Example {
  text: "I'll tell you what I heard there and you tell me if I got it or not, but it's kind of like, you've been so busy from the time you were a girl, being a role model, and having these abilities, that you had no resting place."
})
MERGE (ex16)-[:DEMONSTRATES]->(ra)
MERGE (ex16)-[:EXPRESSES]->(ear)

MERGE (ex17:Example {
  text: "You’ve got the strength and ability to handle this. What strategies have worked for you in the past?"
})
MERGE (ex17)-[:DEMONSTRATES]->(ra)
MERGE (ex17)-[:EXPRESSES]->(ear)

////////////////////////////////////////////////////////////////////////
// EAR Examples (no linked skill)
////////////////////////////////////////////////////////////////////////
MERGE (ex18:Example {
  text: "You’re safe here to express whatever you’re feeling. There’s no judgment, only support."
})
MERGE (ex18)-[:EXPRESSES]->(ear)

MERGE (ex19:Example {
  text: "I hear you, and I want to understand what you're experiencing."
})
MERGE (ex19)-[:EXPRESSES]->(ear)

////////////////////////////////////////////////////////////////////////
// CP/RA Examples
////////////////////////////////////////////////////////////////////////
MERGE (ex20:Example {
  text: "You know yourself better than anyone else. What do you think would be the most helpful next step?"
})
MERGE (ex20)-[:DEMONSTRATES]->(ra)  // Links to Respect for Autonomy (RA)
MERGE (ex20)-[:EXPRESSES]->(cp)  // Links to CP

MERGE (ex21:Example {
  text: "We’ll move at a pace that feels comfortable for you. Let me know if you ever need to slow down or take a break."
})
MERGE (ex21)-[:DEMONSTRATES]->(ra)
MERGE (ex21)-[:EXPRESSES]->(cp)

MERGE (ex22:Example {
  text: "How do you feel about the options we’ve discussed? Which one resonates most with you?"
})
MERGE (ex22)-[:DEMONSTRATES]->(ra)
MERGE (ex22)-[:EXPRESSES]->(cp)

MERGE (ex23:Example {
  text: "You have a lot of insight into your own life. What do you believe is the root of this issue?"
})
MERGE (ex23)-[:DEMONSTRATES]->(ra)
MERGE (ex23)-[:EXPRESSES]->(cp)

MERGE (ex24:Example {
  text: "I believe you have the skills to manage this situation. How would you like to approach it?"
})
MERGE (ex24)-[:DEMONSTRATES]->(ra)
MERGE (ex24)-[:EXPRESSES]->(cp)

MERGE (ex25:Example {
  text: "It’s your decision, and I’m here to support you in whatever you choose. What possibilities are you considering?"
})
MERGE (ex25)-[:DEMONSTRATES]->(ra)
MERGE (ex25)-[:EXPRESSES]->(cp)

MERGE (ex26:Example {
  text: "You are certainly the expert in knowing yourself, and we will need to draw on that expertise as we progress."
})
MERGE (ex26)-[:DEMONSTRATES]->(ra)
MERGE (ex26)-[:EXPRESSES]->(cp)

////////////////////////////////////////////////////////////////////////
// CP/G Examples
////////////////////////////////////////////////////////////////////////
MERGE (ex27:Example {
  text: "I realize I might not fully understand your experience right now, and I appreciate your patience as we work through this together."
})
MERGE (ex27)-[:DEMONSTRATES]->(gn)  // Links to Genuineness (G)
MERGE (ex27)-[:EXPRESSES]->(cp)

////////////////////////////////////////////////////////////////////////
// CP Examples (no linked skill)
////////////////////////////////////////////////////////////////////////
MERGE (ex28:Example {
  text: "Although no course of treatment is foolproof, I do believe that we can work together to help you deal with your problems."
})
MERGE (ex28)-[:EXPRESSES]->(cp)

MERGE (ex29:Example {
  text: "You are certainly the expert in knowing yourself, and we will need to draw on that expertise as we progress. And, as an expert in this treatment approach, I can help to guide you through the process of therapy. The important thing is that we collaborate throughout the experience. Does this make sense?"
})
MERGE (ex29)-[:EXPRESSES]->(cp)

MERGE (ex30:Example {
  text: "You have a say in your treatment, and we'll collaborate on the best path forward."
})
MERGE (ex30)-[:EXPRESSES]->(cp)

MERGE (ex31:Example {
  text: "Our work together is a collaboration. Your insights and feedback are essential in tailoring our sessions to your needs."
})
MERGE (ex31)-[:EXPRESSES]->(cp)

MERGE (ex32:Example {
  text: "Your therapy is about you. We'll customize our approach to align with your specific needs and aspirations."
})
MERGE (ex32)-[:EXPRESSES]->(cp)

MERGE (ex33:Example {
  text: "I hope you feel comfortable sharing your true thoughts and feelings here. Your honesty is a vital part of our work together."
})
MERGE (ex33)-[:EXPRESSES]->(cp)

MERGE (ex34:Example {
  text: "I know you’re feeling frustrated right now, and I’m here to support you. Let’s work together to find a way through this."
})
MERGE (ex34)-[:EXPRESSES]->(cp)

////////////////////////////////////////////////////////////////////////
// GA/RA Examples
////////////////////////////////////////////////////////////////////////
MERGE (ex35:Example {
  text: "Let’s focus on what you want to achieve in therapy. What are your goals for our work together?"
})
MERGE (ex35)-[:DEMONSTRATES]->(ra)  // Links to Respect for Autonomy (RA)
MERGE (ex35)-[:FOSTERS]->(ga)  // Links to Goal Alignment (GA)

MERGE (ex36:Example {
  text: "It’s important that the direction we take aligns with what you want to accomplish. What are your priorities right now?"
})
MERGE (ex36)-[:DEMONSTRATES]->(ra)
MERGE (ex36)-[:FOSTERS]->(ga)

MERGE (ex37:Example {
  text: "Let's work together to define some realistic objectives for you."
})
MERGE (ex37)-[:DEMONSTRATES]->(ra)
MERGE (ex37)-[:FOSTERS]->(ga)

MERGE (ex38:Example {
  text: "If at any point you feel the need to adjust our goals or priorities, please don't hesitate to let me know."
})
MERGE (ex38)-[:DEMONSTRATES]->(ra)
MERGE (ex38)-[:FOSTERS]->(ga)

////////////////////////////////////////////////////////////////////////
// GA/OQ Examples
////////////////////////////////////////////////////////////////////////
MERGE (ex39:Example {
  text: "Can you tell me more about what brings you to therapy and what changes you’re hoping to see in your life?"
})
MERGE (ex39)-[:DEMONSTRATES]->(oq)  // Links to Open-ended Question (OQ)
MERGE (ex39)-[:FOSTERS]->(ga)

MERGE (ex40:Example {
  text: "What would you like to achieve through our sessions together? What are the most important changes you want to make?"
})
MERGE (ex40)-[:DEMONSTRATES]->(oq)
MERGE (ex40)-[:FOSTERS]->(ga)

MERGE (ex41:Example {
  text: "I want to make sure that the goals we set are ones that feel right for you. How do these goals align with what you’re hoping to achieve?"
})
MERGE (ex41)-[:DEMONSTRATES]->(oq)
MERGE (ex41)-[:FOSTERS]->(ga)

MERGE (ex42:Example {
  text: "Let’s work together to identify some concrete steps you can take towards your goals. What are some small, manageable actions that you feel ready to start with?"
})
MERGE (ex42)-[:DEMONSTRATES]->(oq)
MERGE (ex42)-[:FOSTERS]->(ga)

MERGE (ex43:Example {
  text: "By setting these goals, we’re creating a roadmap for your progress. How do you feel about these goals?"
})
MERGE (ex43)-[:DEMONSTRATES]->(oq)
MERGE (ex43)-[:FOSTERS]->(ga)

////////////////////////////////////////////////////////////////////////
// GA/RL/OQ Examples
////////////////////////////////////////////////////////////////////////
MERGE (ex44:Example {
  text: "It sounds like you’ve been feeling very discouraged and overwhelmed. Can you help me understand more about what’s contributing to these feelings?"
})
MERGE (ex44)-[:DEMONSTRATES]->(rl)  // Links to Reflective Listening (RL)
MERGE (ex44)-[:DEMONSTRATES]->(oq)  // Links to Open-ended Question (OQ)
MERGE (ex44)-[:FOSTERS]->(ga)

////////////////////////////////////////////////////////////////////////
// GA/SS/OQ Examples
////////////////////////////////////////////////////////////////////////
//MERGE (ex45:Example {
//  text: "Based on what we’ve discussed, it seems like reducing your anxiety and improving your self-confidence are key goals for you. How do you feel about focusing on these areas?"
//})
//MERGE (ex45)-[:DEMONSTRATES]->(ss)  // Links to Specific Steps (SS)
//MERGE (ex45)-[:DEMONSTRATES]->(oq)  // Links to Open-ended Question (OQ)
//MERGE (ex45)-[:FOSTERS]->(ga)

////////////////////////////////////////////////////////////////////////
// GA/SS Examples
////////////////////////////////////////////////////////////////////////
//MERGE (ex46:Example {
//  text: "You mentioned wanting to improve your relationships and feel more motivated at work. Let’s talk about specific goals we can set to work towards these outcomes."
//})
//MERGE (ex46)-[:DEMONSTRATES]->(ss)  // Links to Specific Steps (SS)
//MERGE (ex46)-[:FOSTERS]->(ga)

////////////////////////////////////////////////////////////////////////
// GA Examples (no linked skill)
////////////////////////////////////////////////////////////////////////
MERGE (ex47:Example {
  text: "That has been really useful to help me understand a little about what has led you to seek treatment; next it might be helpful for us to think together about what your hopes for the future might be."
})
MERGE (ex47)-[:FOSTERS]->(ga)

MERGE (ex48:Example {
  text: "Ok, now that we have agreed upon the goals you want to work on, it would be helpful to get an idea of where you are right now with each of the goals. This will help us get an idea of where we are starting from, and what you have already managed to achieve, and it can help us keep track of how far you have moved on, at a later date."
})
MERGE (ex48)-[:FOSTERS]->(ga)

////////////////////////////////////////////////////////////////////////
// GA/V Examples
////////////////////////////////////////////////////////////////////////
MERGE (ex49:Example {
  text: "I can appreciate your desire to stay with your past. Can we think about that in terms of our treatment plan and goals? I am open to revising our focus if it makes sense to us in terms of what we are trying to accomplish—and it very well may."
})
MERGE (ex49)-[:DEMONSTRATES]->(v)  // Links to Validation (V)
MERGE (ex49)-[:FOSTERS]->(ga)

////////////////////////////////////////////////////////////////////////
// TA/RA Examples
////////////////////////////////////////////////////////////////////////
MERGE (ex50:Example {
  text: "You know yourself better than anyone else. What do you think would be the most helpful next step?"
})
MERGE (ex50)-[:DEMONSTRATES]->(ra)  // Links to Respect for Autonomy (RA)
MERGE (ex50)-[:FOSTERS]->(ta)  // Links to Task Agreement (TA)

MERGE (ex51:Example {
  text: "We’ll move at a pace that feels comfortable for you. Let me know if you ever need to slow down or take a break."
})
MERGE (ex51)-[:DEMONSTRATES]->(ra)
MERGE (ex51)-[:FOSTERS]->(ta)

MERGE (ex52:Example {
  text: "How do you feel about the options we’ve discussed? Which one resonates most with you?"
})
MERGE (ex52)-[:DEMONSTRATES]->(ra)
MERGE (ex52)-[:FOSTERS]->(ta)

MERGE (ex53:Example {
  text: "What do you think would be the best approach for you to take in this situation?"
})
MERGE (ex53)-[:DEMONSTRATES]->(ra)
MERGE (ex53)-[:FOSTERS]->(ta)

MERGE (ex54:Example {
  text: "I’ve been thinking about incorporating some elements of art therapy into our sessions. Would you be interested in that?"
})
MERGE (ex54)-[:DEMONSTRATES]->(ra)
MERGE (ex54)-[:FOSTERS]->(ta)

MERGE (ex55:Example {
  text: "In our sessions, my role is to guide and support you in exploring your thoughts and feelings, while your role is to actively engage in this process and share openly. Does that sound good to you?"
})
MERGE (ex55)-[:DEMONSTRATES]->(ra)
MERGE (ex55)-[:FOSTERS]->(ta)

MERGE (ex56:Example {
  text: "We’ll meet here weekly for 50-minute sessions. If you ever need to reschedule or have any concerns about the setting, please let me know. Does that work for you?"
})
MERGE (ex56)-[:DEMONSTRATES]->(ra)
MERGE (ex56)-[:FOSTERS]->(ta)

////////////////////////////////////////////////////////////////////////
// TA/CP Examples
////////////////////////////////////////////////////////////////////////
MERGE (ex57:Example {
  text: "You are certainly the expert in knowing yourself, and we will need to draw on that expertise as we progress. And, as an expert in this treatment approach, I can help to guide you through the process of therapy. The important thing is that we collaborate throughout the experience. Does this make sense?"
})
MERGE (ex57)-[:DEMONSTRATES]->(cp)  // Links to Collaboration and Partnership (CP)
MERGE (ex57)-[:FOSTERS]->(ta)

MERGE (ex58:Example {
  text: "Our work together is a collaboration. Your insights and feedback are essential in tailoring our sessions to your needs."
})
MERGE (ex58)-[:DEMONSTRATES]->(cp)
MERGE (ex58)-[:FOSTERS]->(ta)

MERGE (ex59:Example {
  text: "Today, I thought we could focus on the anxiety you’ve been experiencing at work. Does that align with what you want to work on today?"
})
MERGE (ex59)-[:DEMONSTRATES]->(cp)
MERGE (ex59)-[:FOSTERS]->(ta)

MERGE (ex60:Example {
  text: "We’ve been working on developing coping strategies for your stress. Do you feel that these strategies are aligning with your overall goal of feeling more in control?"
})
MERGE (ex60)-[:DEMONSTRATES]->(cp)
MERGE (ex60)-[:FOSTERS]->(ta)

MERGE (ex61:Example {
  text: "After you've told me about your challenges, I have some ideas about how we could best address them. I'll explain them to you and would like to understand if they align with what you had in mind when you decided to start therapy. If you have any questions or input, please let me know."
})
MERGE (ex61)-[:DEMONSTRATES]->(cp)
MERGE (ex61)-[:FOSTERS]->(ta)

////////////////////////////////////////////////////////////////////////
// TA/OQ Examples
////////////////////////////////////////////////////////////////////////
MERGE (ex62:Example {
  text: "Let’s work together to identify some concrete steps you can take towards your goals. What are some small, manageable actions that you feel ready to start with?"
})
MERGE (ex62)-[:DEMONSTRATES]->(oq)  // Links to Open-ended Question (OQ)
MERGE (ex62)-[:FOSTERS]->(ta)

MERGE (ex63:Example {
  text: "How are you feeling about the progress we’re making towards your goals? Are there any adjustments you think we need to make?"
})
MERGE (ex63)-[:DEMONSTRATES]->(oq)
MERGE (ex63)-[:FOSTERS]->(ta)

MERGE (ex64:Example {
  text: "Our sessions will take place here in this office, which is a confidential and safe space for you to talk about anything you need to. Is there anything you need to feel more comfortable in this setting?"
})
MERGE (ex64)-[:DEMONSTRATES]->(oq)
MERGE (ex64)-[:FOSTERS]->(ta)

////////////////////////////////////////////////////////////////////////
// TA Examples (no linked skill)
////////////////////////////////////////////////////////////////////////
MERGE (ex65:Example {
  text: "We will try to understand what stresses and relationships in your life may be contributing to depression."
})
MERGE (ex65)-[:FOSTERS]->(ta)

MERGE (ex66:Example {
  text: "I want to make sure you understand that therapy is a collaborative process. We’ll work together to identify the issues you want to focus on and develop strategies to address them. Is that clear?"
})
MERGE (ex66)-[:FOSTERS]->(ta)

MERGE (ex67:Example {
  text: "I'd like to meet with you once a week for twelve to sixteen more times for about an hour each time, to try to understand with you the stresses in your life and how they relate to your depression."
})
MERGE (ex67)-[:FOSTERS]->(ta)

////////////////////////////////////////////////////////////////////////
// TA/AP Examples
////////////////////////////////////////////////////////////////////////
MERGE (ex68:Example {
  text: "I’d like to try a mindfulness exercise that might help you manage your anxiety. Would you be open to giving it a try?"
})
MERGE (ex68)-[:DEMONSTRATES]->(ap)  // Links to Asking for Permission (AP)
MERGE (ex68)-[:FOSTERS]->(ta)

MERGE (ex69:Example {
  text: "I have a homework assignment that might help you practice the skills we’re working on. Would you be willing to try it this week?"
})
MERGE (ex69)-[:DEMONSTRATES]->(ap)
MERGE (ex69)-[:FOSTERS]->(ta)