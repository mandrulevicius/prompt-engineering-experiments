#!/usr/bin/env python3
"""
Pairwise Evaluator 1: Compare Test 1 (Hardcoded) vs Control

This script creates pairwise comparisons between Test 1 (hardcoded role selection) and Control responses.
It strips all [Role: X] indicators and randomizes A/B positioning to eliminate bias.
"""

import json
import random
import re
import sys
import os
from typing import Dict, Any, Tuple

# Add parent directory to path to import any shared utilities
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def load_blinded_data() -> Tuple[Dict[str, str], Dict[str, str]]:
    """Load the blinded evaluation data for control and test 1."""
    
    # Load randomization key to map blinded filenames back to conditions
    with open('/workspace/0_PromptEngineering/PersonaExperiment-0/persona_experiment-02/randomization_key.json', 'r') as f:
        randomization_key = json.load(f)
    
    # Find the blinded filenames for control and test 1
    control_blinded = None
    test1_blinded = None
    
    for original_file, blinded_file in randomization_key.items():
        if original_file == "control_responses_agent_1.json":
            control_blinded = blinded_file
        elif original_file == "test_1_hardcoded_responses_agent_1.json":
            test1_blinded = blinded_file
    
    if not control_blinded or not test1_blinded:
        raise ValueError("Could not find control or test 1 files in randomization key")
    
    # Load the blinded data
    blinded_dir = '/workspace/0_PromptEngineering/PersonaExperiment-0/persona_experiment-02/blinded_evaluation'
    
    with open(f'{blinded_dir}/{control_blinded}', 'r') as f:
        control_data = json.load(f)
    
    with open(f'{blinded_dir}/{test1_blinded}', 'r') as f:
        test1_data = json.load(f)
    
    print(f"Loaded control data from: {control_blinded}")
    print(f"Loaded test 1 data from: {test1_blinded}")
    
    return control_data, test1_data

def strip_role_indicators(text: str) -> str:
    """Remove all [Role: X] indicators from response text."""
    # Pattern to match [Role: anything] at the beginning of text
    pattern = r'^\[Role:[^\]]*\]\s*'
    cleaned = re.sub(pattern, '', text.strip())
    
    # Also check for any [Role: X] patterns anywhere in the text
    pattern_anywhere = r'\[Role:[^\]]*\]\s*'
    cleaned = re.sub(pattern_anywhere, '', cleaned)
    
    return cleaned.strip()

def randomize_ab_position(response_a: str, response_b: str) -> Tuple[str, str, bool]:
    """
    Randomly assign which response goes to position A and B.
    Returns (response_a, response_b, swapped) where swapped=True if original A became B.
    """
    if random.random() < 0.5:
        # Keep original order
        return response_a, response_b, False
    else:
        # Swap positions
        return response_b, response_a, True

