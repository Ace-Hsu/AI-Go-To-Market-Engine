# Data Structure Standards - Folder Structure, Naming Conventions, File Formats

## Overview

This document defines the exact standards for folder structures, file naming, and data formats that ALL agents must follow to maintain system consistency and enable seamless integration.

---

## **Standard Agent Folder Structure**

### ✅ Required Folder Structure (Every Agent Must Have)

```
{agent_name}/
├── 1_input/                          ← Input files storage
│   └── {project_name}/               ← Project-specific inputs (auto-created by Agent 0a)
├── 2_system_assets/                  ← System prompts and configuration
│   ├── {project_name}/               ← Project-specific system prompts (auto-created by Agent 0a)
│   ├── examples/                     ← Reference examples (optional)
│   ├── system_prompt.md              ← Default system prompt (required)
│   └── output_template.md            ← Output format template (optional)
├── 3_unlabeled/                      ← Generated outputs before evaluation
│   └── {project_name}/               ← Project-specific outputs
├── 4_labeled_md/                     ← Evaluated content (legacy support)
├── 5_labeled_json/                   ← Evaluation data for iterate system
├── scripts/                          ← All Python scripts
│   ├── generate_simple.py            ← Main generation script (required)
│   └── evaluate.py                   ← Evaluation script (optional)
├── config.json                       ← Agent configuration (required)
├── requirements.txt                  ← Dependencies (standard format)
├── README.md                         ← Agent documentation (required)
├── QUICK_START.md                    ← Usage instructions (required)
└── test_system.py                    ← Test script (optional)
```

### ✅ Folder Purpose and Usage Rules

| Folder | Purpose | File Types | Naming Convention | Auto-Created |
|--------|---------|------------|-------------------|--------------|
| `1_input/` | Input files for processing | `.md, .csv, .json, .txt` | Descriptive names | Manual |
| `1_input/{project}/` | Project-specific inputs | Same as above | Same as above | Agent 0a |
| `2_system_assets/` | System configuration | `.md, .json` | `system_prompt.md`, `output_template.md` | Manual |
| `2_system_assets/{project}/` | Project-specific prompts | `.md` | `system_prompt.md` | Agent 0a |
| `3_unlabeled/` | Raw generated outputs | `.md, .json, .txt` | `{prefix}_{timestamp}.md` | Scripts |
| `3_unlabeled/{project}/` | Project-specific outputs | Same as above | Same as above | Scripts |
| `4_labeled_md/` | Quality-approved content | `.md` | `{prefix}_{timestamp}_approved.md` | Manual |
| `5_labeled_json/` | Evaluation metadata | `.json` | `{filename}_{timestamp}_labeled.json` | Evaluation |
| `scripts/` | Python executable files | `.py` | `{purpose}.py` or `{purpose}_simple.py` | Manual |

---

## **File Naming Conventions**

### ✅ Generated Output Files

**Standard Pattern**: `{agent_prefix}_{timestamp}.{extension}`

**Examples**:
```
messagehouse_20250731_143022.md
userstories_20250731_143045.md
testimonials_20250731_143108.md
gap_analysis_20250731_143125.md
keywords_bank_vocabulary_20250731_143140.md
keywords_bank_expansion_20250731_143155.md
twitter_posts_20250731_143210.md
website_copy_20250731_143225.md
```

**Timestamp Format**: `YYYYMMDD_HHMMSS` (24-hour format)

### ✅ Agent Prefix Standards

| Agent | Prefix | Example Output |
|-------|--------|----------------|
| message_house_agent | `messagehouse` | `messagehouse_20250731_143022.md` |
| user_story_agent | `userstories` | `userstories_20250731_143045.md` |
| user_story_real_reviews_agent | `userstories_reviews` | `userstories_reviews_20250731_143100.md` |
| gap_analysis_agent | `gap_analysis` | `gap_analysis_20250731_143125.md` |
| keywords_bank_agent | `keywords_bank_vocabulary` (Phase 1)<br>`keywords_bank_expansion` (Phase 2) | `keywords_bank_vocabulary_20250731_143140.md`<br>`keywords_bank_expansion_20250731_143155.md` |
| testimonial_agent | `testimonials` | `testimonials_20250731_143108.md` |
| social_media_twitter_agent | `twitter_posts` | `twitter_posts_20250731_143210.md` |
| website_copy_agent | `website_copy` | `website_copy_20250731_143225.md` |

