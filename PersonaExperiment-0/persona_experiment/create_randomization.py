#!/usr/bin/env python3
import json
import shutil
import random
import string
from pathlib import Path

def generate_random_string(length=8):
    """Generate a random string for blinding."""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def create_randomization_mapping():
    """Create a mapping from original filenames to random dataset IDs."""
    
    # Set seed for reproducibility
    random.seed(42)
    
    responses_dir = Path("/workspace/0_PromptEngineering/persona_experiment/responses")
    blinded_dir = Path("/workspace/0_PromptEngineering/persona_experiment/blinded_evaluation")
    blinded_dir.mkdir(exist_ok=True)
    
    # Get all response files
    response_files = list(responses_dir.glob("*.json"))
    
    # Create randomization mapping
    randomization_key = {}
    used_codes = set()
    
    for response_file in response_files:
        # Generate unique random code
        while True:
            random_code = f"dataset_{generate_random_string()}"
            if random_code not in used_codes:
                used_codes.add(random_code)
                break
        
        randomization_key[response_file.name] = f"{random_code}.json"
    
    # Save randomization key
    with open("/workspace/0_PromptEngineering/persona_experiment/randomization_key.json", "w") as f:
        json.dump(randomization_key, f, indent=2)
    
    # Copy and rename files to blinded directory
    for original_name, blinded_name in randomization_key.items():
        shutil.copy2(
            responses_dir / original_name, 
            blinded_dir / blinded_name
        )
    
    print(f"Created randomization mapping for {len(randomization_key)} files")
    print(f"Files copied to {blinded_dir}")
    
    return randomization_key

if __name__ == "__main__":
    mapping = create_randomization_mapping()
    print("\nRandomization completed successfully!")
    print("Files ready for blind evaluation.")