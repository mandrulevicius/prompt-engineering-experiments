# Isolated Persona Switching Experiments
Version 0.2

## Experimental Strategy: Isolate Each Variable

By separating tests, we can identify exactly where value comes from and where problems arise.

## Test 1: Hardcoded Roles (Baseline Role Effectiveness)
**Question: Do specialized roles produce better responses than generic responses?**

### Pre-Prompt A1 (Research Librarian Version):
```
You are a Research Librarian. Your primary goal is to find current, accurate information. 
Always prefer searching for recent data over relying on training knowledge for factual queries. 
Be thorough, cite sources, and verify information when possible.
```

### Pre-Prompt A2 (Domain Expert Version):
```
You are a Domain Expert. Provide deep, technical insights assuming user competence. 
Use precise terminology, detailed explanations, and draw from specialized knowledge confidently.
```

### Pre-Prompt A3 (Practical Advisor Version):
```
You are a Practical Advisor. Focus on actionable guidance and step-by-step approaches. 
Consider real-world constraints and provide concrete next steps the user can implement.
```

### Test Protocol:
- Use 7 subagents for this test condition  
- Manually assign each query to most appropriate hardcoded role (Research Librarian for pricing/facts, Domain Expert for technical questions, Practical Advisor for guidance)
- Compare against control (no role instruction)
- Measures: **Pure role effectiveness**

---

## Test 2: Predefined Role Selection (Selection Accuracy)
**Question: Can the model reliably choose appropriate predefined roles?**

### Pre-Prompt B:
```
Before responding, analyze the query and choose the most appropriate role:

- Research Librarian: For pricing, current events, factual lookups needing verification
- Domain Expert: For technical questions requiring specialized knowledge  
- Practical Advisor: For decisions, recommendations, how-to guidance
- Creative Collaborator: For brainstorming, writing, ideation
- Socratic Guide: For learning questions, complex problems needing exploration

Choose one role, indicate it with [Role: X], then respond in that role.
```

### Test Protocol:
- Use 7 subagents for this test condition
- Same queries as Test 1
- Compare role selection accuracy vs. human judgment
- Compare response quality vs. Test 1 hardcoded versions
- Measures: **Selection accuracy + role effectiveness combined**

---

## Test 3: Dynamic Role Creation (Maximum Flexibility)
**Question: Does creating custom roles on-demand work better than predefined roles?**

### Pre-Prompt C:
```
Before responding, analyze what type of response would be most helpful for this specific query. 
Create an appropriate role/persona that would best serve the user's needs, then adopt that role.

Indicate your chosen role with [Role: X] and respond accordingly.
```

### Test Protocol:
- Use 7 subagents for this test condition
- Same queries as previous tests
- Track what roles the model invents
- Compare response quality vs. predefined role versions
- Measures: **Creative role adaptation + effectiveness**

---

## Test 4: Dynamic Roles with Tone Consistency (Practical Constraints)
**Question: Can we maintain flexibility while avoiding jarring tone shifts?**

### Pre-Prompt D:
```
Before responding, analyze what type of response would be most helpful for this specific query. 
Create an appropriate role/persona that would best serve the user's needs.

IMPORTANT: Maintain a consistent, professional tone throughout. Avoid sudden personality shifts 
that might feel jarring to the user. Your role should enhance helpfulness while keeping the 
interaction feeling natural and coherent.

Indicate your chosen role with [Role: X] and respond accordingly.
```

### Test Protocol:
- Use 7 subagents for this test condition
- Same queries as previous tests
- Add evaluation criteria for "tone consistency" and "natural interaction feel"
- Compare effectiveness vs. pure dynamic approach (Test 3)
- Measures: **Practical usability + effectiveness**

## Evaluation Framework

### Metrics for Each Test
**Core Metrics (all tests):**
- Helpfulness (1-5)
- Appropriateness (1-5) 
- Completeness (1-5)
- Actionability (1-5)

**Additional Metrics by Test:**
- **Test 2**: Role selection accuracy (correct/incorrect)
- **Test 3**: Role creativity/novelty (1-5)
- **Test 4**: Tone consistency (1-5), Natural interaction feel (1-5)

### Sample Query Set (Strategic Selection)
**Clear Research Librarian queries:**
1. "How much does GitHub Copilot cost in 2025?"
2. "What's the latest news about OpenAI's GPT models?"

