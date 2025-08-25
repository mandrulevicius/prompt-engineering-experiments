#!/usr/bin/env python3
"""
Create a simple text-based visualization of the persona experiment results
"""

def create_text_visualization():
    """Create text-based charts for the results"""
    
    # Win rates data
    evaluators = ["Evaluator 1\n(Test1 vs Control)", "Evaluator 2\n(Test2 vs Control)", "Evaluator 3\n(Test3 vs Control)"]
    test_win_rates = [0.0, 100.0, 77.8]
    control_win_rates = [100.0, 0.0, 22.2]
    p_values = [0.0039, 0.0020, 0.1797]
    significant = [True, True, False]
    
    # Category performance
    categories = ["Research", "Technical", "Advisory"]
    category_win_rates = [55.6, 58.3, 66.7]
    category_p_values = [0.5000, 0.1250, 0.0625]
    
    # Absolute scores
    evaluator_scores = {
        "Test 1 (Hardcoded)": 4.75,
        "Test 2 (Predefined)": 3.92, 
        "Test 4 (Dynamic Tone)": 4.58
    }
    
    print("╔═══════════════════════════════════════════════════════════════════════════════╗")
    print("║                    PERSONA EXPERIMENT 02 - VISUAL SUMMARY                    ║")
    print("╚═══════════════════════════════════════════════════════════════════════════════╝")
    
    print("\n📊 PAIRWISE EVALUATION WIN RATES")
    print("─" * 80)
    print(f"{'Evaluator':<25} {'Test Win %':<12} {'Control Win %':<15} {'P-Value':<10} {'Significant'}")
    print("─" * 80)
    
    for i in range(len(evaluators)):
        eval_name = evaluators[i].replace('\n', ' ')
        sig_status = "✅ Yes" if significant[i] else "❌ No"
        print(f"{eval_name:<25} {test_win_rates[i]:>8.1f}%   {control_win_rates[i]:>10.1f}%     {p_values[i]:<8.4f}  {sig_status}")
    
    print(f"\n{'OVERALL':<25} {'60.7%':>8}   {'39.3%':>10}     {'0.3449':<8}  ❌ No")
    
    # Visual bar chart for win rates
    print("\n📈 WIN RATE VISUALIZATION")
    print("─" * 50)
    for i, eval_name in enumerate(["Test 1", "Test 2", "Test 3"]):
        rate = test_win_rates[i]
        bar_length = int(rate / 5)  # Scale to fit in 20 chars max
        bar = "█" * bar_length
        sig_marker = " ✅" if significant[i] else " ❌"
        print(f"{eval_name:<8} │{bar:<20}│ {rate:5.1f}%{sig_marker}")
    
    print("         │" + "─" * 20 + "│")
    print("         0%        50%       100%")
    
    # Category performance
    print(f"\n🏷️  QUERY CATEGORY PERFORMANCE")
    print("─" * 50)
    print(f"{'Category':<12} {'Win Rate':<10} {'P-Value':<10} {'Status'}")
    print("─" * 50)
    
    for i, category in enumerate(categories):
        rate = category_win_rates[i]
        p_val = category_p_values[i]
        if p_val < 0.05:
            status = "✅ Significant"
        elif rate > 60:
            status = "🤔 Promising"
        else:
            status = "❌ No effect"
        
        print(f"{category:<12} {rate:>6.1f}%    {p_val:<8.4f}  {status}")
    
    # Absolute quality scores
    print(f"\n⭐ ABSOLUTE QUALITY SCORES (1-5 scale)")
    print("─" * 50)
    for test_name, score in evaluator_scores.items():
        bar_length = int((score - 1) * 5)  # Scale from 1-5 to 0-20
        bar = "★" * bar_length
        print(f"{test_name:<20} │{bar:<20}│ {score:.2f}/5.0")
    
    print("                     │" + "─" * 20 + "│")
    print("                     1.0     3.0     5.0")
    
    # Key insights
    print(f"\n🔍 KEY INSIGHTS")
    print("─" * 80)
    print("• Test 2 (Predefined Personas) shows perfect 100% win rate with high significance")
    print("• Test 1 (Hardcoded Personas) significantly underperforms (0% win rate)")  
    print("• Test 3 (Dynamic Personas) shows strong but non-significant improvement (77.8%)")
    print("• Advisory queries benefit most from persona switching (66.7% win rate)")
    print("• Overall quality scores are high (4.42/5.0), indicating good response quality")
    print("• Statistical significance is mixed - need larger sample sizes for definitive results")
    
    print(f"\n💡 RECOMMENDATIONS")
    print("─" * 80)
    print("✅ PRIORITY: Focus on Test 2 (Predefined Personas) approach")
    print("🧪 TEST: Expand advisory query optimization with personas")  
    print("📊 RESEARCH: Investigate why Test 1 underperformed significantly")
    print("🔬 EXPERIMENT: Run larger-scale tests to improve statistical power")
    print("⚖️  CONSIDER: Hybrid approach using personas selectively by query type")

if __name__ == "__main__":
    create_text_visualization()