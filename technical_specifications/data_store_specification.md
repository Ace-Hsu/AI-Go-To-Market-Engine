# Data Store Structure Specification

## Overview

This document defines the file organization structure for the AI Agent Pipeline system. Each project runs in complete isolation with dedicated folders across all agents.

---

## Project-Based Structure

### Core Architecture
```
{agent_name}/
├── 1_input/{project_name}/           # Project inputs
├── 2_system_assets/{project_name}/   # Project-specific prompts
├── 3_unlabeled/{project_name}/       # Project outputs
├── 4_labeled_md/                     # Quality assets (shared)
└── 5_labeled_json/                   # Learning data (shared)
```

### Project Naming Convention
```
Format: {product_type}_{descriptive_name}_{YYYYMMDD}

Examples:
├── saas_projectmgmt_20250124/
├── health_turmeric_20250124/
├── finance_budgetapp_20250124/
└── competitor_asana_20250124/
```

---

## Complete Agent Directory Structure

### v2.7 Pipeline Agents (11 Total)

```
message_house_agent/
├── 1_input/
│   ├── saas_projectmgmt_20250124/
│   │   └── qa_session_content.md
│   └── health_turmeric_20250124/
│       └── qa_session_content.md
├── 2_system_assets/
│   ├── saas_projectmgmt_20250124/
│   │   └── system_prompt.md
│   └── health_turmeric_20250124/
│       └── system_prompt.md
└── 3_unlabeled/
    ├── saas_projectmgmt_20250124/
    │   └── messagehouse_saas_20250124_143022.md
    └── health_turmeric_20250124/
        └── messagehouse_health_20250124_150315.md

user_story_agent/
├── 1_input/{project_name}/
├── 2_system_assets/{project_name}/
└── 3_unlabeled/{project_name}/

user_story_real_reviews_agent/
├── 1_input/{project_name}/
├── 2_system_assets/{project_name}/
└── 3_unlabeled/{project_name}/

gap_analysis_agent/
├── 1_input/{project_name}/
├── 2_system_assets/{project_name}/
└── 3_unlabeled/{project_name}/

keywords_bank_agent/
├── 1_input/{project_name}/
├── 2_system_assets/{project_name}/
└── 3_unlabeled/{project_name}/

stakeholder_persona_agent/
├── 1_input/{project_name}/
├── 2_system_assets/{project_name}/
└── 3_unlabeled/{project_name}/

platform_persona_agent/
├── 1_input/{project_name}/
├── 2_system_assets/{project_name}/
└── 3_unlabeled/{project_name}/

testimonial_agent/
├── 1_input/{project_name}/
├── 2_system_assets/{project_name}/
└── 3_unlabeled/{project_name}/

social_media_twitter_agent/
├── 1_input/{project_name}/
├── 2_system_assets/{project_name}/
└── 3_unlabeled/{project_name}/

website_copy_agent/
├── 1_input/{project_name}/
├── 2_system_assets/{project_name}/
└── 3_unlabeled/{project_name}/

consistency_check_agent/
├── 1_input/{project_name}/
├── 2_system_assets/{project_name}/
└── 3_unlabeled/{project_name}/
```

---

## File Location Map

### Phase 1: Foundation Assets

| **Asset Type** | **Agent** | **Location** | **Filename Pattern** |
|----------------|-----------|--------------|---------------------|
| Message House | Agent 1 | `message_house_agent/3_unlabeled/{project}/` | `messagehouse_{project}_{timestamp}.md` |
| Brand Personas | Agent 2 | `user_story_agent/3_unlabeled/{project}/` | `brandside_personas_{project}_{timestamp}.md` |
| Customer Personas | Agent 3 | `user_story_real_reviews_agent/3_unlabeled/{project}/` | `customerside_personas_{project}_{timestamp}.md` |
| Gap Analysis | Agent 4 | `gap_analysis_agent/3_unlabeled/{project}/` | `gap_analysis_{project}_{timestamp}.md` |

### Phase 2: Content Assets

