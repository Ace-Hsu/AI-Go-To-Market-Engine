# Message House Agent - Complete System

## Overview
An AI-powered system that transforms business strategy Q&A into professional message house documents. Uses Claude API for generation and human evaluation for continuous improvement.

## System Architecture

```
1_input/              ← 12 Strategic Questions Q&A
    ↓
2_system_assets/      ← System Prompts + Templates + Examples
    ↓
3_unlabeled/          ← Generated message houses (Claude API output)
    ↓
5_labeled_json/       ← Human evaluations = Training data for improvement
```

## Directory Structure

- **`1_input/`** - Business Q&A files and templates
- **`2_system_assets/`** - System prompts, output templates, training examples
- **`3_unlabeled/`** - Generated message houses awaiting evaluation
- **`5_labeled_json/`** - Labeled evaluations for system learning
- **`scripts/`** - Generation and evaluation tools
- **`config.json`** - Claude API configuration

## Core Components

### Input System
- **Template**: `1_input/12_questions_template.md` 
- **Example**: `1_input/turmeric_example_qa.md`
- **Format**: Strategic Q&A covering positioning, differentiation, customer psychology

### Generation System  
- **Script**: `scripts/generate_simple.py`
- **API**: Claude 3.5 Sonnet integration
- **Output**: Professional message house documents (8.5+ quality target)

### Evaluation System (Optional Enhancement)
- **Script**: `scripts/evaluate.py` 
- **Interface**: GUI for scoring and tagging
- **Design Philosophy**: System works perfectly without evaluation - evaluation is post-pipeline optional enhancement
- **Workflow**: Complete pipeline first → Review all assets → Then evaluate at your convenience
- **Criteria**: Strategic depth, consistency, proof points, customer psychology, competitive intelligence

### Learning System (v3.0 Example Map Architecture)
- **Training Data**: All evaluations in `5_labeled_json/`
- **Example Map Learning**: Reads ALL evaluation files for comprehensive pattern recognition
- **Dual Learning**: Uses both high-quality examples as benchmarks AND poor examples to avoid failure patterns
- **No Evaluation Required**: System works perfectly with 0 evaluations - each evaluation just makes it better
- **Optional Enhancement**: More evaluations = higher quality through accumulated wisdom
- **Flexibility**: Evaluate when convenient after completing full pipeline

## Key Features

✅ **Standalone Operation** - No external dependencies beyond Python + Claude API  
✅ **Self-Improving** - Gets better with each evaluation cycle  
✅ **Industry Agnostic** - Works across business domains  
✅ **Optional Quality Enhancement** - Human evaluation improves quality but not required for operation  
✅ **Scalable** - Reusable templates and processes  

## Quick Start

See **`QUICK_START.md`** for detailed usage instructions.

**Basic Workflow:**
1. `python scripts/generate_simple.py` → Generate message house
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
- Uses 1-5: Good baseline quality
- Uses 5-10: Pattern recognition emerges  
- Uses 10+: Expert-level strategic insights

## Technical Notes

- **API**: Claude 3.5 Sonnet via Anthropic API
- **Language**: Python 3.x
- **Dependencies**: Minimal (tkinter, json, pathlib)
- **Encoding**: UTF-8 throughout
- **Platform**: Cross-platform compatible

## Quality Standards

Message houses are evaluated on:
- Strategic depth and contrarian positioning
- Internal consistency across sections
- Proof point quality and credibility  
- Customer psychology understanding
- Competitive intelligence and differentiation

**Target Score**: 8.5+ for business-ready documents

## v3.0 Blueprint Alignment

This agent fully implements the v3.0 specifications:
- **Phase 1 Foundation**: Core strategic messaging foundation for entire pipeline
- **Example Map Learning**: Implemented iterative learning system using ALL evaluation data
- **Multi-Project Support**: Compatible with project-based folder structure
- **Pipeline Integration**: 
  - **Direct feeds**: Agent 2 (User Story), Agent 5 (Keywords), Agent 9 (Website Copy)
  - **Indirect feeds**: Agent 7 (Testimonials) via Agent 2 in Brand Mode
  - **Mode flexibility**: Supports both Validation Mode and Brand Mode execution
  - **Optional agents**: Compatible with Agent 6 (Stakeholder Strategy) and Agent 6.5 (Platform Intelligence)
- **Quality Design**: System works perfectly without evaluation - evaluation is optional post-pipeline enhancement

---

*A complete, self-improving AI system for strategic message house creation.*