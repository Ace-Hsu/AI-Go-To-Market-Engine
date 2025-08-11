# Agent Development Template - Complete Checklist

## Quick Start: Creating a New Agent

Follow this checklist to create any new agent that maintains system consistency and integrates seamlessly with the existing pipeline.

---

## **Step 1: Agent Folder Structure Setup**

### ✅ Create Standard Folder Structure
```
your_new_agent/
├── 1_input/                          ← Input files storage
├── 2_system_assets/                  ← System prompts and templates
│   └── examples/                     ← Reference examples (optional)
├── 3_unlabeled/                      ← Generated outputs (before evaluation)
├── 4_labeled_md/                     ← Evaluated content (legacy support)
├── 5_labeled_json/                   ← Evaluation data for iterate system
├── scripts/                          ← All Python scripts
├── config.json                       ← Agent configuration
├── requirements.txt                  ← Dependencies (if any)
├── README.md                         ← Agent documentation
└── QUICK_START.md                    ← Usage instructions
```

### ✅ Project-Specific Structure (Auto-created by Agent 0a)
```
your_new_agent/
├── 1_input/{project_name}/           ← Project-specific inputs
├── 2_system_assets/{project_name}/   ← Project-specific prompts
└── 3_unlabeled/{project_name}/       ← Project-specific outputs
```

---

## **Step 2: Core Files Creation**

### ✅ config.json (Required)
```json
{
  "anthropic_api_key": "your_api_key_here",
  "model": "claude-3-5-sonnet-20241022",
  "max_tokens": 2000,
  "temperature": 0.3,
  "current_project": null
}
```

### ✅ requirements.txt (Standard)
```
# No external dependencies required for core functionality
# All agents use Python stdlib (urllib) for API calls
# Add only if your specific business logic requires additional packages
```

### ✅ 2_system_assets/system_prompt.md (Required)
```markdown
You are [ROLE DESCRIPTION - specific to your business logic].

[BUSINESS LOGIC SPECIFIC INSTRUCTIONS]

Key requirements:
- [Business logic requirement 1]
- [Business logic requirement 2]
- [Output format specifications]
- [Quality standards]

Maintain [TONE/STYLE] while ensuring [SPECIFIC OUTCOMES].
```

---

## **Step 3: Scripts Creation**

### ✅ scripts/generate_simple.py (REQUIRED - Use Template)

**Copy this foundation and modify only the business logic sections:**

```python
#!/usr/bin/env python3
"""
[AGENT NAME] Generator Script

[BUSINESS LOGIC DESCRIPTION]
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
                if overall_score >= 8.0 and '[CONTENT_KEY]' in example_data:
                    content = example_data['[CONTENT_KEY]']
                    
                    # Get improvement insights from detailed scores
                    insights = []
                    if 'detailed_scores' in example_data:
                        for criteria, details in example_data['detailed_scores'].items():
                            if isinstance(details, dict) and 'comments' in details:
                                insights.append(f"- {criteria.replace('_', ' ').title()}: {details['comments']}")
                    
                    # FORMAT YOUR EXAMPLE TEMPLATE HERE - BUSINESS LOGIC SPECIFIC
                    example_text = f"""
**HIGH-QUALITY EXAMPLE (Score: {overall_score}/10):**

[YOUR EXAMPLE FORMAT BASED ON BUSINESS LOGIC]

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

def generate_content(input_content, system_prompt, example, config):
    """Generate content using Claude API - MODIFY THIS FOR YOUR BUSINESS LOGIC"""
    # Construct the full prompt
    full_prompt = f"""
{system_prompt}

{example}

---

**INPUT TO TRANSFORM:**

{input_content}

---

**INSTRUCTIONS:**
[YOUR BUSINESS LOGIC SPECIFIC INSTRUCTIONS HERE]

Generate the content now:
"""

    return call_claude_api(full_prompt, config)

def save_output(content, output_dir):
    """Save generated content to unlabeled folder"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"[AGENT_PREFIX]_{timestamp}.md"  # Replace [AGENT_PREFIX] with your agent name
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
    """Main execution function - MODIFY INPUT FILE DETECTION FOR YOUR BUSINESS LOGIC"""
    print("[AGENT NAME] Generator Starting...")
    
    # Get project-aware paths
    paths = get_project_paths()
    input_dir = paths["input_dir"]
    system_assets_dir = paths["system_assets_dir"]
    output_dir = paths["output_dir"]
    
    # MODIFY THIS SECTION FOR YOUR INPUT FILE REQUIREMENTS
    # Find input file (flexible detection)
    input_files = list(input_dir.glob("*.md"))  # Adjust pattern as needed
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
    
    # Check if files exist
    print(f"Using input file: {input_file.name}")
    
    # Load configuration
    print("Loading configuration...")
    config = load_config()
    
    # Load input files
    print("Loading input content...")
    input_content = load_file(input_file)
    if not input_content:
        sys.exit(1)
    
    print("Loading system prompt...")
    system_prompt = load_file(system_prompt_file)
    if not system_prompt:
        sys.exit(1)
    
    print("Loading examples...")
    example = load_example_from_json()
    
    # Generate content
    print("Generating content...")
    generated_content = generate_content(input_content, system_prompt, example, config)
    if not generated_content:
        sys.exit(1)
    
    # Save output
    print("Saving output...")
    output_path = save_output(generated_content, output_dir)
    if not output_path:
        sys.exit(1)
    
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

if __name__ == "__main__":
    main()
```

