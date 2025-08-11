#!/usr/bin/env python3
"""
Simple User Story Generator Script (No external dependencies)

This script reads a message house file, combines it with system prompts and examples,
then uses Claude API to generate detailed user personas and stories.
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
                if overall_score >= 8.0 and 'user_stories_content' in example_data:
                    content = example_data['user_stories_content']
                    
                    # Get improvement insights from detailed scores
                    insights = []
                    if 'detailed_scores' in example_data:
                        for criteria, details in example_data['detailed_scores'].items():
                            if isinstance(details, dict) and 'comments' in details:
                                insights.append(f"- {criteria.replace('_', ' ').title()}: {details['comments']}")
                    
                    example_text = f"""
**HIGH-QUALITY EXAMPLE (Score: {overall_score}/10):**

{content['generated_personas']}

**Why this scored {overall_score}/10:**
{chr(10).join(insights) if insights else "High-quality user persona development with emotional authenticity"}
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
                if 'user_stories_content' in example_data:
                    content = example_data['user_stories_content']
                    return f"""
**EXAMPLE USER PERSONAS:**

{content['generated_personas']}

This example demonstrates the quality, depth, and emotional authenticity we're targeting.
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

def generate_user_stories(message_house_content, system_prompt, example, config):
    """Generate user stories using Claude API"""
    # Construct the full prompt
    full_prompt = f"""
{system_prompt}

{example}

---

**MESSAGE HOUSE TO TRANSFORM:**

{message_house_content}

---

**INSTRUCTIONS:**
Transform the above message house into detailed user personas following the exact structure and quality demonstrated in the example. Extract customer psychology, pain points, and value propositions to create 5-7 authentic persona profiles. Each persona should have different demographics, emotional states, and relationships with the product.

Generate the user personas now:
"""

    return call_claude_api(full_prompt, config)

def save_output(content, output_dir):
    """Save generated content to unlabeled folder"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"userstories_{timestamp}.md"
    output_path = output_dir / filename
    
    try:
        # Ensure output directory exists
        output_dir.mkdir(exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"User stories saved to: {output_path}")
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
    print("User Story Generator Starting...")
    
    # Get project-aware paths
    paths = get_project_paths()
    input_dir = paths["input_dir"]
    system_assets_dir = paths["system_assets_dir"]
    output_dir = paths["output_dir"]
    
    # Find message house files in input directory
    system_prompt_file = system_assets_dir / "system_prompt.md"
    
    # Find message house files in input directory
    input_files = list(input_dir.glob("*.md"))
    if not input_files:
        print(f"Error: No .md files found in {input_dir}")
        print("Please place a message house document in 1_input/")
        sys.exit(1)
    
    # Use the most recent file
    input_file = max(input_files, key=lambda f: f.stat().st_mtime)
    print(f"Using input file: {input_file.name}")
    
    # Load configuration
    print("Loading configuration...")
    config = load_config()
    
    # Load input files
    print("Loading message house...")
    message_house_content = load_file(input_file)
    if not message_house_content:
        sys.exit(1)
    
    print("Loading system prompt...")
    system_prompt = load_file(system_prompt_file)
    if not system_prompt:
        sys.exit(1)
    
    print("Loading example...")
    example = load_example_from_json()
    
    # Generate user stories
    print("Generating user stories...")
    generated_content = generate_user_stories(message_house_content, system_prompt, example, config)
    if not generated_content:
        sys.exit(1)
    
    # Save output
    print("Saving output...")
    output_path = save_output(generated_content, output_dir)
    if not output_path:
        sys.exit(1)
    
    print(f"""
SUCCESS! User stories generated successfully.

Input: {input_file.name}
Output: {output_path.name}
Location: 3_unlabeled/

Next steps:
1. Review the generated user stories in 3_unlabeled/
2. Evaluate and score them using scripts/evaluate.py
3. Move to 5_labeled_json/ when reviewed for system learning
""")

if __name__ == "__main__":
    main()