### ✅ Evaluation Files

**Standard Pattern**: `{original_filename}_{timestamp}_labeled.json`

**Examples**:
```
messagehouse_20250731_143022_20250731_150030_labeled.json
userstories_20250731_143045_20250731_150045_labeled.json
testimonials_20250731_143108_20250731_150100_labeled.json
```

### ✅ Project Naming Convention

**Standard Pattern**: `{industry}_{product}_{timestamp}`

**Examples**:
```
dietary_supplement_ourjrney_nano_turmeric_drink_mix_20250722
intimate_care_femininewash2.0_20250729
saas_personathink_20250725
health_supplements_companyname_20250801
```

**Industry Categories**:
- `dietary_supplement`
- `intimate_care`
- `saas`
- `health_supplements`
- `fitness_equipment`
- `beauty_products`
- `financial_services`
- `ecommerce_platform`

---

## **File Format Standards**

### ✅ Configuration Files

#### **config.json (Required in Every Agent)**
```json
{
  "anthropic_api_key": "your_api_key_here",
  "model": "claude-3-5-sonnet-20241022",
  "max_tokens": 2000,
  "temperature": 0.3,
  "current_project": null
}
```

**Field Specifications**:
- `anthropic_api_key`: String, API key for Claude
- `model`: String, exact model identifier
- `max_tokens`: Integer, 1000-4000 range
- `temperature`: Float, 0.0-1.0 range
- `current_project`: String or null, project folder name

#### **requirements.txt (Standard Format)**
```
# Standard agents use no external dependencies
# All agents use Python stdlib (urllib) for API calls
# Add dependencies only if business logic requires them

# Example for agents with special requirements:
# pandas>=1.3.0
# numpy>=1.21.0
```

### ✅ System Prompt Files

#### **system_prompt.md (Required)**
```markdown
You are [ROLE DESCRIPTION - specific to business logic].

[BUSINESS LOGIC SPECIFIC INSTRUCTIONS]

Key requirements:
- [Requirement 1]
- [Requirement 2]
- [Output format specifications]
- [Quality standards]

Maintain [TONE/STYLE] while ensuring [SPECIFIC OUTCOMES].
```

### ✅ Output Content Files

#### **Markdown Output Format (.md)**
- **Encoding**: UTF-8
- **Line Endings**: LF (Unix style)
- **Headers**: Use `#`, `##`, `###` format
- **Tables**: Use GitHub-flavored markdown format
- **Code Blocks**: Use triple backticks with language specification

#### **JSON Output Format (.json)**
- **Encoding**: UTF-8
- **Indentation**: 2 spaces
- **Key Format**: snake_case
- **Date Format**: ISO 8601 (`YYYY-MM-DDTHH:mm:ssZ`)

### ✅ Evaluation Data Format

#### **Labeled JSON Structure (5_labeled_json/)**
```json
{
  "evaluation_metadata": {
    "document_id": "string - original filename without extension",
    "original_file_path": "string - relative path to original file",
    "evaluation_date": "string - ISO 8601 datetime",
    "evaluator_id": "string - human_reviewer or system_id",
    "evaluation_version": "string - version number",
    "overall_score": "number - float 0.0-10.0"
  },
  "detailed_scores": {
    "criteria_1": {
      "score": "number - int 1-10",
      "weight": "number - float 0.0-1.0",
      "comments": "string - evaluation comments"
    },
    "criteria_2": {
      "score": "number - int 1-10", 
      "weight": "number - float 0.0-1.0",
      "comments": "string - evaluation comments"
    }
  },
  "improvement_analysis": {
    "tags": ["array of strings - all tags"],
    "strengths": ["array of strings - strength tags"],
    "minor_improvements": ["array of strings - improvement tags"]
  },
  "comments": "string - human evaluator comments",
  "[content_key]": "object - actual content structure for iterate system",
  "system_learning": {
    "example_quality": "string - high/medium/low",
    "use_as_training": "boolean - true if score >= 8.0",
    "key_patterns": ["array of strings - successful patterns"]
  }
}
```

