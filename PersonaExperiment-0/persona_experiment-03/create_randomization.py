#!/usr/bin/env python3
"""
Create randomization mapping for persona experiment 03
"""
import json
import random
import string
from pathlib import Path
import shutil

def generate_random_id(length=8):
    """Generate a random alphanumeric string"""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def create_randomization_mapping():
    """Create randomization mapping for all response files"""
    
    # All response files we expect
    response_files = []
    
    # Control responses (agents 4-7)
    for i in range(4, 8):
        response_files.append(f"control_responses_agent_{i}.json")
    
    # Test condition responses (agents 4-7)
    for test_num in range(1, 5):
        for i in range(4, 8):
            if test_num == 1:
                response_files.append(f"test_1_hardcoded_responses_agent_{i}.json")
            elif test_num == 2:
                response_files.append(f"test_2_predefined_responses_agent_{i}.json")
            elif test_num == 3:
                response_files.append(f"test_3_dynamic_responses_agent_{i}.json")
            elif test_num == 4:
                response_files.append(f"test_4_dynamic_tone_responses_agent_{i}.json")
    
    # Create randomization mapping
    randomization_key = {}
    used_ids = set()
    
    for filename in response_files:
        # Generate unique random ID
        while True:
            random_id = generate_random_id()
            if random_id not in used_ids:
                used_ids.add(random_id)
                break
        
        randomization_key[filename] = f"dataset_{random_id}.json"
    
    return randomization_key

def copy_and_blind_files(randomization_key):
    """Copy response files to blinded evaluation directory with randomized names"""
    
    responses_dir = Path("responses")
    blinded_dir = Path("blinded_evaluation")
    blinded_dir.mkdir(exist_ok=True)
    
    for original_file, blinded_file in randomization_key.items():
        original_path = responses_dir / original_file
        blinded_path = blinded_dir / blinded_file
        
        if original_path.exists():
            shutil.copy2(original_path, blinded_path)
            print(f"Copied {original_file} -> {blinded_file}")
        else:
            print(f"WARNING: {original_file} not found!")

def main():
    """Main execution"""
    print("Creating randomization mapping for persona experiment 03...")
    
    # Set random seed for reproducibility
    random.seed(42)
    
    # Create mapping
    randomization_key = create_randomization_mapping()
    
    # Save mapping
    with open("randomization_key.json", "w") as f:
        json.dump(randomization_key, f, indent=2)
    
    print(f"Created randomization mapping for {len(randomization_key)} files")
    
    # Copy and blind files
    copy_and_blind_files(randomization_key)
    
    print("Randomization complete!")
    print("Blinded datasets ready for evaluation")

if __name__ == "__main__":
    main()