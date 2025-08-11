#!/usr/bin/env python3
"""
Simple Testimonial Generator Script (No external dependencies)

This script reads brand persona, customer persona, and keywords bank files,
then uses Claude API to generate authentic marketing testimonials.
"""

import json
import os
import sys
import urllib.request
import urllib.parse
from datetime import datetime
from pathlib import Path

def load_config():
    """Load configuration from config.json"""
    config_path = Path(__file__).parent.parent / "config.json"
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print("Error: config.json not found. Please create it with your API key.")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error: config.json is not valid JSON.")
        sys.exit(1)

def load_file(file_path):
    """Load content from a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
        return None
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

def find_input_files(input_dir):
    """Find required input files from upstream agents"""
    input_files = {}
    
    # Look for all .md files
    md_files = list(input_dir.glob("*.md"))
    
    for file in md_files:
        filename = file.name.lower()
        if "userstories" in filename:
            if "reviews" in filename:
                input_files['customer_persona'] = file
            else:
                input_files['brand_persona'] = file
        elif "keywords" in filename or "expansion" in filename:
            input_files['keywords_bank'] = file
    
    return input_files

def load_example_from_json():
    """Load ALL examples from labeled JSON for system prompt (Example Map)"""
    example_folder = Path(__file__).parent.parent / "5_labeled_json"
    
    try:
        # Get all JSON files in the folder
        json_files = list(example_folder.glob("*.json"))
        
        if not json_files:
            print("Warning: No example files found in 5_labeled_json folder")
            return "No examples available."
        
        examples_text = []
        print(f"Loading {len(json_files)} evaluation files for example map...")
        
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    example_data = json.load(f)
                
                # Only use high-quality examples with actual content
                overall_score = example_data.get('overall_score', 0)
                if overall_score >= 8.0 and 'testimonials_content' in example_data:
                    content = example_data['testimonials_content']
                    
                    # Get improvement insights from detailed scores
                    insights = []
                    if 'detailed_scores' in example_data:
                        for criteria, details in example_data['detailed_scores'].items():
                            if isinstance(details, dict) and 'comments' in details:
                                insights.append(f"- {criteria.replace('_', ' ').title()}: {details['comments']}")
                    
                    example_text = f"""
**HIGH-QUALITY EXAMPLE (Score: {overall_score}/10):**

{content}

**Why this scored {overall_score}/10:**
{chr(10).join(insights) if insights else "High-quality testimonials with perfect strategic messaging and authentic customer voice"}
"""
                    examples_text.append(example_text)
                    
            except Exception as e:
                print(f"Warning: Could not parse {json_file.name}: {e}")
                continue
        
        if not examples_text:
            # Fallback to any available file if no high-quality examples found
            try:
                with open(json_files[0], 'r', encoding='utf-8') as f:
                    example_data = json.load(f)
                if 'testimonials_content' in example_data:
                    content = example_data['testimonials_content']
                    return f"""
**EXAMPLE TESTIMONIALS:**

{content}

This example demonstrates the perfect blending of strategic messaging with authentic customer voice patterns.
"""
            except:
                pass
            
            return "No suitable examples available."
        
        # Combine all high-quality examples (limit to top 3)
        combined_examples = "\n\n" + "="*60 + "\n\n".join(examples_text[:3])
        print(f"Loaded {len(examples_text)} high-quality examples (8.0+ score) for learning")
        
        return combined_examples
        
    except Exception as e:
        print(f"Warning: Could not load examples from folder: {e}")
        return "No examples available."

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
        req.add_header('x-api-key', config['api_key'])
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

def generate_testimonials(brand_persona, customer_persona, keywords_bank, system_prompt, example, config):
    """Generate testimonials using Claude API"""
    # Construct the full prompt
    full_prompt = f"""
{system_prompt}

{example}

---

**INPUT ASSETS TO BLEND:**

**BRAND PERSONA (Strategic Messaging):**
{brand_persona}

---

**CUSTOMER PERSONA (Authentic Voice & Context):**
{customer_persona}

---

