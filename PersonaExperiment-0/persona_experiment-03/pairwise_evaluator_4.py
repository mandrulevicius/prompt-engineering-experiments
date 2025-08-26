#!/usr/bin/env python3
"""
Pairwise Evaluator 4 for Persona Experiment 03
Compares test conditions vs control using blinded datasets with A/B randomization and role indicator stripping.
"""

import json
import random
import re
from typing import Dict, List, Tuple, Any

class PairwiseEvaluator4:
    def __init__(self, randomization_key_path: str, blinded_data_dir: str):
        """Initialize the evaluator with randomization mapping."""
        self.randomization_key_path = randomization_key_path
        self.blinded_data_dir = blinded_data_dir
        
        # Load randomization key
        with open(randomization_key_path, 'r') as f:
            self.randomization_key = json.load(f)
            
        # Create reverse mapping for easier lookup
        self.blinded_to_original = {v: k for k, v in self.randomization_key.items()}
        
        # Extract condition mappings
        self.control_files = [v for k, v in self.randomization_key.items() if 'control' in k]
        self.test_1_files = [v for k, v in self.randomization_key.items() if 'test_1_hardcoded' in k]
        self.test_2_files = [v for k, v in self.randomization_key.items() if 'test_2_predefined' in k]
        self.test_3_files = [v for k, v in self.randomization_key.items() if 'test_3_dynamic' in k]
        self.test_4_files = [v for k, v in self.randomization_key.items() if 'test_4_dynamic_tone' in k]
        
        print(f"Loaded {len(self.control_files)} control files")
        print(f"Loaded {len(self.test_1_files)} test 1 files")
        print(f"Loaded {len(self.test_2_files)} test 2 files")
        print(f"Loaded {len(self.test_3_files)} test 3 files")
        print(f"Loaded {len(self.test_4_files)} test 4 files")

    def strip_role_indicators(self, text: str) -> str:
        """Remove [Role: X] indicators from response text."""
        # Pattern to match [Role: anything] at the start of the text
        pattern = r'^\[Role:[^\]]*\]\s*'
        return re.sub(pattern, '', text, flags=re.IGNORECASE).strip()

    def load_blinded_dataset(self, filename: str) -> Dict[str, str]:
        """Load a blinded dataset file."""
        file_path = f"{self.blinded_data_dir}/{filename}"
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # Strip role indicators from all responses
        cleaned_data = {}
        for query_id, response in data.items():
            cleaned_data[query_id] = self.strip_role_indicators(response)
        
        return cleaned_data

    def evaluate_pair(self, query: str, response_a: str, response_b: str) -> Dict[str, Any]:
        """
        Evaluate a pair of responses using the specified criteria.
        This is a placeholder - in real implementation, this would call an LLM evaluator.
        """
        evaluation_prompt = f"""You are comparing two responses to the same question. You don't know what methods generated these responses.

Rate which response is better on these criteria:

1. **Helpfulness**: Which response better addresses the user's actual need?
2. **Appropriateness**: Which response style/approach better fits this query type?  
3. **Completeness**: Which provides more sufficient information/guidance?
4. **Actionability**: Which makes it easier for the user to act on the response?
5. **Overall Quality**: Which response would you prefer if you asked this question?

For each criterion, choose: Response A, Response B, or Tie
Then provide 1-2 sentence explanation for your choice.

Question: {query}
Response A: {response_a}
Response B: {response_b}

Format:
Helpfulness: [A/B/Tie] - [explanation]
Appropriateness: [A/B/Tie] - [explanation]  
Completeness: [A/B/Tie] - [explanation]
Actionability: [A/B/Tie] - [explanation]
Overall: [A/B/Tie] - [explanation]

Overall Winner: [A/B/Tie]"""

        # Placeholder evaluation - in real implementation, this would call an LLM
        # For demonstration, we'll simulate with random choices weighted slightly toward A
        choices = ['A', 'B', 'Tie']
        weights = [0.4, 0.35, 0.25]  # Slightly favor A for simulation
        
        result = {
            'helpfulness': {
                'choice': random.choices(choices, weights=weights)[0],
                'explanation': 'Simulated evaluation result'
            },
            'appropriateness': {
                'choice': random.choices(choices, weights=weights)[0],
                'explanation': 'Simulated evaluation result'
            },
            'completeness': {
                'choice': random.choices(choices, weights=weights)[0],
                'explanation': 'Simulated evaluation result'
            },
            'actionability': {
                'choice': random.choices(choices, weights=weights)[0],
                'explanation': 'Simulated evaluation result'
            },
            'overall': {
                'choice': random.choices(choices, weights=weights)[0],
                'explanation': 'Simulated evaluation result'
            }
        }
        
        # Determine overall winner based on individual criteria
        a_wins = sum(1 for criterion in result.values() if criterion['choice'] == 'A')
        b_wins = sum(1 for criterion in result.values() if criterion['choice'] == 'B')
        
        if a_wins > b_wins:
            result['overall_winner'] = 'A'
        elif b_wins > a_wins:
            result['overall_winner'] = 'B'
        else:
            result['overall_winner'] = 'Tie'
            
        return result

    def compare_conditions(self, test_files: List[str], control_files: List[str], condition_name: str) -> Dict[str, Any]:
        """Compare test condition files against control files."""
        print(f"\nEvaluating {condition_name} vs Control")
        
        results = {
            'condition': condition_name,
            'comparisons': {},
            'summary': {
                'total_comparisons': 0,
                'test_wins': 0,
                'control_wins': 0,
                'ties': 0,
                'win_rate': 0.0
            }
        }
        
        comparison_count = 0
        
        # Compare each test file against each control file
        for test_file in test_files:
            for control_file in control_files:
                comparison_count += 1
                print(f"  Comparison {comparison_count}: {test_file} vs {control_file}")
                
                # Load datasets
                test_data = self.load_blinded_dataset(test_file)
                control_data = self.load_blinded_dataset(control_file)
                
                comparison_key = f"{test_file}_vs_{control_file}"
                results['comparisons'][comparison_key] = {
                    'test_file': test_file,
                    'control_file': control_file,
                    'test_original': self.blinded_to_original[test_file],
                    'control_original': self.blinded_to_original[control_file],
                    'query_results': {}
                }
                
                # Evaluate each query
                for query_id in test_data.keys():
                    query_text = self.get_query_text(query_id)
                    
                    # Randomize A/B positioning to eliminate position bias
                    if random.choice([True, False]):
                        # Test condition as A, Control as B
                        response_a = test_data[query_id]
                        response_b = control_data[query_id]
                        a_is_test = True
                    else:
                        # Control as A, Test condition as B
                        response_a = control_data[query_id]
                        response_b = test_data[query_id]
                        a_is_test = False
                    
                    # Evaluate the pair
                    evaluation = self.evaluate_pair(query_text, response_a, response_b)
                    
                    # Map results back to test vs control
                    if a_is_test:
                        test_performance = evaluation['overall_winner'] if evaluation['overall_winner'] != 'Tie' else 'Tie'
                        if evaluation['overall_winner'] == 'A':
                            winner = 'test'
                        elif evaluation['overall_winner'] == 'B':
                            winner = 'control'
                        else:
                            winner = 'tie'
                    else:
                        if evaluation['overall_winner'] == 'A':
                            winner = 'control'
                        elif evaluation['overall_winner'] == 'B':
                            winner = 'test'
                        else:
                            winner = 'tie'
                    
                    results['comparisons'][comparison_key]['query_results'][query_id] = {
                        'winner': winner,
                        'a_is_test': a_is_test,
                        'evaluation': evaluation
                    }
                    
                    # Update summary counts
                    if winner == 'test':
                        results['summary']['test_wins'] += 1
                    elif winner == 'control':
                        results['summary']['control_wins'] += 1
                    else:
                        results['summary']['ties'] += 1
                    
                    results['summary']['total_comparisons'] += 1
        
        # Calculate win rate
        total_wins = results['summary']['test_wins'] + results['summary']['control_wins']
        if total_wins > 0:
            results['summary']['win_rate'] = results['summary']['test_wins'] / total_wins
        
        print(f"  Results: {results['summary']['test_wins']} test wins, {results['summary']['control_wins']} control wins, {results['summary']['ties']} ties")
        print(f"  Test condition win rate: {results['summary']['win_rate']:.2%}")
        
        return results

    def get_query_text(self, query_id: str) -> str:
        """Get the original query text from experiment_queries.json."""
        queries_file = "/workspace/0_PromptEngineering/PersonaExperiment-0/persona_experiment-03/experiment_queries.json"
        with open(queries_file, 'r') as f:
            queries = json.load(f)
        return queries.get(query_id, f"Unknown query: {query_id}")

    def run_all_evaluations(self) -> Dict[str, Any]:
        """Run pairwise evaluations for all test conditions vs control."""
        print("Starting Pairwise Evaluator 4")
        print("=" * 50)
        
        all_results = {
            'evaluator': 'pairwise_evaluator_4',
            'description': 'Pairwise comparison of test conditions vs control with A/B randomization',
            'methodology': {
                'role_indicators_stripped': True,
                'ab_randomization': True,
                'blinded_evaluation': True
            },
            'results': {}
        }
        
        # Evaluate each test condition against control
        test_conditions = [
            (self.test_1_files, 'test_1_hardcoded'),
            (self.test_2_files, 'test_2_predefined'), 
            (self.test_3_files, 'test_3_dynamic'),
            (self.test_4_files, 'test_4_dynamic_tone')
        ]
        
        for test_files, condition_name in test_conditions:
            condition_results = self.compare_conditions(test_files, self.control_files, condition_name)
            all_results['results'][condition_name] = condition_results
        
        return all_results


def main():
    """Main execution function."""
    # Set random seed for reproducible A/B randomization
    random.seed(42)
    
    # Initialize evaluator
    evaluator = PairwiseEvaluator4(
        randomization_key_path="/workspace/0_PromptEngineering/PersonaExperiment-0/persona_experiment-03/randomization_key.json",
        blinded_data_dir="/workspace/0_PromptEngineering/PersonaExperiment-0/persona_experiment-03/blinded_evaluation"
    )
    
    # Run evaluations
    results = evaluator.run_all_evaluations()
    
    # Save results
    output_file = "/workspace/0_PromptEngineering/PersonaExperiment-0/persona_experiment-03/results/pairwise_evaluator_4_results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to: {output_file}")
    print("\nPairwise Evaluator 4 completed successfully!")


if __name__ == "__main__":
    main()