### ✅ scripts/evaluate.py (OPTIONAL - For Iterate System)

**Use this template and modify the scoring criteria for your business logic:**

```python
#!/usr/bin/env python3
"""
[AGENT NAME] Evaluation Script

GUI-based evaluation tool for [BUSINESS LOGIC DESCRIPTION]
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import json
import os
from datetime import datetime
from pathlib import Path

class EvaluationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("[AGENT NAME] Evaluation Tool")
        self.root.geometry("1000x800")
        
        # MODIFY THESE CRITERIA FOR YOUR BUSINESS LOGIC
        self.criteria = {
            "[CRITERIA_1]": {"weight": 0.25, "description": "[Description of criteria 1]"},
            "[CRITERIA_2]": {"weight": 0.20, "description": "[Description of criteria 2]"}, 
            "[CRITERIA_3]": {"weight": 0.20, "description": "[Description of criteria 3]"},
            "[CRITERIA_4]": {"weight": 0.20, "description": "[Description of criteria 4]"},
            "[CRITERIA_5]": {"weight": 0.15, "description": "[Description of criteria 5]"}
        }
        
        # MODIFY THESE TAGS FOR YOUR BUSINESS LOGIC
        self.improvement_tags = [
            "[improvement_tag_1]", "[improvement_tag_2]", "[improvement_tag_3]",
            "[improvement_tag_4]", "[improvement_tag_5]"
        ]
        
        self.strength_tags = [
            "[strength_tag_1]", "[strength_tag_2]", "[strength_tag_3]",
            "[strength_tag_4]", "[strength_tag_5]"
        ]
        
        self.current_file = None
        self.content = ""
        self.scores = {}
        
        self.setup_ui()
    
    def setup_ui(self):
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # File selection
        file_frame = ttk.LabelFrame(main_frame, text="File Selection", padding="5")
        file_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(file_frame, text="Select File", command=self.select_file).grid(row=0, column=0, padx=(0, 10))
        self.file_label = ttk.Label(file_frame, text="No file selected")
        self.file_label.grid(row=0, column=1, sticky=tk.W)
        
        # Content display
        content_frame = ttk.LabelFrame(main_frame, text="Content Preview", padding="5")
        content_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        self.content_text = scrolledtext.ScrolledText(content_frame, height=15, wrap=tk.WORD)
        self.content_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scoring section
        scoring_frame = ttk.LabelFrame(main_frame, text="Evaluation Scoring", padding="5")
        scoring_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        
        row = 0
        self.score_vars = {}
        for criteria, info in self.criteria.items():
            ttk.Label(scoring_frame, text=f"{criteria.replace('_', ' ').title()} ({info['weight']*100:.0f}%):").grid(row=row, column=0, sticky=tk.W, pady=2)
            ttk.Label(scoring_frame, text=info['description'], font=('TkDefaultFont', 8)).grid(row=row+1, column=0, sticky=tk.W, padx=(20, 0))
            
            var = tk.StringVar(value="5")
            self.score_vars[criteria] = var
            score_frame = ttk.Frame(scoring_frame)
            score_frame.grid(row=row, column=1, sticky=tk.W, padx=(10, 0))
            
            ttk.Scale(score_frame, from_=1, to=10, orient=tk.HORIZONTAL, variable=var, length=200).grid(row=0, column=0)
            ttk.Label(score_frame, textvariable=var, width=3).grid(row=0, column=1, padx=(5, 0))
            
            row += 2
        
        # Tags selection
        tags_frame = ttk.LabelFrame(main_frame, text="Analysis Tags", padding="5")
        tags_frame.grid(row=2, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        
        ttk.Label(tags_frame, text="Improvement Areas:").grid(row=0, column=0, sticky=tk.W)
        self.improvement_vars = {}
        for i, tag in enumerate(self.improvement_tags):
            var = tk.BooleanVar()
            self.improvement_vars[tag] = var
            ttk.Checkbutton(tags_frame, text=tag.replace('_', ' ').title(), variable=var).grid(row=i+1, column=0, sticky=tk.W)
        
        ttk.Label(tags_frame, text="Strengths:").grid(row=len(self.improvement_tags)+2, column=0, sticky=tk.W, pady=(10, 0))
        self.strength_vars = {}
        for i, tag in enumerate(self.strength_tags):
            var = tk.BooleanVar()
            self.strength_vars[tag] = var
            ttk.Checkbutton(tags_frame, text=tag.replace('_', ' ').title(), variable=var).grid(row=len(self.improvement_tags)+3+i, column=0, sticky=tk.W)
        
        # Comments
        comment_frame = ttk.LabelFrame(main_frame, text="Comments", padding="5")
        comment_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.comment_text = tk.Text(comment_frame, height=4, wrap=tk.WORD)
        self.comment_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=(10, 0))
        
        ttk.Button(button_frame, text="Calculate Score", command=self.calculate_score).grid(row=0, column=0, padx=(0, 10))
        self.score_label = ttk.Label(button_frame, text="Overall Score: --")
        self.score_label.grid(row=0, column=1, padx=(0, 20))
        
        ttk.Button(button_frame, text="Save Evaluation", command=self.save_evaluation).grid(row=0, column=2)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        content_frame.columnconfigure(0, weight=1)
        content_frame.rowconfigure(0, weight=1)
        comment_frame.columnconfigure(0, weight=1)
    
    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="Select [AGENT NAME] Output File",
            filetypes=[("Markdown files", "*.md"), ("All files", "*.*")],
            initialdir=Path(__file__).parent.parent / "3_unlabeled"
        )
        
        if file_path:
            self.current_file = Path(file_path)
            self.file_label.config(text=self.current_file.name)
            
            # Load and display content
            try:
                with open(self.current_file, 'r', encoding='utf-8') as f:
                    self.content = f.read()
                self.content_text.delete(1.0, tk.END)
                self.content_text.insert(1.0, self.content)
            except Exception as e:
                messagebox.showerror("Error", f"Could not load file: {e}")
    
    def calculate_score(self):
        if not self.current_file:
            messagebox.showwarning("Warning", "Please select a file first")
            return
        
        # Calculate weighted score
        total_score = 0
        total_weight = 0
        
        for criteria, info in self.criteria.items():
            score = float(self.score_vars[criteria].get())
            weight = info['weight']
            total_score += score * weight
            total_weight += weight
        
        overall_score = total_score / total_weight if total_weight > 0 else 0
        self.score_label.config(text=f"Overall Score: {overall_score:.1f}/10")
        
        return overall_score
    
    def save_evaluation(self):
        if not self.current_file:
            messagebox.showwarning("Warning", "Please select a file first")
            return
        
        overall_score = self.calculate_score()
        
        # Collect detailed scores
        detailed_scores = {}
        for criteria, info in self.criteria.items():
            detailed_scores[criteria] = {
                "score": float(self.score_vars[criteria].get()),
                "weight": info['weight'],
                "comments": info['description']
            }
        
        # Collect tags
        improvement_tags = [tag for tag, var in self.improvement_vars.items() if var.get()]
        strength_tags = [tag for tag, var in self.strength_vars.items() if var.get()]
        
        # Create evaluation record
        evaluation_data = {
            "evaluation_metadata": {
                "document_id": self.current_file.stem,
                "original_file_path": f"3_unlabeled/{self.current_file.name}",
                "evaluation_date": datetime.now().isoformat(),
                "evaluator_id": "human_reviewer",
                "evaluation_version": "1.0",
                "overall_score": overall_score
            },
            "detailed_scores": detailed_scores,
            "improvement_analysis": {
                "tags": improvement_tags + strength_tags,
                "strengths": strength_tags,
                "minor_improvements": improvement_tags
            },
            "comments": self.comment_text.get(1.0, tk.END).strip(),
            "[CONTENT_KEY]": "[MODIFY THIS TO MATCH YOUR CONTENT STRUCTURE]",  # Add your content structure here
            "system_learning": {
                "example_quality": "high" if overall_score >= 8.0 else "medium" if overall_score >= 6.0 else "low",
                "use_as_training": overall_score >= 8.0,
                "key_patterns": strength_tags
            }
        }
        
        # Save to 5_labeled_json
        labeled_dir = Path(__file__).parent.parent / "5_labeled_json"
        labeled_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"{self.current_file.stem}_{timestamp}_labeled.json"
        output_path = labeled_dir / output_filename
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(evaluation_data, f, indent=2, ensure_ascii=False)
            
            messagebox.showinfo("Success", f"Evaluation saved to:\n{output_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not save evaluation: {e}")

def main():
    root = tk.Tk()
    app = EvaluationGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
```

