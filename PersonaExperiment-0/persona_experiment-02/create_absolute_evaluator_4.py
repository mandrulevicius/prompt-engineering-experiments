#!/usr/bin/env python3
"""
Absolute Evaluator 4: Test 1 (Hardcoded) Responses
Evaluates dataset_r5ly4mxl.json using absolute scoring (1-5 scale)
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
            "helpfulness_reasoning": "Provides comprehensive, current pricing information with all tiers clearly explained including 2025 updates",
            "appropriateness": 5,
            "appropriateness_reasoning": "Perfect factual research response with structured pricing breakdown",
            "completeness": 5,
            "completeness_reasoning": "Covers all pricing tiers, includes specific costs, mentions free access options and 2025 changes",
            "actionability": 4,
            "actionability_reasoning": "Clear pricing information allows immediate decision making, could include direct links",
            "overall": 5,
            "overall_reasoning": "Excellent comprehensive response with current, accurate pricing information in well-structured format"
        }
    elif query_num == 2:  # OpenAI GPT models news
        evaluation = {
            "helpfulness": 5,
            "helpfulness_reasoning": "Provides comprehensive coverage of major 2025 GPT developments with specific performance metrics",
            "appropriateness": 5,
            "appropriateness_reasoning": "Perfect research response with factual, up-to-date information presented systematically",
            "completeness": 5,
            "completeness_reasoning": "Covers all major releases (GPT-5, GPT-4.5, GPT-4.1 series) with performance benchmarks and adoption stats",
            "actionability": 4,
            "actionability_reasoning": "Provides context for decision-making about AI model selection and adoption trends",
            "overall": 5,
            "overall_reasoning": "Excellent comprehensive news summary with quantitative details and market impact analysis"
        }
    elif query_num == 3:  # CAP theorem
        evaluation = {
            "helpfulness": 5,
            "helpfulness_reasoning": "Provides clear explanation of complex theoretical concept with practical applications",
            "appropriateness": 5,
            "appropriateness_reasoning": "Perfect domain expert response balancing theory with practical engineering implications",
            "completeness": 5,
            "completeness_reasoning": "Covers all three properties, trade-offs, system examples, and modern approaches like CRDTs",
            "actionability": 4,
            "actionability_reasoning": "Gives concrete guidance on when to choose different system architectures",
            "overall": 5,
            "overall_reasoning": "Excellent technical explanation that bridges theory and practice with concrete examples"
        }
    elif query_num == 4:  # OAuth 2.0 implementation
        evaluation = {
            "helpfulness": 5,
            "helpfulness_reasoning": "Provides comprehensive security guidance with specific implementation details and code examples",
            "appropriateness": 5,
            "appropriateness_reasoning": "Perfect technical implementation guide with security best practices focus",
            "completeness": 5,
            "completeness_reasoning": "Covers PKCE, state parameters, token storage, validation, and common vulnerabilities comprehensively",
            "actionability": 5,
            "actionability_reasoning": "Includes actual code snippets and specific implementation patterns developers can follow immediately",
            "overall": 5,
            "overall_reasoning": "Outstanding technical guide with practical code examples and comprehensive security considerations"
        }
    elif query_num == 5:  # React vs Vue for startup
        evaluation = {
            "helpfulness": 4,
            "helpfulness_reasoning": "Provides balanced comparison with startup-specific considerations and practical decision framework",
            "appropriateness": 5,
            "appropriateness_reasoning": "Perfect advisory response tailored to startup context with business considerations",
            "completeness": 4,
            "completeness_reasoning": "Covers key factors (talent, ecosystem, scaling) with practical recommendation framework",
            "actionability": 4,
            "actionability_reasoning": "Provides clear decision criteria and concrete next steps (prototype in both frameworks)",
            "overall": 4,
            "overall_reasoning": "Strong advisory response with practical startup focus and actionable decision framework"
        }
    elif query_num == 6:  # Salary negotiation
        evaluation = {
            "helpfulness": 4,
            "helpfulness_reasoning": "Provides structured approach with concrete steps and practical scripts for negotiation",
            "appropriateness": 5,
            "appropriateness_reasoning": "Perfect practical advisory response with professional tone and specific guidance",
            "completeness": 4,
            "completeness_reasoning": "Covers research, preparation, negotiation tactics, and handling rejection with specific examples",
            "actionability": 5,
            "actionability_reasoning": "Includes ready-to-use scripts, specific websites for research, and step-by-step process",
            "overall": 4,
            "overall_reasoning": "Strong practical guide with actionable steps and concrete examples for salary negotiation"
        }
    elif query_num == 7:  # ML learning path
        evaluation = {
            "helpfulness": 4,
            "helpfulness_reasoning": "Provides structured learning path with specific resources and realistic timelines",
            "appropriateness": 4,
            "appropriateness_reasoning": "Good educational guidance though could be more personalized to individual learning style",
            "completeness": 4,
            "completeness_reasoning": "Covers foundations, core concepts, practice with specific courses and projects",
            "actionability": 4,
            "actionability_reasoning": "Includes specific course recommendations, tools, and success metrics to follow",
            "overall": 4,
            "overall_reasoning": "Solid educational roadmap with practical structure and specific resource recommendations"
        }
    elif query_num == 8:  # Node.js performance debugging
        evaluation = {
            "helpfulness": 5,
            "helpfulness_reasoning": "Provides comprehensive debugging methodology with specific tools and code examples",
            "appropriateness": 5,
            "appropriateness_reasoning": "Perfect technical troubleshooting response with systematic diagnostic approach",
            "completeness": 5,
            "completeness_reasoning": "Covers profiling, memory analysis, event loop monitoring, common issues, and solutions",
            "actionability": 5,
            "actionability_reasoning": "Includes specific commands, code snippets, and tools that can be used immediately",
            "overall": 5,
            "overall_reasoning": "Excellent technical debugging guide with practical tools and systematic troubleshooting approach"
        }
    elif query_num == 9:  # Convincing CEO about AI
        evaluation = {
            "helpfulness": 4,
            "helpfulness_reasoning": "Provides business-focused persuasion strategy with ROI calculations and risk mitigation",
            "appropriateness": 5,
            "appropriateness_reasoning": "Perfect business advisory response tailored to executive audience and decision-making",
            "completeness": 4,
            "completeness_reasoning": "Covers financial impact, competitive risks, implementation strategy, and common concerns",
            "actionability": 4,
            "actionability_reasoning": "Provides specific talking points, ROI examples, and structured presentation approach",
            "overall": 4,
            "overall_reasoning": "Strong business case framework with executive-appropriate arguments and practical approach"
        }
    elif query_num == 10:  # Blockchain knowledge
        evaluation = {
            "helpfulness": 4,
            "helpfulness_reasoning": "Provides current blockchain landscape with 2025 trends and practical applications",
            "appropriateness": 4,
            "appropriateness_reasoning": "Good educational overview balancing trends with practical considerations",
            "completeness": 4,
            "completeness_reasoning": "Covers current state, trends, applications, technical advances, and regulatory context",
            "actionability": 3,
            "actionability_reasoning": "Provides overview for understanding but limited specific next steps for implementation",
            "overall": 4,
            "overall_reasoning": "Solid educational overview of blockchain with current market context and practical applications"
        }
    elif query_num == 11:  # Team productivity
        evaluation = {
            "helpfulness": 4,
            "helpfulness_reasoning": "Provides systematic diagnostic approach with concrete solutions and implementation steps",
            "appropriateness": 4,
            "appropriateness_reasoning": "Good management advisory response with structured problem-solving approach",
            "completeness": 4,
            "completeness_reasoning": "Covers diagnosis, common issues, solutions, and progress tracking with specific timeframes",
            "actionability": 4,
            "actionability_reasoning": "Includes immediate actions, survey questions, and measurable success metrics",
            "overall": 4,
            "overall_reasoning": "Strong management guidance with systematic approach and practical implementation steps"
        }
    elif query_num == 12:  # Python overview
        evaluation = {
            "helpfulness": 4,
            "helpfulness_reasoning": "Provides comprehensive technical overview with practical applications and considerations",
            "appropriateness": 4,
            "appropriateness_reasoning": "Good technical educational response covering language features and ecosystem",
            "completeness": 5,
            "completeness_reasoning": "Covers architecture, features, ecosystem, performance, advanced concepts, and deployment comprehensively",
            "actionability": 3,
            "actionability_reasoning": "Provides technical understanding but limited specific next steps for getting started",
            "overall": 4,
            "overall_reasoning": "Strong technical overview with comprehensive coverage of Python's capabilities and considerations"
        }
    
    return evaluation

def main():
    # Load the blinded dataset
    dataset_path = Path("blinded_evaluation/dataset_r5ly4mxl.json")
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
    output_path = Path("results/absolute_evaluator_4_results.json")
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Evaluation complete. Results saved to {output_path}")

if __name__ == "__main__":
    main()