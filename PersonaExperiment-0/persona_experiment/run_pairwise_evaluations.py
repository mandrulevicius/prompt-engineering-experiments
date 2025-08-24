#!/usr/bin/env python3
import json
import random
from pathlib import Path
from collections import defaultdict

def load_responses(filepath):
    """Load responses from a JSON file."""
    with open(filepath, 'r') as f:
        return json.load(f)

def load_queries():
    """Load the original queries."""
    with open("/workspace/0_PromptEngineering/persona_experiment/experiment_queries.json", 'r') as f:
        return json.load(f)['queries']

def get_control_datasets():
    """Get the blinded filenames for control datasets."""
    with open("/workspace/0_PromptEngineering/persona_experiment/randomization_key.json", 'r') as f:
        mapping = json.load(f)
    
    control_datasets = []
    for original, blinded in mapping.items():
        if 'control_responses' in original:
            control_datasets.append(blinded)
    
    return control_datasets

def get_test_datasets():
    """Get the blinded filenames for test condition datasets."""
    with open("/workspace/0_PromptEngineering/persona_experiment/randomization_key.json", 'r') as f:
        mapping = json.load(f)
    
    test_conditions = {
        'test_1_hardcoded': [],
        'test_2_predefined': [],
        'test_3_dynamic': [],
        'test_4_dynamic_tone': []
    }
    
    for original, blinded in mapping.items():
        for condition in test_conditions.keys():
            if condition in original:
                test_conditions[condition].append(blinded)
                break
    
    return test_conditions

def run_pairwise_evaluation_batch():
    """Run pairwise evaluations using Task subagents."""
    
    # Load data
    queries = load_queries()
    control_datasets = get_control_datasets()
    test_conditions = get_test_datasets()
    
    blinded_dir = Path("/workspace/0_PromptEngineering/persona_experiment/blinded_evaluation")
    results_dir = Path("/workspace/0_PromptEngineering/persona_experiment/results")
    results_dir.mkdir(exist_ok=True)
    
    # Create evaluation tasks for each evaluator
    evaluation_tasks = []
    
    for evaluator_id in [1, 2, 3]:  # 3 pairwise evaluators
        # Compare each test condition vs control
        for condition_name, test_datasets in test_conditions.items():
            for test_dataset in test_datasets:
                # Pick a random control dataset for comparison
                control_dataset = random.choice(control_datasets)
                
                task_info = {
                    'evaluator_id': evaluator_id,
                    'condition_name': condition_name,
                    'test_dataset': test_dataset,
                    'control_dataset': control_dataset,
                    'output_file': f"pairwise_evaluator_{evaluator_id}_{condition_name}_{test_dataset.split('.')[0]}_results.json"
                }
                evaluation_tasks.append(task_info)
    
    # Save evaluation task manifest
    with open(results_dir / "evaluation_tasks_manifest.json", 'w') as f:
        json.dump(evaluation_tasks, f, indent=2)
    
    print(f"Created {len(evaluation_tasks)} evaluation tasks")
    print(f"Task manifest saved to: {results_dir}/evaluation_tasks_manifest.json")
    print("\nEvaluation tasks ready for subagent execution.")
    
    return evaluation_tasks

if __name__ == "__main__":
    tasks = run_pairwise_evaluation_batch()
    print("Pairwise evaluation setup complete!")