---

## **Step 4: Documentation Files**

### ✅ README.md
```markdown
# [Agent Name]

## Purpose
[Business logic description - what this agent does]

## Inputs
- [Input file 1]: [Description]
- [Input file 2]: [Description]

## Outputs  
- [Output file]: [Description and format]

## Usage
```bash
cd [agent_folder]
python scripts/generate_simple.py
```

## Integration
This agent is part of the AI Marketing Asset Pipeline:
- **Position**: Agent [X] in pipeline
- **Depends on**: [List of input agents]
- **Feeds into**: [List of downstream agents]

## Evaluation
Use the evaluation script to maintain quality:
```bash
python scripts/evaluate.py
```

Score criteria: [List your 5 criteria]
```

### ✅ QUICK_START.md
```markdown
# Quick Start Guide

## 1. Setup
1. Ensure config.json has your API key
2. Place input files in `1_input/` or `1_input/{project_name}/`

## 2. Generate Content
```bash
python scripts/generate_simple.py
```

## 3. Review Output
Check `3_unlabeled/` or `3_unlabeled/{project_name}/` for generated content

## 4. Evaluate (Optional)
```bash
python scripts/evaluate.py
```

## Common Issues
- **No API key**: Update config.json
- **No input files**: Check 1_input/ directory
- **API errors**: Check internet connection and API credits
```

