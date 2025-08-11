#!/usr/bin/env python3
"""
Message House Generator Script

This script reads a Q&A file, combines it with system prompts and examples,
then uses Claude API to generate a professional message house document.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
import anthropic

def load_config():
    """Load configuration from config.json"""
    config_path = Path(__file__).parent.parent / "config.json"
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print("❌ Error: config.json not found. Please create it with your API key.")
        sys.exit(1)
    except json.JSONDecodeError:
        print("❌ Error: config.json is not valid JSON.")
        sys.exit(1)

def load_file(file_path):
    """Load content from a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ Error: File not found: {file_path}")
        return None
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
        return None

def load_example_from_json():
    """Load the example from labeled JSON for system prompt"""
    example_path = Path(__file__).parent.parent / "5_labeled_json" / "ourjrney_turmeric_001.json"
    try:
        with open(example_path, 'r', encoding='utf-8') as f:
            example_data = json.load(f)
        
        # Extract the message house content for the prompt
        content = example_data['message_house_content']
        
        example_text = f"""
**EXAMPLE OF 8.5/10 QUALITY MESSAGE HOUSE:**

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
"""
        return example_text
        
    except Exception as e:
        print(f"⚠️ Warning: Could not load example from JSON: {e}")
        return "No example available."

def generate_message_house(qa_content, system_prompt, example, config):
    """Generate message house using Claude API"""
    try:
        client = anthropic.Anthropic(api_key=config['anthropic_api_key'])
        
        # Construct the full prompt
        full_prompt = f"""
{system_prompt}

{example}

---

**INPUT Q&A TO TRANSFORM:**

{qa_content}

---

**INSTRUCTIONS:**
Transform the above Q&A into a complete message house following the exact structure and quality demonstrated in the example. Extract insights from each question and map them to the appropriate sections. Maintain the strategic depth and emotional resonance shown in the 8.5/10 example.

Generate the message house now:
"""

        # Call Claude API
        print("🤖 Calling Claude API...")
        response = client.messages.create(
            model=config['model'],
            max_tokens=config['max_tokens'],
            temperature=config['temperature'],
            messages=[
                {
                    "role": "user",
                    "content": full_prompt
                }
            ]
        )
        
        return response.content[0].text
        
    except Exception as e:
        print(f"❌ Error calling Claude API: {e}")
        return None

def save_output(content, output_dir):
    """Save generated content to unlabeled folder"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"messagehouse_{timestamp}.md"
    output_path = output_dir / filename
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Message house saved to: {output_path}")
        return output_path
    except Exception as e:
        print(f"❌ Error saving output: {e}")
        return None

def main():
    """Main execution function"""
    print("🏠 Message House Generator Starting...")
    
    # Set up paths
    script_dir = Path(__file__).parent
    project_dir = script_dir.parent
    
    # File paths
    input_file = project_dir / "1_input" / "Record_ Q&A for Message House Development (Full Transcript) Turmeric 20250710.md"
    system_prompt_file = project_dir / "2_system_assets" / "system_prompt.md"
    output_dir = project_dir / "3_unlabeled"
    
    # Load configuration
    print("📋 Loading configuration...")
    config = load_config()
    
    # Load input files
    print("📖 Loading input Q&A...")
    qa_content = load_file(input_file)
    if not qa_content:
        sys.exit(1)
    
    print("📖 Loading system prompt...")
    system_prompt = load_file(system_prompt_file)
    if not system_prompt:
        sys.exit(1)
    
    print("📖 Loading example...")
    example = load_example_from_json()
    
    # Generate message house
    print("🎯 Generating message house...")
    generated_content = generate_message_house(qa_content, system_prompt, example, config)
    if not generated_content:
        sys.exit(1)
    
    # Save output
    print("💾 Saving output...")
    output_path = save_output(generated_content, output_dir)
    if not output_path:
        sys.exit(1)
    
    print(f"""
✅ SUCCESS! Message house generated successfully.

📁 Input: {input_file.name}
📁 Output: {output_path.name}
📁 Location: 3_unlabeled/

Next steps:
1. Review the generated message house in 3_unlabeled/
2. Evaluate and score it (manual process)
3. Move to 4_labeled_md/ and 5_labeled_json/ when reviewed
""")

if __name__ == "__main__":
    main()