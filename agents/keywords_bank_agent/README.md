# Keywords Bank Agent - Complete System

## Overview
A two-phase AI-powered system that transforms brand strategy into comprehensive keyword banks and expansion engines. Uses Claude API for generation and human evaluation for Phase 1 quality control.

## System Architecture

```
Phase 1: Foundation Generation + Human Evaluation
1_input/ → generate_phase1.py → 3_unlabeled/ → evaluate_phase1.py → 5_labeled_json/
                                        ↓
Phase 2: Expansion Engine (No Evaluation)
Approved Phase 1 → generate_phase2.py → 3_unlabeled/ → Direct to Agents 7,8,9
```

## Directory Structure

- **`1_input/`** - Message house, personas, and optional external keywords
- **`2_system_assets/`** - System prompts for Phase 1 & 2, examples
- **`3_unlabeled/`** - Generated vocabulary and expansion outputs
- **`5_labeled_json/`** - Phase 1 human evaluations for approval tracking
- **`scripts/`** - Generation and evaluation tools
- **`config.json`** - Claude API configuration

## Core Components

### Critical Quality Control Architecture

**Phase 1: Strategic Foundation Generation**
- **Script**: `scripts/generate_phase1.py`
- **Input**: Message house + Brand persona + Customer persona + external_keywords.csv (optional)
- **Output**: Strategic keyword bank vocabulary foundation
- **Quality Control**: Human evaluation with 5-criteria system (25% strategic alignment focus)
- **Approval Threshold**: ≥7.0 score required to proceed
- **Purpose**: **Critical checkpoint** - ensures internal strategy aligns before external asset creation

**Phase 2: Massive Expansion Engine** 
- **Script**: `scripts/generate_phase2.py`
- **Input**: Approved Phase 1 vocabulary (quality-controlled foundation)
- **Output**: 150+ keywords across 6 strategic vectors for downstream agents
- **Quality Control**: None - trusts approved foundation, focuses on volume and diversity
- **Purpose**: **Internal → External asset transfer** - scales approved strategy to content creation

## Strategic Business Logic (Advanced Design)

### **Critical Insight: Internal-External Asset Misalignment Problem**
Traditional pipelines suffer from **strategy drift** - internal messaging gets diluted/altered as it flows through multiple agents. This agent solves that with a **strategic checkpoint architecture**.

### **Two-Phase Solution Design:**

**Phase 1: Strategy Validation Gateway**
- Extracts core vocabulary from all internal assets (Agents 1-3)
- Human evaluates if brand strategy is properly captured and synthesized
- **≥7.0 threshold** ensures messaging consistency before external asset creation
- **Prevents downstream cascade failures** - bad foundation = bad everything

**Phase 2: Trusted Volume Generation**
- Once foundation is approved, generates massive keyword scale (150+)
- No evaluation bottleneck - trusts approved foundation
- **Agent-specific vectors** - tailored keywords for each downstream agent's needs
- **Strategic consistency maintained** at scale

### **Why This Architecture Works:**
> *"Fix the message house inconsistency before it becomes external asset inconsistency"*

- **Quality Control Point**: Human validates core strategy transfer
- **Scale Without Quality Loss**: Phase 2 generates volume while maintaining strategic alignment  
- **Pipeline Optimization**: Prevents re-work in downstream agents (7,8,9)

### Implementation System
- **Project-Aware**: Multi-project directory structure with backward compatibility
- **Smart File Detection**: Auto-finds most recent timestamped files
- **API**: Claude 3.5 Sonnet integration
- **Output**: Structured markdown documents (vocabulary + expansion)

### Evaluation System (Phase 1 Only)
- **Script**: `scripts/evaluate_phase1.py`
- **Interface**: GUI for scoring and approval
- **Criteria**: Strategic alignment, completeness, creative expansion, insightfulness, actionability

### Strategic Vectors (Phase 2 Output)

**SEO & Search-Focused (for Agent 9: Website Copy)**
- Vector A: Question-based keywords (20+)
- Vector B: Modifier-based keywords (30+)
- Vector C: Intent-based keywords (40+)

**Creative & Copywriting-Focused (for Agents 7&8: Testimonials & Social)**
- Vector D: Persona quote starters (25+)
- Vector E: Social media hooks & hashtags (20+)
- Vector F: Feature-to-benefit angles (30+)

## Key Features

✅ **Two-Phase Quality Control** - Foundation evaluated, expansion trusted  
✅ **Agent-Specific Outputs** - Tailored for downstream content agents  
✅ **Strategic Alignment** - All keywords trace back to brand strategy  
✅ **Massive Scale** - 150+ keywords across 6 vectors  
✅ **Human-in-the-Loop** - Quality control where it matters most  

## Quick Start

See **`QUICK_START.md`** for detailed usage instructions.

**Basic Workflow:**
1. `python scripts/generate_phase1.py` → Generate vocabulary foundation
2. `python scripts/evaluate_phase1.py` → Evaluate and approve/reject
3. `python scripts/generate_phase2.py` → Generate expansion engine (if approved)

## System Intelligence

**Phase 1 Learning**: The system tracks evaluation patterns to improve vocabulary generation quality over time.

**Phase 2 Efficiency**: No evaluation bottleneck - massive content generation for immediate use by content agents.

**Quality Philosophy**: 
- Phase 1: High-quality foundation determines everything else
- Phase 2: Volume and diversity for downstream agent flexibility

## Integration with Agent Pipeline

**Upstream Dependencies (Agents 1-3):**
- Agent 1: message_house.md
- Agent 2: brand_side_persona.md  
- Agent 3: customer_side_persona.md

**Downstream Consumers (Agents 7-9):**
- Agent 7: Testimonial Agent → Uses Vectors D, E, F
- Agent 8: Social Media Agent → Uses Vectors E, F, A
- Agent 9: Website Copy Agent → Uses Vectors A, B, C

## Technical Notes

- **API**: Claude 3.5 Sonnet via Anthropic API
- **Language**: Python 3.x
- **Dependencies**: Minimal (anthropic, tkinter)
- **Encoding**: UTF-8 throughout
- **Platform**: Cross-platform compatible

## Quality Standards

**Phase 1 Evaluation Criteria:**
- Strategic Alignment (25%): Message house extraction quality
- Completeness (20%): All persona language captured
- Creative Expansion (20%): Semantic variations beyond synonyms
- Insightfulness (20%): Thematic cluster analysis
- Actionability (15%): Clear structure for expansion

**Approval Threshold**: 7.0+ for Phase 2 progression

**Phase 2 Output Standards:**
- Minimum 150 keywords across 6 vectors
- Agent-specific optimization
- Strategic consistency with approved foundation
- Immediate actionability for content generation

---

*A strategic keyword generation system that bridges brand strategy with content creation at scale.*