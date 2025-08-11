#!/usr/bin/env python3
"""
Agent 0a: Project Configurator Script

This script creates complete project workspace for new product/industry.
Run ONCE per new project to set up folder structure and industry-specific prompts.
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

def get_project_input():
    """Get project details from user input"""
    print("\n=== Project Configuration Setup ===")
    print("Please provide the following project details:")
    
    # Product or brand name
    product_name = input("1. Enter product or brand name: ").strip()
    
    # Product type selection  
    product_types = ["SaaS", "Health", "Finance", "Ecommerce", "Beauty", "Food", "Tech", "Education"]
    print(f"\n2. Supported product types: {', '.join(product_types)}")
    print("   (You can enter any type - not limited to the list above)")
    product_type = input("   Enter product type: ").strip()
    
    if product_type not in product_types:
        print(f"   Using custom product type: {product_type}")
    
    # Industry focus (target users)
    print(f"\n3. Industry focus examples: 'wellness consumers', 'B2B small teams', 'fitness enthusiasts'")
    industry_focus = input("   Enter industry focus (target users): ").strip()
    
    # Generate project name with timestamp
    timestamp = datetime.now().strftime("%Y%m%d")
    full_project_name = f"{product_type.lower()}_{product_name.lower().replace(' ', '')}_{timestamp}"
    
    return {
        "product_name": product_name,
        "product_type": product_type,
        "project_name": full_project_name,
        "industry_focus": industry_focus
    }

def create_project_structure(project_name, base_path, agent_list):
    """Create folder hierarchy across all agents"""
    print(f"\nCreating project structure for: {project_name}")
    
    created_folders = []
    
    for agent_name in agent_list:
        agent_path = Path(base_path) / agent_name
        
        # Create project subfolders
        folders_to_create = [
            agent_path / "1_input" / project_name,
            agent_path / "2_system_assets" / project_name,
            agent_path / "3_unlabeled" / project_name
        ]
        
        for folder_path in folders_to_create:
            try:
                folder_path.mkdir(parents=True, exist_ok=True)
                created_folders.append(str(folder_path))
                print(f"  ✓ Created: {folder_path}")
            except Exception as e:
                print(f"  ✗ Failed to create {folder_path}: {e}")
                return False, []
    
    return True, created_folders

def call_claude_api(prompt, config):
    """Call Claude API using urllib"""
    try:
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
        
        json_data = json.dumps(data).encode('utf-8')
        
        req = urllib.request.Request(url)
        req.add_header('Content-Type', 'application/json')
        req.add_header('x-api-key', config['anthropic_api_key'])
        req.add_header('anthropic-version', '2023-06-01')
        
        print("  Calling Claude API for prompt generation...")
        
        with urllib.request.urlopen(req, json_data) as response:
            response_data = json.loads(response.read().decode('utf-8'))
            
        if 'content' in response_data and len(response_data['content']) > 0:
            return response_data['content'][0]['text']
        else:
            print("Error: Unexpected API response format")
            return None
            
    except Exception as e:
        print(f"Error calling Claude API: {e}")
        return None

def generate_system_prompts(project_details, config):
    """Generate industry-specific prompts for all agents"""
    print(f"\nGenerating industry-specific prompts for {project_details['product_type']}...")
    
    prompt_generation_request = f"""
Generate industry-specific system prompts for a {project_details['product_type']} product with the following details:

**Project Details:**
- Product/Brand: {project_details['product_name']}
- Product Type: {project_details['product_type']}
- Industry Focus: {project_details['industry_focus']}

**Required Output:**
Generate broad, flexible system prompts optimized for each of these 8 agents:

1. **message_house_agent** - Strategic messaging and positioning
2. **user_story_agent** - Brand-side persona development  
3. **user_story_real_reviews_agent** - Customer-side persona development
4. **gap_analysis_agent** - Strategic gap analysis
5. **keywords_bank_agent** - Keyword and vocabulary development
6. **testimonial_agent** - Marketing testimonial generation
7. **social_media_twitter_agent** - Twitter content generation
8. **website_copy_agent** - Website copy generation

**Format Required:**
```
=== AGENT_1_MESSAGE_HOUSE ===
[Comprehensive system prompt for message house agent optimized for {project_details['product_type']} industry]

=== AGENT_2_USER_STORY ===
[Comprehensive system prompt for user story agent optimized for {project_details['product_type']} industry]

... continue for all 8 agents
```

