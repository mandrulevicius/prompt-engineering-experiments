#!/usr/bin/env python3
"""
Simplified Statistical Analysis for Persona Experiment 03

This script performs statistical analysis using only built-in Python libraries
when advanced packages are not available.

Author: Claude Code
Date: 2025-08-26
"""

import json
import math
import statistics
from collections import defaultdict, Counter
from pathlib import Path
from typing import Dict, List, Tuple, Any

class SimplifiedAnalyzer:
    """Statistical analyzer using only built-in Python libraries."""
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.results_path = self.base_path / "results"
        self.output_path = self.base_path / "analysis"
        self.output_path.mkdir(exist_ok=True)
        
        # Condition mapping
        self.conditions = [
            'control',
            'test_1_hardcoded', 
            'test_2_predefined',
            'test_3_dynamic',
            'test_4_dynamic_tone'
        ]
        
        self.evaluation_metrics = [
            'helpfulness', 'appropriateness', 'completeness', 'actionability', 'overall'
        ]
        
        # Query categories
        self.query_categories = {
            'query_1': 'factual',      # GitHub Copilot cost
            'query_2': 'factual',      # OpenAI news
            'query_3': 'technical',    # CAP theorem
            'query_4': 'technical',    # OAuth implementation
            'query_5': 'advisory',     # React vs Vue
            'query_6': 'advisory',     # Salary negotiation
            'query_7': 'guidance',     # ML learning
            'query_8': 'technical',    # Debug performance
            'query_9': 'advisory',     # Convince CEO
            'query_10': 'factual',     # Blockchain
            'query_11': 'advisory',    # Team productivity
            'query_12': 'factual'      # Python
        }
        
        # Load data
        self.randomization_key = self.load_randomization_key()
        self.absolute_data = self.load_absolute_evaluation_data()
        self.pairwise_data = self.load_pairwise_evaluation_data()
        
    def load_randomization_key(self) -> Dict[str, str]:
        """Load the randomization key for de-randomization."""
        with open(self.base_path / "randomization_key.json", 'r') as f:
            return json.load(f)
    
    def load_absolute_evaluation_data(self) -> List[Dict]:
        """Load and process absolute evaluation data."""
        all_data = []
        
        # Load absolute evaluation results
        for evaluator_id in [4, 5, 6, 7]:
            file_path = self.results_path / f"absolute_evaluator_{evaluator_id}_results.json"
            if file_path.exists():
                with open(file_path, 'r') as f:
                    data = json.load(f)
                
                # Process each condition's results
                for dataset_name, dataset_results in data['dataset_results'].items():
                    # Map back to original condition using randomization key
                    original_file = dataset_results['original_file']
                    condition = self.extract_condition_from_filename(original_file)
                    agent_id = self.extract_agent_id_from_filename(original_file)
                    
                    # Process each query evaluation
                    for query_id, query_data in dataset_results['query_evaluations'].items():
                        query_category = self.query_categories.get(query_id, 'unknown')
                        
                        for metric, metric_data in query_data['evaluation'].items():
                            row = {
                                'evaluator_id': evaluator_id,
                                'condition': condition,
                                'agent_id': agent_id,
                                'query_id': query_id,
                                'query_category': query_category,
                                'metric': metric,
                                'score': metric_data['score'],
                                'dataset_file': dataset_name,
                                'original_file': original_file
                            }
                            all_data.append(row)
        
        return all_data
    
    def load_pairwise_evaluation_data(self) -> List[Dict]:
        """Load and process pairwise evaluation data."""
        all_data = []
        
        # Load pairwise evaluation results (only evaluator 4 exists)
        file_path = self.results_path / "pairwise_evaluator_4_results.json"
        if file_path.exists():
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # Process each test condition's comparisons
            for condition, condition_data in data['results'].items():
                if condition == 'control':  # Skip control comparisons
                    continue
                
                for comparison_key, comparison_data in condition_data['comparisons'].items():
                    # Process each query comparison
                    for query_id, query_result in comparison_data['query_results'].items():
                        query_category = self.query_categories.get(query_id, 'unknown')
                        
                        # Extract agent information
                        test_agent = self.extract_agent_id_from_filename(comparison_data['test_original'])
                        control_agent = self.extract_agent_id_from_filename(comparison_data['control_original'])
                        
                        # Record overall winner
                        row = {
                            'evaluator_id': 4,
                            'test_condition': condition,
                            'test_agent': test_agent,
                            'control_agent': control_agent,
                            'query_id': query_id,
                            'query_category': query_category,
                            'winner': query_result['winner'],
                            'test_wins': 1 if query_result['winner'] == 'test' else 0,
                            'control_wins': 1 if query_result['winner'] == 'control' else 0,
                            'comparison_key': comparison_key
                        }
                        all_data.append(row)
        
        return all_data
    
    def extract_condition_from_filename(self, filename: str) -> str:
        """Extract condition name from response filename."""
        for condition in self.conditions:
            if condition in filename:
                return condition
        return 'unknown'
    
    def extract_agent_id_from_filename(self, filename: str) -> int:
        """Extract agent ID from filename."""
        parts = filename.split('_')
        for part in parts:
            if part.isdigit():
                return int(part)
        return 0
    
    def calculate_basic_statistics(self, values: List[float]) -> Dict[str, float]:
        """Calculate basic statistics for a list of values."""
        if not values:
            return {}
        
        return {
            'count': len(values),
            'mean': statistics.mean(values),
            'median': statistics.median(values),
            'std': statistics.stdev(values) if len(values) > 1 else 0,
            'min': min(values),
            'max': max(values)
        }
    
    def t_test_two_sample(self, sample1: List[float], sample2: List[float]) -> Dict[str, float]:
        """Perform two-sample t-test using built-in functions."""
        if not sample1 or not sample2 or len(sample1) < 2 or len(sample2) < 2:
            return {}
        
        n1, n2 = len(sample1), len(sample2)
        mean1, mean2 = statistics.mean(sample1), statistics.mean(sample2)
        var1, var2 = statistics.variance(sample1), statistics.variance(sample2)
        
        # Welch's t-test (unequal variances)
        se = math.sqrt(var1/n1 + var2/n2)
        t_stat = (mean1 - mean2) / se if se > 0 else 0
        
        # Degrees of freedom for Welch's t-test
        df = (var1/n1 + var2/n2)**2 / ((var1/n1)**2/(n1-1) + (var2/n2)**2/(n2-1))
        
        # Calculate Cohen's d
        pooled_std = math.sqrt(((n1-1)*var1 + (n2-1)*var2) / (n1+n2-2))
        cohens_d = (mean1 - mean2) / pooled_std if pooled_std > 0 else 0
        
        return {
            't_statistic': round(t_stat, 4),
            'degrees_of_freedom': round(df, 2),
            'mean_difference': round(mean1 - mean2, 4),
            'cohens_d': round(cohens_d, 4),
            'effect_size_interpretation': self.interpret_cohens_d(cohens_d),
            'sample1_mean': round(mean1, 4),
            'sample1_std': round(math.sqrt(var1), 4),
            'sample1_n': n1,
            'sample2_mean': round(mean2, 4),
            'sample2_std': round(math.sqrt(var2), 4),
            'sample2_n': n2
        }
    
    def interpret_cohens_d(self, d: float) -> str:
        """Interpret Cohen's d effect size."""
        abs_d = abs(d)
        if abs_d < 0.2:
            return "negligible"
        elif abs_d < 0.5:
            return "small"
        elif abs_d < 0.8:
            return "medium"
        else:
            return "large"
    
    def analyze_absolute_evaluations(self) -> Dict[str, Any]:
        """Analyze absolute evaluation results."""
        results = {}
        
        # Group data by condition and metric
        grouped_data = defaultdict(lambda: defaultdict(list))
        for row in self.absolute_data:
            grouped_data[row['condition']][row['metric']].append(row['score'])
        
        # Calculate statistics for each condition and metric
        condition_stats = {}
        for condition in self.conditions:
            condition_stats[condition] = {}
            for metric in self.evaluation_metrics:
                values = grouped_data[condition][metric]
                condition_stats[condition][metric] = self.calculate_basic_statistics(values)
        
        results['condition_statistics'] = condition_stats
        
        # Perform t-tests comparing each condition to control
        pairwise_tests = {}
        for metric in self.evaluation_metrics:
            pairwise_tests[metric] = {}
            control_scores = grouped_data['control'][metric]
            
            for condition in self.conditions[1:]:  # Skip control
                test_scores = grouped_data[condition][metric]
                test_result = self.t_test_two_sample(test_scores, control_scores)
                if test_result:
                    pairwise_tests[metric][f"{condition}_vs_control"] = test_result
        
        results['pairwise_tests'] = pairwise_tests
        
        return results
    
    def analyze_pairwise_comparisons(self) -> Dict[str, Any]:
        """Analyze pairwise comparison results."""
        if not self.pairwise_data:
            return {'error': 'No pairwise data available'}
        
        results = {}
        
        # Calculate win rates by condition
        win_rates = {}
        for condition in ['test_1_hardcoded', 'test_2_predefined', 'test_3_dynamic', 'test_4_dynamic_tone']:
            condition_data = [row for row in self.pairwise_data if row['test_condition'] == condition]
            
            if condition_data:
                total_wins = sum(row['test_wins'] for row in condition_data)
                total_comparisons = len(condition_data)
                win_rate = total_wins / total_comparisons if total_comparisons > 0 else 0
                
                win_rates[condition] = {
                    'wins': total_wins,
                    'total_comparisons': total_comparisons,
                    'win_rate': round(win_rate, 4),
                    'win_rate_percent': round(win_rate * 100, 2)
                }
        
        results['win_rates'] = win_rates
        
        # Analyze by query category
        category_performance = defaultdict(lambda: defaultdict(int))
        for row in self.pairwise_data:
            category_performance[row['test_condition']][row['query_category']] += row['test_wins']
        
        results['category_performance'] = dict(category_performance)
        
        return results
    
    def analyze_query_categories(self) -> Dict[str, Any]:
        """Analyze performance by query category."""
        results = {}
        
        # Group by query category
        category_data = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
        for row in self.absolute_data:
            category_data[row['query_category']][row['condition']][row['metric']].append(row['score'])
        
        # Calculate statistics for each category
        category_stats = {}
        for category in set(self.query_categories.values()):
            category_stats[category] = {}
            for condition in self.conditions:
                category_stats[category][condition] = {}
                for metric in self.evaluation_metrics:
                    values = category_data[category][condition][metric]
                    category_stats[category][condition][metric] = self.calculate_basic_statistics(values)
        
        results['category_statistics'] = category_stats
        
        return results
    
    def run_analysis(self) -> Dict[str, Any]:
        """Run complete analysis."""
        print("Running simplified statistical analysis for Persona Experiment 03...")
        
        results = {
            'experiment_metadata': {
                'experiment_name': 'persona_experiment_03',
                'analysis_date': '2025-08-26',
                'analyzer_type': 'simplified',
                'conditions': self.conditions,
                'evaluation_metrics': self.evaluation_metrics,
                'query_categories': list(set(self.query_categories.values()))
            },
            'absolute_evaluation_analysis': self.analyze_absolute_evaluations(),
            'pairwise_comparison_analysis': self.analyze_pairwise_comparisons(),
            'query_category_analysis': self.analyze_query_categories()
        }
        
        # Calculate sample sizes
        results['sample_size_info'] = {
            'total_absolute_evaluations': len(self.absolute_data),
            'total_pairwise_comparisons': len(self.pairwise_data),
            'evaluations_per_condition': {
                condition: len([row for row in self.absolute_data if row['condition'] == condition])
                for condition in self.conditions
            }
        }
        
        # Save results
        output_file = self.output_path / 'simplified_analysis_results.json'
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"Analysis complete. Results saved to {output_file}")
        return results

