# Project Structure Guide

This document provides a complete navigation guide to the AI-Go-To-Market-Engine repository structure.

## 📁 Repository Overview

The AI-Go-To-Market-Engine is organized into clear functional areas, each serving a specific purpose in the overall system architecture.

```
AI-Go-To-Market-Engine/
├── README.md                    ← Main project overview
├── docs/                        ← User-facing documentation (YOU ARE HERE)
├── agents/                      ← Core agent system (11 agents)
├── examples/                    ← Complete usage examples & templates
├── technical_specifications/    ← Complete technical documentation, implementation details & diagrams, System design history & evolution
├── contrib/                     ← Framework extension resources
└── config.template.json         ← API configuration template
```

---

## 📋 Detailed Folder Structure

### **`agents/` - Core Agent System**
**Purpose**: The actual AI agent pipeline (11 agents)

```
agents/
├── agent_0a_configurator/       ← Project setup & configuration
├── agent_0b_orchestrator/       ← Pipeline execution & orchestration
├── message_house_agent/         ← Agent 1: Strategic foundation
├── user_story_agent/            ← Agent 2: Brand personas
├── user_story_real_reviews_agent/ ← Agent 3: Customer reality analysis
├── gap_analysis_agent/          ← Agent 4: Strategic gap analysis
├── keywords_bank_agent/         ← Agent 5: Keywords engine (quality gate)
├── stakeholder_persona_agent/   ← Agent 6: Stakeholder strategy decks  
├── platform_persona_agent/     ← Agent 6.5: Platform intelligence plugin
├── testimonial_agent/           ← Agent 7: Testimonial generation
├── social_media_twitter_agent/  ← Agent 8: Social media content
├── website_copy_agent/          ← Agent 9: Website copy with psychology logic
└── consistency_check_agent/     ← Agent 10: Consistency validation
```

**Each Agent Contains:**
- `README.md` - Agent documentation
- `1_input/` - Input files and templates  
- `2_system_assets/` - System prompts and examples
- `3_unlabeled/` - Generated outputs
- `5_labeled_json/` - Quality evaluations (learning data)
- `scripts/` - Execution scripts
- `config.json` - API configuration

### **`docs/` - User Documentation**  
**Purpose**: Essential user-facing guides and navigation

- `README.md` - Documentation navigation (YOU ARE HERE)
- `GETTING_STARTED.md` - Setup and first run guide
- `PROJECT_STRUCTURE.md` - This complete folder guide

### **`examples/` - Usage Examples & Templates**
**Purpose**: Complete end-to-end project examples and user templates

- Sample projects (SaaS, e-commerce, service business) with input files and expected outputs
- Input templates for strategic questions and customer reviews
- Quick start workflows and minimal examples
- Template files for new users to copy and customize

### **`technical_specifications/` - Complete Technical Documentation**
**Purpose**: All technical documentation, implementation details, diagrams, and system design history

**Contains:**
- **System Architecture** - Complete system design and technical specifications
- **Implementation Details** - Data architecture, API documentation, integration guides
- **Visual Documentation** - System flowcharts, diagrams, and architecture visualization
- **Design History** - System evolution from v2.2 to v3.0, design decisions and rationale
- **Development Specifications** - Technical standards and implementation requirements

**Key Files:**
- `data_store_specification.md` - Multi-project data architecture
- `diagrams/pipeline_diagrams.md` - Complete system flowcharts (Mermaid format)
- System architecture documents (consolidated from blueprints)
- Historical design evolution and version changes
- **START HERE** for complete technical understanding

### **`contrib/` - Framework Extension Resources**
**Purpose**: Tools and templates for extending and contributing to the system

- `AGENT_DEVELOPMENT_TEMPLATE.md` - Agent creation guide
- `SCRIPT_PATTERNS_LIBRARY.py` - Code templates and patterns
- `DATA_STRUCTURE_STANDARDS.md` - Folder structure and naming standards
- `INTEGRATION_CHECKLIST.md` - Pipeline integration guide
- Development tools for building new agents and extending functionality

---

## 🎯 Quick Navigation by Use Case

### **"I Want to Try the System"**
1. [`GETTING_STARTED.md`](GETTING_STARTED.md) - Setup and first run
2. [`../examples/`](../examples/) - Sample projects and templates
3. [`../examples/12_questions_template.md`](../examples/12_questions_template.md) - Strategic questions template

### **"I Want to Understand the Architecture"**
1. [`../technical_specifications/`](../technical_specifications/) - **PRIMARY TECHNICAL REFERENCE**
2. [`../technical_specifications/diagrams/pipeline_diagrams.md`](../technical_specifications/diagrams/pipeline_diagrams.md) - Visual system flowcharts
3. Complete system architecture and design documents (consolidated technical documentation)

### **"I Want to Run the Full Pipeline"**
1. [`../agents/agent_0a_configurator/`](../agents/agent_0a_configurator/) - Project setup and configuration
2. [`../agents/agent_0b_orchestrator/`](../agents/agent_0b_orchestrator/) - Automated pipeline execution
3. [`../agents/keywords_bank_agent/scripts/evaluate_phase1.py`](../agents/keywords_bank_agent/) - Quality gate evaluation

### **"I Want to Extend the System"**
1. [`../contrib/AGENT_DEVELOPMENT_TEMPLATE.md`](../contrib/AGENT_DEVELOPMENT_TEMPLATE.md) - Agent creation guide
2. [`../contrib/INTEGRATION_CHECKLIST.md`](../contrib/INTEGRATION_CHECKLIST.md) - Pipeline integration guide
3. [`../technical_specifications/`](../technical_specifications/) - Complete implementation specifications

---

## 📊 Agent Execution Sequence

The agents run in a specific order based on dependencies:

**Phase 0: Setup**
- Agent 0a → Agent 0b (Configuration & Orchestration)

**Phase 1: Foundation**  
- Agent 1 → Agent 2 → Agent 3 → Agent 4 (Strategic foundation)

**Phase 2: Content Generation**
- Agent 5 (Quality Gate) → Agent 7, 8, 9 (Content creation)

**Phase 3: Optional**
- Agent 6, 6.5, 10 (Enhanced features)

---

## 🔗 Key Template Files

### **Strategic Input Templates**
- [`../examples/12_questions_template.md`](../examples/12_questions_template.md) - Strategic questions template

### **Configuration Templates** 
- [`../config.template.json`](../config.template.json) - API configuration template

### **Development Templates**
- [`../contrib/AGENT_DEVELOPMENT_TEMPLATE.md`](../contrib/AGENT_DEVELOPMENT_TEMPLATE.md) - New agent creation
- [`../contrib/SCRIPT_PATTERNS_LIBRARY.py`](../contrib/SCRIPT_PATTERNS_LIBRARY.py) - Code patterns

---

## ⚡ Workflow Priority

**PRIMARY SOURCE OF TRUTH:**
1. **[`../technical_specifications/`](../technical_specifications/)** → Your MAIN reference for complete system understanding and technical details

**DEVELOPMENT SUPPORT:**
2. **[`../contrib/`](../contrib/)** → When creating new agents or extending the system
3. **[`../examples/`](../examples/)** → Sample projects and templates for users

**Always start with technical_specifications for complete system understanding, then use this structure guide for navigation.**

---

*For complete system architecture and technical details, see [`../technical_specifications/`](../technical_specifications/)*