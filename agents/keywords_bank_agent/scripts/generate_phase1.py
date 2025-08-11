#!/usr/bin/env python3
"""
Keywords Bank Agent - Phase 1: Vocabulary Generation Script
Generates foundational keyword bank vocabulary for human evaluation
"""

import os
import json
import datetime
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path
from typing import Dict, List, Optional

class KeywordsBankPhase1Generator:
    def __init__(self, config_path: str = "config.json"):
        """Initialize the Phase 1 generator with configuration."""
        self.config = self._load_config(config_path)
        # No client needed - using direct HTTP requests
        self.base_dir = Path(__file__).parent.parent
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.current_project = self.config.get("current_project", None)
        
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from JSON file."""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Config file {config_path} not found. Please create it with your API key.")
            return {}
            
    def _load_system_prompt(self) -> str:
        """Load the Phase 1 system prompt."""
        if self.current_project:
            # Use project-specific system prompt
            prompt_path = self.base_dir / "2_system_assets" / self.current_project / "system_prompt.md"
            if prompt_path.exists():
                with open(prompt_path, 'r', encoding='utf-8') as f:
                    return f.read()
            else:
                print(f">>> WARNING: Project-specific system prompt not found: {prompt_path}")
        
        # Fallback to generic system prompt
        prompt_path = self.base_dir / "2_system_assets" / "system_prompt_phase1.md"
        with open(prompt_path, 'r', encoding='utf-8') as f:
            return f.read()
            
    def _load_input_files(self) -> Dict[str, str]:
        """Load all input files from the 1_input directory."""
        if self.current_project:
            # Use project-specific input directory
            input_dir = self.base_dir / "1_input" / self.current_project
            if not input_dir.exists():
                print(f">>> WARNING: Project-specific input directory not found: {input_dir}")
                input_dir = self.base_dir / "1_input"  # Fallback
        else:
            # Fallback to generic input directory
            input_dir = self.base_dir / "1_input"
        
        print(f">>> Loading input files from: {input_dir}")
        input_files = {}
        
        # Required files - match your actual naming patterns
        required_files = [
            ("messagehouse", "message_house"),
            ("userstories", "brand_side_persona"), 
            ("userstories_reviews", "customer_side_persona")
        ]
        
        # Load required files
        for file_pattern, file_key in required_files:
            matching_files = list(input_dir.glob(f"{file_pattern}_*.md"))
            if matching_files:
                # Get the most recent file
                latest_file = max(matching_files, key=os.path.getmtime)
                with open(latest_file, 'r', encoding='utf-8') as f:
                    input_files[file_key] = f.read()
                print(f">>> Loaded {file_key}: {latest_file.name}")
            else:
                print(f">>> WARNING: No {file_pattern} file found in 1_input directory")
                
        # Optional external keywords file
        csv_files = list(input_dir.glob("external_keywords.csv"))
        if csv_files:
            latest_csv = max(csv_files, key=os.path.getmtime)
            with open(latest_csv, 'r', encoding='utf-8') as f:
                input_files["external_keywords"] = f.read()
            print(f">>> Loaded external keywords: {latest_csv.name}")
        else:
            print(">>> No external keywords file found (optional)")
            
        return input_files
        
    def _create_user_prompt(self, input_files: Dict[str, str]) -> str:
        """Create the user prompt with all input data."""
        prompt_parts = []
        
        # Add message house
        if "message_house" in input_files:
            prompt_parts.append(f"## MESSAGE HOUSE\n\n{input_files['message_house']}")
            
        # Add brand side persona
        if "brand_side_persona" in input_files:
            prompt_parts.append(f"## BRAND SIDE PERSONA\n\n{input_files['brand_side_persona']}")
            
        # Add customer side persona
        if "customer_side_persona" in input_files:
            prompt_parts.append(f"## CUSTOMER SIDE PERSONA\n\n{input_files['customer_side_persona']}")
            
        # Add external keywords if available
        if "external_keywords" in input_files:
            prompt_parts.append(f"## EXTERNAL KEYWORDS DATA\n\n{input_files['external_keywords']}")
            
        # Add generation instruction
        prompt_parts.append("""