| **Asset Type** | **Agent** | **Location** | **Filename Pattern** |
|----------------|-----------|--------------|---------------------|
| Keywords Bank | Agent 5 | `keywords_bank_agent/3_unlabeled/{project}/` | `keywords_bank_{project}_{timestamp}.md` |
| Testimonials | Agent 7 | `testimonial_agent/3_unlabeled/{project}/` | `testimonials_{project}_{timestamp}.md` |
| Social Media | Agent 8 | `social_media_twitter_agent/3_unlabeled/{project}/` | `twitter_content_{project}_{timestamp}.md` |
| Website Copy | Agent 9 | `website_copy_agent/3_unlabeled/{project}/` | `website_copy_{project}_{timestamp}.md` |

### Optional Enhancements

| **Asset Type** | **Agent** | **Location** | **Filename Pattern** |
|----------------|-----------|--------------|---------------------|
| Stakeholder Decks | Agent 6 | `stakeholder_persona_agent/3_unlabeled/{project}/` | `stakeholder_decks_{project}_{timestamp}.md` |
| Platform Intelligence | Agent 6.5 | `platform_persona_agent/3_unlabeled/{project}/` | `platform_personas_{project}_{timestamp}.md` |
| Consistency Report | Agent 10 | `consistency_check_agent/3_unlabeled/{project}/` | `consistency_report_{project}_{timestamp}.md` |

---

## Agent Configuration

### config.json Structure
Each agent contains a `config.json` file specifying the current project:

```json
{
  "anthropic_api_key": "sk-ant-api03-...",
  "current_project": "saas_projectmgmt_20250124",
  "model": "claude-3-5-sonnet-20241022",
  "max_tokens": 4000,
  "temperature": 0.7
}
```

### System Prompts
Industry-specific prompts are stored in:
```
{agent_name}/2_system_assets/{project_name}/system_prompt.md
```

---

## File Flow Between Agents

### Pipeline Asset Flow
```
Agent 1 Output  →  Agent 2,4,6 Input
Agent 2 Output  →  Agent 4,6,6.5 Input  
Agent 3 Output  →  Agent 4,6.5 Input
Agent 4 Output  →  [Keywords Evaluation Gate]
Agent 5 Output  →  Agent 7,8,9 Input
Agent 7,8,9 Output  →  Agent 10 Input
```

### File Copy Operations
Agent 0b orchestrator handles all file copying between agents:
```
Source: {source_agent}/3_unlabeled/{project}/
Target: {target_agent}/1_input/{project}/
```

---

## Project Management

### Active Projects
Projects are managed through Agent 0 system:
- **Agent 0a**: Creates project structure and configurations
- **Agent 0b**: Executes pipeline within project boundaries

### Project Discovery
Each agent automatically detects available projects by scanning:
```
{agent_name}/1_input/*/
{agent_name}/2_system_assets/*/
{agent_name}/3_unlabeled/*/
```

---

## Quick Reference Examples

### Finding a Specific Asset
**Question**: Where is the keywords bank for the SaaS project?
**Answer**: `keywords_bank_agent/3_unlabeled/saas_projectmgmt_20250124/keywords_bank_*.md`

### Setting Up New Project
**Question**: What folders need to be created for a new health project?
**Answer**: Create `health_supplement_20250124/` folder in `1_input/`, `2_system_assets/`, and `3_unlabeled/` for all 11 agents.

### Project Isolation Check  
**Question**: How do I verify projects don't mix files?
**Answer**: Each project name appears only in its dedicated subfolders across all agents.

---

## Storage Specifications

### Disk Usage Per Project
- **Foundation assets**: ~200KB (4 files)
- **Content assets**: ~800KB (4 files)  
- **Optional assets**: ~400KB (3 files)
- **Total per project**: ~1.4MB average

### Scaling Considerations
- **100 projects**: ~140MB storage
- **500 projects**: ~700MB storage
- **1000 projects**: ~1.4GB storage

---

*This structure ensures complete project isolation, prevents file collisions, and enables systematic asset organization across the entire AI agent pipeline.*