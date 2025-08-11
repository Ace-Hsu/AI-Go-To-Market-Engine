# Testimonial Agent - Complete System

## Overview
An AI-powered system that transforms brand strategy, personas, and customer voice patterns into authentic marketing testimonials. Uses Claude API for generation and human evaluation for continuous improvement.

## System Architecture

```
1_input/              ← Brand + Customer Personas + Keywords Bank (from upstream agents)
    ↓
2_system_assets/      ← System Prompts + Templates + Examples
    ↓
3_unlabeled/          ← Generated testimonials (Claude API output)
    ↓
5_labeled_json/       ← Human evaluations = Training data for improvement
```

## Directory Structure

- **`1_input/`** - Brand persona, customer persona, and keywords bank from upstream agents
- **`2_system_assets/`** - System prompts, output templates, training examples
- **`3_unlabeled/`** - Generated testimonials awaiting evaluation
- **`5_labeled_json/`** - Labeled evaluations for system learning
- **`scripts/`** - Generation and evaluation tools
- **`config.json`** - Claude API configuration

## Core Components

### Input System
- **Primary Integration**: Customer persona (Agent 3) + Keywords bank (Agent 5)
- **New Brand Mode Fallback**: Uses brand persona (Agent 2) when customer reviews unavailable
- **Smart File Detection**: Auto-identifies files by keywords ('userstories', 'reviews', 'keywords', 'expansion')
- **Project-Aware**: Multi-project structure with backward compatibility

### Generation System  
- **Script**: `scripts/generate_simple.py`
- **API**: Claude 3.5 Sonnet integration
- **Core Innovation**: Strategic Blending Framework - weaves brand messaging into authentic customer voice
- **Multi-Format Output**: Short-form, medium-form, long-form, and diverse customer profiles
- **Output**: Authentic marketing testimonials (8.5+ quality target)

### Evaluation System
- **Script**: `scripts/evaluate.py` 
- **Interface**: GUI for scoring and tagging
- **Criteria**: Authenticity, strategic alignment, emotional resonance, believability, marketing effectiveness
- **Marketing Focus**: Evaluates immediate usability across marketing channels

### Learning System
- **v3.0 Example Map**: Loads ALL evaluation files with quality filtering (8.0+ threshold)
- **Insight Extraction**: Pulls improvement guidance from detailed evaluation scores
- **Progressive Learning**: Quality improves with accumulated evaluation dataset
- **Pattern Recognition**: Learns successful blending techniques from high-scoring examples

## Advanced Features (Script Implementation)

**Smart Pipeline Integration:**
- Auto-detects required input files from upstream agents
- New Brand Mode: Automatically uses brand persona when customer reviews unavailable
- Multi-format testimonial generation (short, medium, long-form + diverse profiles)
- Project-aware file structure with backward compatibility

## Key Features

✅ **Pipeline Integration** - Uses outputs from Agents 2, 3, 5  
✅ **Authentic Voice** - Blends strategy with real customer language patterns  
✅ **Self-Improving** - Gets better with each evaluation cycle  
✅ **Industry Agnostic** - Works across business domains  
✅ **Quality Control** - Human-in-the-loop evaluation  
✅ **Marketing Ready** - Direct use in campaigns and channels  

## Quick Start

See **`QUICK_START.md`** for detailed usage instructions.

**Basic Workflow:**
1. `python scripts/generate_simple.py` → Generate marketing testimonials
2. `python scripts/evaluate.py` → Evaluate and score  
3. Repeat → Each cycle produces better results

## System Intelligence

The system learns from every evaluation:
- **High scores** (8.5+) become quality benchmarks
- **Low scores** teach failure patterns  
- **Improvement tags** guide refinement focus
- **Pattern recognition** improves with dataset size

**Performance Trajectory:**
- Uses 1-5: Good baseline quality
- Uses 5-10: Pattern recognition emerges  
- Uses 10+: Expert-level testimonial creation

## Technical Notes

- **API**: Claude 3.5 Sonnet via Anthropic API
- **Language**: Python 3.x
- **Dependencies**: Minimal (tkinter, json, pathlib)
- **Encoding**: UTF-8 throughout
- **Platform**: Cross-platform compatible

## Quality Standards

Testimonials are evaluated on:
- **Authenticity**: Believable customer voice and realistic scenarios
- **Strategic Alignment**: Reflects brand positioning and value props
- **Emotional Resonance**: Connects with target audience pain points and desires
- **Believability**: Sounds like real customer experiences, not marketing copy
- **Marketing Effectiveness**: Ready for immediate use across marketing channels

**Target Score**: 8.5+ for business-ready testimonials

## Input Requirements

Expected input from upstream agents:
- **brand_side_persona.md** (Agent 2): Brand voice and positioning
- **customer_side_persona.md** (Agent 3): Authentic customer insights
- **keywords_bank.md** (Agent 5): Strategic keywords + customer voice patterns (Vector G)

## Output Format

Generated testimonials include:
- **Multiple Testimonial Formats**: Short, medium, long-form versions
- **Diverse Customer Profiles**: Different demographics and use cases
- **Strategic Messaging**: Aligned with brand positioning
- **Authentic Voice**: Real customer language patterns
- **Marketing Ready**: Immediate use across channels

## Integration with Agent Pipeline

**Upstream Dependencies (Agents 2, 3, 5):**
- Agent 2: brand_side_persona.md → Brand voice alignment
- Agent 3: customer_side_persona.md → Customer insights
- Agent 5: keywords_bank.md → Customer voice patterns (Vector G)

**Downstream Usage:**
- Marketing campaigns and collateral
- Website testimonial sections
- Social media content
- Sales enablement materials
- Email marketing campaigns

---

*A complete, self-improving AI system for authentic marketing testimonial creation.*