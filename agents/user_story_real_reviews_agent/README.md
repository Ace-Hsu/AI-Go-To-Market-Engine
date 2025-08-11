# User Story Real Reviews Agent - Complete System

## Overview
An AI-powered system that transforms real customer reviews into vivid user personas and narrative-driven user stories. Uses Claude API for generation and human evaluation for continuous improvement. Built to extract authentic customer voices from actual purchase reviews.

## System Architecture

```
1_input/              ← Customer Review CSV Files (Positive + Negative)
    ↓
2_system_assets/      ← System Prompts + Templates + Examples
    ↓
3_unlabeled/          ← Generated user stories (Claude API output)
    ↓
5_labeled_json/       ← Human evaluations = Training data for improvement
```

## Directory Structure

- **`1_input/`** - Customer review CSV files (positive and negative)
- **`2_system_assets/`** - System prompts, output templates, training examples
- **`3_unlabeled/`** - Generated user personas awaiting evaluation
- **`5_labeled_json/`** - Labeled evaluations for system learning
- **`scripts/`** - Generation and evaluation tools
- **`config.json`** - Claude API configuration

## Core Components

### Input System
- **Source**: Customer review CSV files with Username, Stars, Area, Review Content
- **Format**: Positive and negative review files covering real customer experiences

### Generation System  
- **Script**: `scripts/generate_simple.py`
- **API**: Claude 3.5 Sonnet integration
- **Output**: Detailed user personas based on real customer language (8.5+ quality target)

### Evaluation System
- **Script**: `scripts/evaluate.py` 
- **Interface**: GUI for scoring and tagging
- **Criteria**: Persona authenticity, narrative depth, user story clarity, emotional resonance, review alignment

### Learning System
- **Training Data**: All evaluations in `5_labeled_json/`
- **Improvement**: Each evaluation enhances next generation
- **Quality**: Progressive improvement with usage

## Key Features

✅ **Real Customer Voice** - Extracts authentic personas from actual purchase reviews  
✅ **Pipeline Integration** - Feeds into Gap Analysis Agent (Agent 4)  
✅ **Industry Agnostic** - Works across product categories  
✅ **Quality Control** - Human-in-the-loop evaluation  
✅ **Scalable** - Reusable templates and processes  

## Quick Start

See **`QUICK_START.md`** for detailed usage instructions.

**Basic Workflow:**
1. `python scripts/generate_simple.py` → Generate user personas from reviews
2. `python scripts/evaluate.py` → Evaluate and score  
3. Repeat → Each cycle produces better results

## System Intelligence

**Strategic Design Decision (v3.0):** This agent intentionally **excludes** the iterative learning system to preserve creative strategic reasoning. Each customer review dataset is unique and requires fresh analytical approach rather than pattern learning from previous examples.

**Performance Focus:**
- Authentic voice extraction from real customer data
- Fresh strategic reasoning for each review dataset
- Preserves creative analytical thinking
- Maintains objective customer voice interpretation

## Technical Notes

- **API**: Claude 3.5 Sonnet via Anthropic API
- **Language**: Python 3.x
- **Dependencies**: Minimal (tkinter, json, pathlib, csv)
- **Encoding**: UTF-8 throughout
- **Platform**: Cross-platform compatible

## Quality Standards

User personas are evaluated on:
- **Persona Authenticity**: Believable demographics extracted from review language
- **Narrative Depth**: Vivid first-person scenarios reflecting real customer experiences  
- **User Story Clarity**: Clear 'As a... I want... So that...' format and actionability
- **Emotional Resonance**: Deep understanding of real customer emotions and pain points
- **Review Alignment**: Alignment with actual customer review content and experiences

**Target Score**: 8.5+ for business-ready personas

## Integration with Agent Pipeline

**Position**: Agent 3 in the strategic pipeline

**Downstream Usage:**
- Agent 4: Gap Analysis Agent (compares with brand personas)
- Agent 5: Keywords Bank Agent (authentic customer language)
- Agent 7: Testimonial Agent (real customer voice patterns)
- Agent 8: Social Media Twitter Agent (authentic audience insights)
- Agent 9: Website Copy Agent (customer psychology patterns)

## Data Sources

Expected CSV format:
```
Username,Stars,Area,Review Content
John Doe,5,United States,"Great product, helped with my joint pain..."
Jane Smith,2,United States,"Too expensive and didn't work as expected..."
```

---

*A complete, self-improving AI system for authentic customer persona creation from real reviews.*