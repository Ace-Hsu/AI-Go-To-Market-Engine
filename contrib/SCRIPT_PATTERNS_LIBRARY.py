#!/usr/bin/env python3
"""
Script Patterns Library - Copy-Paste Code Templates

This file contains all standard code patterns used across agents.
Copy these patterns directly into your new agent scripts.

DO NOT modify the foundation patterns - only customize the business logic sections.
"""

# =============================================================================
# PATTERN 1: STANDARD IMPORTS (Required in ALL agents)
# =============================================================================

import json
import os
import sys
import urllib.request
import urllib.parse
from datetime import datetime
from pathlib import Path

# =============================================================================
# PATTERN 2: CONFIGURATION LOADING (Universal - DO NOT MODIFY)
# =============================================================================

def load_config():
    """Load configuration from config.json - STANDARD PATTERN"""
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

# =============================================================================
# PATTERN 3: FILE LOADING (Universal - DO NOT MODIFY)
# =============================================================================

def load_file(file_path):
    """Load content from a file - STANDARD PATTERN"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
        return None
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

# =============================================================================
# PATTERN 4: PROJECT PATH HANDLING (Universal - DO NOT MODIFY)
# =============================================================================

def get_project_paths(config_file="config.json"):
    """Get project-specific paths from configuration - STANDARD PATTERN"""
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

# =============================================================================
# PATTERN 5: CLAUDE API CALLING (Universal - DO NOT MODIFY)
# =============================================================================

def call_claude_api(prompt, config):
    """Call Claude API using urllib - STANDARD PATTERN"""
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

# =============================================================================
# PATTERN 6: OUTPUT SAVING (Universal - DO NOT MODIFY)
# =============================================================================

def save_output(content, output_dir, agent_prefix="content"):
    """Save generated content to unlabeled folder - STANDARD PATTERN"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{agent_prefix}_{timestamp}.md"
    output_path = output_dir / filename
    
    try:
        # Ensure output directory exists
        output_dir.mkdir(exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Content saved to: {output_path}")
        return output_path
    except Exception as e:
        print(f"Error saving output: {e}")
        return None

# =============================================================================
# PATTERN 7: ITERATE SYSTEM INTEGRATION (Optional - Modify Example Format Only)
# =============================================================================

def load_example_from_json(content_key="content"):
    """
    Load ALL examples from labeled JSON for system prompt (Example Map)
    
    CUSTOMIZE: Modify the example_text formatting section for your business logic
    DO NOT MODIFY: File loading and filtering logic
    """
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
                if overall_score >= 8.0 and content_key in example_data:
                    content = example_data[content_key]
                    
                    # Get improvement insights from detailed scores
                    insights = []
                    if 'detailed_scores' in example_data:
                        for criteria, details in example_data['detailed_scores'].items():
                            if isinstance(details, dict) and 'comments' in details:
                                insights.append(f"- {criteria.replace('_', ' ').title()}: {details['comments']}")
                    
                    # CUSTOMIZE THIS SECTION FOR YOUR BUSINESS LOGIC
                    example_text = f"""
**HIGH-QUALITY EXAMPLE (Score: {overall_score}/10):**

[FORMAT YOUR EXAMPLE CONTENT HERE - BUSINESS LOGIC SPECIFIC]
{content}

**Why this scored {overall_score}/10:**
{chr(10).join(insights) if insights else "High-quality content"}
"""
                    examples_text.append(example_text)
                    
            except Exception as e:
                print(f"Warning: Could not parse {json_file.name}: {e}")
                continue
        
        if not examples_text:
            return "No suitable examples available."
        
        # Combine all high-quality examples (limit to top 3)
        combined_examples = "\n\n" + "="*60 + "\n\n".join(examples_text[:3])
        print(f"Loaded {len(examples_text)} high-quality examples (8.0+ score) for learning")
        
        return combined_examples
        
    except Exception as e:
        print(f"Warning: Could not load examples from folder: {e}")
        return "No examples available."

# =============================================================================
# PATTERN 8: INPUT FILE DETECTION (Customize for Your Requirements)
# =============================================================================

def find_input_files(input_dir, pattern="*.md"):
    """
    Find input files in the input directory
    
    CUSTOMIZE: Modify pattern and selection logic for your business logic
    STANDARD: Error handling and directory checking
    """
    input_files = list(input_dir.glob(pattern))
    
    if not input_files:
        print(f"Error: No input files found in {input_dir}")
        print("Available directories:")
        for d in input_dir.parent.iterdir():
            if d.is_dir():
                print(f"  - {d.name}")
        return None
    
    # Use the most recent file (or customize selection logic)
    selected_file = max(input_files, key=lambda f: f.stat().st_mtime)
    print(f"Using input file: {selected_file.name}")
    
    return selected_file

# =============================================================================
# PATTERN 9: MAIN EXECUTION TEMPLATE (Customize Business Logic Sections)
# =============================================================================

def main_execution_template(agent_name, agent_prefix, content_key="content"):
    """
    Main execution template - STANDARD STRUCTURE
    
    CUSTOMIZE: Input file detection, content generation logic
    DO NOT MODIFY: Path handling, API calling, file saving structure
    """
    print(f"{agent_name} Generator Starting...")
    
    # Get project-aware paths (STANDARD)
    paths = get_project_paths()
    input_dir = paths["input_dir"]
    system_assets_dir = paths["system_assets_dir"]
    output_dir = paths["output_dir"]
    
    # Find input files (CUSTOMIZE PATTERN AS NEEDED)
    input_file = find_input_files(input_dir, "*.md")  # Modify pattern as needed
    if not input_file:
        sys.exit(1)
    
    system_prompt_file = system_assets_dir / "system_prompt.md"
    
    # Load configuration (STANDARD)
    print("Loading configuration...")
    config = load_config()
    
    # Load input files (STANDARD)
    print("Loading input content...")
    input_content = load_file(input_file)
    if not input_content:
        sys.exit(1)
    
    print("Loading system prompt...")
    system_prompt = load_file(system_prompt_file)
    if not system_prompt:
        sys.exit(1)
    
    print("Loading examples...")
    example = load_example_from_json(content_key)
    
    # Generate content (CUSTOMIZE THIS FUNCTION)
    print("Generating content...")
    generated_content = generate_content_custom(input_content, system_prompt, example, config)
    if not generated_content:
        sys.exit(1)
    
    # Save output (STANDARD)
    print("Saving output...")
    output_path = save_output(generated_content, output_dir, agent_prefix)
    if not output_path:
        sys.exit(1)
    
    # Success message (STANDARD)
    print(f"""
SUCCESS! Content generated successfully.

Input: {input_file.name}
Output: {output_path.name}
Location: {output_path.parent.name}/

Next steps:
1. Review the generated content in {output_path.parent.name}/
2. Evaluate and score it using scripts/evaluate.py
3. Move to 4_labeled_md/ and 5_labeled_json/ when reviewed
""")

# =============================================================================
# PATTERN 10: CONTENT GENERATION TEMPLATE (Customize Entirely)
# =============================================================================

def generate_content_custom(input_content, system_prompt, example, config):
    """
    Generate content using Claude API - CUSTOMIZE THIS ENTIRE FUNCTION
    
    This is where your business logic goes. Modify the prompt construction
    and instructions to match your specific requirements.
    """
    # CUSTOMIZE: Construct your specific prompt
    full_prompt = f"""
{system_prompt}

{example}

---

**INPUT TO TRANSFORM:**

{input_content}

---

**INSTRUCTIONS:**
[YOUR BUSINESS LOGIC SPECIFIC INSTRUCTIONS HERE]
- Transform the input according to your requirements
- Follow your specific output format
- Apply your quality standards
- Include your specific content elements

Generate the content now:
"""

    return call_claude_api(full_prompt, config)

# =============================================================================
# PATTERN 11: EVALUATION CRITERIA TEMPLATE (Customize for Your Business Logic)
# =============================================================================

# Standard evaluation criteria structure - CUSTOMIZE VALUES
EVALUATION_CRITERIA_TEMPLATE = {
    "criteria_1_name": {
        "weight": 0.25,
        "description": "Description of what this criteria evaluates"
    },
    "criteria_2_name": {
        "weight": 0.20, 
        "description": "Description of what this criteria evaluates"
    },
    "criteria_3_name": {
        "weight": 0.20,
        "description": "Description of what this criteria evaluates"
    },
    "criteria_4_name": {
        "weight": 0.20,
        "description": "Description of what this criteria evaluates"
    },
    "criteria_5_name": {
        "weight": 0.15,
        "description": "Description of what this criteria evaluates"
    }
}

# Standard tag sets - CUSTOMIZE VALUES
IMPROVEMENT_TAGS_TEMPLATE = [
    "improvement_area_1", "improvement_area_2", "improvement_area_3",
    "improvement_area_4", "improvement_area_5"
]

STRENGTH_TAGS_TEMPLATE = [
    "strength_area_1", "strength_area_2", "strength_area_3", 
    "strength_area_4", "strength_area_5"
]

# =============================================================================
# PATTERN 12: CONFIGURATION FILE TEMPLATE (Copy Exactly)
# =============================================================================

CONFIG_JSON_TEMPLATE = {
    "anthropic_api_key": "your_api_key_here",
    "model": "claude-3-5-sonnet-20241022",
    "max_tokens": 2000,
    "temperature": 0.3,
    "current_project": None
}

# =============================================================================
# USAGE EXAMPLES
# =============================================================================

"""
EXAMPLE 1: Basic Agent with Standard Patterns

```python
#!/usr/bin/env python3
from script_patterns_library import *

def generate_my_content(input_content, system_prompt, example, config):
    # Your business logic here
    full_prompt = f"{system_prompt}\n\n{input_content}\n\nGenerate [YOUR_OUTPUT_TYPE]:"
    return call_claude_api(full_prompt, config)

def main():
    main_execution_template("My Agent", "myagent", "my_content_key")

if __name__ == "__main__":
    main()
```

EXAMPLE 2: Agent with Custom Input Detection

```python
#!/usr/bin/env python3
from script_patterns_library import *

def find_my_input_files(input_dir):
    # Custom logic for finding specific input files
    csv_files = list(input_dir.glob("*.csv"))
    if csv_files:
        return max(csv_files, key=lambda f: f.stat().st_mtime)
    return None

def main():
    paths = get_project_paths()
    input_file = find_my_input_files(paths["input_dir"])
    # ... rest of standard flow
```

EXAMPLE 3: Agent with No Iterate System

```python
#!/usr/bin/env python3
from script_patterns_library import *

def main():
    # Standard setup
    paths = get_project_paths()
    config = load_config()
    
    # Skip example loading
    example = "No examples needed for this agent."
    
    # Continue with standard flow
    generated_content = generate_my_content(input_content, system_prompt, example, config)
    save_output(generated_content, paths["output_dir"], "myagent")
```
"""

# =============================================================================
# CUSTOMIZATION CHECKLIST
# =============================================================================

"""
When creating a new agent, customize these sections ONLY:

1. ✅ generate_content_custom() - Your entire business logic
2. ✅ find_input_files() - Your input file requirements  
3. ✅ load_example_from_json() - Your example formatting (if using iterate system)
4. ✅ EVALUATION_CRITERIA_TEMPLATE - Your scoring criteria
5. ✅ IMPROVEMENT_TAGS_TEMPLATE - Your improvement areas
6. ✅ STRENGTH_TAGS_TEMPLATE - Your strength areas
7. ✅ Agent name, prefix, and content key in main()

DO NOT MODIFY these foundation patterns:
- Configuration loading
- Path handling
- API calling
- File saving
- Error handling
- Project structure support
"""

if __name__ == "__main__":
    print("This is a library file - import these patterns into your agent scripts")
    print("See usage examples in the docstring above")