**Prompt Design Principles:**
- Focus on {project_details['product_type']} industry terminology and best practices
- Target communication style for: {project_details['industry_focus']}
- Keep prompts broad and flexible - specific strategy will come from user's Q&A content
- Emphasize industry-appropriate tone, language, and approach
- Do not narrow the scope - let the user's content drive specific features and strategy

Generate comprehensive, industry-optimized but flexible prompts now:
"""

    return call_claude_api(prompt_generation_request, config)

def parse_generated_prompts(generated_content):
    """Parse generated content into individual agent prompts"""
    if not generated_content:
        return {}
    
    prompts = {}
    current_agent = None
    current_content = []
    
    lines = generated_content.split('\n')
    
    for line in lines:
        # Look for agent headers with more flexible matching
        if ('=== AGENT_' in line.upper() or 
            'AGENT_' in line.upper() and ('===' in line or '---' in line or '###' in line)):
            
            # Save previous agent content
            if current_agent and current_content:
                clean_content = '\n'.join(current_content).strip()
                if clean_content:  # Only save if there's actual content
                    prompts[current_agent] = clean_content
            
            # Extract agent identifier from line
            line_upper = line.upper()
            if 'MESSAGE_HOUSE' in line_upper:
                current_agent = 'AGENT_1_MESSAGE_HOUSE'
            elif 'USER_STORY' in line_upper and 'REAL' not in line_upper and 'REVIEW' not in line_upper:
                current_agent = 'AGENT_2_USER_STORY'
            elif 'USER_STORY' in line_upper and ('REAL' in line_upper or 'REVIEW' in line_upper):
                current_agent = 'AGENT_3_USER_STORY_REAL_REVIEWS'
            elif 'GAP_ANALYSIS' in line_upper:
                current_agent = 'AGENT_4_GAP_ANALYSIS'
            elif 'KEYWORDS' in line_upper:
                current_agent = 'AGENT_5_KEYWORDS_BANK'
            elif 'TESTIMONIAL' in line_upper:
                current_agent = 'AGENT_7_TESTIMONIAL'
            elif 'TWITTER' in line_upper or 'SOCIAL' in line_upper:
                current_agent = 'AGENT_8_SOCIAL_MEDIA_TWITTER'
            elif 'WEBSITE' in line_upper or 'WEB' in line_upper:
                current_agent = 'AGENT_9_WEBSITE_COPY'
            else:
                current_agent = line.replace('===', '').replace('---', '').replace('###', '').strip()
            
            current_content = []
        else:
            current_content.append(line)
    
    # Save last agent
    if current_agent and current_content:
        clean_content = '\n'.join(current_content).strip()
        if clean_content:
            prompts[current_agent] = clean_content
    
    # Debug output
    print(f"\nParsed {len(prompts)} agent prompts:")
    for key in prompts.keys():
        print(f"  - {key}")
    
    return prompts

def write_system_prompts(project_name, base_path, agent_list, prompts):
    """Write prompt files to each agent's 2_system_assets folder"""
    print(f"\nWriting system prompts to agent folders...")
    
    agent_mapping = {
        "AGENT_1_MESSAGE_HOUSE": "message_house_agent",
        "AGENT_2_USER_STORY": "user_story_agent",
        "AGENT_3_USER_STORY_REAL_REVIEWS": "user_story_real_reviews_agent",
        "AGENT_4_GAP_ANALYSIS": "gap_analysis_agent",
        "AGENT_5_KEYWORDS_BANK": "keywords_bank_agent",
        "AGENT_7_TESTIMONIAL": "testimonial_agent",
        "AGENT_8_SOCIAL_MEDIA_TWITTER": "social_media_twitter_agent",
        "AGENT_9_WEBSITE_COPY": "website_copy_agent"
    }
    
    written_files = []
    missing_prompts = []
    
    # Debug: Show what we're trying to map
    print(f"Available prompts: {list(prompts.keys())}")
    print(f"Expected mappings: {list(agent_mapping.keys())}")
    
    for prompt_key, prompt_content in prompts.items():
        if prompt_key in agent_mapping:
            agent_name = agent_mapping[prompt_key]
            prompt_path = Path(base_path) / agent_name / "2_system_assets" / project_name / "system_prompt.md"
            
            try:
                prompt_path.parent.mkdir(parents=True, exist_ok=True)
                with open(prompt_path, 'w', encoding='utf-8') as f:
                    f.write(prompt_content)
                written_files.append(str(prompt_path))
                print(f"  ✓ Written: {agent_name}/system_prompt.md")
            except Exception as e:
                print(f"  ✗ Failed to write {prompt_path}: {e}")
        else:
            print(f"  ⚠️ No mapping found for: {prompt_key}")
    
    # Check for missing agents
    for expected_key, agent_name in agent_mapping.items():
        if expected_key not in prompts:
            missing_prompts.append(f"{expected_key} -> {agent_name}")
    
    if missing_prompts:
        print(f"\n⚠️ Missing prompts for {len(missing_prompts)} agents:")
        for missing in missing_prompts:
            print(f"  - {missing}")
    
    return written_files

