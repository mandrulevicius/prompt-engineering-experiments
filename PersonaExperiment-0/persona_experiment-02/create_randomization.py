#!/usr/bin/env python3

import json
import random
import string
import shutil
import os
from pathlib import Path

def generate_random_id(length=8):
    """Generate a random alphanumeric ID"""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def create_randomization_key():
    """Create randomization mapping for response files"""
    
    # Original response files
    response_files = [
        "control_responses_agent_1.json",
        "test_1_hardcoded_responses_agent_1.json", 
        "test_2_predefined_responses_agent_1.json",
        "test_3_dynamic_responses_agent_1.json",
        "test_4_dynamic_tone_responses_agent_1.json"
    ]
    
    # Generate random dataset names
    randomization_key = {}
    used_ids = set()
    
    for filename in response_files:
        # Generate unique random ID
        while True:
            random_id = generate_random_id()
            if random_id not in used_ids:
                used_ids.add(random_id)
                break
        
        blinded_name = f"dataset_{random_id}.json"
        randomization_key[filename] = blinded_name
    
    return randomization_key

def create_blinded_dataset(randomization_key):
    """Copy response files to blinded directory with randomized names"""
    
    responses_dir = Path("responses")
    blinded_dir = Path("blinded_evaluation")
    
    # Ensure blinded directory exists
    blinded_dir.mkdir(exist_ok=True)
    
    # Copy and rename files
    for original_name, blinded_name in randomization_key.items():
        src = responses_dir / original_name
        dst = blinded_dir / blinded_name
        
        if src.exists():
            shutil.copy2(src, dst)
            print(f"Copied {original_name} -> {blinded_name}")
        else:
            print(f"Warning: {src} not found")

def strip_role_indicators(response_text):
    """Remove [Role: X] indicators from response text"""
    import re
    # Remove role indicators at the beginning of responses
    cleaned = re.sub(r'^\[Role:[^\]]+\]\s*', '', response_text)
    return cleaned

def create_clean_blinded_dataset(randomization_key):
    """Create blinded dataset with role indicators removed"""
    
    responses_dir = Path("responses")
    blinded_dir = Path("blinded_evaluation")
    
    # Ensure blinded directory exists
    blinded_dir.mkdir(exist_ok=True)
    
    for original_name, blinded_name in randomization_key.items():
        src = responses_dir / original_name
        dst = blinded_dir / blinded_name
        
        if src.exists():
            # Load original responses
            with open(src, 'r') as f:
                data = json.load(f)
            
            # Strip role indicators from all responses
            cleaned_data = {}
            for query_key, response in data.items():
                cleaned_data[query_key] = strip_role_indicators(response)
            
            # Save cleaned version
            with open(dst, 'w') as f:
                json.dump(cleaned_data, f, indent=2)
            
            print(f"Cleaned and copied {original_name} -> {blinded_name}")
        else:
            print(f"Warning: {src} not found")

def main():
    """Main function to execute randomization process"""
    
    print("Creating randomization key...")
    randomization_key = create_randomization_key()
    
    # Save randomization key
    with open("randomization_key.json", 'w') as f:
        json.dump(randomization_key, f, indent=2)
    
    print("Randomization key saved to randomization_key.json")
    print("Mapping:")
    for original, blinded in randomization_key.items():
        print(f"  {original} -> {blinded}")
    
    print("\nCreating blinded dataset (with role indicators removed)...")
    create_clean_blinded_dataset(randomization_key)
    
    print("\nBlinded dataset created successfully!")
    print("Evaluators will only see randomized filenames without role indicators.")

if __name__ == "__main__":
    main()