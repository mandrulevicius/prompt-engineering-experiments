#!/usr/bin/env python3
"""
Comprehensive Statistical Analysis of Persona Experiment 02
Analyzes pairwise and absolute evaluation results to determine effectiveness of persona switching
"""

import json
import numpy as np
from scipy import stats
from scipy.stats import binom_test, ttest_1samp
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict, Counter
import pandas as pd
from datetime import datetime

# Set style for plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class PersonaExperimentAnalysis:
    def __init__(self):
        self.pairwise_results = {}
        self.absolute_results = {}
        self.queries = {}
        
        # Load all data
        self.load_data()
        
        # Query categorization
        self.query_categories = {
            'research': ['query_1', 'query_2', 'query_10'],  # GitHub Copilot pricing, OpenAI news, blockchain
            'technical': ['query_3', 'query_4', 'query_8', 'query_12'],  # CAP theorem, OAuth, Node.js debug, Python
            'advisory': ['query_5', 'query_6', 'query_7', 'query_9', 'query_11']  # React/Vue, salary, ML learning, AI tools, productivity
        }
        
    def load_data(self):
        """Load all evaluation data from JSON files"""
        # Load pairwise evaluation results
        for i in range(1, 4):
            with open(f'/workspace/0_PromptEngineering/PersonaExperiment-0/persona_experiment-02/results/pairwise_evaluator_{i}_results.json') as f:
                self.pairwise_results[f'evaluator_{i}'] = json.load(f)
        
        # Load absolute evaluation results
        for i in range(4, 7):
            with open(f'/workspace/0_PromptEngineering/PersonaExperiment-0/persona_experiment-02/results/absolute_evaluator_{i}_results.json') as f:
                self.absolute_results[f'evaluator_{i}'] = json.load(f)
                
        # Load experiment queries
        with open('/workspace/0_PromptEngineering/PersonaExperiment-0/persona_experiment-02/experiment_queries.json') as f:
            self.queries = json.load(f)
    
    def analyze_pairwise_results(self):
        """Analyze pairwise evaluation results and calculate win rates"""
        results = {}
        
        for evaluator, data in self.pairwise_results.items():
            wins = {'control': 0, 'test': 0, 'ties': 0}
            detailed_results = []
            
            for query_id, query_data in data.items():
                winner = query_data['evaluation']['winner']
                original_a = query_data['metadata']['original_a_was']
                original_b = query_data['metadata']['original_b_was']
                
                # Determine which condition won
                if winner == 'Tie':
                    wins['ties'] += 1
                    actual_winner = 'tie'
                elif winner == 'A':
                    actual_winner = original_a
                else:  # winner == 'B'
                    actual_winner = original_b
                
                if actual_winner == 'control':
                    wins['control'] += 1
                elif actual_winner in ['test1', 'test2', 'test3']:
                    wins['test'] += 1
                
                detailed_results.append({
                    'query_id': query_id,
                    'winner': actual_winner,
                    'original_a': original_a,
                    'original_b': original_b,
                    'evaluation': query_data['evaluation']
                })
            
            total_comparisons = wins['control'] + wins['test'] + wins['ties']
            
            # Calculate win rates (excluding ties)
            non_tie_total = wins['control'] + wins['test']
            if non_tie_total > 0:
                control_win_rate = wins['control'] / non_tie_total
                test_win_rate = wins['test'] / non_tie_total
            else:
                control_win_rate = test_win_rate = 0
            
            # Perform binomial test
            if non_tie_total > 0:
                # Test if test condition significantly outperforms control (p > 0.5)
                p_value = binom_test(wins['test'], non_tie_total, p=0.5, alternative='greater')
                # Also test for any significant difference
                p_value_two_sided = binom_test(wins['test'], non_tie_total, p=0.5, alternative='two-sided')
            else:
                p_value = p_value_two_sided = 1.0
                
            # Calculate confidence intervals for win rates
            if non_tie_total > 0:
                # Wilson score interval for test win rate
                z = 1.96  # 95% confidence
                p_hat = test_win_rate
                n = non_tie_total
                
                denominator = 1 + z**2 / n
                center = (p_hat + z**2 / (2*n)) / denominator
                margin = z * np.sqrt((p_hat * (1 - p_hat) + z**2 / (4*n))) / np.sqrt(n) / denominator
                
                ci_lower = max(0, center - margin)
                ci_upper = min(1, center + margin)
            else:
                ci_lower = ci_upper = 0
            
            results[evaluator] = {
                'wins': wins,
                'total_comparisons': total_comparisons,
                'win_rates': {
                    'control': control_win_rate,
                    'test': test_win_rate
                },
                'statistical_tests': {
                    'binomial_test_one_sided': p_value,
                    'binomial_test_two_sided': p_value_two_sided,
                    'significant_at_05': p_value < 0.05
                },
                'confidence_interval': {
                    'test_win_rate_ci_95': [ci_lower, ci_upper]
                },
                'detailed_results': detailed_results
            }
        
        return results
    
    def analyze_absolute_results(self):
        """Analyze absolute evaluation results and calculate average scores"""
        results = {}
        
        for evaluator, data in self.absolute_results.items():
            scores = {
                'helpfulness': [],
                'appropriateness': [],
                'completeness': [],
                'actionability': [],
                'overall': []
            }
            
            detailed_results = []
            
            for query_id, query_data in data.items():
                eval_data = query_data['evaluation']
                
                for metric in scores.keys():
                    scores[metric].append(eval_data[metric])
                
                detailed_results.append({
                    'query_id': query_id,
                    'scores': {k: eval_data[k] for k in scores.keys()},
                    'response_length': len(query_data['response'])
                })
            
            # Calculate statistics for each metric
            metric_stats = {}
            for metric, values in scores.items():
                values = np.array(values)
                
                # Basic statistics
                mean_score = np.mean(values)
                std_score = np.std(values)
                median_score = np.median(values)
                
                # Test if mean is significantly different from neutral (3.0)
                t_stat, p_value = ttest_1samp(values, 3.0)
                
                # 95% confidence interval for the mean
                ci = stats.t.interval(0.95, len(values)-1, loc=mean_score, scale=stats.sem(values))
                
                metric_stats[metric] = {
                    'mean': mean_score,
                    'std': std_score,
                    'median': median_score,
                    'min': np.min(values),
                    'max': np.max(values),
                    't_test_vs_neutral': {
                        't_stat': t_stat,
                        'p_value': p_value,
                        'significant_at_05': p_value < 0.05
                    },
                    'confidence_interval_95': ci,
                    'score_distribution': Counter(values).most_common()
                }
            
            results[evaluator] = {
                'metric_statistics': metric_stats,
                'detailed_results': detailed_results,
                'n_queries': len(detailed_results)
            }
        
        return results
    
    def analyze_by_query_type(self):
        """Analyze results broken down by query type"""
        results = {}
        
        for category, query_list in self.query_categories.items():
            results[category] = {
                'pairwise': {},
                'absolute': {}
            }
            
            # Analyze pairwise results by category
            for evaluator, data in self.pairwise_results.items():
                category_wins = {'control': 0, 'test': 0, 'ties': 0}
                
                for query_id in query_list:
                    if query_id in data:
                        winner = data[query_id]['evaluation']['winner']
                        original_a = data[query_id]['metadata']['original_a_was']
                        original_b = data[query_id]['metadata']['original_b_was']
                        
                        if winner == 'Tie':
                            category_wins['ties'] += 1
                        elif winner == 'A':
                            actual_winner = original_a
                        else:
                            actual_winner = original_b
                        
                        if winner != 'Tie':
                            if actual_winner == 'control':
                                category_wins['control'] += 1
                            elif actual_winner in ['test1', 'test2', 'test3']:
                                category_wins['test'] += 1
                
                non_tie_total = category_wins['control'] + category_wins['test']
                if non_tie_total > 0:
                    test_win_rate = category_wins['test'] / non_tie_total
                    p_value = binom_test(category_wins['test'], non_tie_total, p=0.5, alternative='greater')
                else:
                    test_win_rate = 0
                    p_value = 1.0
                
                results[category]['pairwise'][evaluator] = {
                    'wins': category_wins,
                    'test_win_rate': test_win_rate,
                    'p_value': p_value
                }
            
            # Analyze absolute results by category
            for evaluator, data in self.absolute_results.items():
                category_scores = {metric: [] for metric in ['helpfulness', 'appropriateness', 'completeness', 'actionability', 'overall']}
                
                for query_id in query_list:
                    if query_id in data:
                        eval_data = data[query_id]['evaluation']
                        for metric in category_scores.keys():
                            category_scores[metric].append(eval_data[metric])
                
                metric_means = {}
                for metric, scores in category_scores.items():
                    if scores:
                        metric_means[metric] = np.mean(scores)
                    else:
                        metric_means[metric] = None
                
                results[category]['absolute'][evaluator] = {
                    'metric_means': metric_means,
                    'n_queries': len([q for q in query_list if q in data])
                }
        
        return results
    
    def create_visualizations(self):
        """Create comprehensive visualizations"""
        fig = plt.figure(figsize=(20, 24))
        
        # 1. Pairwise Win Rates
        plt.subplot(4, 2, 1)
        pairwise_analysis = self.analyze_pairwise_results()
        
        evaluators = list(pairwise_analysis.keys())
        test_win_rates = [pairwise_analysis[eval]['win_rates']['test'] for eval in evaluators]
        control_win_rates = [pairwise_analysis[eval]['win_rates']['control'] for eval in evaluators]
        
        x = np.arange(len(evaluators))
        width = 0.35
        
        plt.bar(x - width/2, control_win_rates, width, label='Control', alpha=0.8)
        plt.bar(x + width/2, test_win_rates, width, label='Test Personas', alpha=0.8)
        plt.axhline(y=0.5, color='red', linestyle='--', alpha=0.7, label='Random Chance')
        
        plt.xlabel('Evaluators')
        plt.ylabel('Win Rate')
        plt.title('Win Rates: Control vs Test Personas (Pairwise Evaluations)')
        plt.xticks(x, [e.replace('evaluator_', 'Eval ') for e in evaluators])
        plt.legend()
        plt.ylim(0, 1)
        
        # 2. Absolute Scores by Metric
        plt.subplot(4, 2, 2)
        absolute_analysis = self.analyze_absolute_results()
        
        metrics = ['helpfulness', 'appropriateness', 'completeness', 'actionability', 'overall']
        evaluator_names = list(absolute_analysis.keys())
        
        score_data = []
        for eval_name in evaluator_names:
            eval_scores = []
            for metric in metrics:
                eval_scores.append(absolute_analysis[eval_name]['metric_statistics'][metric]['mean'])
            score_data.append(eval_scores)
        
        score_data = np.array(score_data)
        
        x = np.arange(len(metrics))
        width = 0.25
        
        for i, eval_name in enumerate(evaluator_names):
            plt.bar(x + i*width, score_data[i], width, label=eval_name.replace('evaluator_', 'Test '), alpha=0.8)
        
        plt.axhline(y=3.0, color='red', linestyle='--', alpha=0.7, label='Neutral (3.0)')
        plt.xlabel('Evaluation Metrics')
        plt.ylabel('Average Score (1-5)')
        plt.title('Average Scores by Metric (Absolute Evaluations)')
        plt.xticks(x + width, metrics, rotation=45)
        plt.legend()
        plt.ylim(1, 5)
        
        # 3. Query Type Analysis - Pairwise
        plt.subplot(4, 2, 3)
        query_type_analysis = self.analyze_by_query_type()
        
        categories = list(self.query_categories.keys())
        
        # Average test win rates across evaluators for each category
        category_win_rates = []
        for category in categories:
            win_rates = []
            for evaluator in query_type_analysis[category]['pairwise'].keys():
                win_rates.append(query_type_analysis[category]['pairwise'][evaluator]['test_win_rate'])
            category_win_rates.append(np.mean(win_rates) if win_rates else 0)
        
        plt.bar(categories, category_win_rates, alpha=0.8)
        plt.axhline(y=0.5, color='red', linestyle='--', alpha=0.7, label='Random Chance')
        plt.xlabel('Query Categories')
        plt.ylabel('Test Win Rate')
        plt.title('Test Persona Win Rates by Query Type')
        plt.xticks(rotation=45)
        plt.legend()
        plt.ylim(0, 1)
        
        # 4. Query Type Analysis - Absolute Scores
        plt.subplot(4, 2, 4)
        
        category_overall_scores = []
        for category in categories:
            scores = []
            for evaluator in query_type_analysis[category]['absolute'].keys():
                overall_mean = query_type_analysis[category]['absolute'][evaluator]['metric_means']['overall']
                if overall_mean is not None:
                    scores.append(overall_mean)
            category_overall_scores.append(np.mean(scores) if scores else 0)
        
        plt.bar(categories, category_overall_scores, alpha=0.8)
        plt.axhline(y=3.0, color='red', linestyle='--', alpha=0.7, label='Neutral (3.0)')
        plt.xlabel('Query Categories')
        plt.ylabel('Average Overall Score')
        plt.title('Average Overall Scores by Query Type')
        plt.xticks(rotation=45)
        plt.legend()
        plt.ylim(1, 5)
        
        # 5. Statistical Significance Heatmap - Pairwise
        plt.subplot(4, 2, 5)
        
        sig_matrix = []
        for eval_name in evaluators:
            p_val = pairwise_analysis[eval_name]['statistical_tests']['binomial_test_two_sided']
            sig_matrix.append([1 if p_val < 0.05 else 0])
        
        plt.imshow(sig_matrix, cmap='RdYlGn', aspect='auto')
        plt.yticks(range(len(evaluators)), [e.replace('evaluator_', 'Eval ') for e in evaluators])
        plt.xticks([0], ['Significance'])
        plt.title('Statistical Significance (p < 0.05)\nPairwise Evaluations')
        plt.colorbar(label='Significant (1) / Not Significant (0)')
        
        # 6. Score Distribution
        plt.subplot(4, 2, 6)
        
        all_overall_scores = []
        for evaluator in absolute_analysis.keys():
            for result in absolute_analysis[evaluator]['detailed_results']:
                all_overall_scores.append(result['scores']['overall'])
        
        plt.hist(all_overall_scores, bins=range(1, 7), alpha=0.7, edgecolor='black')
        plt.axvline(x=np.mean(all_overall_scores), color='red', linestyle='--', 
                   label=f'Mean: {np.mean(all_overall_scores):.2f}')
        plt.axvline(x=3.0, color='orange', linestyle='--', alpha=0.7, label='Neutral (3.0)')
        plt.xlabel('Overall Score')
        plt.ylabel('Frequency')
        plt.title('Distribution of Overall Scores')
        plt.xticks(range(1, 6))
        plt.legend()
        
        # 7. Effect Sizes
        plt.subplot(4, 2, 7)
        
        effect_sizes = []
        eval_labels = []
        
        for eval_name in evaluators:
            wins = pairwise_analysis[eval_name]['wins']
            non_tie_total = wins['control'] + wins['test']
            
            if non_tie_total > 0:
                # Cohen's h for difference in proportions
                p1 = wins['test'] / non_tie_total
                p2 = wins['control'] / non_tie_total
                h = 2 * (np.arcsin(np.sqrt(p1)) - np.arcsin(np.sqrt(p2)))
                effect_sizes.append(h)
                eval_labels.append(eval_name.replace('evaluator_', 'Eval '))
        
        plt.barh(range(len(effect_sizes)), effect_sizes, alpha=0.8)
        plt.axvline(x=0, color='red', linestyle='--', alpha=0.7, label='No Effect')
        plt.axvline(x=0.2, color='green', linestyle=':', alpha=0.7, label='Small Effect')
        plt.axvline(x=0.5, color='orange', linestyle=':', alpha=0.7, label='Medium Effect')
        plt.xlabel('Effect Size (Cohen\'s h)')
        plt.ylabel('Evaluators')
        plt.title('Effect Sizes for Test vs Control')
        plt.yticks(range(len(effect_sizes)), eval_labels)
        plt.legend()
        
        # 8. Confidence Intervals
        plt.subplot(4, 2, 8)
        
        test_means = []
        ci_lowers = []
        ci_uppers = []
        eval_names = []
        
        for eval_name in evaluators:
            win_rate = pairwise_analysis[eval_name]['win_rates']['test']
            ci = pairwise_analysis[eval_name]['confidence_interval']['test_win_rate_ci_95']
            
            test_means.append(win_rate)
            ci_lowers.append(ci[0])
            ci_uppers.append(ci[1])
            eval_names.append(eval_name.replace('evaluator_', 'Eval '))
        
        y_pos = np.arange(len(eval_names))
        
        plt.errorbar(test_means, y_pos, 
                    xerr=[np.array(test_means) - np.array(ci_lowers), 
                          np.array(ci_uppers) - np.array(test_means)],
                    fmt='o', alpha=0.8, capsize=5)
        plt.axvline(x=0.5, color='red', linestyle='--', alpha=0.7, label='Random Chance')
        plt.xlabel('Test Win Rate')
        plt.ylabel('Evaluators')
        plt.title('Test Win Rates with 95% Confidence Intervals')
        plt.yticks(y_pos, eval_names)
        plt.xlim(0, 1)
        plt.legend()
        
        plt.tight_layout()
        plt.savefig('/workspace/0_PromptEngineering/PersonaExperiment-0/persona_experiment-02/persona_experiment_analysis.png', 
                   dpi=300, bbox_inches='tight')
        plt.close()
        
    def generate_comprehensive_report(self):
        """Generate comprehensive statistical report"""
        
        # Analyze all data
        pairwise_analysis = self.analyze_pairwise_results()
        absolute_analysis = self.analyze_absolute_results()
        query_type_analysis = self.analyze_by_query_type()
        
        # Create visualizations
        self.create_visualizations()
        
        # Compile comprehensive report
        report = {
            "experiment_info": {
                "name": "Persona Experiment 02",
                "date": datetime.now().isoformat(),
                "description": "Analysis of persona switching effectiveness on AI response quality",
                "evaluators": {
                    "pairwise": ["evaluator_1 (Test 1 vs Control)", "evaluator_2 (Test 2 vs Control)", "evaluator_3 (Test 3 vs Control)"],
                    "absolute": ["evaluator_4 (Test 1)", "evaluator_5 (Test 2)", "evaluator_6 (Test 4)"]
                },
                "query_categories": self.query_categories,
                "total_queries": len(self.queries)
            },
            
            "executive_summary": {
                "key_findings": [],
                "statistical_significance": False,
                "recommendation": "",
                "confidence_level": "low"
            },
            
            "pairwise_evaluation_results": pairwise_analysis,
            "absolute_evaluation_results": absolute_analysis,
            "query_type_analysis": query_type_analysis,
            
            "statistical_summary": {
                "overall_test_performance": {},
                "significant_results": [],
                "effect_sizes": {},
                "confidence_intervals": {}
            },
            
            "detailed_findings": {
                "best_performing_personas": [],
                "query_type_effectiveness": {},
                "evaluation_consistency": {}
            },
            
            "production_recommendations": {
                "implement_persona_switching": False,
                "specific_recommendations": [],
                "risk_assessment": "low",
                "next_steps": []
            }
        }
        
        # Calculate overall statistics
        total_test_wins = sum([pairwise_analysis[eval]['wins']['test'] for eval in pairwise_analysis])
        total_control_wins = sum([pairwise_analysis[eval]['wins']['control'] for eval in pairwise_analysis])
        total_ties = sum([pairwise_analysis[eval]['wins']['ties'] for eval in pairwise_analysis])
        
        overall_test_win_rate = total_test_wins / (total_test_wins + total_control_wins) if (total_test_wins + total_control_wins) > 0 else 0
        
        # Test overall significance
        overall_p_value = binom_test(total_test_wins, total_test_wins + total_control_wins, p=0.5, alternative='two-sided') if (total_test_wins + total_control_wins) > 0 else 1.0
        
        report["statistical_summary"]["overall_test_performance"] = {
            "total_comparisons": total_test_wins + total_control_wins + total_ties,
            "test_wins": total_test_wins,
            "control_wins": total_control_wins,
            "ties": total_ties,
            "test_win_rate": overall_test_win_rate,
            "overall_p_value": overall_p_value,
            "statistically_significant": overall_p_value < 0.05
        }
        
        # Calculate average absolute scores
        all_overall_scores = []
        for evaluator in absolute_analysis:
            for result in absolute_analysis[evaluator]['detailed_results']:
                all_overall_scores.append(result['scores']['overall'])
        
        avg_overall_score = np.mean(all_overall_scores) if all_overall_scores else 0
        
        # Generate key findings
        key_findings = []
        
        if overall_test_win_rate > 0.6:
            key_findings.append(f"Test personas show strong performance with {overall_test_win_rate:.1%} win rate")
        elif overall_test_win_rate > 0.5:
            key_findings.append(f"Test personas show slight advantage with {overall_test_win_rate:.1%} win rate")
        else:
            key_findings.append(f"Test personas underperform with {overall_test_win_rate:.1%} win rate")
        
        if overall_p_value < 0.05:
            key_findings.append("Results are statistically significant (p < 0.05)")
        else:
            key_findings.append("Results are not statistically significant")
        
        if avg_overall_score > 4.0:
            key_findings.append(f"High average quality scores ({avg_overall_score:.2f}/5.0)")
        elif avg_overall_score > 3.5:
            key_findings.append(f"Good average quality scores ({avg_overall_score:.2f}/5.0)")
        else:
            key_findings.append(f"Moderate average quality scores ({avg_overall_score:.2f}/5.0)")
        
        # Determine recommendation
        if overall_test_win_rate > 0.55 and overall_p_value < 0.05:
            recommendation = "IMPLEMENT - Persona switching shows statistically significant improvement"
            confidence = "high"
            implement = True
        elif overall_test_win_rate > 0.6:
            recommendation = "CONSIDER - Strong performance but not statistically significant"
            confidence = "medium"
            implement = False
        elif overall_test_win_rate > 0.5:
            recommendation = "PILOT TEST - Slight advantage warrants further testing"
            confidence = "low"
            implement = False
        else:
            recommendation = "DO NOT IMPLEMENT - No clear advantage demonstrated"
            confidence = "high"
            implement = False
        
        # Best performing query types
        best_categories = []
        for category in self.query_categories:
            category_win_rates = []
            for evaluator in query_type_analysis[category]['pairwise'].keys():
                category_win_rates.append(query_type_analysis[category]['pairwise'][evaluator]['test_win_rate'])
            
            avg_win_rate = np.mean(category_win_rates) if category_win_rates else 0
            if avg_win_rate > 0.6:
                best_categories.append(f"{category} queries ({avg_win_rate:.1%} win rate)")
        
        # Update report
        report["executive_summary"]["key_findings"] = key_findings
        report["executive_summary"]["statistical_significance"] = overall_p_value < 0.05
        report["executive_summary"]["recommendation"] = recommendation
        report["executive_summary"]["confidence_level"] = confidence
        
        report["production_recommendations"]["implement_persona_switching"] = implement
        report["production_recommendations"]["specific_recommendations"] = [
            "Continue A/B testing with larger sample sizes" if confidence == "low" else "Proceed with careful implementation" if implement else "Focus on other optimization approaches",
            "Monitor for query-type specific performance differences",
            "Consider hybrid approach using personas for specific query categories" if best_categories else "No category-specific advantages found"
        ]
        
        if best_categories:
            report["detailed_findings"]["best_performing_personas"] = best_categories
        
        # Next steps
        next_steps = []
        if implement:
            next_steps.extend([
                "Design production persona switching system",
                "Implement gradual rollout with monitoring",
                "Set up continuous evaluation metrics"
            ])
        else:
            next_steps.extend([
                "Investigate alternative improvement approaches",
                "Consider different persona designs",
                "Analyze specific failure modes"
            ])
        
        report["production_recommendations"]["next_steps"] = next_steps
        
        return report

def main():
    """Main analysis function"""
    analyzer = PersonaExperimentAnalysis()
    
    print("🔬 Starting Comprehensive Persona Experiment Analysis...")
    print("=" * 60)
    
    # Generate comprehensive report
    report = analyzer.generate_comprehensive_report()
    
    # Save report to JSON
    with open('/workspace/0_PromptEngineering/PersonaExperiment-0/persona_experiment-02/experiment_02_final_report.json', 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    print("📊 Analysis Complete!")
    print(f"📈 Overall Test Win Rate: {report['statistical_summary']['overall_test_performance']['test_win_rate']:.1%}")
    print(f"🎯 Statistical Significance: {'Yes' if report['executive_summary']['statistical_significance'] else 'No'}")
    print(f"💡 Recommendation: {report['executive_summary']['recommendation']}")
    print(f"📁 Full report saved to: experiment_02_final_report.json")
    print(f"📊 Visualizations saved to: persona_experiment_analysis.png")

if __name__ == "__main__":
    main()