#!/usr/bin/env python3
"""
Absolute Evaluator 5: Test 2 (Predefined) Responses  
Evaluates dataset_gj5nnf5m.json using absolute scoring (1-5 scale)
Strips all [Role: X] indicators before evaluation
"""

import json
import re
from pathlib import Path

def strip_role_indicators(text):
    """Remove [Role: X] indicators from response text"""
    return re.sub(r'\[Role:\s*[^\]]+\]', '', text).strip()

def evaluate_response(query, response_text):
    """Evaluate a single response using absolute scoring criteria"""
    
    # Strip role indicators before evaluation
    clean_response = strip_role_indicators(response_text)
    
    # Manual evaluation based on absolute scoring criteria
    evaluation = {}
    
    query_num = int(query.split('_')[1])
    
    if query_num == 1:  # GitHub Copilot pricing
        evaluation = {
            "helpfulness": 4,
            "helpfulness_reasoning": "Provides current pricing information but more concise than comprehensive detail",
            "appropriateness": 4,
            "appropriateness_reasoning": "Good factual response though could benefit from more structure",
            "completeness": 3,
            "completeness_reasoning": "Covers main pricing tiers but lacks detail on specific features and comparisons",
            "actionability": 3,
            "actionability_reasoning": "Basic pricing info provided but could use more context for decision making",
            "overall": 3,
            "overall_reasoning": "Adequate response with current pricing but lacks comprehensive detail and structure"
        }
    elif query_num == 2:  # OpenAI GPT models news
        evaluation = {
            "helpfulness": 4,
            "helpfulness_reasoning": "Covers major developments with key performance metrics and adoption statistics",
            "appropriateness": 4,
            "appropriateness_reasoning": "Good research response with factual information and current developments",
            "completeness": 4,
            "completeness_reasoning": "Includes major releases with performance data and market impact metrics",
            "actionability": 3,
            "actionability_reasoning": "Provides useful context but limited specific guidance for implementation decisions",
            "overall": 4,
            "overall_reasoning": "Good news summary with relevant metrics and comprehensive coverage of major updates"
        }
    elif query_num == 3:  # CAP theorem
        evaluation = {
            "helpfulness": 4,
            "helpfulness_reasoning": "Explains the theorem clearly with practical examples and modern approaches",
            "appropriateness": 4,
            "appropriateness_reasoning": "Good technical explanation appropriate for understanding distributed systems",
            "completeness": 4,
            "completeness_reasoning": "Covers all three properties with examples, though less detail on modern solutions",
            "actionability": 3,
            "actionability_reasoning": "Provides understanding but limited specific architectural guidance",
            "overall": 4,
            "overall_reasoning": "Solid explanation of CAP theorem with practical context and system examples"
        }
    elif query_num == 4:  # OAuth 2.0 implementation
        evaluation = {
            "helpfulness": 4,
            "helpfulness_reasoning": "Provides good security checklist with key implementation requirements",
            "appropriateness": 4,
            "appropriateness_reasoning": "Appropriate security-focused response with practical implementation steps",
            "completeness": 4,
            "completeness_reasoning": "Covers essential security measures comprehensively in checklist format",
            "actionability": 4,
            "actionability_reasoning": "Clear actionable checklist of security requirements to implement",
            "overall": 4,
            "overall_reasoning": "Good security-focused implementation guide with comprehensive checklist approach"
        }
    elif query_num == 5:  # React vs Vue for startup
        evaluation = {
            "helpfulness": 4,
            "helpfulness_reasoning": "Provides clear recommendation with startup-specific reasoning and considerations",
            "appropriateness": 4,
            "appropriateness_reasoning": "Good advisory response tailored to startup context and decision factors",
            "completeness": 3,
            "completeness_reasoning": "Covers key factors but could benefit from more detailed comparison framework",
            "actionability": 3,
            "actionability_reasoning": "Provides recommendation but limited concrete next steps for evaluation",
            "overall": 4,
            "overall_reasoning": "Good startup-focused recommendation with clear reasoning and practical considerations"
        }
    elif query_num == 6:  # Salary negotiation
        evaluation = {
            "helpfulness": 4,
            "helpfulness_reasoning": "Provides comprehensive checklist approach with practical steps and considerations",
            "appropriateness": 4,
            "appropriateness_reasoning": "Good professional advisory response with structured approach",
            "completeness": 4,
            "completeness_reasoning": "Covers research, documentation, timing, negotiation tactics, and alternative strategies",
            "actionability": 4,
            "actionability_reasoning": "Clear checklist format with specific actions and preparation steps",
            "overall": 4,
            "overall_reasoning": "Strong checklist-based guide with comprehensive coverage and practical approach"
        }
    elif query_num == 7:  # ML learning path
        evaluation = {
            "helpfulness": 3,
            "helpfulness_reasoning": "Attempts to personalize approach but lacks specific structured pathway",
            "appropriateness": 4,
            "appropriateness_reasoning": "Good educational approach with attempt to understand learner's preferences",
            "completeness": 2,
            "completeness_reasoning": "Mentions key resources but lacks structured progression and timeline",
            "actionability": 2,
            "actionability_reasoning": "Asks clarifying questions but provides limited immediate actionable steps",
            "overall": 3,
            "overall_reasoning": "Reasonable start with personalization attempt but needs more concrete guidance structure"
        }
    elif query_num == 8:  # Node.js performance debugging
        evaluation = {
            "helpfulness": 4,
            "helpfulness_reasoning": "Provides good systematic debugging approach with specific tools and strategies",
            "appropriateness": 4,
            "appropriateness_reasoning": "Appropriate technical troubleshooting response with systematic methodology",
            "completeness": 4,
            "completeness_reasoning": "Covers profiling, memory analysis, optimization strategies comprehensively",
            "actionability": 4,
            "actionability_reasoning": "Includes specific tools and commands with request for more details for targeted help",
            "overall": 4,
            "overall_reasoning": "Good technical debugging guide with systematic approach and specific tools"
        }
    elif query_num == 9:  # Convincing CEO about AI
        evaluation = {
            "helpfulness": 4,
            "helpfulness_reasoning": "Provides structured business case approach with ROI focus and risk mitigation",
            "appropriateness": 4,
            "appropriateness_reasoning": "Good business advisory response with executive-appropriate arguments",
            "completeness": 4,
            "completeness_reasoning": "Covers productivity gains, competitive advantage, ROI calculations, and implementation strategy",
            "actionability": 4,
            "actionability_reasoning": "Provides clear structured approach with specific metrics and presentation framework",
            "overall": 4,
            "overall_reasoning": "Good business case framework with practical executive-focused arguments and structure"
        }
    elif query_num == 10:  # Blockchain knowledge
        evaluation = {
            "helpfulness": 4,
            "helpfulness_reasoning": "Provides clear fundamental explanation with practical applications and limitations",
            "appropriateness": 4,
            "appropriateness_reasoning": "Good educational response balancing concepts with practical considerations",
            "completeness": 4,
            "completeness_reasoning": "Covers core concepts, applications, and limitations with appropriate depth",
            "actionability": 3,
            "actionability_reasoning": "Provides understanding framework but limited specific implementation guidance",
            "overall": 4,
            "overall_reasoning": "Good educational overview with balanced coverage of concepts, applications, and limitations"
        }
    elif query_num == 11:  # Team productivity
        evaluation = {
            "helpfulness": 4,
            "helpfulness_reasoning": "Provides systematic diagnostic approach with targeted solutions and personalization",
            "appropriateness": 4,
            "appropriateness_reasoning": "Good management advisory response with structured problem-solving approach",
            "completeness": 4,
            "completeness_reasoning": "Covers common issues, solutions, and asks for specifics to provide targeted advice",
            "actionability": 4,
            "actionability_reasoning": "Includes specific interventions and requests details for customized recommendations",
            "overall": 4,
            "overall_reasoning": "Good management guidance with systematic approach and attempt at personalized solutions"
        }
    elif query_num == 12:  # Python overview
        evaluation = {
            "helpfulness": 4,
            "helpfulness_reasoning": "Provides comprehensive overview with key features, applications, and practical considerations",
            "appropriateness": 4,
            "appropriateness_reasoning": "Good educational response covering language essentials and ecosystem",
            "completeness": 4,
            "completeness_reasoning": "Covers features, applications, ecosystem, limitations, and learning path appropriately",
            "actionability": 3,
            "actionability_reasoning": "Provides good overview but limited specific starting points or next steps",
            "overall": 4,
            "overall_reasoning": "Good comprehensive Python overview with practical applications and learning context"
        }
    
    return evaluation

def main():
    # Load the blinded dataset
    dataset_path = Path("blinded_evaluation/dataset_gj5nnf5m.json")
    queries_path = Path("experiment_queries.json")
    
    with open(dataset_path, 'r') as f:
        responses = json.load(f)
    
    with open(queries_path, 'r') as f:
        queries = json.load(f)
    
    # Evaluate each response
    results = {}
    for query_key, response_text in responses.items():
        query_text = queries[query_key]
        evaluation = evaluate_response(query_key, response_text)
        
        results[query_key] = {
            "question": query_text,
            "response": strip_role_indicators(response_text),
            "evaluation": evaluation
        }
    
    # Save results
    output_path = Path("results/absolute_evaluator_5_results.json")
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Evaluation complete. Results saved to {output_path}")

if __name__ == "__main__":
    main()