---

## **Step 5: Integration Checklist**

### ✅ Pipeline Integration (If applicable)
1. **Add to Agent 0a Configurator**:
   - Update project creation to include your agent
   - Add industry-specific system prompt generation

2. **Add to Agent 0b Orchestrator**:
   - Include in appropriate phase (Phase 1 or Phase 2)
   - Define input dependencies 
   - Add file copying logic

3. **Update Documentation**:
   - Add agent to main blueprint
   - Update execution guide
   - Add to dependency matrix

### ✅ Testing Checklist
1. **Manual Testing**:
   - [ ] Agent creates output file
   - [ ] Output format is correct
   - [ ] Project-specific paths work
   - [ ] Legacy paths work (backward compatibility)
   - [ ] Evaluation script works
   - [ ] Pipeline integration works

2. **Content Quality**:
   - [ ] Business logic produces expected results
   - [ ] Output matches specifications
   - [ ] Iterate system learns from evaluations
   - [ ] System prompts are effective

---

## **Customization Points**

### ✅ Business Logic Sections to Modify

1. **system_prompt.md**: Your specific instructions and requirements
2. **generate_simple.py**:
   - `[CONTENT_KEY]` - Key for content in JSON examples
   - `[AGENT_PREFIX]` - Filename prefix for outputs
   - `load_example_from_json()` - Example formatting template
   - `generate_content()` - Prompt construction and instructions
   - Input file detection logic in `main()`

3. **evaluate.py**:
   - `self.criteria` - Your 5 scoring criteria
   - `self.improvement_tags` - Relevant improvement areas
   - `self.strength_tags` - Relevant strength areas
   - `[CONTENT_KEY]` - Match your content structure

### ✅ Foundation Sections (DO NOT MODIFY)
- Project path handling
- API calling logic
- File saving patterns
- Configuration loading
- Error handling
- Timestamp naming

---

This template maintains **100% consistency** with existing agents while allowing **complete customization** of business logic. The foundation stays identical - only your specific requirements change.