**KEYWORDS BANK (Customer Voice Patterns - Vector G):**
{keywords_bank}

---

**INSTRUCTIONS:**
Create authentic marketing testimonials that perfectly blend strategic messaging with customer voice patterns. Follow the blending examples in the system prompt to create testimonials that sound like real customers while strategically reinforcing brand positioning.

Generate multiple testimonial formats (short, medium, long-form) with diverse customer profiles. Each testimonial should feel authentic and be immediately usable in marketing campaigns.

Generate the testimonials now:
"""

    return call_claude_api(full_prompt, config)

def save_output(content, output_dir):
    """Save generated content to unlabeled folder"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"testimonials_{timestamp}.md"
    output_path = output_dir / filename
    
    try:
        # Ensure output directory exists
        output_dir.mkdir(exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Testimonials saved to: {output_path}")
        return output_path
    except Exception as e:
        print(f"Error saving output: {e}")
        return None

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

def main():
    """Main execution function"""
    print("Testimonial Generator Starting...")
    
    # Get project-aware paths
    paths = get_project_paths()
    input_dir = paths["input_dir"]
    system_assets_dir = paths["system_assets_dir"]
    output_dir = paths["output_dir"]
    
    system_prompt_file = system_assets_dir / "system_prompt.md"
    
    # Find required input files
    input_files = find_input_files(input_dir)
    
    # Check for required files - with New Brand Mode fallback
    if 'keywords_bank' not in input_files:
        print("Error: Missing keywords_bank file. Please ensure Agent 5 has completed.")
        print("Expected: keywords_bank_expansion_*.md (from Agent 5)")
        sys.exit(1)
    
    if 'brand_persona' not in input_files:
        print("Error: Missing brand_persona file. Please ensure Agent 2 has completed.")
        print("Expected: userstories_*.md (from Agent 2)")
        sys.exit(1)
    
    # Handle New Brand Mode: use brand_persona for customer_persona if not available
    if 'customer_persona' not in input_files:
        print(">>> NEW BRAND MODE: Customer reviews not available")
        print(">>> Using brand_persona as customer insights source")
        input_files['customer_persona'] = input_files['brand_persona']
    
    print(f"Using brand persona: {input_files['brand_persona'].name}")
    print(f"Using customer persona: {input_files['customer_persona'].name}")
    print(f"Using keywords bank: {input_files['keywords_bank'].name}")
    
    # Load configuration
    print("Loading configuration...")
    config = load_config()
    
    # Load input files
    print("Loading brand persona...")
    brand_persona = load_file(input_files['brand_persona'])
    if not brand_persona:
        sys.exit(1)
    
    print("Loading customer persona...")
    customer_persona = load_file(input_files['customer_persona'])
    if not customer_persona:
        sys.exit(1)
    
    print("Loading keywords bank...")
    keywords_bank = load_file(input_files['keywords_bank'])
    if not keywords_bank:
        sys.exit(1)
    
    print("Loading system prompt...")
    system_prompt = load_file(system_prompt_file)
    if not system_prompt:
        sys.exit(1)
    
    print("Loading example...")
    example = load_example_from_json()
    
    # Generate testimonials
    print("Generating testimonials...")
    generated_content = generate_testimonials(
        brand_persona, customer_persona, keywords_bank, 
        system_prompt, example, config
    )
    if not generated_content:
        sys.exit(1)
    
    # Save output
    print("Saving output...")
    output_path = save_output(generated_content, output_dir)
    if not output_path:
        sys.exit(1)
    
    print(f"""
SUCCESS! Testimonials generated successfully.

Inputs Used:
- Brand Persona: {input_files['brand_persona'].name}
- Customer Persona: {input_files['customer_persona'].name}  
- Keywords Bank: {input_files['keywords_bank'].name}

Output: {output_path.name}
Location: 3_unlabeled/

Next steps:
1. Review the generated testimonials in 3_unlabeled/
2. Evaluate and score them using scripts/evaluate.py
3. Use high-scoring testimonials in marketing campaigns
""")

if __name__ == "__main__":
    main()