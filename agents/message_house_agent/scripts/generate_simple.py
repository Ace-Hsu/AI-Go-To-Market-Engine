#!/usr/bin/env python3
"""
Simple Message House Generator Script (No external dependencies)

This script reads a Q&A file, combines it with system prompts and examples,
then uses Claude API to generate a professional message house document.
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
                if overall_score >= 8.0 and 'message_house_content' in example_data:
                    content = example_data['message_house_content']
                    
                    # Get improvement insights from detailed scores
                    insights = []
                    if 'detailed_scores' in example_data:
                        for criteria, details in example_data['detailed_scores'].items():
                            if isinstance(details, dict) and 'comments' in details:
                                insights.append(f"- {criteria.replace('_', ' ').title()}: {details['comments']}")
                    
                    example_text = f"""
**HIGH-QUALITY EXAMPLE (Score: {overall_score}/10):**

### **{content['brand_name']}: Official Message House**

This document is the single source of truth for all marketing, sales, and product messaging.

### **The Roof: Our Core Message**

**Positioning Statement:**
**"{content['roof_core_message']['positioning_statement']}"**

**Brand Tagline:**
**"{content['roof_core_message']['brand_tagline']}"**

### **The Pillars: How We Deliver on Our Promise**

| {content['pillars_value_propositions']['pillar_1']['title']} | {content['pillars_value_propositions']['pillar_2']['title']} | {content['pillars_value_propositions']['pillar_3']['title']} |
| :---- | :---- | :---- |
| {content['pillars_value_propositions']['pillar_1']['description']} | {content['pillars_value_propositions']['pillar_2']['description']} | {content['pillars_value_propositions']['pillar_3']['description']} |

### **The Foundation: Proof Points & Audience Insights**

#### **Audience & Pain Points**
* **Bullseye User:** {content['foundation_supporting_evidence']['audience_insights']['bullseye_user']}
* **Acute Pain:** {content['foundation_supporting_evidence']['audience_insights']['acute_pain']}
* **The "Worst Day" Scenario:** {content['foundation_supporting_evidence']['audience_insights']['worst_day_scenario']}

#### **Competitive Landscape**
* **True Competitor:** {content['foundation_supporting_evidence']['competitive_landscape']['true_competitor']}
* **"Good Enough" Alternative:** {content['foundation_supporting_evidence']['competitive_landscape']['good_enough_alternative']}
* **Our Contrarian View:** {content['foundation_supporting_evidence']['competitive_landscape']['contrarian_view']}

**Why this scored {overall_score}/10:**
{chr(10).join(insights) if insights else "High-quality strategic messaging and positioning"}
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
                if 'message_house_content' in example_data:
                    content = example_data['message_house_content']
                    return f"""
**EXAMPLE MESSAGE HOUSE:**

### **{content['brand_name']}: Official Message House**

**Positioning Statement:**
"{content['roof_core_message']['positioning_statement']}"

**Brand Tagline:**
"{content['roof_core_message']['brand_tagline']}"
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

def generate_message_house(qa_content, system_prompt, example, config):
    """Generate message house using Claude API"""
    # Construct the full prompt
    full_prompt = f"""
{system_prompt}

{example}

---

**INPUT Q&A TO TRANSFORM:**

{qa_content}

---

**INSTRUCTIONS:**
Transform the above Q&A into a complete message house following the EXACT structure shown in the example. You MUST follow these strict rules:

1. **ROOF CORE MESSAGE:** Use Question 12's positioning statement as the EXACT positioning statement. Use Question 11's five-word promise as the EXACT brand tagline.

2. **STRUCTURE:** Follow the exact "Roof/Pillars/Foundation" format with proper markdown headers:
   - ### **[Brand]: Official Message House**
   - ### **The Roof: Our Core Message**
   - ### **The Pillars: How We Deliver on Our Promise**
   - ### **The Foundation: Proof Points & Audience Insights**

3. **CONTENT MAPPING:** Extract insights from the Q&A and map them to the appropriate sections. Use the emotional depth and specific scenarios from the answers.

4. **QUALITY:** Maintain the strategic depth and emotional resonance shown in the high-scoring example.

Generate the message house now following this EXACT structure:
"""

    return call_claude_api(full_prompt, config)

def save_output(content, output_dir):
    """Save generated content to unlabeled folder"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"messagehouse_{timestamp}.md"
    output_path = output_dir / filename
    
    try:
        # Ensure output directory exists
        output_dir.mkdir(exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Message house saved to: {output_path}")
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
            # New project-based structure
            return {
                "input_dir": Path(__file__).parent.parent / "1_input" / project,
                "system_assets_dir": Path(__file__).parent.parent / "2_system_assets" / project,
                "output_dir": Path(__file__).parent.parent / "3_unlabeled" / project
            }
        else:
            # Legacy structure (backward compatibility)
            return {
                "input_dir": Path(__file__).parent.parent / "1_input",
                "system_assets_dir": Path(__file__).parent.parent / "2_system_assets",
                "output_dir": Path(__file__).parent.parent / "3_unlabeled"
            }
    except:
        # Fallback to legacy structure
        return {
            "input_dir": Path(__file__).parent.parent / "1_input",
            "system_assets_dir": Path(__file__).parent.parent / "2_system_assets",
            "output_dir": Path(__file__).parent.parent / "3_unlabeled"
        }

def main():
    """Main execution function"""
    print("Message House Generator Starting...")
    
    # Get project-aware paths
    paths = get_project_paths()
    input_dir = paths["input_dir"]
    system_assets_dir = paths["system_assets_dir"]
    output_dir = paths["output_dir"]
    
    # Find input file (flexible detection)
    input_files = list(input_dir.glob("*.md"))
    if not input_files:
        print(f"Error: No input files found in {input_dir}")
        print("Available directories:")
        for d in input_dir.parent.iterdir():
            if d.is_dir():
                print(f"  - {d.name}")
        sys.exit(1)
    
    # Use the first markdown file found (or most recent)
    input_file = max(input_files, key=lambda f: f.stat().st_mtime)
    system_prompt_file = system_assets_dir / "system_prompt.md"
    
    # Check if files exist (input file already validated above)
    print(f"Using input file: {input_file.name}")
    
    # Load configuration
    print("Loading configuration...")
    config = load_config()
    
    # Load input files
    print("Loading input Q&A...")
    qa_content = load_file(input_file)
    if not qa_content:
        sys.exit(1)
    
    print("Loading system prompt...")
    system_prompt = load_file(system_prompt_file)
    if not system_prompt:
        sys.exit(1)
    
    print("Loading example...")
    example = load_example_from_json()
    
    # Generate message house
    print("Generating message house...")
    generated_content = generate_message_house(qa_content, system_prompt, example, config)
    if not generated_content:
        sys.exit(1)
    
    # Save output
    print("Saving output...")
    output_path = save_output(generated_content, output_dir)
    if not output_path:
        sys.exit(1)
    
    print(f"""
SUCCESS! Message house generated successfully.

Input: {input_file.name}
Output: {output_path.name}
Location: {output_path.parent.name}/

Next steps:
1. Review the generated message house in {output_path.parent.name}/
2. Evaluate and score it (manual process)
3. Move to 4_labeled_md/ and 5_labeled_json/ when reviewed
""")

if __name__ == "__main__":
    main()