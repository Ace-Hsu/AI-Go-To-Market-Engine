# Agent 0b: Pipeline Orchestrator - Complete System

## Overview
The most sophisticated orchestration system in the pipeline, featuring two-phase execution architecture with state persistence, dependency management, and quality control checkpoints. Automates the entire AI agent pipeline with intelligent mode detection and resume functionality.

## System Architecture

```
Phase 1: Foundation Building (Agents 1-4)
Agent 0a Setup → Interactive Project Selection → Mode Detection
    ↓
State Management → Agent 1→2→3→4 → Agent 5 Keywords Phase 1 
    ↓
Evaluation Checkpoint (≥7.0 Score Required)
    ↓  
Phase 2: Content Generation (Agents 5,7,8,9)
Keywords Validation → Agent 5→7→8→9 → Final Asset Portfolio
    ↓
2_system_assets/ → Execution State Tracking (JSON)
3_unlabeled/ → Pipeline Execution Reports
```

## Directory Structure

- **`1_input/`** - (Not used - orchestrator reads from other agents)
- **`2_system_assets/`** - Phase state tracking files (phase1_state_*.json, phase2_state_*.json)
- **`3_unlabeled/`** - Pipeline execution reports and completion logs
- **`5_labeled_json/`** - (Not used - no evaluation system)
- **`scripts/`** - Two-phase orchestration scripts and legacy single-phase script
- **`config.json`** - Agent dependencies, mappings, and execution configuration

## Core Components

### Input System
- **Project Detection**: Auto-discovers projects from Agent 0a setup
- **Interactive Selection**: GUI for project selection with state display
- **Mode Detection**: Automatic Validation vs Brand Mode based on available files
- **State Loading**: Resume functionality from previous execution points

### Generation System  
- **Phase 1 Script**: `scripts/run_pipeline_phase1.py` - Foundation building with state tracking
- **Phase 2 Script**: `scripts/run_pipeline_phase2.py` - Content generation with quality validation
- **Legacy Script**: `scripts/generate_simple.py` - Single-phase execution (deprecated)
- **Output**: Complete asset portfolio across all pipeline agents

### Evaluation System
- **Design**: No direct evaluation - orchestrates other agents' evaluation systems
- **Quality Gate**: Keywords Agent evaluation checkpoint (≥7.0 score required)
- **Validation**: State verification and dependency checking before phase transitions

### Learning System
- **Architecture**: No iterative learning - deterministic orchestration process  
- **Intelligence**: State persistence, dependency management, and failure recovery
- **Optimization**: Two-phase separation prevents strategy drift and enables quality control

## Advanced Pipeline Orchestration

### **Core Innovation: Two-Phase Quality Control Architecture**

**The Problem Solved:**
Traditional single-phase pipelines suffer from "strategy drift" - internal messaging gets diluted as it flows through multiple agents without quality checkpoints.

**Agent 0b's Solution:**
- **Phase 1**: Build strategic foundation (Agents 1-4) with Agent 5 Keywords Phase 1 generation
- **Quality Gate**: Human evaluation of Keywords Phase 1 with ≥7.0 score requirement  
- **Phase 2**: Trusted content generation at scale using approved foundation

### **Intelligent Mode Detection System:**

**Validation Mode (Full Pipeline)**
- **Trigger**: Both `qa_session_content.md` AND `customer_reviews.csv` exist
- **Phase 1**: Agent 1→2→3→4→5 (Message House, Brand Personas, Customer Personas, Gap Analysis, Keywords vocabulary)
- **Phase 2**: Agent 5→7→8→9 (Keywords expansion, Testimonials, Social Media, Website Copy with Psychology Logic)
- **Features**: Complete brand vs customer analysis with gap identification

**New Brand Mode (Streamlined)**  
- **Trigger**: Only `qa_session_content.md` exists (no customer reviews)
- **Phase 1**: Agent 1→2→5 (Message House, Brand Personas, Keywords vocabulary) 
- **Phase 2**: Agent 5→7→8→9 (Keywords expansion, Testimonials, Social Media, Website Copy with Psychology Logic)
- **Features**: New Brand-focused strategy without customer validation layer