**Clear Domain Expert queries:**
3. "Explain the CAP theorem and its practical implications"
4. "How do I implement OAuth 2.0 flow securely?"

**Clear Practical Advisor queries:**
5. "Should I use React or Vue for my startup's frontend?"
6. "How do I structure salary negotiations as a senior engineer?"

**Ambiguous/Complex queries (test adaptability):**
7. "I want to learn machine learning but I'm a complete beginner" *(Could be Socratic Guide OR Practical Advisor)*
8. "Help me debug this performance issue in my Node.js app" *(Could be Domain Expert OR Practical Advisor)*
9. "I need to convince my CEO to adopt AI tools" *(Could be Practical Advisor OR Creative Collaborator)*

**Deliberately ambiguous queries (test edge cases):**
10. "What should I know about blockchain?" *(Research Librarian for facts, Domain Expert for technical depth, or Practical Advisor for decision guidance?)*
11. "I'm having trouble with my team's productivity" *(Practical Advisor for solutions, Socratic Guide for exploration, or Creative Collaborator for novel approaches?)*
12. "Tell me about Python" *(Domain Expert for technical details, Practical Advisor for learning path, or Socratic Guide for needs assessment?)*

### Experimental Timeline
**Each test condition requires:**
- 7 subagents generating responses to 12 queries
- 14 evaluators (7 pairwise + 7 absolute) with bias controls
- A/B position randomization and role indicator hiding

**Estimated timeline:**
- Response generation: ~45 min per test condition
- Evaluation setup and execution: ~60 min per test condition
- **Total time for all 4 tests: ~7 hours**

## Expected Insights

### Test 1 Results Will Show:
- Whether specialized roles actually improve responses
- Which types of roles work best for which queries
- Baseline effectiveness ceiling

### Test 2 Results Will Show:
- How accurately the model selects appropriate roles
- Whether automatic selection maintains quality from Test 1
- Common selection mistakes

### Test 3 Results Will Show:
- Whether dynamic role creation outperforms predefined roles
- What kinds of novel roles the model invents
- Whether flexibility improves or hurts consistency

### Test 4 Results Will Show:
- Cost of adding tone consistency constraints
- Whether "natural interaction" is compatible with role switching
- Practical usability for real conversations

## Decision Tree Based on Results

### If Test 1 fails:
- **Stop here** - role-based responses aren't better than generic
- Maybe try different role definitions or query types

### If Test 1 succeeds but Test 2 fails:
- **Use hardcoded role assignment** (manual or rule-based)
- Model can't reliably choose roles automatically

### If Tests 1-2 succeed but Test 3 fails:
- **Stick with predefined roles** - flexibility doesn't add value
- Focus on expanding/refining predefined role library

### If Tests 1-3 succeed but Test 4 fails:
- **Trade-off decision needed** - effectiveness vs. usability
- Maybe tone consistency matters more than peak performance

### If all tests succeed:
- **Jackpot** - dynamic role creation with tone consistency works
- Proceed to build automated version

## Documentation Strategy

### Track Everything:
- Exact prompts used
- All responses generated  
- Role selections made (Tests 2-4)
- Evaluation scores with explanations
- Personal observations about response quality
- Any surprising or unexpected behaviors

### Create Comparison Matrix:
| Query | Control | Test 1 | Test 2 | Test 3 | Test 4 | Best Performer |
|-------|---------|--------|--------|--------|--------|----------------|
| Q1    | Score   | Score  | Score  | Score  | Score  | Winner         |

### Prepare Executive Summary:
"We tested 4 approaches to persona switching:
- Hardcoded roles improved responses by X%
- Automatic role selection worked Y% of the time
- Dynamic roles [improved/didn't improve] on predefined
- Tone consistency [cost/didn't cost] performance
- Recommendation: Approach Z for production implementation"

## The Beauty of This Design

1. **Clean variable isolation** - we know exactly what contributes to success/failure
2. **Incremental complexity** - each test builds on the previous
3. **Practical constraints included** - Test 4 addresses real-world usability
4. **Clear decision framework** - results directly inform next steps
5. **Still zero cost** - just time and systematic execution

This experimental design is honestly quite sophisticated for something that costs nothing but time!