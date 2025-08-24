# Claude Code Implementation Guide

## Project Overview
Implement an automated persona switching experiment using subagents and double-blind evaluation to test whether different AI personas improve response quality.

## Required Artifacts
You have access to these design documents:
- `isolated_persona_experiments` - Complete experimental framework with test prompts and queries
- `evaluator_prompts` - All evaluator prompts and workflow instructions

## Implementation Steps

### Phase 1: Project Setup
```bash
# Create directory structure
mkdir persona_experiment
cd persona_experiment
mkdir responses blinded_evaluation results
```

### Phase 2: Subagent Response Generation

Create subagents for each test condition and generate responses:

**Test Conditions to Implement:**
1. **Control** (3 subagents): No special instructions, standard helpful responses
2. **Test 1 Hardcoded** (3 subagents each): Research Librarian, Domain Expert, Practical Advisor prompts
3. **Test 2 Predefined Selection** (3 subagents): Auto-select from predefined roles 
4. **Test 3 Dynamic Roles** (3 subagents): Create custom roles on-demand
5. **Test 4 Dynamic + Tone** (3 subagents): Dynamic roles with tone consistency

**Response Generation Requirements:**
- Each subagent processes all 12 queries from the experimental framework
- Output format: JSON files named by condition (e.g., `test_1_hardcoded_responses_agent_1.json`)
- JSON structure: `{"query_1": "response text", "query_2": "response text", ...}`
- Include role indicators where applicable: `[Role: X] response text`

### Phase 3: Bias Elimination

**Randomization Process:**
```python
# Generate randomization mapping
randomization_key = {
    "control_responses_agent_1.json": "dataset_" + random_string(),
    "test_1_hardcoded_responses_agent_1.json": "dataset_" + random_string(),
    # ... for all response files
}

# Save mapping for later analysis
save_json(randomization_key, "randomization_key.json")

# Copy and rename files to blinded directory
for original, blinded in randomization_key.items():
    copy_file(f"responses/{original}", f"blinded_evaluation/{blinded}")
```

### Phase 4: Evaluation Setup

**Create 6 Evaluator Subagents:**

**Pairwise Evaluators (1-3):**
- Compare each test condition vs control
- Use pairwise evaluator prompt from artifacts
- Randomize A/B order within comparisons
- Output: `pairwise_evaluator_X_results.json`

**Absolute Evaluators (4-6):**  
- Score each dataset independently
- Use absolute scoring prompt from artifacts
- No comparisons, just individual ratings
- Output: `absolute_evaluator_X_results.json`

**Evaluation Execution:**
```python
# For pairwise evaluations
for test_condition in ["test_1", "test_2", "test_3", "test_4"]:
    for evaluator in [1, 2, 3]:
        compare_datasets(
            condition_file=get_blinded_filename(test_condition),
            control_file=get_blinded_filename("control"),
            evaluator_id=evaluator,
            randomize_order=True
        )

# For absolute evaluations  
for dataset_file in blinded_files:
    for evaluator in [4, 5, 6]:
        score_dataset(
            dataset_file=dataset_file,
            evaluator_id=evaluator
        )
```

### Phase 5: Results Analysis

**De-randomization and Statistical Analysis:**
1. Use randomization key to map results back to original conditions
2. Calculate inter-evaluator reliability (agreement between evaluators)
3. Compute statistical significance tests
4. Generate visualizations and comprehensive report

**Required Analysis:**
- **Pairwise Results**: Win/loss rates for each test vs control
- **Absolute Results**: Average scores by condition with confidence intervals
- **Cross-validation**: Do pairwise and absolute results agree?
- **Query Type Breakdown**: Which personas work best for which query types
- **Statistical Significance**: t-tests, effect sizes, confidence intervals

### Phase 6: Report Generation

Create comprehensive report including:
- Executive summary with key findings
- Detailed results by test condition  
- Statistical analysis with significance tests
- Visualizations (charts, graphs)
- Recommendations for next steps

## Expected Deliverables

1. **Raw Data Files:**
   - All response files by condition and agent
   - All evaluation results
   - Randomization key and metadata

2. **Analysis Results:**
   - Statistical summary with significance tests
   - Inter-evaluator reliability scores
   - Query-type breakdown analysis

3. **Visualizations:**
   - Box plots of scores by condition
   - Win/loss charts for pairwise comparisons  
   - Heatmaps of performance by query type

4. **Final Report:**
   - Executive summary with clear recommendations
   - Detailed methodology and results
   - Discussion of implications and next steps

## Quality Controls

- Verify all subagents generate expected number of responses
- Check evaluator output format consistency
- Calculate inter-evaluator agreement scores  
- Flag any systematic biases or anomalies
- Include confidence intervals for all estimates
- Document any technical issues or limitations

## Success Criteria

The experiment succeeds if it produces:
- Clear evidence whether persona switching improves response quality
- Identification of which specific approaches work best
- Statistical confidence in the results (p < 0.05 for significant findings)
- Actionable recommendations for production implementation

## Timeline Estimate
- Setup and subagent creation: 1-2 hours
- Response generation: 2-3 hours  
- Evaluation execution: 3-4 hours
- Analysis and reporting: 2-3 hours
- **Total: 8-12 hours of automated execution**

This should produce publication-quality experimental results that definitively answer whether persona switching improves AI assistant responses.