#!/usr/bin/env python3
"""
Twitter Content Generation Script

This script generates Twitter content using Claude API.
"""

import json
import os
import sys
import glob
import urllib.request
import urllib.parse
from pathlib import Path
from datetime import datetime

def get_project_paths(config_file="config.json"):
    """Get project-specific paths from configuration"""
    config_path = Path(__file__).parent.parent / config_file
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        project = config.get("current_project", None)
        
        if project:
            return {
                "input_dir": Path(__file__).parent.parent / "1_input" / project,
                "system_assets_dir": Path(__file__).parent.parent / "2_system_assets" / project,
                "output_dir": Path(__file__).parent.parent / "3_unlabeled" / project
            }
        else:
            return {
                "input_dir": Path(__file__).parent.parent / "1_input",
                "system_assets_dir": Path(__file__).parent.parent / "2_system_assets",
                "output_dir": Path(__file__).parent.parent / "3_unlabeled"
            }
    except:
        return {
            "input_dir": Path(__file__).parent.parent / "1_input",
            "system_assets_dir": Path(__file__).parent.parent / "2_system_assets",
            "output_dir": Path(__file__).parent.parent / "3_unlabeled"
        }

def find_input_files(input_dir):
    """
    Auto-detect and map timestamped input files to generic names
    """
    file_mapping = {}
    
    # Define file patterns and their generic mappings
    patterns = {
        'message_house.md': ['messagehouse_*.md'],
        'brand_side_persona.md': ['userstories_20*.md'],  # Brand side user stories
        'customer_side_persona.md': ['userstories_reviews_*.md'],  # Customer side from reviews
        'keywords_bank.md': ['keywords_bank_*.md'],
        'testimonials.md': ['testimonials_*.md'],
        'platform_personas.md': ['platform_personas_*.md']  # Optional
    }
    
    for generic_name, patterns_list in patterns.items():
        found_file = None
        for pattern in patterns_list:
            matches = glob.glob(str(input_dir / pattern))
            if matches:
                # Get the most recent file if multiple matches
                found_file = max(matches, key=os.path.getmtime)
                break
        
        if found_file:
            file_mapping[generic_name] = found_file
            print(f"[OK] Found {generic_name}: {os.path.basename(found_file)}")
        else:
            if generic_name != 'platform_personas.md':  # Platform personas is optional
                print(f"[WARN] Missing required file: {generic_name}")
            else:
                print(f"[INFO] Optional file not found: {generic_name}")
    
    return file_mapping

def load_input_content(file_mapping):
    """
    Load content from all mapped input files
    """
    content = {}
    
    for generic_name, file_path in file_mapping.items():
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content[generic_name] = f.read()
                print(f"[OK] Loaded {generic_name} ({len(content[generic_name])} chars)")
        except Exception as e:
            print(f"[FAIL] Error loading {generic_name}: {e}")
            content[generic_name] = ""
    
    return content

def load_example_from_json():
    """Load the example from labeled JSON for system prompt"""
    example_path = Path(__file__).parent.parent / "5_labeled_json" / "twitter_example_001.json"
    try:
        with open(example_path, 'r', encoding='utf-8') as f:
            example_data = json.load(f)
        
        # Extract the Twitter content for the prompt
        content = example_data['twitter_content']
        
        example_text = f"""
**EXAMPLE OF 8.2/10 QUALITY TWITTER CONTENT:**

# **Twitter Content Strategy**

## **Category 1: {content['categories']['category_1']['title']}**

### **Post 1A: {content['categories']['category_1']['posts']['post_1a']['type']}**
{content['categories']['category_1']['posts']['post_1a']['content']}

### **Post 1B: {content['categories']['category_1']['posts']['post_1b']['type']}**
{content['categories']['category_1']['posts']['post_1b']['content']}

### **Post 1C: {content['categories']['category_1']['posts']['post_1c']['type']}**
{content['categories']['category_1']['posts']['post_1c']['content']}

## **Category 2: {content['categories']['category_2']['title']}**

### **Post 2A: {content['categories']['category_2']['posts']['post_2a']['type']}**
{content['categories']['category_2']['posts']['post_2a']['content']}

### **Post 2B: {content['categories']['category_2']['posts']['post_2b']['type']}**
{content['categories']['category_2']['posts']['post_2b']['content']}

### **Post 2C: {content['categories']['category_2']['posts']['post_2c']['type']}**
{content['categories']['category_2']['posts']['post_2c']['content']}

## **Category 3: {content['categories']['category_3']['title']}**

### **Post 3A: {content['categories']['category_3']['posts']['post_3a']['type']}**
{content['categories']['category_3']['posts']['post_3a']['content']}

### **Post 3B: {content['categories']['category_3']['posts']['post_3b']['type']}**
{content['categories']['category_3']['posts']['post_3b']['content']}

### **Post 3C: {content['categories']['category_3']['posts']['post_3c']['type']}**
{content['categories']['category_3']['posts']['post_3c']['content']}

## **Category 4: {content['categories']['category_4']['title']}**

### **Post 4A: {content['categories']['category_4']['posts']['post_4a']['type']}**
{content['categories']['category_4']['posts']['post_4a']['content']}

### **Post 4B: {content['categories']['category_4']['posts']['post_4b']['type']}**
{content['categories']['category_4']['posts']['post_4b']['content']}

### **Post 4C: {content['categories']['category_4']['posts']['post_4c']['type']}**
{content['categories']['category_4']['posts']['post_4c']['content']}

---

{content['optimization_notes']}
"""
        return example_text
        
    except Exception as e:
        print(f"Warning: Could not load example from JSON: {e}")
        return "No example available."