def main():
    """Main execution function."""
    base_path = "/workspace/0_PromptEngineering/PersonaExperiment-0/persona_experiment-03"
    analyzer = SimplifiedAnalyzer(base_path)
    
    # Run analysis
    results = analyzer.run_analysis()
    
    # Print summary
    print("\n=== ANALYSIS SUMMARY ===")
    print(f"Total absolute evaluations: {results['sample_size_info']['total_absolute_evaluations']}")
    print(f"Total pairwise comparisons: {results['sample_size_info']['total_pairwise_comparisons']}")
    
    print("\n=== WIN RATES (Pairwise Comparisons) ===")
    if 'win_rates' in results['pairwise_comparison_analysis']:
        for condition, stats in results['pairwise_comparison_analysis']['win_rates'].items():
            print(f"{condition}: {stats['win_rate_percent']:.1f}% ({stats['wins']}/{stats['total_comparisons']})")
    
    print("\n=== STATISTICAL SIGNIFICANCE (vs Control) ===")
    if 'pairwise_tests' in results['absolute_evaluation_analysis']:
        for metric in ['overall']:  # Focus on overall metric for summary
            if metric in results['absolute_evaluation_analysis']['pairwise_tests']:
                print(f"\n{metric.upper()}:")
                for test_name, test_result in results['absolute_evaluation_analysis']['pairwise_tests'][metric].items():
                    effect_size = test_result.get('cohens_d', 0)
                    interpretation = test_result.get('effect_size_interpretation', 'unknown')
                    mean_diff = test_result.get('mean_difference', 0)
                    print(f"  {test_name}: Δ={mean_diff:+.3f}, d={effect_size:.3f} ({interpretation})")
    
    return results

if __name__ == "__main__":
    results = main()