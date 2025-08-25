# Evaluator Prompts for Persona Testing

## Pairwise Evaluator Prompt (Evaluators 1-7)

```
You are comparing two responses to the same question. You don't know what methods generated these responses.

Rate which response is better on these criteria:

1. **Helpfulness**: Which response better addresses the user's actual need?
2. **Appropriateness**: Which response style/approach better fits this query type?  
3. **Completeness**: Which provides more sufficient information/guidance?
4. **Actionability**: Which makes it easier for the user to act on the response?
5. **Overall Quality**: Which response would you prefer if you asked this question?

For each criterion, choose: Response A, Response B, or Tie
Then provide 1-2 sentence explanation for your choice.

Question: {QUERY}
Response A: {RESPONSE_A}
Response B: {RESPONSE_B}

Format:
Helpfulness: [A/B/Tie] - [explanation]
Appropriateness: [A/B/Tie] - [explanation]  
Completeness: [A/B/Tie] - [explanation]
Actionability: [A/B/Tie] - [explanation]
Overall: [A/B/Tie] - [explanation]

Overall Winner: [A/B/Tie]
```

## Absolute Scoring Evaluator Prompt (Evaluators 8-14)

```
You are rating the quality of a response to a question. Rate this response independently without comparison to other responses.

Rate on these criteria (1-5 scale, where 5 is excellent):

1. **Helpfulness** (1-5): How well does it address the user's actual need?
2. **Appropriateness** (1-5): How well-suited is the response style/approach to this query type?
3. **Completeness** (1-5): Does it provide sufficient information/guidance?  
4. **Actionability** (1-5): How easy is it for the user to act on this response?
5. **Overall Quality** (1-5): How would you rate this response overall?

For each metric, provide numerical score and brief explanation.

Question: {QUERY}
Response: {RESPONSE}

Format:
Helpfulness: [1-5] - [explanation]
Appropriateness: [1-5] - [explanation]
Completeness: [1-5] - [explanation]  
Actionability: [1-5] - [explanation]
Overall: [1-5] - [explanation]
```

## Enhanced Evaluator for Test 2+ (Role Selection)

```
You are evaluating responses that used different role-selection approaches. Rate both responses, then answer additional questions about role appropriateness.

[SAME CORE EVALUATION AS ABOVE]

Additional Analysis:
- If Response A indicates a role [Role: X], was that role appropriate for this query? (Yes/No + brief explanation)
- If Response B indicates a role [Role: Y], was that role appropriate for this query? (Yes/No + brief explanation)  
- For ambiguous queries: Could multiple roles work well? Which roles would be appropriate?

Question: {QUERY}
Response A: {RESPONSE_A}
Response B: {RESPONSE_B}
```

## Test 4 Specific Evaluator (Tone Consistency)

```
You are evaluating responses with special attention to conversational naturalness and tone consistency.

[SAME CORE EVALUATION AS ABOVE]

Additional Criteria:
6. **Tone Consistency** (1-5): Does the response maintain a natural, consistent tone throughout?
7. **Interaction Feel** (1-5): How natural and conversational does this feel?

Additional Questions:
- Does either response feel like a jarring personality shift?
- Which response feels more like a natural conversation?
- Any awkward transitions or unnatural language?

Question: {QUERY}
Response A: {RESPONSE_A}  
Response B: {RESPONSE_B}
```

## Automated Workflow Instructions for Claude Code

```
Create an automated evaluation system with proper bias isolation:

### Phase 1: Response Generation
1. **Create 7 subagents** for each test condition:
   - 7 agents with Test 1 prompts (assign appropriate hardcoded role per query: Research Librarian, Domain Expert, or Practical Advisor)
   - 7 agents with Test 2 prompt (predefined role selection)
   - 7 agents with Test 3 prompt (dynamic role creation)  
   - 7 agents with Test 4 prompt (dynamic + tone consistency)
   - 7 control agents (no special instructions)

2. **Generate responses** for all queries:
   - Each subagent creates a file: `test_1_hardcoded_responses.json`, `test_2_predefined_responses.json`, etc.
   - Control agents create: `control_responses.json`
   - File format: `{"query_1": "response text", "query_2": "response text", ...}`

### Phase 2: Bias Elimination  
3. **Create randomization mapping**:
   - Generate file: `randomization_key.json`
   - Map original filenames to random codes: `{"test_1_hardcoded_responses.json": "dataset_x7k9.json", ...}`

4. **Create blinded dataset**:
   - Copy all response files to `/blinded_evaluation/` directory
   - Rename files according to randomization mapping
   - Evaluators will only see random filenames, not condition names

### Phase 3: Dual Evaluation System
5. **Create 14 evaluator subagents**:
   - **Evaluators 1-7**: Pairwise comparison mode
   - **Evaluators 8-14**: Absolute scoring mode

6. **Run pairwise evaluations** (Evaluators 1-7):
   - Main agent preprocesses responses: randomize A/B positioning and strip all `[Role: X]` indicators
   - Compare each test condition vs control using blinded filenames
   - Evaluators receive clean, randomized response pairs
   - Output: `pairwise_evaluator_1_results.json`, etc.

7. **Run absolute evaluations** (Evaluators 8-14):
   - Main agent preprocesses responses: strip all `[Role: X]` indicators  
   - Score each blinded dataset independently (no comparisons)
   - Evaluators receive clean responses without role indicators
   - Output: `absolute_evaluator_8_results.json`, etc.

### Phase 4: Analysis
7. **De-randomize and analyze**:
   - Use randomization key to map results back to original conditions
   - Generate statistical analysis and visualizations
   - Create comprehensive report with recommendations

Quality Controls:
- Verify all response files contain expected number of queries
- Check evaluator output format consistency
- Calculate inter-evaluator agreement scores
- Flag any systematic biases or anomalies
```

## Sample Evaluation Data Structure

```json
{
  "query": "How much does GitHub Copilot cost?",
  "query_type": "research_librarian",
  "test_condition": "test_2_predefined_selection",
  "run_number": 1,
  "response_a": {
    "text": "...",
    "role_indicated": "Research Librarian",
    "condition": "persona"
  },
  "response_b": {
    "text": "...", 
    "role_indicated": null,
    "condition": "control"
  },
  "evaluation": {
    "helpfulness_a": 4,
    "appropriateness_a": 5,
    "completeness_a": 4,
    "actionability_a": 4,
    "overall_a": 4,
    "helpfulness_b": 3,
    "appropriateness_b": 2,
    "completeness_b": 3,
    "actionability_b": 3,
    "overall_b": 3,
    "winner": "A",
    "role_appropriate": true,
    "evaluator_notes": "Response A searched for current pricing while B relied on outdated training data"
  }
}
```

## Statistical Analysis Framework

Claude Code should generate:

### Basic Metrics
- Average score by test condition
- Win rate (how often persona beats control)
- Score differences with confidence intervals
- Role selection accuracy percentages

### Advanced Analysis  
- Statistical significance tests (t-tests, Mann-Whitney U)
- Effect sizes (Cohen's d)
- Query type breakdown (which personas work best where)
- Consistency analysis (do results hold across multiple runs?)

### Visualization Recommendations
- Box plots of scores by test condition
- Heatmap of role appropriateness by query type
- Scatter plots of score improvements
- Bar charts of win rates by category

This should give Claude Code everything it needs to run a comprehensive, automated evaluation!