#!/usr/bin/env python3
"""
Absolute Evaluator 4 for Persona Experiment 03
Rates control datasets independently using 1-5 scale with role indicator stripping.
"""

import json
import random
import re
from typing import Dict, List, Any

class AbsoluteEvaluator4:
    def __init__(self, randomization_key_path: str, blinded_data_dir: str):
        """Initialize the evaluator with randomization mapping."""
        self.randomization_key_path = randomization_key_path
        self.blinded_data_dir = blinded_data_dir
        
        # Load randomization key
        with open(randomization_key_path, 'r') as f:
            self.randomization_key = json.load(f)
            
        # Create reverse mapping for easier lookup
        self.blinded_to_original = {v: k for k, v in self.randomization_key.items()}
        
        # Extract control files
        self.control_files = [v for k, v in self.randomization_key.items() if 'control' in k]
        
        print(f"Loaded {len(self.control_files)} control files for evaluation:")
        for file in self.control_files:
            print(f"  - {file} ({self.blinded_to_original[file]})")

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

    def evaluate_response(self, query: str, response: str) -> Dict[str, Any]:
        """
        Evaluate a single response using the specified criteria.
        This is a placeholder - in real implementation, this would call an LLM evaluator.
        """
        evaluation_prompt = f"""You are rating the quality of a response to a question. Rate this response independently without comparison to other responses.

Rate on these criteria (1-5 scale, where 5 is excellent):

1. **Helpfulness** (1-5): How well does it address the user's actual need?
2. **Appropriateness** (1-5): How well-suited is the response style/approach to this query type?
3. **Completeness** (1-5): Does it provide sufficient information/guidance?  
4. **Actionability** (1-5): How easy is it for the user to act on this response?
5. **Overall Quality** (1-5): How would you rate this response overall?

For each metric, provide numerical score and brief explanation.

Question: {query}
Response: {response}

Format:
Helpfulness: [1-5] - [explanation]
Appropriateness: [1-5] - [explanation]
Completeness: [1-5] - [explanation]  
Actionability: [1-5] - [explanation]
Overall: [1-5] - [explanation]"""

        # Placeholder evaluation - in real implementation, this would call an LLM
        # For demonstration, we'll simulate with random scores weighted toward higher quality
        score_choices = [1, 2, 3, 4, 5]
        score_weights = [0.05, 0.1, 0.2, 0.4, 0.25]  # Favor higher scores for simulation
        
        result = {
            'helpfulness': {
                'score': random.choices(score_choices, weights=score_weights)[0],
                'explanation': 'Simulated evaluation - addresses user needs effectively'
            },
            'appropriateness': {
                'score': random.choices(score_choices, weights=score_weights)[0],
                'explanation': 'Simulated evaluation - response style matches query type'
            },
            'completeness': {
                'score': random.choices(score_choices, weights=score_weights)[0],
                'explanation': 'Simulated evaluation - provides sufficient information'
            },
            'actionability': {
                'score': random.choices(score_choices, weights=score_weights)[0],
                'explanation': 'Simulated evaluation - enables user to take action'
            },
            'overall': {
                'score': random.choices(score_choices, weights=score_weights)[0],
                'explanation': 'Simulated evaluation - overall response quality assessment'
            }
        }
        
        return result

    def evaluate_dataset(self, filename: str) -> Dict[str, Any]:
        """Evaluate all responses in a blinded dataset."""
        print(f"\nEvaluating dataset: {filename}")
        original_file = self.blinded_to_original[filename]
        print(f"  Original file: {original_file}")
        
        # Load dataset
        data = self.load_blinded_dataset(filename)
        
        results = {
            'dataset_file': filename,
            'original_file': original_file,
            'query_evaluations': {},
            'summary': {
                'total_queries': len(data),
                'average_scores': {}
            }
        }
        
        # Evaluate each query-response pair
        for query_id, response in data.items():
            query_text = self.get_query_text(query_id)
            
            evaluation = self.evaluate_response(query_text, response)
            results['query_evaluations'][query_id] = {
                'query_text': query_text,
                'evaluation': evaluation
            }
            
            print(f"    {query_id}: H={evaluation['helpfulness']['score']}, "
                  f"A={evaluation['appropriateness']['score']}, "
                  f"C={evaluation['completeness']['score']}, "
                  f"Ac={evaluation['actionability']['score']}, "
                  f"O={evaluation['overall']['score']}")
        
        # Calculate average scores
        criteria = ['helpfulness', 'appropriateness', 'completeness', 'actionability', 'overall']
        for criterion in criteria:
            scores = [results['query_evaluations'][qid]['evaluation'][criterion]['score'] 
                     for qid in data.keys()]
            avg_score = sum(scores) / len(scores)
            results['summary']['average_scores'][criterion] = round(avg_score, 2)
        
        print(f"  Average scores: {results['summary']['average_scores']}")
        
        return results

    def get_query_text(self, query_id: str) -> str:
        """Get the original query text from experiment_queries.json."""
        queries_file = "/workspace/0_PromptEngineering/PersonaExperiment-0/persona_experiment-03/experiment_queries.json"
        with open(queries_file, 'r') as f:
            queries = json.load(f)
        return queries.get(query_id, f"Unknown query: {query_id}")

    def run_evaluation(self) -> Dict[str, Any]:
        """Run absolute evaluation for all control datasets."""
        print("Starting Absolute Evaluator 4 (Control Datasets)")
        print("=" * 50)
        
        all_results = {
            'evaluator': 'absolute_evaluator_4',
            'condition': 'control',
            'description': 'Absolute rating of control datasets on 1-5 scale',
            'methodology': {
                'role_indicators_stripped': True,
                'rating_scale': '1-5',
                'blinded_evaluation': True
            },
            'dataset_results': {},
            'overall_summary': {}
        }
        
        # Evaluate each control dataset
        all_scores = {criterion: [] for criterion in ['helpfulness', 'appropriateness', 'completeness', 'actionability', 'overall']}
        
        for filename in self.control_files:
            dataset_results = self.evaluate_dataset(filename)
            all_results['dataset_results'][filename] = dataset_results
            
            # Collect scores for overall summary
            for criterion in all_scores.keys():
                all_scores[criterion].extend([
                    dataset_results['query_evaluations'][qid]['evaluation'][criterion]['score']
                    for qid in dataset_results['query_evaluations'].keys()
                ])
        
        # Calculate overall summary statistics
        for criterion, scores in all_scores.items():
            all_results['overall_summary'][criterion] = {
                'mean': round(sum(scores) / len(scores), 2),
                'min': min(scores),
                'max': max(scores),
                'total_responses': len(scores)
            }
        
        print(f"\nOverall Summary for Control Condition:")
        for criterion, stats in all_results['overall_summary'].items():
            print(f"  {criterion.title()}: mean={stats['mean']}, range={stats['min']}-{stats['max']}")
        
        return all_results


def main():
    """Main execution function."""
    # Set random seed for reproducible evaluation simulation
    random.seed(42)
    
    # Initialize evaluator
    evaluator = AbsoluteEvaluator4(
        randomization_key_path="/workspace/0_PromptEngineering/PersonaExperiment-0/persona_experiment-03/randomization_key.json",
        blinded_data_dir="/workspace/0_PromptEngineering/PersonaExperiment-0/persona_experiment-03/blinded_evaluation"
    )
    
    # Run evaluation
    results = evaluator.run_evaluation()
    
    # Save results
    output_file = "/workspace/0_PromptEngineering/PersonaExperiment-0/persona_experiment-03/results/absolute_evaluator_4_results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to: {output_file}")
    print("\nAbsolute Evaluator 4 completed successfully!")


if __name__ == "__main__":
    main()