**Competitor Analysis Mode**
- **Trigger**: Only `qa_session_content.md` exists (no customer reviews)
- **Phase 1**: Agent 1→2→5 (Message House, Brand Personas, Keywords vocabulary) 
- **Phase 2**: Agent 5→7→8→9 (Keywords expansion, Testimonials, Social Media, Website Copy with Psychology Logic)
- **Features**: Reverse-engineer competitor strategy focusing on market response patterns

### **Advanced Dependency Management System:**

**Mode-Specific Dependency Resolution:**

**Validation Mode Dependencies:**
- **Agent 1**: Requires PRE-SYSTEM human expert input (completed 12 Strategic Questions Q&A → message_house.md)
- **Agent 2**: Requires Agent 1 (message_house.md → brand_side_persona.md)
- **Agent 3**: Independent (customer_reviews.csv → customer_side_persona.md)
- **Agent 4**: Requires Agents 2,3 (brand_side_persona.md + customer_side_persona.md → gap_analysis.md)
- **Agent 5**: Requires Agents 1,2,3 (message_house.md + brand_side_persona.md + customer_side_persona.md → keywords_bank.md)
- **Agent 7**: Requires Agents 3,5 (customer_side_persona.md + keywords_bank.md → testimonials.md)
- **Agent 8**: Requires Agents 1,2,5,7 (message_house.md + brand_side_persona.md + keywords_bank.md + testimonials.md → twitter_posts.md)
- **Agent 9**: Requires Agents 1,5,7 (message_house.md + keywords_bank.md + testimonials.md → website_copy.md with strategic homepage logic)

**New Brand Mode Dependencies (Agent 3,4 Skipped):**
- **Agent 1**: Requires PRE-SYSTEM human expert input (completed 12 Strategic Questions Q&A → message_house.md)
- **Agent 2**: Requires Agent 1 (message_house.md → brand_side_persona.md)
- **Agent 5**: Requires Agents 1,2 (message_house.md + brand_side_persona.md → keywords_bank.md)
- **Agent 7**: Requires Agents 2,5 (brand_side_persona.md + keywords_bank.md → testimonials.md)
- **Agent 8**: Requires Agents 1,2,5,7 (message_house.md + brand_side_persona.md + keywords_bank.md + testimonials.md → twitter_posts.md)
- **Agent 9**: Requires Agents 1,5,7 (message_house.md + keywords_bank.md + testimonials.md → website_copy.md with strategic homepage logic)

**Competitor Analysis Mode Dependencies:**
- Same as New Brand Mode. Still requires human expert input for strategic foundation, but if competitor customer data collected, follows same path as Validation Mode

**Intelligent File Copying:**
- **Latest Output Detection**: Finds most recent timestamped files
- **Automatic Propagation**: Copies outputs to all downstream agent inputs
- **Failure Recovery**: Retry mechanisms with user confirmation
- **Cross-Phase Integration**: Merges Phase 1 and Phase 2 states for dependency checking

## Key Features

✅ **Two-Phase Architecture** - Strategic foundation with quality gate before content generation  
✅ **Intelligent Mode Detection** - Automatic Validation vs Brand Mode based on available files  
✅ **State Persistence** - Resume from any point with complete state tracking  
✅ **Dependency Management** - Smart file copying and prerequisite validation  
✅ **Quality Control** - Keywords evaluation checkpoint prevents strategy drift  

## Quick Start

**Two-Phase Execution:**
1. `python scripts/run_pipeline_phase1.py` → Foundation building (Agents 1-4)
2. `python keywords_bank_agent/scripts/evaluate_phase1.py` → Quality gate (≥7.0 score)
3. `python scripts/run_pipeline_phase2.py` → Content generation (Agents 5,7,8,9)

**Each script provides:**
- Interactive project selection
- Current state display  
- Resume functionality
- Progress tracking

## System Intelligence

**Project Management Intelligence:**
- **Auto-Discovery**: Scans all agents for available projects
- **State Tracking**: Maintains execution state across sessions with JSON persistence
- **Resume Capability**: Continue from any interruption point without data loss
- **Mode Flexibility**: Seamlessly switches between Validation and Brand modes

**Advanced Orchestration Logic:**
- **Dependency Validation**: Checks prerequisites before agent execution
- **Smart File Management**: Automatic output detection and downstream propagation
- **Failure Recovery**: Retry mechanisms with user control over continuation
- **Quality Assurance**: Keywords evaluation checkpoint prevents downstream cascade failures