---

## **Path Handling Standards**

### ✅ Project-Aware Path Resolution

All agents must support both project-specific and legacy paths:

```python
def get_project_paths(config_file="config.json"):
    config_path = Path(__file__).parent.parent / config_file
    config = json.load(open(config_path))
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
```

### ✅ Absolute vs Relative Paths

**Always Use Absolute Paths**:
- All file operations must use absolute paths
- Path construction relative to script location: `Path(__file__).parent.parent`
- Never use relative paths like `../` or `./`

**Path Construction Pattern**:
```python
# Correct
agent_root = Path(__file__).parent.parent
config_path = agent_root / "config.json"
input_path = agent_root / "1_input" / "file.md"

# Incorrect
config_path = "../config.json"
input_path = "./1_input/file.md"
```

---

## **Integration Standards**

### ✅ Agent Dependencies File Format

Each agent should document its dependencies in README.md:

```markdown
## Dependencies

### Input Dependencies
- **Agent 1**: message_house.md
- **Agent 2**: brand_side_persona.md

### Output Used By
- **Agent 7**: Uses this agent's output as input
- **Agent 8**: Uses this agent's output as input

### Integration Points
- **Phase**: 1 or 2
- **Mode Requirements**: validation_mode, new_brand_mode, or both
- **Quality Gates**: None or evaluation_required
```

### ✅ File Copy Patterns (For Pipeline Integration)

When an agent's output becomes another agent's input:

```python
# Standard file copying pattern
def copy_to_dependent_agent(source_file, target_agent, project_name=None):
    if project_name:
        target_dir = Path(f"../{target_agent}/1_input/{project_name}")
    else:
        target_dir = Path(f"../{target_agent}/1_input")
    
    target_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_file, target_dir / source_file.name)
```

---

## **Quality Standards**

### ✅ File Size Limits

| File Type | Maximum Size | Typical Size |
|-----------|--------------|--------------|
| System Prompts (.md) | 10 KB | 1-3 KB |
| Input Files (.md) | 100 KB | 10-50 KB |
| Output Files (.md) | 200 KB | 20-100 KB |
| Evaluation Files (.json) | 50 KB | 5-20 KB |
| Configuration (.json) | 5 KB | 1 KB |

### ✅ Content Standards

**Markdown Files**:
- Clear headers with proper hierarchy
- No empty sections
- Consistent formatting
- No trailing whitespace

**JSON Files**:
- Valid JSON syntax
- Consistent indentation (2 spaces)
- No trailing commas
- Meaningful key names

**Text Encoding**:
- UTF-8 encoding for all files
- LF line endings (Unix style)
- No BOM (Byte Order Mark)

---

## **Validation Checklist**

### ✅ Agent Structure Validation

Before deploying any agent, verify:

- [ ] All required folders exist
- [ ] config.json follows standard format
- [ ] system_prompt.md exists and is properly formatted
- [ ] generate_simple.py follows standard patterns
- [ ] File naming follows conventions
- [ ] Path handling supports both project and legacy modes
- [ ] Integration dependencies are documented
- [ ] README.md and QUICK_START.md exist

### ✅ Runtime Validation

During agent execution, verify:

- [ ] Input files are found correctly
- [ ] Output files are created with proper naming
- [ ] API calls succeed
- [ ] Project paths resolve correctly
- [ ] Error handling works properly
- [ ] Success messages display correct paths

### ✅ Integration Validation

For pipeline integration, verify:

- [ ] Agent integrates with Agent 0a configurator
- [ ] Agent integrates with Agent 0b orchestrator (if applicable)
- [ ] File copying works between dependent agents
- [ ] Project isolation is maintained
- [ ] Backward compatibility is preserved

---

These standards ensure **100% consistency** across all agents while maintaining **complete flexibility** for business logic customization. Follow these standards exactly to ensure seamless integration with the existing pipeline.