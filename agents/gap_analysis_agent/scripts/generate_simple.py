#!/usr/bin/env python3
"""
Simple Gap Analysis Generator Script (No external dependencies)

This script reads two persona files (brand-side and customer-side), applies the Strategic Gap Analysis Framework,
then uses Claude API to generate a comprehensive gap analysis report.
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

def identify_file_types(input_dir):
    """Identify brand and customer persona files"""
    md_files = list(input_dir.glob("*.md"))
    
    if len(md_files) != 2:
        print(f"Error: Expected exactly 2 .md files, found {len(md_files)}")
        print("Please ensure you have exactly one brand persona file and one customer persona file.")
        return None, None
    
    brand_file = None
    customer_file = None
    
    # Try to identify files by name patterns
    for file in md_files:
        filename = file.name.lower()
        if any(keyword in filename for keyword in ['brand', 'message', 'house']):
            brand_file = file
        elif any(keyword in filename for keyword in ['review', 'customer', 'real']):
            customer_file = file
    
    # If we couldn't identify by name, ask user to rename or use alphabetical order
    if not brand_file or not customer_file:
        sorted_files = sorted(md_files, key=lambda f: f.name)
        print(f"Warning: Could not identify files by name. Using alphabetical order:")
        print(f"Brand file: {sorted_files[0].name}")
        print(f"Customer file: {sorted_files[1].name}")
        brand_file = sorted_files[0]
        customer_file = sorted_files[1]
    
    return brand_file, customer_file

def format_personas_for_analysis(brand_content, customer_content, brand_filename, customer_filename):
    """Format persona data for gap analysis"""
    formatted_content = f"""**PERSONA DATA FOR GAP ANALYSIS:**

### **BRAND-SIDE PERSONAS** (Source: {brand_filename})

{brand_content}

---

### **CUSTOMER-SIDE PERSONAS** (Source: {customer_filename})

{customer_content}

---

**ANALYSIS TASK:**
Apply the Strategic Gap Analysis Framework to identify and prioritize gaps between brand assumptions and customer reality across the 5 key features:

1. **Income & Price**: Financial reality and cost attitudes
2. **Primary Motivation**: Core job customers hire product to do
3. **Lifestyle**: Daily activities and self-perception
4. **Product Experience**: Direct sensory interaction with product
5. **Key Pain Points**: Specific frustrations driving solution search

Follow the 4-step methodology:
- Step 1: Extract data into structured comparison
- Step 2: Identify thematic patterns for each feature
- Step 3: Quantify differences with percentages
- Step 4: Apply gap statement template and prioritize by business impact
"""
    
    return formatted_content

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
                if overall_score >= 8.0 and 'gap_analysis_content' in example_data:
                    content = example_data['gap_analysis_content']
                    
                    # Get improvement insights from detailed scores
                    insights = []
                    if 'detailed_scores' in example_data:
                        for criteria, details in example_data['detailed_scores'].items():
                            if isinstance(details, dict) and 'comments' in details:
                                insights.append(f"- {criteria.replace('_', ' ').title()}: {details['comments']}")
                    
                    example_text = f"""
**HIGH-QUALITY EXAMPLE (Score: {overall_score}/10):**

{content['generated_report']}

**Why this scored {overall_score}/10:**
{chr(10).join(insights) if insights else "High-quality gap analysis with systematic methodology and quantitative evidence"}
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
                if 'gap_analysis_content' in example_data:
                    content = example_data['gap_analysis_content']
                    return f"""
**EXAMPLE GAP ANALYSIS REPORT:**

{content['generated_report']}

This example demonstrates the systematic methodology and business-focused prioritization we're targeting.
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

def generate_gap_analysis(persona_data, system_prompt, example, config):
    """Generate gap analysis using Claude API"""
    # Construct the full prompt
    full_prompt = f"""
{system_prompt}

{example}

---

{persona_data}

---

**INSTRUCTIONS:**
Apply the Strategic Gap Analysis Framework to the persona data above. Follow the 4-step methodology exactly:

1. Extract data into 5-feature comparison table
2. Identify thematic patterns for brand vs customer
3. Quantify differences with actual percentages
4. Generate prioritized gap statements using the exact template

Generate the complete Strategic Gap Analysis Report now following the required output structure.
"""

    return call_claude_api(full_prompt, config)

def save_output(content, output_dir):
    """Save generated content to unlabeled folder"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"gap_analysis_{timestamp}.md"
    output_path = output_dir / filename
    
    try:
        # Ensure output directory exists
        output_dir.mkdir(exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Gap analysis saved to: {output_path}")
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
    print("Strategic Gap Analysis Generator Starting...")
    
    # Get project-aware paths
    paths = get_project_paths()
    input_dir = paths["input_dir"]
    system_assets_dir = paths["system_assets_dir"]
    output_dir = paths["output_dir"]
    
    system_prompt_file = system_assets_dir / "system_prompt.md"
    
    # Identify brand and customer files
    brand_file, customer_file = identify_file_types(input_dir)
    if not brand_file or not customer_file:
        sys.exit(1)
    
    print(f"Brand personas: {brand_file.name}")
    print(f"Customer personas: {customer_file.name}")
    
    # Load configuration
    print("Loading configuration...")
    config = load_config()
    
    # Load persona files
    print("Loading brand personas...")
    brand_content = load_file(brand_file)
    if not brand_content:
        sys.exit(1)
    
    print("Loading customer personas...")
    customer_content = load_file(customer_file)
    if not customer_content:
        sys.exit(1)
    
    # Format for analysis
    persona_data = format_personas_for_analysis(brand_content, customer_content, brand_file.name, customer_file.name)
    
    print("Loading system prompt...")
    system_prompt = load_file(system_prompt_file)
    if not system_prompt:
        sys.exit(1)
    
    print("Loading example...")
    example = load_example_from_json()
    
    # Generate gap analysis
    print("Generating strategic gap analysis...")
    generated_content = generate_gap_analysis(persona_data, system_prompt, example, config)
    if not generated_content:
        sys.exit(1)
    
    # Save output
    print("Saving output...")
    output_path = save_output(generated_content, output_dir)
    if not output_path:
        sys.exit(1)
    
    print(f"""
SUCCESS! Strategic Gap Analysis generated successfully.

Brand Input: {brand_file.name}
Customer Input: {customer_file.name}
Output: {output_path.name}
Location: 3_unlabeled/

Next steps:
1. Review the generated gap analysis in 3_unlabeled/
2. Evaluate and score using scripts/evaluate.py
3. Use insights for strategic business decisions
""")

if __name__ == "__main__":
    main()