def call_claude_api(prompt, config):
    """Call Claude API using urllib"""
    try:
        # Prepare the request
        url = "https://api.anthropic.com/v1/messages"
        
        data = {
            "model": config['model'],
            "max_tokens": config['max_tokens'],
            "temperature": config['temperature'],
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        # Convert to JSON
        json_data = json.dumps(data).encode('utf-8')
        
        # Create request
        req = urllib.request.Request(url)
        req.add_header('Content-Type', 'application/json')
        req.add_header('x-api-key', config['anthropic_api_key'])
        req.add_header('anthropic-version', '2023-06-01')
        
        print("Calling Claude API...")
        
        # Make the request
        with urllib.request.urlopen(req, json_data) as response:
            response_data = json.loads(response.read().decode('utf-8'))
            
        # Extract the content
        if 'content' in response_data and len(response_data['content']) > 0:
            return response_data['content'][0]['text']
        else:
            print("Error: Unexpected API response format")
            print("Response:", response_data)
            return None
            
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.reason}")
        error_body = e.read().decode('utf-8')
        print(f"Error details: {error_body}")
        return None
    except Exception as e:
        print(f"Error calling Claude API: {e}")
        return None

def generate_twitter_content(input_content, system_prompt, example, config):
    """Generate Twitter content using Claude API"""
    # Construct the full prompt
    full_prompt = f"""
{system_prompt}

{example}

---

**INPUT CONTENT TO TRANSFORM:**

MESSAGE HOUSE:
{input_content.get('message_house.md', 'Not available')}

BRAND PERSONA:
{input_content.get('brand_side_persona.md', 'Not available')}

CUSTOMER PERSONA:
{input_content.get('customer_side_persona.md', 'Not available')}

KEYWORDS BANK:
{input_content.get('keywords_bank.md', 'Not available')}

TESTIMONIALS:
{input_content.get('testimonials.md', 'Not available')}

---

**INSTRUCTIONS:**
Transform the above input content into Twitter content following the exact structure and quality demonstrated in the example. Create 12 Twitter posts across 4 categories that align with the brand messaging, customer insights, and strategic keywords. Maintain the platform authenticity and engagement potential shown in the 8.2/10 example.

Generate the Twitter content now:
"""

    return call_claude_api(full_prompt, config)

def main():
    """
    Main execution function with project-aware paths
    """
    print("Twitter Content Generator Starting...")
    
    # Get project-aware paths
    paths = get_project_paths()
    input_dir = paths["input_dir"]
    output_dir = paths["output_dir"]
    system_assets_dir = paths["system_assets_dir"]
    
    print("Twitter Content Generation Demo")
    print("=" * 50)
    
    # Check if input directory exists
    if not input_dir.exists():
        print(f"[FAIL] Input directory not found: {input_dir}")
        return
    
    # Find and map input files
    print("\nDetecting input files...")
    file_mapping = find_input_files(input_dir)
    
    # Check for required files - with New Brand Mode fallback
    required_core_files = ['message_house.md', 'brand_side_persona.md', 'keywords_bank.md', 'testimonials.md']
    missing_core = [f for f in required_core_files if f not in file_mapping]
    
    if missing_core:
        print(f"\n[FAIL] Missing required files: {missing_core}")
        print("Please ensure all required input files are in the 1_input/ directory")
        return
    
    # Handle New Brand Mode: use brand_side_persona for customer_side_persona if not available
    if 'customer_side_persona.md' not in file_mapping:
        print(">>> NEW BRAND MODE: Customer reviews not available")
        print(">>> Using brand_side_persona as customer insights source")
        file_mapping['customer_side_persona.md'] = file_mapping['brand_side_persona.md']
    
    # Load input content
    print("\nLoading input content...")
    input_content = load_input_content(file_mapping)
    
    # Load system prompt
    system_prompt_path = system_assets_dir / "system_prompt.md"
    try:
        with open(system_prompt_path, 'r', encoding='utf-8') as f:
            system_prompt = f.read()
        print(f"[OK] Loaded system prompt ({len(system_prompt)} chars)")
    except Exception as e:
        print(f"[FAIL] Error loading system prompt: {e}")
        return
    
    # Show successful file mapping
    print("\nFile mapping successful:")
    for generic_name, file_path in file_mapping.items():
        print(f"  {generic_name} -> {os.path.basename(file_path)}")
    
    print(f"\nTotal input content: {sum(len(content) for content in input_content.values())} characters")
    
    # Load configuration for API call
    print("\nLoading configuration...")
    config_path = Path(__file__).parent.parent / "config.json"
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except Exception as e:
        print(f"[FAIL] Error loading config: {e}")
        return
    
    # Load example
    print("Loading example...")
    example = load_example_from_json()
    
    # Generate Twitter content using Claude API
    print("\nGenerating Twitter content...")
    print("This may take 30-60 seconds for comprehensive analysis...")
    generated_content = generate_twitter_content(input_content, system_prompt, example, config)
    
    if not generated_content:
        print("[FAIL] Content generation failed")
        return
    
    # Save output
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"twitter_posts_{timestamp}.md"
    output_path = output_dir / output_filename
    
    # Ensure output directory exists
    output_dir.mkdir(exist_ok=True)
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(generated_content)
        print(f"[SUCCESS] Twitter content saved to: {output_filename}")
        print(f"Full path: {output_path}")
        
    except Exception as e:
        print(f"[FAIL] Error saving content: {e}")
        return
    
    print(f"""
=== Generation Complete ===
Review the output in: {output_path}
Use scripts/evaluate.py to score and provide feedback
""")

if __name__ == "__main__":
    main()