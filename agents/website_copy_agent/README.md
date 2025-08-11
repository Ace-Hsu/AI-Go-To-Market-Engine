# Website Copy Agent - Complete System

## Overview
An AI-powered system that transforms brand strategy assets into comprehensive website copy with strategic homepage logic. Uses Claude API for generation and human evaluation for continuous improvement, focusing on intelligent content prioritization based on customer psychology and industry patterns.

## System Architecture

```
1_input/              ← Message House, Testimonials, Keywords (from Agents 1,5,7)
    ↓
2_system_assets/      ← Strategic Logic Framework + Content Module Templates
    ↓
3_unlabeled/          ← Generated website copy with strategic logic (Claude API output)
    ↓
5_labeled_json/       ← Human evaluations = Training data for improvement
```

## Directory Structure

- **`1_input/`** - Brand strategy assets from upstream agents (1,5,7)
- **`2_system_assets/`** - System prompts, strategic frameworks, content templates
- **`3_unlabeled/`** - Generated website copy awaiting evaluation
- **`5_labeled_json/`** - Labeled evaluations for system learning
- **`scripts/`** - Generation and evaluation tools
- **`config.json`** - Claude API configuration

## Core Components

### Input System
- **Smart Auto-Detection**: Identifies file types by filename patterns + content analysis
- **3 Required Assets**: Message house + Keywords bank + Testimonials (from Agents 1,5,7)
- **Dual Detection Logic**: Priority 1: Filename matching, Priority 2: Content pattern analysis
- **Project-Aware**: Multi-project structure with backward compatibility

### Generation System  
- **Script**: `scripts/generate_simple.py`
- **API**: Claude 3.5 Sonnet integration
- **Core Innovation**: Strategic Logic Generation - creates compelling psychology reasoning BEFORE content
- **Two-Phase Process**: 1) Sell the strategic logic, 2) Provide the content modules
- **Output**: Psychology-driven homepage strategy + 7 content modules (8.5+ quality target)

### Evaluation System
- **Script**: `scripts/evaluate.py` 
- **Interface**: GUI for scoring and tagging
- **Criteria**: Strategic logic quality, customer psychology accuracy, content module effectiveness, narrative flow, business impact

### Learning System
- **Strategic Design**: No iterative learning to maintain creative freshness
- **Quality Control**: Human evaluation for output validation only
- **Fresh Analysis**: Each generation creates unique psychology insights

## Core Innovation: Strategic Logic Generation

**The system's primary value isn't generating content - it's generating fresh, compelling reasoning behind why this specific homepage flow will convert YOUR specific customer psychology.**

### **Strategic Flow Reasoning (Generated Fresh Each Time)**
```
[Custom Flow] → [Based on Your Assets] → [Unique Psychology Pattern] → [Conversion Logic]
```

**Real Examples Generated:**
- **"Liberation Through Validation"** - ego-safe change narrative for B2B experts
- **"Permission to Believe"** - trust-building progression for wellness anxiety
- **"Expert Empowerment vs System Failure"** - reframes pain without ego threat

### **Strategic Design Decision:**
Unlike other agents, this system **maintains creative freshness** - no iterative learning to avoid strategic overfitting. Each analysis generates unique psychology insights based purely on your pipeline assets.

### **Why This Matters:**
> *"When user sees the logic and they buy it, the next asset is solid."*

## Strategic Homepage Logic Framework

### Two-Phase Output System

**Phase 1: Strategic Logic Analysis**
- Analyze customer psychology patterns from input assets
- Identify optimal homepage narrative flow
- Create compelling logic explanation that "sells" the strategy
- Determine content module priorities

**Phase 2: Content Module Generation**
- Generate 7 core content modules:
  - A. Core Emotional Promise (Tagline)
  - B. Customer Pain Point Narrative (Story)
  - C. Authentic Community Voice (Testimonials)
  - D. Scientific Breakthrough (Technology/Process)
  - E. Quantifiable Proof (Data/Results)
  - F. Aspirational Vision (Lifestyle Goal)
  - G. Brand's Deeper Purpose (Mission)

### Strategic Intelligence
The system analyzes:
1. **Customer Psychology Type** (trust-driven vs aspiration-driven vs logic-driven)
2. **Industry Conversion Pattern** (B2B vs B2C vs health vs luxury)
3. **Optimal Narrative Flow** (which emotional journey works best)
4. **Content Prioritization** (which modules lead vs support)

## Key Features

✅ **Strategic Intelligence** - Analyzes customer psychology for optimal logic  
✅ **Content Module System** - 7 proven content types for comprehensive coverage  
✅ **Logic Explanation** - "Sells" the strategy with compelling reasoning  
✅ **Pipeline Integration** - Uses existing brand strategy assets  

## Quick Start

See **`QUICK_START.md`** for detailed usage instructions.

**Basic Workflow:**
1. `python scripts/generate_simple.py` → Generate fresh strategic website copy
2. `python scripts/evaluate.py` → Validate output quality (no system learning)

## System Intelligence

**Creative Freshness Design:**
- Each analysis generates unique psychology insights
- No pattern learning to avoid strategic overfitting
- Fresh strategic reasoning for every brand context
- Maintains expert-level homepage logic through consistent framework application

## Technical Notes

- **API**: Claude 3.5 Sonnet via Anthropic API
- **Language**: Python 3.x
- **Dependencies**: Minimal (anthropic, tkinter)
- **Encoding**: UTF-8 throughout
- **Platform**: Cross-platform compatible

## Quality Standards

Website copy is evaluated on:
- **Strategic Logic Quality**: Convincing reasoning for homepage narrative flow
- **Customer Psychology Accuracy**: Deep understanding of target audience patterns
- **Content Module Effectiveness**: Quality and relevance of 7 content modules
- **Narrative Flow**: Logical progression from empathy to conversion
- **Business Impact**: Focus on revenue/conversion optimization

**Target Score**: 8.5+ for business-ready website copy

## Input Requirements

Expected input:
- **Message house file**: Core brand strategy and positioning (auto-detected)
- **Keywords file**: Customer language and SEO optimization (auto-detected)
- **Testimonials file**: Social proof and community voice (auto-detected)
- **Format**: Any 3 .md files with identifying keywords in filename or content
- **Completeness**: All 3 content types required for comprehensive analysis

## Output Format

Generated website copy follows this structure:
- **Strategic Logic Explanation**: Why this narrative flow works for this audience
- **Content Module Priority**: Ordered list with strategic reasoning
- **7 Content Modules**: Ready-to-use website sections
- **Implementation Notes**: Technical guidance for website integration
- **A/B Testing Recommendations**: Alternative approaches for optimization

## Integration with Agent Pipeline

**Upstream Dependencies (Agents 1,5,7):**
- Agent 1: message_house.md → Core brand strategy
- Agent 5: keywords_bank.md → Customer language patterns
- Agent 7: marketing_testimonials.md → Social proof content

**Downstream Usage:**
- Direct website implementation
- Content management system integration
- Landing page optimization
- A/B testing framework

---

*A strategic AI system for website copy generation with fresh, psychology-driven homepage logic.*