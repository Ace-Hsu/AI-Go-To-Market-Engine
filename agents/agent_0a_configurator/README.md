# Agent 0a: Project Configurator - Complete System

## Overview
A comprehensive project initialization system that creates complete workspace structures and industry-specific prompts across the entire AI agent pipeline. Run ONCE per new project to establish project-isolated folders and optimized system prompts for all downstream agents.

## System Architecture

```
Interactive Setup ← User Input (Product Type, Industry Focus, Product Name)
    ↓
Claude API Call → Industry-Specific Prompt Generation (8 Agents)
    ↓
Folder Creation → Project Structure Across All Agents
    ↓
Config Updates → Agent Preparation for Pipeline Execution
    ↓
3_unlabeled/ → Project Setup Log (JSON) → Ready for Agent 0b
```

## Directory Structure

- **`1_input/`** - Project configuration templates
- **`2_system_assets/`** - Prompt generation templates and examples
- **`3_unlabeled/`** - Project setup logs and completion records
- **`5_labeled_json/`** - (Not used - no evaluation system)
- **`scripts/`** - Project configuration and workspace creation tools
- **`config.json`** - Claude API configuration and agent list

## Core Components

### Input System
- **Interactive Setup**: Command-line prompts for project details
- **Product Types**: SaaS, Health, Finance, Ecommerce, Beauty, Food, Tech, Education
- **Industry Focus**: Target market and user demographics
- **Project Naming**: Automated timestamp-based project identification

### Generation System  
- **Script**: `scripts/generate_simple.py`
- **API**: Claude 3.5 Sonnet integration for prompt generation
- **Multi-Agent Setup**: Creates workspace for all 8 core agents simultaneously
- **Output**: Complete project workspace with industry-optimized prompts

### Evaluation System
- **Design**: No evaluation system - one-time setup agent
- **Validation**: Project structure verification and configuration updates
- **Logging**: Setup completion tracking and error handling

### Learning System
- **Architecture**: No iterative learning - deterministic setup process
- **Intelligence**: Industry-specific prompt optimization per project type
- **Consistency**: Standardized folder structure across all projects

## Advanced Project Orchestration

### **Core Innovation: Industry-Specific Pipeline Preparation**

**Intelligence Behind Agent 0a:**
- Analyzes product type and industry to generate optimized system prompts for each downstream agent
- Creates project-isolated workspace preventing cross-contamination between different products
- Configures entire pipeline with single setup command

### **Project Isolation Architecture:**
```
{agent_name}/
├── 1_input/{project_name}/           ← Project-specific inputs
├── 2_system_assets/{project_name}/   ← Industry-optimized prompts  
├── 3_unlabeled/{project_name}/       ← Project-specific outputs
```

### **Industry Optimization Engine:**
- **Health Products**: Wellness terminology, FDA compliance awareness, customer psychology
- **SaaS Products**: B2B language, technical features, user adoption patterns
- **Finance Products**: Trust-building, regulatory awareness, ROI-focused messaging
- **Ecommerce Products**: Purchase psychology, seasonal patterns, conversion optimization

### **8-Agent Prompt Generation Process:**
1. **Message House Agent**: Strategic positioning system prompts
2. **User Story Agent**: Brand persona development system prompts
3. **User Story Real Reviews Agent**: Customer analysis system prompts
4. **Gap Analysis Agent**: Strategic comparison system prompts
5. **Keywords Bank Agent**: Vocabulary development system prompts
6. **Testimonial Agent**: Authentic voice generation system prompts
7. **Social Media Twitter Agent**: Platform-specific content system prompts
8. **Website Copy Agent**: Conversion-focused copy system prompts

## Key Features

✅ **One-Command Setup** - Complete pipeline preparation with single execution  
✅ **Industry Intelligence** - Claude API-generated prompts optimized per product type  
✅ **Project Isolation** - Multi-project workspace with zero cross-contamination  
✅ **8-Agent Configuration** - Simultaneous setup across entire core pipeline  
✅ **Automated Naming** - Timestamp-based project identification system  

