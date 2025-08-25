#!/usr/bin/env python3
"""
Absolute Evaluator 6: Test 4 (Dynamic+Tone) Responses
Evaluates dataset_f92q4icc.json using absolute scoring (1-5 scale)
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
            "helpfulness": 5,
            "helpfulness_reasoning": "Provides comprehensive current pricing with clear structure and 2025 updates",
            "appropriateness": 5,
            "appropriateness_reasoning": "Perfect informational response with clear organization and professional tone",
            "completeness": 5,
            "completeness_reasoning": "Covers all tiers, pricing, features, and changes with excellent detail and structure",
            "actionability": 4,
            "actionability_reasoning": "Clear pricing enables decision-making with good context on options",
            "overall": 5,
            "overall_reasoning": "Excellent response with comprehensive information, clear structure, and professional presentation"
        }
    elif query_num == 2:  # OpenAI GPT models news
        evaluation = {
            "helpfulness": 5,
            "helpfulness_reasoning": "Comprehensive coverage with specific metrics, timeline, and market impact analysis",
            "appropriateness": 5,
            "appropriateness_reasoning": "Perfect news summary with professional tone and well-organized information",
            "completeness": 5,
            "completeness_reasoning": "Covers all major releases with performance data, user stats, and market implications thoroughly",
            "actionability": 4,
            "actionability_reasoning": "Provides excellent context for AI strategy decisions with trend analysis",
            "overall": 5,
            "overall_reasoning": "Outstanding news summary with comprehensive coverage and professional presentation"
        }
    elif query_num == 3:  # CAP theorem
        evaluation = {
            "helpfulness": 5,
            "helpfulness_reasoning": "Excellent explanation with practical examples and modern architectural approaches",
            "appropriateness": 5,
            "appropriateness_reasoning": "Perfect technical explanation with balanced theory and practice",
            "completeness": 5,
            "completeness_reasoning": "Comprehensive coverage including examples, trade-offs, and modern solutions like BASE",
            "actionability": 4,
            "actionability_reasoning": "Provides concrete guidance for system architecture decisions with examples",
            "overall": 5,
            "overall_reasoning": "Excellent technical content with comprehensive coverage and practical architectural guidance"
        }
    elif query_num == 4:  # OAuth 2.0 implementation
        evaluation = {
            "helpfulness": 5,
            "helpfulness_reasoning": "Comprehensive security guide with code examples and systematic implementation approach",
            "appropriateness": 5,
            "appropriateness_reasoning": "Perfect technical implementation guide with security focus and professional tone",
            "completeness": 5,
            "completeness_reasoning": "Covers flow, PKCE, token storage, security practices, and vulnerabilities comprehensively",
            "actionability": 5,
            "actionability_reasoning": "Includes specific code examples and actionable security practices ready for implementation",
            "overall": 5,
            "overall_reasoning": "Outstanding technical guide with practical implementation details and comprehensive security coverage"
        }
    elif query_num == 5:  # React vs Vue for startup
        evaluation = {
            "helpfulness": 5,
            "helpfulness_reasoning": "Excellent startup-focused comparison with practical decision framework and specific considerations",
            "appropriateness": 5,
            "appropriateness_reasoning": "Perfect advisory tone with conversational yet professional approach for startup context",
            "completeness": 5,
            "completeness_reasoning": "Comprehensive comparison covering technical, business, and strategic factors with recommendations",
            "actionability": 5,
            "actionability_reasoning": "Provides clear decision criteria and next steps including specific framework suggestions",
            "overall": 5,
            "overall_reasoning": "Excellent startup advisory response with comprehensive analysis and practical recommendations"
        }
    elif query_num == 6:  # Salary negotiation
        evaluation = {
            "helpfulness": 5,
            "helpfulness_reasoning": "Comprehensive strategic guide with market research, preparation, and negotiation tactics",
            "appropriateness": 5,
            "appropriateness_reasoning": "Perfect professional advisory tone with strategic depth and practical approach",
            "completeness": 5,
            "completeness_reasoning": "Covers preparation, strategy, tactics, alternatives, and advanced techniques comprehensively",
            "actionability": 5,
            "actionability_reasoning": "Includes specific research tools, negotiation scripts, and tactical approaches ready to use",
            "overall": 5,
            "overall_reasoning": "Outstanding strategic guide with comprehensive coverage and immediately actionable advice"
        }
    elif query_num == 7:  # ML learning path
        evaluation = {
            "helpfulness": 5,
            "helpfulness_reasoning": "Excellent structured learning path with phases, timelines, and specific resources",
            "appropriateness": 5,
            "appropriateness_reasoning": "Perfect educational tone with encouraging and supportive approach for beginners",
            "completeness": 5,
            "completeness_reasoning": "Comprehensive roadmap covering math, programming, concepts, practice, and career timeline",
            "actionability": 5,
            "actionability_reasoning": "Specific courses, tools, projects, and success metrics provide clear actionable path",
            "overall": 5,
            "overall_reasoning": "Outstanding educational roadmap with comprehensive structure and practical learning path"
        }
    elif query_num == 8:  # Node.js performance debugging
        evaluation = {
            "helpfulness": 5,
            "helpfulness_reasoning": "Comprehensive debugging methodology with specific tools, commands, and systematic approach",
            "appropriateness": 5,
            "appropriateness_reasoning": "Perfect technical troubleshooting tone with systematic and professional approach",
            "completeness": 5,
            "completeness_reasoning": "Covers profiling, memory analysis, diagnostics, common issues, and optimization strategies",
            "actionability": 5,
            "actionability_reasoning": "Includes specific commands, code examples, and tools ready for immediate use",
            "overall": 5,
            "overall_reasoning": "Excellent technical debugging guide with comprehensive tools and systematic methodology"
        }
    elif query_num == 9:  # Convincing CEO about AI
        evaluation = {
            "helpfulness": 5,
            "helpfulness_reasoning": "Excellent business case framework with ROI calculations, risk mitigation, and strategic arguments",
            "appropriateness": 5,
            "appropriateness_reasoning": "Perfect business advisory tone with executive-appropriate language and strategic focus",
            "completeness": 5,
            "completeness_reasoning": "Covers impact, strategy, implementation, concerns, and specific talking points comprehensively",
            "actionability": 5,
            "actionability_reasoning": "Provides specific ROI calculations, presentation structure, and executive talking points",
            "overall": 5,
            "overall_reasoning": "Outstanding business case framework with strategic depth and executive-ready presentation"
        }
    elif query_num == 10:  # Blockchain knowledge
        evaluation = {
            "helpfulness": 5,
            "helpfulness_reasoning": "Comprehensive 2025 blockchain overview with current trends, applications, and future outlook",
            "appropriateness": 5,
            "appropriateness_reasoning": "Perfect educational tone with balanced coverage and current market context",
            "completeness": 5,
            "completeness_reasoning": "Covers concepts, types, applications, limitations, and 2025 outlook comprehensively",
            "actionability": 4,
            "actionability_reasoning": "Provides excellent understanding foundation though could include more implementation steps",
            "overall": 5,
            "overall_reasoning": "Excellent educational overview with current market context and comprehensive coverage"
        }
    elif query_num == 11:  # Team productivity
        evaluation = {
            "helpfulness": 5,
            "helpfulness_reasoning": "Comprehensive management guide with systematic diagnosis, solutions, and implementation framework",
            "appropriateness": 5,
            "appropriateness_reasoning": "Perfect management advisory tone with structured and professional approach",
            "completeness": 5,
            "completeness_reasoning": "Covers diagnosis, common issues, solutions, implementation timeline, and success metrics",
            "actionability": 5,
            "actionability_reasoning": "Provides specific actions, timelines, metrics, and systematic implementation approach",
            "overall": 5,
            "overall_reasoning": "Outstanding management guide with comprehensive framework and practical implementation steps"
        }
    elif query_num == 12:  # Python overview
        evaluation = {
            "helpfulness": 5,
            "helpfulness_reasoning": "Comprehensive Python overview with features, applications, ecosystem, and career context",
            "appropriateness": 5,
            "appropriateness_reasoning": "Perfect educational tone with comprehensive yet accessible technical explanation",
            "completeness": 5,
            "completeness_reasoning": "Covers language features, ecosystem, performance, learning path, and career opportunities thoroughly",
            "actionability": 4,
            "actionability_reasoning": "Provides excellent understanding and learning path though could include more immediate starting steps",
            "overall": 5,
            "overall_reasoning": "Excellent comprehensive Python overview with practical applications and career context"
        }
    
    return evaluation

def main():
    # Load the blinded dataset
    dataset_path = Path("blinded_evaluation/dataset_f92q4icc.json")
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
    output_path = Path("results/absolute_evaluator_6_results.json")
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Evaluation complete. Results saved to {output_path}")

if __name__ == "__main__":
    main()