## GENERATION INSTRUCTION

Based on the provided input assets, generate a comprehensive keyword bank vocabulary following the exact structure specified in the system prompt. Focus on:

1. **Strategic Synthesis** - Extract core themes from message house and personas
2. **Creative Expansion** - Generate meaningful semantic variations
3. **Foundation Building** - Create vocabulary that expansion engines can leverage
4. **Quality over Quantity** - Ensure every keyword serves a strategic purpose

Generate the complete `keywords_bank_vocabulary_[timestamp].md` file now.
""")
        
        return "\n\n".join(prompt_parts)
        
    def generate_vocabulary(self) -> str:
        """Generate the Phase 1 vocabulary using Claude API."""
        print("\n>>> Starting Phase 1: Vocabulary Generation")
        print("=" * 50)
        
        # Load system prompt
        system_prompt = self._load_system_prompt()
        
        # Load input files
        input_files = self._load_input_files()
        if not input_files:
            raise ValueError("No input files found. Please add required files to 1_input directory.")
            
        # Create user prompt
        user_prompt = self._create_user_prompt(input_files)
        
        # Generate vocabulary with Claude
        print("\n>>> Generating vocabulary with Claude...")
        
        try:
            # Prepare API request
            url = "https://api.anthropic.com/v1/messages"
            
            data = {
                "model": self.config.get("model", "claude-3-5-sonnet-20241022"),
                "max_tokens": self.config.get("max_tokens", 4000),
                "temperature": self.config.get("temperature", 0.7),
                "system": system_prompt,
                "messages": [
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ]
            }
            
            # Convert to JSON
            json_data = json.dumps(data).encode('utf-8')
            
            # Create request
            req = urllib.request.Request(url)
            req.add_header('Content-Type', 'application/json')
            req.add_header('x-api-key', self.config['anthropic_api_key'])
            req.add_header('anthropic-version', '2023-06-01')
            
            # Make the request
            with urllib.request.urlopen(req, json_data) as response:
                response_data = json.loads(response.read().decode('utf-8'))
                
            # Extract the content
            if 'content' in response_data and len(response_data['content']) > 0:
                generated_content = response_data['content'][0]['text']
                print(">>> Vocabulary generation completed")
                return generated_content
            else:
                print(">>> Error: Unexpected API response format")
                print("Response:", response_data)
                raise ValueError("Unexpected API response format")
                
        except urllib.error.HTTPError as e:
            print(f">>> HTTP Error: {e.code} - {e.reason}")
            error_body = e.read().decode('utf-8')
            print(f"Error details: {error_body}")
            raise
        except Exception as e:
            print(f">>> Error generating vocabulary: {str(e)}")
            raise
            
    def save_output(self, content: str) -> str:
        """Save the generated vocabulary to the unlabeled directory."""
        if self.current_project:
            # Use project-specific output directory
            output_dir = self.base_dir / "3_unlabeled" / self.current_project
        else:
            # Fallback to generic output directory  
            output_dir = self.base_dir / "3_unlabeled"
            
        output_dir.mkdir(parents=True, exist_ok=True)
        
        filename = f"keywords_bank_vocabulary_{self.timestamp}.md"
        output_path = output_dir / filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f">>> Output saved to: {output_path}")
        return str(output_path)
        
    def run(self) -> str:
        """Run the complete Phase 1 generation process."""
        try:
            # Generate vocabulary
            vocabulary = self.generate_vocabulary()
            
            # Save output
            output_path = self.save_output(vocabulary)
            
            print("\n>>> Phase 1 Generation Complete!")
            print(f">>> Generated file: {output_path}")
            print("\n>>> Next Steps:")
            print("1. Run evaluate_phase1.py to evaluate the generated vocabulary")
            print("2. If approved (score >= 7.0), run generate_phase2.py")
            print("3. If not approved, regenerate Phase 1 with improvements")
            
            return output_path
            
        except Exception as e:
            print(f"\n>>> Phase 1 generation failed: {str(e)}")
            raise

if __name__ == "__main__":
    generator = KeywordsBankPhase1Generator()
    generator.run()