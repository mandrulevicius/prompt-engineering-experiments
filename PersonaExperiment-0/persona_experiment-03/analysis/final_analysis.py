#!/usr/bin/env python3
"""
Persona Experiment 03 - Final Statistical Analysis

This script performs comprehensive statistical analysis of persona experiment 03 results,
including absolute evaluation analysis, pairwise comparison analysis, and visualization generation.

Author: Claude Code
Date: 2025-08-26
"""

import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import ttest_ind, mannwhitneyu, wilcoxon
import os
from pathlib import Path
from typing import Dict, List, Tuple, Any
import warnings
warnings.filterwarnings('ignore')

# Set up plotting parameters
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12
sns.set_style("whitegrid")
sns.set_palette("Set2")

class PersonaExperiment03Analyzer:
    """Comprehensive statistical analyzer for persona experiment 03 results."""
    
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
        
        # Load data
        self.randomization_key = self.load_randomization_key()
        self.query_types = self.load_query_types()
        self.absolute_data = self.load_absolute_evaluation_data()
        self.pairwise_data = self.load_pairwise_evaluation_data()
        
    def load_randomization_key(self) -> Dict[str, str]:
        """Load the randomization key for de-randomization."""
        with open(self.base_path / "randomization_key.json", 'r') as f:
            return json.load(f)
    
    def load_query_types(self) -> Dict[str, str]:
        """Load and categorize query types."""
        with open(self.base_path / "experiment_queries.json", 'r') as f:
            queries = json.load(f)
        
        # Categorize queries by type
        query_categories = {
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
        
        return query_categories
    
    def load_absolute_evaluation_data(self) -> pd.DataFrame:
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
                        query_category = self.query_types.get(query_id, 'unknown')
                        
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
        
        return pd.DataFrame(all_data)
    
    def load_pairwise_evaluation_data(self) -> pd.DataFrame:
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
                        query_category = self.query_types.get(query_id, 'unknown')
                        
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
        
        return pd.DataFrame(all_data)
    
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
    
    def calculate_absolute_statistics(self) -> Dict[str, Any]:
        """Calculate comprehensive statistics for absolute evaluations."""
        stats_results = {}
        
        # Overall condition statistics
        condition_stats = self.absolute_data.groupby(['condition', 'metric'])['score'].agg([
            'mean', 'std', 'count', 'min', 'max'
        ]).round(3)
        
        stats_results['condition_stats'] = condition_stats.to_dict('index')
        
        # Statistical significance tests (t-tests) between conditions
        pairwise_tests = {}
        for metric in self.evaluation_metrics:
            metric_data = self.absolute_data[self.absolute_data['metric'] == metric]
            pairwise_tests[metric] = {}
            
            # Test each condition vs control
            control_scores = metric_data[metric_data['condition'] == 'control']['score']
            
            for condition in self.conditions[1:]:  # Skip control
                test_scores = metric_data[metric_data['condition'] == condition]['score']
                
                if len(test_scores) > 0 and len(control_scores) > 0:
                    # Perform t-test
                    t_stat, p_value = ttest_ind(test_scores, control_scores, equal_var=False)
                    
                    # Calculate Cohen's d (effect size)
                    pooled_std = np.sqrt(((len(test_scores) - 1) * test_scores.var() + 
                                         (len(control_scores) - 1) * control_scores.var()) / 
                                        (len(test_scores) + len(control_scores) - 2))
                    cohens_d = (test_scores.mean() - control_scores.mean()) / pooled_std
                    
                    # 95% confidence interval for mean difference
                    se_diff = np.sqrt(test_scores.var()/len(test_scores) + 
                                     control_scores.var()/len(control_scores))
                    mean_diff = test_scores.mean() - control_scores.mean()
                    ci_95 = (mean_diff - 1.96*se_diff, mean_diff + 1.96*se_diff)
                    
                    pairwise_tests[metric][f"{condition}_vs_control"] = {
                        't_statistic': round(t_stat, 4),
                        'p_value': round(p_value, 4),
                        'significant': p_value < 0.05,
                        'cohens_d': round(cohens_d, 4),
                        'effect_size_interpretation': self.interpret_cohens_d(cohens_d),
                        'mean_difference': round(mean_diff, 4),
                        'ci_95_lower': round(ci_95[0], 4),
                        'ci_95_upper': round(ci_95[1], 4),
                        'test_mean': round(test_scores.mean(), 4),
                        'control_mean': round(control_scores.mean(), 4),
                        'test_n': len(test_scores),
                        'control_n': len(control_scores)
                    }
        
        stats_results['pairwise_tests'] = pairwise_tests
        
        # Query category analysis
        category_stats = self.absolute_data.groupby(['query_category', 'condition', 'metric'])['score'].agg([
            'mean', 'std', 'count'
        ]).round(3)
        
        stats_results['category_stats'] = category_stats.to_dict('index')
        
        return stats_results
    
    def calculate_pairwise_statistics(self) -> Dict[str, Any]:
        """Calculate win rates and statistics for pairwise comparisons."""
        if self.pairwise_data.empty:
            return {'error': 'No pairwise evaluation data available'}
        
        pairwise_stats = {}
        
        # Overall win rates by condition
        win_rates = self.pairwise_data.groupby('test_condition').agg({
            'test_wins': 'sum',
            'control_wins': 'sum'
        })
        win_rates['total_comparisons'] = win_rates['test_wins'] + win_rates['control_wins']
        win_rates['win_rate'] = win_rates['test_wins'] / win_rates['total_comparisons']
        win_rates['win_rate_pct'] = (win_rates['win_rate'] * 100).round(2)
        
        pairwise_stats['win_rates'] = win_rates.to_dict('index')
        
        # Statistical significance of win rates (binomial test)
        for condition in win_rates.index:
            n_wins = win_rates.loc[condition, 'test_wins']
            n_total = win_rates.loc[condition, 'total_comparisons']
            
            # Binomial test (null hypothesis: win rate = 0.5)
            p_value = stats.binom_test(n_wins, n_total, p=0.5, alternative='two-sided')
            
            pairwise_stats['win_rates'][condition]['binomial_p_value'] = round(p_value, 4)
            pairwise_stats['win_rates'][condition]['significant'] = p_value < 0.05
            
            # 95% confidence interval for win rate
            ci_lower, ci_upper = self.binomial_ci(n_wins, n_total)
            pairwise_stats['win_rates'][condition]['ci_95_lower'] = round(ci_lower, 4)
            pairwise_stats['win_rates'][condition]['ci_95_upper'] = round(ci_upper, 4)
        
        # Win rates by query category
        category_wins = self.pairwise_data.groupby(['test_condition', 'query_category']).agg({
            'test_wins': 'sum',
            'control_wins': 'sum'
        })
        category_wins['total'] = category_wins['test_wins'] + category_wins['control_wins']
        category_wins['win_rate'] = category_wins['test_wins'] / category_wins['total']
        category_wins['win_rate_pct'] = (category_wins['win_rate'] * 100).round(2)
        
        pairwise_stats['category_wins'] = category_wins.to_dict('index')
        
        return pairwise_stats
    
    def calculate_inter_evaluator_reliability(self) -> Dict[str, Any]:
        """Calculate inter-evaluator reliability statistics."""
        reliability_stats = {}
        
        # Create pivot table for each metric
        for metric in self.evaluation_metrics:
            metric_data = self.absolute_data[self.absolute_data['metric'] == metric]
            
            # Pivot to get evaluators as columns, (condition, agent, query) as rows
            pivot_data = metric_data.pivot_table(
                values='score',
                index=['condition', 'agent_id', 'query_id'],
                columns='evaluator_id',
                fill_value=np.nan
            )
            
            # Calculate correlation matrix between evaluators
            corr_matrix = pivot_data.corr()
            
            # Calculate Cronbach's alpha (internal consistency)
            cronbach_alpha = self.calculate_cronbach_alpha(pivot_data.values)
            
            # Intraclass Correlation Coefficient (ICC)
            icc = self.calculate_icc(pivot_data.values)
            
            reliability_stats[metric] = {
                'correlation_matrix': corr_matrix.to_dict(),
                'mean_correlation': corr_matrix.values[np.triu_indices_from(corr_matrix.values, k=1)].mean(),
                'cronbach_alpha': round(cronbach_alpha, 4),
                'icc': round(icc, 4),
                'n_evaluators': len(pivot_data.columns),
                'n_items': len(pivot_data)
            }
        
        return reliability_stats
    
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
    
    def binomial_ci(self, successes: int, trials: int, alpha: float = 0.05) -> Tuple[float, float]:
        """Calculate binomial confidence interval."""
        if trials == 0:
            return 0.0, 0.0
        
        # Wilson score interval
        z = stats.norm.ppf(1 - alpha/2)
        p = successes / trials
        n = trials
        
        denominator = 1 + z**2/n
        centre = (p + z**2/(2*n)) / denominator
        delta = z * np.sqrt(p*(1-p)/n + z**2/(4*n**2)) / denominator
        
        return max(0, centre - delta), min(1, centre + delta)
    
    def calculate_cronbach_alpha(self, data: np.ndarray) -> float:
        """Calculate Cronbach's alpha for internal consistency."""
        data_clean = data[~np.isnan(data).any(axis=1)]  # Remove rows with NaN
        if len(data_clean) == 0:
            return np.nan
        
        n_items = data_clean.shape[1]
        if n_items < 2:
            return np.nan
        
        item_variances = np.var(data_clean, axis=0, ddof=1)
        total_variance = np.var(data_clean.sum(axis=1), ddof=1)
        
        alpha = (n_items / (n_items - 1)) * (1 - item_variances.sum() / total_variance)
        return alpha
    
    def calculate_icc(self, data: np.ndarray) -> float:
        """Calculate Intraclass Correlation Coefficient (ICC)."""
        data_clean = data[~np.isnan(data).any(axis=1)]  # Remove rows with NaN
        if len(data_clean) == 0:
            return np.nan
        
        n_subjects, n_raters = data_clean.shape
        if n_subjects < 2 or n_raters < 2:
            return np.nan
        
        # Calculate ICC(2,1) - two-way random effects, single measures, absolute agreement
        subject_means = np.mean(data_clean, axis=1)
        rater_means = np.mean(data_clean, axis=0)
        grand_mean = np.mean(data_clean)
        
        # Sum of squares
        ss_total = np.sum((data_clean - grand_mean) ** 2)
        ss_between_subjects = n_raters * np.sum((subject_means - grand_mean) ** 2)
        ss_between_raters = n_subjects * np.sum((rater_means - grand_mean) ** 2)
        ss_error = ss_total - ss_between_subjects - ss_between_raters
        
        # Mean squares
        ms_between_subjects = ss_between_subjects / (n_subjects - 1)
        ms_error = ss_error / ((n_subjects - 1) * (n_raters - 1))
        
        # ICC calculation
        icc = (ms_between_subjects - ms_error) / ms_between_subjects
        return max(0, icc)  # ICC should be non-negative
    
    def run_comprehensive_analysis(self) -> Dict[str, Any]:
        """Run complete statistical analysis."""
        print("Running comprehensive statistical analysis for Persona Experiment 03...")
        
        results = {
            'experiment_metadata': {
                'experiment_name': 'persona_experiment_03',
                'date_analyzed': '2025-08-26',
                'n_conditions': len(self.conditions),
                'n_evaluators': len(self.absolute_data['evaluator_id'].unique()),
                'n_queries': len(self.absolute_data['query_id'].unique()),
                'n_agents_per_condition': 4,
                'evaluation_metrics': self.evaluation_metrics,
                'conditions': self.conditions
            },
            'absolute_evaluation_analysis': self.calculate_absolute_statistics(),
            'pairwise_comparison_analysis': self.calculate_pairwise_statistics(),
            'inter_evaluator_reliability': self.calculate_inter_evaluator_reliability()
        }
        
        # Save results
        with open(self.output_path / 'comprehensive_analysis_results.json', 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"Analysis complete. Results saved to {self.output_path}")
        return results

def main():
    """Main execution function."""
    base_path = "/workspace/0_PromptEngineering/PersonaExperiment-0/persona_experiment-03"
    analyzer = PersonaExperiment03Analyzer(base_path)
    
    # Run comprehensive analysis
    results = analyzer.run_comprehensive_analysis()
    
    print("\n=== ANALYSIS SUMMARY ===")
    print(f"Conditions analyzed: {results['experiment_metadata']['conditions']}")
    print(f"Number of evaluators: {results['experiment_metadata']['n_evaluators']}")
    print(f"Number of queries: {results['experiment_metadata']['n_queries']}")
    
    # Print key findings
    print("\n=== KEY FINDINGS ===")
    if 'pairwise_tests' in results['absolute_evaluation_analysis']:
        print("Statistical significance tests (vs control):")
        for metric, tests in results['absolute_evaluation_analysis']['pairwise_tests'].items():
            print(f"\n{metric.upper()}:")
            for test_name, test_result in tests.items():
                if test_result['significant']:
                    print(f"  {test_name}: SIGNIFICANT (p={test_result['p_value']}, d={test_result['cohens_d']})")
                else:
                    print(f"  {test_name}: not significant (p={test_result['p_value']})")
    
    return results

if __name__ == "__main__":
    results = main()