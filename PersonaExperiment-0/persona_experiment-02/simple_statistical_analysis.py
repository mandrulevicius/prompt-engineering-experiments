#!/usr/bin/env python3
"""
Simplified Statistical Analysis of Persona Experiment 02
Analyzes pairwise and absolute evaluation results without external dependencies
"""

import json
import math
from collections import defaultdict, Counter
from datetime import datetime

class SimplePersonaAnalysis:
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
    
    def binomial_probability(self, k, n, p):
        """Calculate binomial probability P(X = k) for n trials with probability p"""
        if n == 0:
            return 1.0 if k == 0 else 0.0
        
        # Calculate C(n,k)
        comb = 1
        for i in range(min(k, n-k)):
            comb = comb * (n - i) // (i + 1)
        
        return comb * (p ** k) * ((1 - p) ** (n - k))
    
    def binomial_test_two_sided(self, k, n, p=0.5):
        """Simple two-sided binomial test"""
        if n == 0:
            return 1.0
        
        observed_p = k / n
        
        # Calculate p-value as 2 * min(P(X <= k), P(X >= k)) under null hypothesis
        if observed_p <= p:
            # Left tail
            p_value = 2 * sum(self.binomial_probability(i, n, p) for i in range(k + 1))
        else:
            # Right tail
            p_value = 2 * sum(self.binomial_probability(i, n, p) for i in range(k, n + 1))
        
        return min(p_value, 1.0)  # Ensure p-value doesn't exceed 1
    
    def calculate_mean_std(self, values):
        """Calculate mean and standard deviation"""
        if not values:
            return 0, 0
            
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values) if len(values) > 1 else 0
        std = math.sqrt(variance)
        return mean, std
    
    def analyze_pairwise_results(self):
        """Analyze pairwise evaluation results and calculate win rates"""
        results = {}
        
        for evaluator, data in self.pairwise_results.items():
            wins = {'control': 0, 'test': 0, 'ties': 0}
            detailed_results = []
            
            # Determine which test condition this evaluator tested
            test_condition = "test1" if evaluator == "evaluator_1" else "test2" if evaluator == "evaluator_2" else "test3"
            
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
                elif actual_winner == test_condition:
                    wins['test'] += 1
                
                detailed_results.append({
                    'query_id': query_id,
                    'winner': actual_winner,
                    'original_a': original_a,
                    'original_b': original_b,
                    'test_condition': test_condition
                })
            
            total_comparisons = wins['control'] + wins['test'] + wins['ties']
            non_tie_total = wins['control'] + wins['test']
            
            # Calculate win rates (excluding ties)
            if non_tie_total > 0:
                control_win_rate = wins['control'] / non_tie_total
                test_win_rate = wins['test'] / non_tie_total
            else:
                control_win_rate = test_win_rate = 0
            
            # Perform simple binomial test
            if non_tie_total > 0:
                p_value_two_sided = self.binomial_test_two_sided(wins['test'], non_tie_total, 0.5)
            else:
                p_value_two_sided = 1.0
                
            # Simple confidence interval (normal approximation)
            if non_tie_total > 0:
                p_hat = test_win_rate
                margin_of_error = 1.96 * math.sqrt(p_hat * (1 - p_hat) / non_tie_total)
                ci_lower = max(0, p_hat - margin_of_error)
                ci_upper = min(1, p_hat + margin_of_error)
            else:
                ci_lower = ci_upper = 0
            
            results[evaluator] = {
                'test_condition': test_condition,
                'wins': wins,
                'total_comparisons': total_comparisons,
                'non_tie_comparisons': non_tie_total,
                'win_rates': {
                    'control': control_win_rate,
                    'test': test_win_rate
                },
                'statistical_tests': {
                    'binomial_test_two_sided': p_value_two_sided,
                    'significant_at_05': p_value_two_sided < 0.05
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
        
        # Map evaluators to test conditions
        evaluator_conditions = {
            'evaluator_4': 'test1',  # Test 1 (hardcoded personas)
            'evaluator_5': 'test2',  # Test 2 (predefined personas)
            'evaluator_6': 'test4'   # Test 4 (dynamic tone)
        }
        
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
                mean_score, std_score = self.calculate_mean_std(values)
                median_score = sorted(values)[len(values)//2] if values else 0
                
                # Simple t-test approximation against neutral (3.0)
                if len(values) > 1 and std_score > 0:
                    t_stat = (mean_score - 3.0) * math.sqrt(len(values)) / std_score
                    # Rough p-value approximation for t-test (not exact)
                    p_value = 0.05 if abs(t_stat) > 2.0 else 0.1
                else:
                    t_stat = 0
                    p_value = 1.0
                
                metric_stats[metric] = {
                    'mean': mean_score,
                    'std': std_score,
                    'median': median_score,
                    'min': min(values) if values else 0,
                    'max': max(values) if values else 0,
                    't_test_vs_neutral': {
                        't_stat': t_stat,
                        'p_value_approx': p_value,
                        'significant_at_05': p_value < 0.05
                    },
                    'score_distribution': Counter(values).most_common()
                }
            
            results[evaluator] = {
                'test_condition': evaluator_conditions.get(evaluator, 'unknown'),
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
                test_condition = "test1" if evaluator == "evaluator_1" else "test2" if evaluator == "evaluator_2" else "test3"
                
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
                            elif actual_winner == test_condition:
                                category_wins['test'] += 1
                
                non_tie_total = category_wins['control'] + category_wins['test']
                if non_tie_total > 0:
                    test_win_rate = category_wins['test'] / non_tie_total
                    p_value = self.binomial_test_two_sided(category_wins['test'], non_tie_total, 0.5)
                else:
                    test_win_rate = 0
                    p_value = 1.0
                
                results[category]['pairwise'][evaluator] = {
                    'test_condition': test_condition,
                    'wins': category_wins,
                    'test_win_rate': test_win_rate,
                    'p_value': p_value,
                    'significant': p_value < 0.05
                }
            
            # Analyze absolute results by category
            evaluator_conditions = {
                'evaluator_4': 'test1',
                'evaluator_5': 'test2', 
                'evaluator_6': 'test4'
            }
            
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
                        metric_means[metric], _ = self.calculate_mean_std(scores)
                    else:
                        metric_means[metric] = None
                
                results[category]['absolute'][evaluator] = {
                    'test_condition': evaluator_conditions.get(evaluator, 'unknown'),
                    'metric_means': metric_means,
                    'n_queries': len([q for q in query_list if q in data])
                }
        
        return results
    
    def generate_comprehensive_report(self):
        """Generate comprehensive statistical report"""
        
        print("📊 Analyzing pairwise evaluation results...")
        pairwise_analysis = self.analyze_pairwise_results()
        
        print("📊 Analyzing absolute evaluation results...")
        absolute_analysis = self.analyze_absolute_results()
        
        print("📊 Analyzing query type performance...")
        query_type_analysis = self.analyze_by_query_type()
        
        # Calculate overall statistics
        total_test_wins = sum([pairwise_analysis[eval]['wins']['test'] for eval in pairwise_analysis])
        total_control_wins = sum([pairwise_analysis[eval]['wins']['control'] for eval in pairwise_analysis])
        total_ties = sum([pairwise_analysis[eval]['wins']['ties'] for eval in pairwise_analysis])
        total_non_tie = total_test_wins + total_control_wins
        
        overall_test_win_rate = total_test_wins / total_non_tie if total_non_tie > 0 else 0
        overall_p_value = self.binomial_test_two_sided(total_test_wins, total_non_tie, 0.5) if total_non_tie > 0 else 1.0
        
        # Calculate average absolute scores
        all_overall_scores = []
        for evaluator in absolute_analysis:
            for result in absolute_analysis[evaluator]['detailed_results']:
                all_overall_scores.append(result['scores']['overall'])
        
        avg_overall_score, _ = self.calculate_mean_std(all_overall_scores)
        
        # Determine statistical significance for individual evaluators
        significant_evaluators = []
        for eval_name, results in pairwise_analysis.items():
            if results['statistical_tests']['significant_at_05']:
                test_condition = results['test_condition']
                win_rate = results['win_rates']['test']
                significant_evaluators.append({
                    'evaluator': eval_name,
                    'test_condition': test_condition,
                    'win_rate': win_rate,
                    'p_value': results['statistical_tests']['binomial_test_two_sided']
                })
        
        # Analyze by query category
        best_categories = {}
        for category in self.query_categories:
            category_win_rates = []
            category_p_values = []
            
            for evaluator in query_type_analysis[category]['pairwise'].keys():
                win_rate = query_type_analysis[category]['pairwise'][evaluator]['test_win_rate']
                p_val = query_type_analysis[category]['pairwise'][evaluator]['p_value']
                category_win_rates.append(win_rate)
                category_p_values.append(p_val)
            
            if category_win_rates:
                avg_win_rate, _ = self.calculate_mean_std(category_win_rates)
                min_p_value = min(category_p_values) if category_p_values else 1.0
                
                best_categories[category] = {
                    'avg_win_rate': avg_win_rate,
                    'min_p_value': min_p_value,
                    'significant': min_p_value < 0.05,
                    'strong_performance': avg_win_rate > 0.6
                }
        
        # Generate key findings
        key_findings = []
        
        # Overall performance
        if overall_test_win_rate > 0.6:
            key_findings.append(f"✅ Test personas show strong performance with {overall_test_win_rate:.1%} win rate")
        elif overall_test_win_rate > 0.5:
            key_findings.append(f"↗️ Test personas show slight advantage with {overall_test_win_rate:.1%} win rate")
        else:
            key_findings.append(f"❌ Test personas underperform with {overall_test_win_rate:.1%} win rate")
        
        # Statistical significance
        if overall_p_value < 0.05:
            key_findings.append("📊 Overall results are statistically significant (p < 0.05)")
        else:
            key_findings.append("📊 Overall results are not statistically significant")
        
        if significant_evaluators:
            key_findings.append(f"🎯 {len(significant_evaluators)} individual evaluators show significant results")
            for sig_eval in significant_evaluators:
                key_findings.append(f"  • {sig_eval['test_condition']} vs Control: {sig_eval['win_rate']:.1%} win rate (p={sig_eval['p_value']:.3f})")
        
        # Quality scores
        if avg_overall_score > 4.0:
            key_findings.append(f"🏆 High average quality scores ({avg_overall_score:.2f}/5.0)")
        elif avg_overall_score > 3.5:
            key_findings.append(f"✨ Good average quality scores ({avg_overall_score:.2f}/5.0)")
        else:
            key_findings.append(f"📈 Moderate average quality scores ({avg_overall_score:.2f}/5.0)")
        
        # Category performance
        strong_categories = [cat for cat, data in best_categories.items() if data['strong_performance']]
        if strong_categories:
            key_findings.append(f"🎯 Strong performance in: {', '.join(strong_categories)}")
        
        significant_categories = [cat for cat, data in best_categories.items() if data['significant']]
        if significant_categories:
            key_findings.append(f"📊 Statistically significant improvement in: {', '.join(significant_categories)}")
        
        # Determine recommendation
        if overall_test_win_rate > 0.55 and overall_p_value < 0.05:
            recommendation = "✅ IMPLEMENT - Persona switching shows statistically significant improvement"
            confidence = "high"
            implement = True
        elif overall_test_win_rate > 0.6:
            recommendation = "🤔 CONSIDER - Strong performance but not statistically significant"
            confidence = "medium"
            implement = False
        elif significant_evaluators and any(sig['win_rate'] > 0.6 for sig in significant_evaluators):
            recommendation = "🧪 PILOT TEST - Some personas show significant advantages"
            confidence = "medium"
            implement = False
        elif overall_test_win_rate > 0.5:
            recommendation = "🔬 FURTHER TESTING - Slight advantage warrants more data"
            confidence = "low"
            implement = False
        else:
            recommendation = "❌ DO NOT IMPLEMENT - No clear advantage demonstrated"
            confidence = "high"
            implement = False
        
        # Compile comprehensive report
        report = {
            "experiment_info": {
                "name": "Persona Experiment 02 - Statistical Analysis",
                "date": datetime.now().isoformat(),
                "description": "Analysis of persona switching effectiveness on AI response quality",
                "evaluators": {
                    "pairwise": [
                        "evaluator_1 (Test 1: Hardcoded vs Control)",
                        "evaluator_2 (Test 2: Predefined vs Control)", 
                        "evaluator_3 (Test 3: Dynamic vs Control)"
                    ],
                    "absolute": [
                        "evaluator_4 (Test 1: Hardcoded only)",
                        "evaluator_5 (Test 2: Predefined only)", 
                        "evaluator_6 (Test 4: Dynamic Tone only)"
                    ]
                },
                "query_categories": self.query_categories,
                "total_queries": len(self.queries)
            },
            
            "executive_summary": {
                "key_findings": key_findings,
                "overall_test_win_rate": overall_test_win_rate,
                "overall_statistical_significance": overall_p_value < 0.05,
                "overall_p_value": overall_p_value,
                "average_quality_score": avg_overall_score,
                "recommendation": recommendation,
                "confidence_level": confidence
            },
            
            "detailed_results": {
                "pairwise_evaluation": pairwise_analysis,
                "absolute_evaluation": absolute_analysis,
                "query_type_analysis": query_type_analysis
            },
            
            "statistical_summary": {
                "total_comparisons": {
                    "test_wins": total_test_wins,
                    "control_wins": total_control_wins,
                    "ties": total_ties,
                    "total": total_test_wins + total_control_wins + total_ties
                },
                "overall_performance": {
                    "test_win_rate": overall_test_win_rate,
                    "control_win_rate": 1 - overall_test_win_rate,
                    "p_value": overall_p_value,
                    "statistically_significant": overall_p_value < 0.05
                },
                "significant_evaluators": significant_evaluators,
                "category_performance": best_categories
            },
            
            "production_recommendations": {
                "implement_persona_switching": implement,
                "confidence_level": confidence,
                "specific_recommendations": self.generate_specific_recommendations(
                    implement, confidence, significant_evaluators, strong_categories
                ),
                "risk_assessment": "low" if implement else "medium",
                "next_steps": self.generate_next_steps(implement, significant_evaluators, confidence)
            }
        }
        
        return report
    
    def generate_specific_recommendations(self, implement, confidence, significant_evaluators, strong_categories):
        """Generate specific recommendations based on results"""
        recommendations = []
        
        if implement:
            recommendations.extend([
                "Implement persona switching in production with careful monitoring",
                "Start with a gradual rollout to monitor real-world performance",
                "Focus on the persona approaches that showed statistical significance"
            ])
        elif confidence == "medium":
            recommendations.extend([
                "Run larger-scale A/B tests to increase statistical power",
                "Test specific persona approaches that showed promise",
                "Consider hybrid approaches using personas for specific query types"
            ])
        else:
            recommendations.extend([
                "Focus on other response quality improvement strategies",
                "Investigate why personas didn't show significant improvement",
                "Consider different persona design approaches"
            ])
        
        if significant_evaluators:
            best_approach = max(significant_evaluators, key=lambda x: x['win_rate'])
            recommendations.append(f"Prioritize {best_approach['test_condition']} approach (showed {best_approach['win_rate']:.1%} win rate)")
        
        if strong_categories:
            recommendations.append(f"Consider category-specific persona implementation for: {', '.join(strong_categories)}")
        
        return recommendations
    
    def generate_next_steps(self, implement, significant_evaluators, confidence):
        """Generate next steps based on results"""
        next_steps = []
        
        if implement:
            next_steps.extend([
                "Design production persona switching architecture",
                "Implement monitoring and evaluation metrics",
                "Plan gradual rollout with success criteria",
                "Set up continuous A/B testing framework"
            ])
        elif significant_evaluators:
            next_steps.extend([
                "Design follow-up experiment with larger sample size",
                "Focus testing on promising persona approaches",
                "Analyze specific queries where personas excelled",
                "Investigate user preference patterns"
            ])
        else:
            next_steps.extend([
                "Analyze failure modes to understand why personas didn't help",
                "Explore alternative response improvement strategies",
                "Consider different persona design methodologies",
                "Investigate query-specific optimization approaches"
            ])
        
        if confidence == "low":
            next_steps.append("Collect more evaluation data before making production decisions")
        
        return next_steps
    
    def print_summary_report(self, report):
        """Print a readable summary of the analysis"""
        print("\n" + "="*80)
        print("🎯 PERSONA EXPERIMENT 02 - FINAL ANALYSIS REPORT")
        print("="*80)
        
        print(f"\n📊 OVERALL RESULTS:")
        print(f"   • Test Win Rate: {report['executive_summary']['overall_test_win_rate']:.1%}")
        print(f"   • Statistical Significance: {'Yes' if report['executive_summary']['overall_statistical_significance'] else 'No'} (p={report['executive_summary']['overall_p_value']:.4f})")
        print(f"   • Average Quality Score: {report['executive_summary']['average_quality_score']:.2f}/5.0")
        
        print(f"\n🎯 KEY FINDINGS:")
        for finding in report['executive_summary']['key_findings']:
            print(f"   • {finding}")
        
        print(f"\n💡 RECOMMENDATION: {report['executive_summary']['recommendation']}")
        print(f"   Confidence Level: {report['executive_summary']['confidence_level'].upper()}")
        
        print(f"\n📋 SPECIFIC RECOMMENDATIONS:")
        for rec in report['production_recommendations']['specific_recommendations']:
            print(f"   • {rec}")
        
        print(f"\n🚀 NEXT STEPS:")
        for step in report['production_recommendations']['next_steps']:
            print(f"   • {step}")
        
        # Detailed breakdown
        print(f"\n📈 DETAILED BREAKDOWN BY EVALUATOR:")
        pairwise = report['detailed_results']['pairwise_evaluation']
        for evaluator, results in pairwise.items():
            test_cond = results['test_condition']
            win_rate = results['win_rates']['test']
            p_val = results['statistical_tests']['binomial_test_two_sided']
            significant = "✅" if results['statistical_tests']['significant_at_05'] else "❌"
            
            print(f"   • {evaluator.replace('evaluator_', 'Evaluator ')} ({test_cond} vs Control):")
            print(f"     - Win Rate: {win_rate:.1%} | P-value: {p_val:.4f} | Significant: {significant}")
        
        # Query category breakdown
        print(f"\n🏷️  PERFORMANCE BY QUERY CATEGORY:")
        categories = report['statistical_summary']['category_performance']
        for category, data in categories.items():
            status = "✅" if data['significant'] else "🤔" if data['strong_performance'] else "❌"
            print(f"   • {category.title()}: {data['avg_win_rate']:.1%} win rate | P-value: {data['min_p_value']:.4f} {status}")

def main():
    """Main analysis function"""
    analyzer = SimplePersonaAnalysis()
    
    print("🔬 Starting Comprehensive Persona Experiment Analysis...")
    
    # Generate comprehensive report
    report = analyzer.generate_comprehensive_report()
    
    # Print summary
    analyzer.print_summary_report(report)
    
    # Save report to JSON
    output_file = '/workspace/0_PromptEngineering/PersonaExperiment-0/persona_experiment-02/experiment_02_final_report.json'
    with open(output_file, 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    print(f"\n📁 Full detailed report saved to: experiment_02_final_report.json")
    print("="*80)

if __name__ == "__main__":
    main()