## Quick Start

**Basic Workflow:**
1. `python scripts/generate_simple.py` → Interactive project setup
2. Provide project details → Industry type, product name, target market
3. Confirm setup → Automated workspace creation across 8 agents
4. **Result**: Complete project ready for Agent 0b pipeline execution

## System Intelligence

**Project Management Architecture:**
- **Smart Naming**: Automatic project naming with format `{type}_{product}_{timestamp}`
- **Folder Creation**: 24+ folders created across 8 agents (3 folders per agent)
- **Prompt Optimization**: Industry-specific system prompts generated via Claude API
- **Configuration Management**: All agent config.json files updated with current project

**Multi-Project Capability:**
- **Workspace Isolation**: Each project exists in separate folder structure
- **Backward Compatibility**: Existing projects unaffected by new project creation
- **Scale Management**: Supports unlimited concurrent projects

## Technical Notes

- **API**: Claude 3.5 Sonnet via Anthropic API (for prompt generation only)
- **Language**: Python 3.x with urllib (no external dependencies)
- **Dependencies**: Standard library only (json, os, pathlib, datetime)
- **Encoding**: UTF-8 throughout for international character support
- **Platform**: Cross-platform compatible

## Quality Standards

Project setup is validated on:
- **Folder Creation Success**: All 24+ folders created across 8 agents
- **Prompt Generation Quality**: Industry-specific system prompts generated for each agent
- **Configuration Updates**: All agent config.json files properly updated
- **Project Naming**: Consistent timestamp-based naming convention
- **Workspace Isolation**: No interference with existing projects

**Success Criteria**: 100% folder creation + 8 system prompts + 8 config updates

## Input Requirements

**Interactive Setup Prompts:**
- **Product Name**: Clear, descriptive product identifier
- **Product Type**: Selection from supported types or custom entry
- **Industry Focus**: Target market description (e.g., "wellness consumers", "B2B teams")

**Configuration Requirements:**
- **Valid API Key**: Anthropic Claude API key in config.json
- **Base Path**: Correct agent folder structure in file system
- **Agent List**: Updated agent_list in config.json for new agents

## Output Format

**Project Workspace Structure:**
```
8 Agents × 3 Folders = 24+ Total Folders Created:
message_house_agent/1_input/{project_name}/
message_house_agent/2_system_assets/{project_name}/system_prompt.md
message_house_agent/3_unlabeled/{project_name}/
[...repeated for all 8 agents]
```

**Generated Assets:**
- **8 System Prompts**: Industry-optimized system prompts in each agent's 2_system_assets folder
- **8 Config Updates**: current_project field updated in each agent's config.json
- **1 Setup Log**: JSON log file in agent_0a_configurator/3_unlabeled/

## Integration with Agent Pipeline

**Position**: Phase 0 - System Configuration (Pre-Pipeline)

**Downstream Dependencies:**
- **Agent 0b**: Orchestrator requires completed project setup for execution
- **Agents 1-9**: All agents require project folders and system prompts before operation

**Upstream Requirements:**
- **Human Input**: Strategic business details for industry optimization
- **File System**: Proper agent folder structure in base directory

**Pipeline Activation:**
- **Setup Complete**: Agent 0a creates workspace
- **Input Files**: Human places content in appropriate 1_input folders
- **Pipeline Execution**: Agent 0b orchestrates generation across all agents

## v3.0 Blueprint Alignment

This agent fully implements the v3.0 specifications:
- **Phase 0 Architecture**: Complete system configuration and workspace preparation
- **Multi-Project Support**: Project-isolated folder structure with timestamp naming
- **Industry Intelligence**: Claude API-powered prompt optimization per product type
- **8-Agent Pipeline**: Full support for core pipeline agents (1,2,3,4,5,7,8,9)
- **Plugin Ready**: Folder structure supports optional Agent 6 (Stakeholder) and Agent 6.5 (Platform)
- **Orchestrator Integration**: Seamless handoff to Agent 0b for pipeline execution

---

*A complete project initialization system for multi-project AI agent pipeline management.*