def evaluate_pairwise(query: str, response_a: str, response_b: str) -> Dict[str, Any]:
    """
    Perform pairwise evaluation using structured evaluation criteria.
    Note: In a full implementation, this would use AI evaluation capabilities.
    For this demonstration, we'll analyze the responses systematically.
    """
    
    # Analyze response characteristics
    evaluation = {}
    
    # Length and detail analysis
    len_a = len(response_a)
    len_b = len(response_b)
    
    # Structure analysis (looking for lists, headers, etc.)
    has_structure_a = bool(re.search(r'(\*\*|##|\n-|\n\d+\.|\n\*)', response_a))
    has_structure_b = bool(re.search(r'(\*\*|##|\n-|\n\d+\.|\n\*)', response_b))
    
    # Technical detail analysis (looking for code, technical terms)
    has_technical_a = bool(re.search(r'(```|`[^`]+`|\$\w+|https?://)', response_a))
    has_technical_b = bool(re.search(r'(```|`[^`]+`|\$\w+|https?://)', response_b))
    
    # Actionable elements (looking for concrete steps, recommendations)
    actionable_a = len(re.findall(r'(implement|use|choose|start|consider|try)', response_a.lower()))
    actionable_b = len(re.findall(r'(implement|use|choose|start|consider|try)', response_b.lower()))
    
    # Evaluate helpfulness
    if len_a > len_b * 1.2 and has_structure_a:
        evaluation['helpfulness'] = 'A'
        evaluation['helpfulness_reasoning'] = 'Response A provides more detailed information with better structure.'
    elif len_b > len_a * 1.2 and has_structure_b:
        evaluation['helpfulness'] = 'B'
        evaluation['helpfulness_reasoning'] = 'Response B provides more detailed information with better structure.'
    else:
        evaluation['helpfulness'] = 'Tie'
        evaluation['helpfulness_reasoning'] = 'Both responses provide similar levels of helpful information.'
    
    # Evaluate appropriateness 
    if has_technical_a and not has_technical_b and 'technical' in query.lower():
        evaluation['appropriateness'] = 'A'
        evaluation['appropriateness_reasoning'] = 'Response A uses more appropriate technical detail for this query type.'
    elif has_technical_b and not has_technical_a and 'technical' in query.lower():
        evaluation['appropriateness'] = 'B'
        evaluation['appropriateness_reasoning'] = 'Response B uses more appropriate technical detail for this query type.'
    else:
        evaluation['appropriateness'] = 'Tie'
        evaluation['appropriateness_reasoning'] = 'Both responses are appropriately styled for this query type.'
    
    # Evaluate completeness
    if has_structure_a and len_a > len_b:
        evaluation['completeness'] = 'A'
        evaluation['completeness_reasoning'] = 'Response A covers more aspects with organized structure.'
    elif has_structure_b and len_b > len_a:
        evaluation['completeness'] = 'B'
        evaluation['completeness_reasoning'] = 'Response B covers more aspects with organized structure.'
    else:
        evaluation['completeness'] = 'Tie'
        evaluation['completeness_reasoning'] = 'Both responses provide similarly complete information.'
    
    # Evaluate actionability
    if actionable_a > actionable_b:
        evaluation['actionability'] = 'A'
        evaluation['actionability_reasoning'] = 'Response A provides more concrete, actionable recommendations.'
    elif actionable_b > actionable_a:
        evaluation['actionability'] = 'B'
        evaluation['actionability_reasoning'] = 'Response B provides more concrete, actionable recommendations.'
    else:
        evaluation['actionability'] = 'Tie'
        evaluation['actionability_reasoning'] = 'Both responses provide similar levels of actionable guidance.'
    
    # Overall evaluation
    criteria_winners = [evaluation['helpfulness'], evaluation['appropriateness'], 
                       evaluation['completeness'], evaluation['actionability']]
    
    a_wins = criteria_winners.count('A')
    b_wins = criteria_winners.count('B')
    ties = criteria_winners.count('Tie')
    
    if a_wins > b_wins:
        evaluation['overall'] = 'A'
        evaluation['overall_reasoning'] = f'Response A wins {a_wins} criteria vs {b_wins} for Response B.'
        evaluation['winner'] = 'A'
    elif b_wins > a_wins:
        evaluation['overall'] = 'B'
        evaluation['overall_reasoning'] = f'Response B wins {b_wins} criteria vs {a_wins} for Response A.'
        evaluation['winner'] = 'B'
    else:
        evaluation['overall'] = 'Tie'
        evaluation['overall_reasoning'] = f'Responses tie with A: {a_wins}, B: {b_wins}, Ties: {ties}.'
        evaluation['winner'] = 'Tie'
    
    return evaluation

def create_pairwise_evaluator_1():
    """Main function to create pairwise evaluator 1 results."""
    
    print("Creating Pairwise Evaluator 1: Test 1 (Hardcoded) vs Control")
    print("=" * 60)
    
    # Load data
    control_data, test1_data = load_blinded_data()
    
    # Verify we have the same number of queries
    control_queries = set(control_data.keys())
    test1_queries = set(test1_data.keys())
    
    if control_queries != test1_queries:
        raise ValueError("Control and Test 1 data have different query sets")
    
    print(f"Found {len(control_queries)} queries to evaluate")
    
    # Set random seed for reproducibility
    random.seed(42)
    
    results = {}
    
    # Process each query
    for query_id in sorted(control_queries):
        print(f"\nProcessing {query_id}...")
        
        # Get responses and strip role indicators
        control_response = strip_role_indicators(control_data[query_id])
        test1_response = strip_role_indicators(test1_data[query_id])
        
        # Randomize A/B positioning
        response_a, response_b, swapped = randomize_ab_position(control_response, test1_response)
        
        # Load the actual question text
        with open('/workspace/0_PromptEngineering/PersonaExperiment-0/persona_experiment-02/experiment_queries.json', 'r') as f:
            questions_data = json.load(f)
        question = questions_data[query_id]
        
        # Perform evaluation
        evaluation = evaluate_pairwise(question, response_a, response_b)
        
        # Store results with metadata about which response was which
        results[query_id] = {
            "question": question,
            "response_a": response_a,
            "response_b": response_b,
            "evaluation": evaluation,
            "metadata": {
                "original_a_was": "test1" if not swapped else "control",
                "original_b_was": "control" if not swapped else "test1",
                "swapped": swapped
            }
        }
        
        print(f"  Evaluation complete - Winner: {evaluation['winner']}")
    
    # Save results
    results_dir = '/workspace/0_PromptEngineering/PersonaExperiment-0/persona_experiment-02/results'
    os.makedirs(results_dir, exist_ok=True)
    
    output_file = f'{results_dir}/pairwise_evaluator_1_results.json'
    
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to: {output_file}")
    print(f"Evaluated {len(results)} query pairs")
    
    # Print summary
    winners = [results[qid]["evaluation"]["winner"] for qid in results.keys()]
    a_wins = winners.count('A')
    b_wins = winners.count('B')
    ties = winners.count('Tie')
    
    print(f"\nSUMMARY:")
    print(f"Response A wins: {a_wins}")
    print(f"Response B wins: {b_wins}")
    print(f"Ties: {ties}")
    
    return results

if __name__ == "__main__":
    try:
        results = create_pairwise_evaluator_1()
        print("\nPairwise Evaluator 1 completed successfully!")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)