def update_agent_configs(project_name, base_path, agent_list):
    """Update config.json files with current_project"""
    print(f"\nUpdating agent configurations...")
    
    updated_configs = []
    
    for agent_name in agent_list:
        config_path = Path(base_path) / agent_name / "config.json"
        
        try:
            # Read existing config
            with open(config_path, 'r') as f:
                agent_config = json.load(f)
            
            # Update project name
            agent_config['current_project'] = project_name
            
            # Write back
            with open(config_path, 'w') as f:
                json.dump(agent_config, f, indent=2)
            
            updated_configs.append(str(config_path))
            print(f"  ✓ Updated: {agent_name}/config.json")
            
        except Exception as e:
            print(f"  ✗ Failed to update {config_path}: {e}")
    
    return updated_configs

def save_project_log(project_details, output_dir):
    """Save project setup log"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"project_setup_{project_details['project_name']}_{timestamp}.json"
    log_path = output_dir / log_filename
    
    log_data = {
        "setup_timestamp": timestamp,
        "project_details": project_details,
        "status": "completed"
    }
    
    try:
        output_dir.mkdir(exist_ok=True)
        with open(log_path, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, indent=2)
        print(f"Project setup log saved: {log_path}")
        return log_path
    except Exception as e:
        print(f"Error saving log: {e}")
        return None

def main():
    """Main execution function"""
    print("Agent 0a: Project Configurator Starting...")
    
    # Load configuration
    config = load_config()
    base_path = "C:/Users/Ace"  # Your base path
    
    # Get project details from user
    project_details = get_project_input()
    
    print(f"\nProject Summary:")
    print(f"  Product/Brand: {project_details['product_name']}")
    print(f"  Product Type: {project_details['product_type']}")
    print(f"  Full Project Name: {project_details['project_name']}")
    print(f"  Industry Focus: {project_details['industry_focus']}")
    
    confirm = input(f"\nProceed with project setup? (y/N): ").strip().lower()
    if confirm != 'y':
        print("Setup cancelled.")
        sys.exit(0)
    
    # Create project structure
    success, created_folders = create_project_structure(
        project_details['project_name'], 
        base_path, 
        config['agent_list']
    )
    
    if not success:
        print("Failed to create project structure.")
        sys.exit(1)
    
    # Generate system prompts
    generated_content = generate_system_prompts(project_details, config)
    if not generated_content:
        print("Failed to generate system prompts.")
        sys.exit(1)
    
    # Parse and write prompts
    prompts = parse_generated_prompts(generated_content)
    if not prompts:
        print("Failed to parse generated prompts.")
        sys.exit(1)
    
    written_files = write_system_prompts(
        project_details['project_name'],
        base_path,
        config['agent_list'],
        prompts
    )
    
    # Update agent configurations
    updated_configs = update_agent_configs(
        project_details['project_name'],
        base_path,
        config['agent_list']
    )
    
    # Save project log
    output_dir = Path(__file__).parent.parent / "3_unlabeled"
    log_path = save_project_log(project_details, output_dir)
    
    print(f"""
SUCCESS! Project workspace created successfully.

✅ Project Name: {project_details['project_name']}
✅ Product Type: {project_details['product_type']} expertise configured
✅ {len(created_folders)} folders created across 8 agents
✅ {len(written_files)} system prompts written and deployed  
✅ {len(updated_configs)} agent configurations updated
✅ Ready for Agent 0b execution

Project Details:
- Product/Brand: {project_details['product_name']}
- Project Name: {project_details['project_name']}
- Product Type: {project_details['product_type']}
- Target Agents: 8 (message_house through website_copy)
- System Prompt Strategy: {project_details['industry_focus']}

Next Steps:
1. Manually place your input files in the appropriate agent folders:
   - message_house_agent/1_input/{project_details['project_name']}/qa_session_content.md
   - user_story_real_reviews_agent/1_input/{project_details['project_name']}/customer_reviews.csv (optional)
   
2. Run Agent 0b to execute the pipeline:
   python agent_0b_orchestrator/scripts/generate_simple.py
""")

if __name__ == "__main__":
    main()