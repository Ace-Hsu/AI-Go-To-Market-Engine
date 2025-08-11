#!/usr/bin/env python3
"""
Keywords Bank Agent - Phase 2: Expansion Engine Script
Generates massive keyword expansion from approved Phase 1 vocabulary
"""

import os
import json
import datetime
from pathlib import Path
from typing import Dict, List, Optional
import urllib.request
import urllib.parse
import urllib.error

class KeywordsBankPhase2Generator:
    def __init__(self, config_path: str = "config.json"):
        """Initialize the Phase 2 generator with configuration."""
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
        """Load the Phase 2 system prompt."""
        if self.current_project:
            # Use project-specific system prompt
            prompt_path = self.base_dir / "2_system_assets" / self.current_project / "system_prompt.md"
            if prompt_path.exists():
                with open(prompt_path, 'r', encoding='utf-8') as f:
                    return f.read()
            else:
                print(f">>> WARNING: Project-specific system prompt not found: {prompt_path}")
        
        # Fallback to generic system prompt
        prompt_path = self.base_dir / "2_system_assets" / "system_prompt_phase2.md"
        with open(prompt_path, 'r', encoding='utf-8') as f:
            return f.read()
            
    def _find_approved_vocabulary(self) -> Optional[str]:
        """Find the most recently approved Phase 1 vocabulary file."""
        json_dir = self.base_dir / "5_labeled_json"
        
        if not json_dir.exists():
            print(">>> No labeled JSON directory found. Please evaluate Phase 1 first.")
            return None
            
        # Find all labeled JSON files
        json_files = list(json_dir.glob("keywords_bank_vocabulary_*_labeled.json"))
        
        if not json_files:
            print(">>> No evaluated vocabulary files found. Please evaluate Phase 1 first.")
            return None
            
        # Find the most recent approved file
        approved_files = []
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if data.get("passed_threshold", False):
                        approved_files.append((json_file, data.get("evaluation_date", "")))
            except Exception as e:
                print(f">>> Warning: Could not read {json_file}: {e}")
                continue
                
        if not approved_files:
            print(">>> No approved vocabulary files found. Please approve Phase 1 first.")
            return None
            
        # Get the most recent approved file
        latest_approved = max(approved_files, key=lambda x: x[1])
        json_file = latest_approved[0]
        
        # Find corresponding vocabulary file
        vocab_filename = json_file.name.replace("_labeled.json", ".md")
        if self.current_project:
            # Try project-specific folder first
            vocab_path = self.base_dir / "3_unlabeled" / self.current_project / vocab_filename
            if not vocab_path.exists():
                # Fallback to root folder
                vocab_path = self.base_dir / "3_unlabeled" / vocab_filename
        else:
            # Use root folder
            vocab_path = self.base_dir / "3_unlabeled" / vocab_filename
        
        if not vocab_path.exists():
            print(f">>> Vocabulary file not found: {vocab_path}")
            return None
            
        return str(vocab_path)
        
    def _load_input_files(self, vocab_path: str) -> Dict[str, str]:
        """Load all input files including approved vocabulary."""
        input_files = {}
        
        # Load approved vocabulary
        with open(vocab_path, 'r', encoding='utf-8') as f:
            input_files["approved_vocabulary"] = f.read()
        print(f">>> Loaded approved vocabulary: {Path(vocab_path).name}")
        
        # Load supporting files from 1_input for context
        input_dir = self.base_dir / "1_input"
        
        context_files = [
            "message_house",
            "brand_side_persona", 
            "customer_side_persona"
        ]
        
        for file_type in context_files:
            matching_files = list(input_dir.glob(f"{file_type}_*.md"))
            if matching_files:
                latest_file = max(matching_files, key=os.path.getmtime)
                with open(latest_file, 'r', encoding='utf-8') as f:
                    input_files[file_type] = f.read()
                print(f">>> Loaded {file_type} for context: {latest_file.name}")
                
        return input_files
        
    def _create_user_prompt(self, input_files: Dict[str, str]) -> str:
        """Create the user prompt with approved vocabulary and context."""
        prompt_parts = []
        
        # Add approved vocabulary (primary input)
        if "approved_vocabulary" in input_files:
            prompt_parts.append(f"## APPROVED PHASE 1 VOCABULARY (PRIMARY INPUT)\n\n{input_files['approved_vocabulary']}")
            
        # Add context files
        context_section = "## CONTEXT FILES (For Reference Only)\n\n"
        
        if "message_house" in input_files:
            context_section += f"### Message House\n{input_files['message_house']}\n\n"
            
        if "brand_side_persona" in input_files:
            context_section += f"### Brand Side Persona\n{input_files['brand_side_persona']}\n\n"
            
        if "customer_side_persona" in input_files:
            context_section += f"### Customer Side Persona\n{input_files['customer_side_persona']}\n\n"
            
        prompt_parts.append(context_section)
        
        # Add generation instruction
        prompt_parts.append("""
## GENERATION INSTRUCTION

Based on the APPROVED Phase 1 vocabulary above, generate a comprehensive keyword expansion across all 6 vectors following the exact structure specified in the system prompt.

**Key Requirements:**
- Generate 150+ total keywords/phrases across all vectors
- Each vector must serve its specific purpose (SEO vs Creative)
- All expansions must trace back to the approved vocabulary foundation
- Focus on volume, diversity, and strategic alignment
- Create immediately actionable content for downstream agents

**Vector Distribution:**
- Vector A: 20+ question-based keywords
- Vector B: 30+ modifier-based keywords  
- Vector C: 40+ intent-based keywords
- Vector D: 25+ persona quote starters
- Vector E: 20+ social media hooks & hashtags
- Vector F: 30+ feature-to-benefit angles

Generate the complete `keywords_bank_expansion_[timestamp].md` file now.
""")
        
        return "\n\n".join(prompt_parts)
        
    def generate_expansion(self, vocab_path: str) -> str:
        """Generate the Phase 2 expansion using Claude API."""
        print("\n>>> Starting Phase 2: Expansion Engine Generation")
        print("=" * 60)
        
        # Load system prompt
        system_prompt = self._load_system_prompt()
        
        # Load input files
        input_files = self._load_input_files(vocab_path)
        
        # Create user prompt
        user_prompt = self._create_user_prompt(input_files)
        
        # Generate expansion with Claude
        print("\n>>> Generating massive keyword expansion with Claude...")
        print("   Target: 150+ keywords across 6 vectors")
        
        try:
            # Prepare API request
            url = "https://api.anthropic.com/v1/messages"
            
            data = {
                "model": self.config.get("model", "claude-3-5-sonnet-20241022"),
                "max_tokens": self.config.get("max_tokens_phase2", 8000),
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
                print(">>> Expansion generation completed")
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
            print(f">>> Error generating expansion: {str(e)}")
            raise
            
    def save_output(self, content: str) -> str:
        """Save the generated expansion to the unlabeled directory."""
        if self.current_project:
            # Use project-specific output directory
            output_dir = self.base_dir / "3_unlabeled" / self.current_project
        else:
            # Fallback to root directory
            output_dir = self.base_dir / "3_unlabeled"
            
        output_dir.mkdir(parents=True, exist_ok=True)
        
        filename = f"keywords_bank_expansion_{self.timestamp}.md"
        output_path = output_dir / filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f">>> Output saved to: {output_path}")
        return str(output_path)
        
    def run(self) -> str:
        """Run the complete Phase 2 generation process."""
        try:
            # Find approved vocabulary
            vocab_path = self._find_approved_vocabulary()
            if not vocab_path:
                return None
                
            # Generate expansion
            expansion = self.generate_expansion(vocab_path)
            
            # Save output
            output_path = self.save_output(expansion)
            
            print("\n>>> Phase 2 Generation Complete!")
            print(f">>> Generated file: {output_path}")
            print(f">>> Content: 150+ keywords across 6 strategic vectors")
            print("\n>>> Next Steps:")
            print("1. This expansion output feeds directly into:")
            print("   - Agent 7: Testimonial Agent")
            print("   - Agent 8: Social Media Twitter Agent") 
            print("   - Agent 9: Product Core Long Form Copy Agent")
            print("2. No evaluation needed - quality controlled by downstream agents")
            print("3. Ready for content generation pipeline!")
            
            return output_path
            
        except Exception as e:
            print(f"\n>>> Phase 2 generation failed: {str(e)}")
            raise

if __name__ == "__main__":
    generator = KeywordsBankPhase2Generator()
    generator.run()