**Performance Trajectory:**
- **Phase 1**: Foundation building execution (~5 minutes)
- **Quality Gate**: Human evaluation checkpoint (5-10 minutes)
- **Phase 2**: Content generation execution (~5 minutes)
- **Total Pipeline**: 15-20 minutes for complete asset portfolio

## Technical Notes

- **API**: No direct Claude API calls - orchestrates other agents' API usage
- **Language**: Python 3.x with subprocess management for agent execution
- **Dependencies**: Standard library (json, os, subprocess, shutil, pathlib)
- **State Files**: JSON persistence in 2_system_assets/ folder
- **Platform**: Cross-platform compatible with Windows path handling

## Quality Standards

Pipeline orchestration is validated on:
- **State Consistency**: Accurate tracking across phase transitions
- **Dependency Resolution**: Correct file copying between agents
- **Error Recovery**: Graceful handling of agent failures with retry options
- **Quality Gate Enforcement**: Keywords evaluation score ≥7.0 requirement
- **Mode Detection Accuracy**: Correct Validation vs Brand Mode identification

**Success Criteria**: Phase 1 completion + Keywords approval + Phase 2 completion = Complete asset portfolio

## Input Requirements

**Phase 1 Prerequisites:**
- **Agent 0a Setup**: Project workspace must be created
- **Required File**: `message_house_agent/1_input/{project_name}/qa_session_content.md`
- **Optional File**: `user_story_real_reviews_agent/1_input/{project_name}/customer_reviews.csv`

**Phase 2 Prerequisites:**
- **Phase 1 Completion**: All foundation agents executed successfully
- **Keywords Approval**: Phase 1 evaluation score ≥7.0

## Output Format

**Generated Asset Portfolio:**
```
Phase 1 Assets:
message_house_agent/3_unlabeled/{project_name}/messagehouse_{timestamp}.md
user_story_agent/3_unlabeled/{project_name}/userstories_{timestamp}.md
user_story_real_reviews_agent/3_unlabeled/{project_name}/customer_personas_{timestamp}.md
gap_analysis_agent/3_unlabeled/{project_name}/gap_analysis_{timestamp}.md

Phase 2 Assets:
keywords_bank_agent/3_unlabeled/{project_name}/keywords_bank_{timestamp}.md
testimonial_agent/3_unlabeled/{project_name}/testimonials_{timestamp}.md  
social_media_twitter_agent/3_unlabeled/{project_name}/twitter_posts_{timestamp}.md
website_copy_agent/3_unlabeled/{project_name}/website_copy_{timestamp}.md
```

**State Tracking Files:**
- **phase1_state_{project_name}.json**: Phase 1 execution state
- **phase2_state_{project_name}.json**: Phase 2 execution state
- **pipeline_execution_{project_name}_{timestamp}.json**: Execution report

## Integration with Agent Pipeline

**Position**: Phase 0 - Pipeline Execution (Post-Setup)

**Upstream Dependencies:**
- **Agent 0a**: Requires completed project setup with folder structure
- **Human Input**: Strategic Q&A and optional customer review files

**Downstream Orchestration:**
- **Phase 1**: Agents 1,2,3,4 (Foundation Building)
- **Quality Gate**: Keywords Agent evaluation checkpoint
- **Phase 2**: Agents 5,7,8,9 (Content Generation)

**Pipeline Flow:**
- **Agent 0a**: Creates workspace with industry-optimized system prompts → **Agent 0b**: Executes pipeline → **Complete Assets**: Ready for business use with full strategic alignment

## v3.0 Blueprint Alignment

This agent fully implements the v3.0 specifications:
- **Two-Phase Architecture**: Strategic foundation with quality control before content generation
- **Mode Detection**: Automatic Validation vs Brand Mode based on file availability
- **State Persistence**: Resume capability with complete execution tracking  
- **Quality Gate**: Keywords evaluation checkpoint prevents strategy drift
- **Dependency Management**: Smart file copying and prerequisite validation
- **Multi-Project Support**: Works with Agent 0a project isolation architecture
- **Error Recovery**: Graceful failure handling with retry mechanisms

---

*The complete pipeline orchestration system for automated AI agent execution with quality control.*