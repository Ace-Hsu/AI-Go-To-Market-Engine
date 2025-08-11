# User Story Agent - Complete System

## Overview
An AI-powered system that transforms message house documents into vivid user personas and narrative-driven user stories. Uses Claude API for generation and human evaluation for continuous improvement.

## System Architecture

```
1_input/              ← Message House Documents (from message_house_agent)
    ↓
2_system_assets/      ← System Prompts + Templates + Examples
    ↓
3_unlabeled/          ← Generated user stories (Claude API output)
    ↓
5_labeled_json/       ← Human evaluations = Training data for improvement
```

## Directory Structure

- **`1_input/`** - Message house documents from message_house_agent
- **`2_system_assets/`** - System prompts, output templates, training examples
- **`3_unlabeled/`** - Generated user personas awaiting evaluation
- **`5_labeled_json/`** - Labeled evaluations for system learning
- **`scripts/`** - Generation and evaluation tools
- **`config.json`** - Claude API configuration

## Core Components

### Input System
- **Source**: Message house documents from message_house_agent output
- **Format**: Complete message house with positioning, pillars, and proof points

### Generation System  
- **Script**: `scripts/generate_simple.py`
- **API**: Claude 3.5 Sonnet integration
- **Output**: Detailed user personas with narratives (8.5+ quality target)

### Evaluation System (Optional Enhancement)
- **Script**: `scripts/evaluate.py` 
- **Interface**: GUI for scoring and tagging
- **Design Philosophy**: System works perfectly without evaluation - evaluation is post-pipeline optional enhancement
- **Workflow**: Complete pipeline first → Review all assets → Then evaluate at your convenience
- **Criteria**: Persona authenticity, narrative depth, user story clarity, emotional resonance, strategic alignment

### Learning System (v3.0 Example Map Architecture)
- **Training Data**: All evaluations in `5_labeled_json/`
- **Example Map Learning**: Reads ALL evaluation files for comprehensive pattern recognition
- **Dual Learning**: Uses both high-quality examples as benchmarks AND poor examples to avoid failure patterns
- **No Evaluation Required**: System works perfectly with 0 evaluations - each evaluation just makes it better
- **Optional Enhancement**: More evaluations = higher quality through accumulated wisdom
- **Flexibility**: Evaluate when convenient after completing full pipeline

## Key Features

✅ **Pipeline Integration** - Seamlessly processes message_house_agent output  
✅ **Self-Improving** - Gets better with each evaluation cycle  
✅ **Industry Agnostic** - Works across business domains  
✅ **Optional Quality Enhancement** - Human evaluation improves quality but not required for operation  
✅ **Scalable** - Reusable templates and processes  

## Quick Start

See **`QUICK_START.md`** for detailed usage instructions.

**Basic Workflow:**
1. `python scripts/generate_simple.py` → Generate user personas
2. `python scripts/evaluate.py` → Evaluate and score  
3. Repeat → Each cycle produces better results

## System Intelligence (v3.0 Implementation)

The system learns from every evaluation using Example Map architecture:
- **High scores** (8.5+) become quality benchmarks for replication
- **Low scores** teach critical failure patterns to avoid
- **All examples** contribute to comprehensive pattern recognition
- **Improvement tags** guide specific refinement focus
- **Accumulated wisdom** improves with complete evaluation dataset

**Performance Trajectory:**
- **Uses 1-5**: Good baseline quality with initial pattern learning
- **Uses 5-10**: Strong pattern recognition emerges for persona authenticity
- **Uses 10+**: Expert-level persona insights with deep narrative sophistication

## Technical Notes

- **API**: Claude 3.5 Sonnet via Anthropic API
- **Language**: Python 3.x
- **Dependencies**: Minimal (tkinter, json, pathlib)
- **Encoding**: UTF-8 throughout
- **Platform**: Cross-platform compatible

## Quality Standards

User personas are evaluated on:
- **Persona Authenticity**: Believable demographics and specific lifestyle details
- **Narrative Depth**: Vivid first-person scenarios with emotional resonance  
- **User Story Clarity**: Clear 'As a... I want... So that...' format and actionability
- **Emotional Resonance**: Deep understanding of customer psychology and pain points
- **Strategic Alignment**: Alignment with message house insights and value propositions

**Target Score**: 8.5+ for business-ready personas

## v3.0 Blueprint Alignment

This agent fully implements the v3.0 specifications:
- **Phase 1 Foundation**: Transforms message house into ideal brand-side personas
- **Example Map Learning**: Implemented iterative learning system using ALL evaluation data
- **Multi-Project Support**: Compatible with project-based folder structure
- **Pipeline Integration**: 
  - **Input**: Agent 1 (Message House) output
  - **Direct feeds**: Agent 4 (Gap Analysis), Agent 5 (Keywords Bank), Agent 6 (Stakeholder Strategy)
  - **Brand Mode fallback**: Feeds Agent 7 (Testimonials) AND Agent 8 (Social Media) when customer data unavailable
  - **Mode flexibility**: Supports both Validation Mode and Brand Mode execution
- **Quality Design**: System works perfectly without evaluation - evaluation is optional post-pipeline enhancement

---

*A complete, self-improving AI system for user persona and story creation.*