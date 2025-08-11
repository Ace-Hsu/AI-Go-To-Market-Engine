#!/usr/bin/env python3
"""
Website Copy Generator Script

This script generates strategic website copy with homepage logic
using Claude API based on brand strategy inputs.
"""

import json
import os
from pathlib import Path
from datetime import datetime
import anthropic

def load_config():
    """Load configuration from config.json"""
    config_path = Path(__file__).parent.parent / "config.json"
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except Exception as e:
        print(f"Error loading config: {e}")
        return None

def load_system_prompt(config):
    """Load system prompt from file"""
    prompt_path = Path(__file__).parent.parent / config["system_prompt_file"]
    
    try:
        with open(prompt_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error loading system prompt: {e}")
        return None

def load_input_files(config, input_dir=None):
    """Load all input files from 1_input directory - auto-detects file types"""
    if input_dir is None:
        input_dir = Path(__file__).parent.parent / config["input_dir"]
    
    if not input_dir.exists():
        print(f"✗ Input directory not found: {input_dir}")
        return None
    
    # Get all .md files
    md_files = list(input_dir.glob("*.md"))
    
    if len(md_files) < 3:
        print(f"✗ Need at least 3 .md files, found {len(md_files)}")
        print("Required: message house, keywords bank, and testimonials files")
        return None
    
    input_content = {}
    file_types = {
        "message_house": None,
        "keywords": None, 
        "testimonials": None
    }
    
    # Auto-detect file types by content patterns
    for file_path in md_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().lower()
            
            filename = file_path.name
            
            # Detect file type by filename first (more reliable), then content
            filename_lower = filename.lower()
            
            # Priority 1: Exact filename matches
            if "keywords_bank_expansion" in filename_lower:
                file_types["keywords"] = file_path
                input_content["keywords_bank.md"] = open(file_path, 'r', encoding='utf-8').read()
                print(f"[OK] Detected keywords bank: {filename}")
                
            elif "testimonials" in filename_lower:
                file_types["testimonials"] = file_path
                input_content["marketing_testimonials.md"] = open(file_path, 'r', encoding='utf-8').read()
                print(f"[OK] Detected testimonials: {filename}")
                
            elif "messagehouse" in filename_lower:
                file_types["message_house"] = file_path
                input_content["message_house.md"] = open(file_path, 'r', encoding='utf-8').read()
                print(f"[OK] Detected message house: {filename}")
                
            # Priority 2: Content-based detection as fallback
            elif any(keyword in content for keyword in ["message house", "brand strategy", "positioning"]):
                file_types["message_house"] = file_path
                input_content["message_house.md"] = open(file_path, 'r', encoding='utf-8').read()
                print(f"[OK] Detected message house (by content): {filename}")
                
            elif any(keyword in content for keyword in ["keywords", "vocabulary", "expansion"]):
                file_types["keywords"] = file_path
                input_content["keywords_bank.md"] = open(file_path, 'r', encoding='utf-8').read()
                print(f"[OK] Detected keywords bank (by content): {filename}")
                
            elif any(keyword in content for keyword in ["testimonial", "review", "customer voice"]):
                file_types["testimonials"] = file_path
                input_content["marketing_testimonials.md"] = open(file_path, 'r', encoding='utf-8').read()
                print(f"[OK] Detected testimonials (by content): {filename}")
        
        except Exception as e:
            print(f"[ERROR] Error reading {file_path}: {e}")
    
    # Check if we found all required types
    missing_types = [ftype for ftype, path in file_types.items() if path is None]
    
    if missing_types:
        print(f"\n[ERROR] Could not auto-detect these file types: {', '.join(missing_types)}")
        print("\nAvailable files:")
        for file_path in md_files:
            print(f"  - {file_path.name}")
        print("\nPlease ensure filenames or content clearly indicate:")
        print("  - Message house/brand strategy file")
        print("  - Keywords/vocabulary bank file") 
        print("  - Testimonials/reviews file")
        return None
    
    print(f"\n[SUCCESS] Successfully loaded all 3 required input types")
    return input_content

def create_user_prompt(input_content):
    """Create the user prompt with input content"""
    prompt = """# Website Copy Generation Request

I need you to analyze the following brand strategy assets and create strategic website copy with intelligent homepage logic.

## Input Assets

### Message House (Brand Strategy)
```
{message_house}
```

### Keywords Bank (Customer Language)
```
{keywords_bank}
```

### Marketing Testimonials (Social Proof)
```
{marketing_testimonials}
```

## Request

Please analyze these assets and provide:

1. **Strategic Logic Explanation**: Why this specific homepage narrative flow works for this audience (this is the most important part)
2. **Content Module Generation**: 7 strategic content modules in priority order

Focus on customer psychology analysis and create compelling reasoning for the content order that will convince me this logic is optimal for conversion.

Remember: The logic behind the content order is more valuable than the content itself."""

    return prompt.format(
        message_house=input_content["message_house.md"],
        keywords_bank=input_content["keywords_bank.md"],
        marketing_testimonials=input_content["marketing_testimonials.md"]
    )

def generate_website_copy(config, system_prompt, user_prompt):
    """Generate website copy using Claude API"""
    
    # Get API key from config
    api_key = config.get("anthropic_api_key")
    if not api_key:
        print("Error: anthropic_api_key not found in config.json")
        return None
    
    try:
        # Initialize Claude client
        client = anthropic.Anthropic(api_key=api_key)
        
        print("Generating website copy...")
        print("This may take 30-60 seconds for comprehensive analysis...")
        
        # Generate response
        response = client.messages.create(
            model=config["model"],
            max_tokens=config["max_tokens"],
            temperature=config["temperature"],
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": user_prompt
                }
            ]
        )
        
        return response.content[0].text
        
    except Exception as e:
        print(f"Error generating website copy: {e}")
        return None

def save_output(config, content, output_dir=None):
    """Save generated website copy to output directory"""
    if output_dir is None:
        output_dir = Path(__file__).parent.parent / config["output_dir"]
    output_dir.mkdir(exist_ok=True)
    
    # Create timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"website_copy_{timestamp}.md"
    filepath = output_dir / filename
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"\n[SUCCESS] Website copy saved to: {filename}")
        print(f"Full path: {filepath}")
        return filepath
        
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
    print("=== Website Copy Agent - Generation ===\n")
    
    # Get project-aware paths
    paths = get_project_paths()
    
    # Load configuration
    config = load_config()
    if not config:
        return
    
    # Load system prompt with project-aware path
    system_prompt = load_system_prompt(config)
    if not system_prompt:
        return
    
    # Load input files with project-aware path
    input_content = load_input_files(config, paths["input_dir"])
    if not input_content:
        return
    
    # Create user prompt
    user_prompt = create_user_prompt(input_content)
    
    # Generate website copy
    website_copy = generate_website_copy(config, system_prompt, user_prompt)
    if not website_copy:
        return
    
    # Save output with project-aware path
    output_path = save_output(config, website_copy, paths["output_dir"])
    if output_path:
        print(f"\n=== Generation Complete ===")
        print(f"Review the output in: {output_path}")
        print(f"Use scripts/evaluate.py to score and provide feedback")
    
if __name__ == "__main__":
    main()