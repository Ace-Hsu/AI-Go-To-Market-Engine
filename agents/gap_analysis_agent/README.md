# Gap Analysis Agent - Complete System

## Overview
An AI-powered system that transforms brand-side and customer-side user personas into comprehensive Strategic Gap Analysis Reports. Uses Claude API with the proven Strategic Gap Analysis Framework to identify, quantify, and prioritize critical gaps between brand assumptions and customer reality.

## System Architecture

```
1_input/              ← Brand & Customer Persona Files (from Agents 2 & 3)
    ↓
2_system_assets/      ← Strategic Gap Analysis Framework + Examples
    ↓
3_unlabeled/          ← Generated gap analysis reports (Claude API output)
    ↓
5_labeled_json/       ← Human evaluations = Training data for improvement
```

## Directory Structure

- **`1_input/`** - Brand and customer persona files (exactly 2 .md files)
- **`2_system_assets/`** - System prompts, framework methodology, examples
- **`3_unlabeled/`** - Generated gap analysis reports awaiting evaluation
- **`5_labeled_json/`** - Labeled evaluations for system learning
- **`scripts/`** - Generation and evaluation tools
- **`config.json`** - Claude API configuration

## Core Components

### Input System
- **Source**: Two persona files - one brand-side (Agent 2), one customer-side (Agent 3)
- **Format**: Markdown files with structured persona data
- **Smart Detection**: Auto-identifies files by keywords ('brand', 'message', 'house' vs 'review', 'customer', 'real')
- **Fallback Logic**: Alphabetical sorting if pattern matching fails
- **Project Support**: Multi-project structure with backward compatibility

### Generation System  
- **Script**: `scripts/generate_simple.py`
- **API**: Claude 3.5 Sonnet integration
- **Framework**: Strategic Gap Analysis Framework (4-phase systematic methodology)
- **Evidence-Based**: Quantitative analysis with actual percentages and thematic patterns
- **Template-Driven**: Exact gap statement format for consistency
- **Output**: Comprehensive gap analysis reports (8.5+ quality target)

### Evaluation System
- **Script**: `scripts/evaluate.py` 
- **Interface**: GUI for scoring and tagging
- **Criteria**: Framework adherence, quantitative evidence, business relevance, gap clarity, strategic prioritization
- **Impact Focus**: Evaluates business impact potential for each gap

### Learning System
- **Training Data**: All evaluations in `5_labeled_json/`
- **v3.0 Example Map**: Loads ALL evaluation files with quality filtering (8.0+ threshold)
- **Insight Extraction**: Pulls improvement guidance from detailed evaluation scores
- **Progressive Learning**: Quality improves with accumulated evaluation dataset
- **Backward Compatible**: Works with 0, 1, or 100+ evaluation files

## Strategic Gap Analysis Framework (Advanced Business Logic)

### **Core Innovation: 4-Phase Systematic Methodology**

**Phase 1: Data Collection & Structuring**
- Intelligent file identification (auto-detects brand vs customer files)
- Structured extraction into 5-feature analysis matrix
- Project-aware multi-file processing

**Phase 2: The 4-Step Analysis Process**
- **Step 2.1**: Thematic comparison across persona sets
- **Step 2.2**: Quantify qualitative patterns with actual percentages
- **Step 2.3**: Apply proven gap statement template with quantitative evidence
- **Step 2.4**: Business impact prioritization (CRITICAL → HIGH-IMPACT → SIGNIFICANT → MODERATE)

### **The 5 Strategic Analysis Features**
1. **Income & Price**: Customer financial reality and attitude towards cost/value
2. **Primary Motivation**: Core "job" the customer hires the product to do
3. **Lifestyle**: Daily activities, hobbies, and self-perception
4. **Product Experience**: Direct, sensory interaction with product
5. **Key Pain Points**: Specific frustration that initiates solution search

### **Advanced Implementation Features**

**Smart File Processing:**
- Auto-identifies brand vs customer files by filename patterns
- Fallback to alphabetical sorting if pattern matching fails
- Project-based multi-file structure support
- UTF-8 encoding throughout for international characters

**Evidence-Based Gap Identification:**
- Exact gap statement template: "On the feature of [Feature], the brand believes customers are driven by [Brand Theme], but customers are actually focused on [Customer Theme]. We know this because [Quantitative Finding]."
- Frequency analysis with actual percentages
- Thematic pattern comparison for evidence support

**Business Impact Prioritization Matrix:**
- **CRITICAL**: Affects immediate sales conversion or core value proposition
- **HIGH-IMPACT**: Affects customer retention or marketing effectiveness
- **SIGNIFICANT**: Affects brand perception or customer experience
- **MODERATE**: Affects tactical execution or messaging refinement

## Key Features

✅ **Systematic Methodology** - Follows proven 4-step framework  
✅ **Pipeline Integration** - Compares brand (Agent 2) vs customer (Agent 3) personas  
✅ **Quantitative Analysis** - Uses data-driven evidence and percentages  
✅ **Business-Focused** - Prioritizes gaps by revenue/growth impact  
✅ **Self-Improving** - Gets better with each evaluation cycle (v3.0 Example Map system)  

## Quick Start

See **`QUICK_START.md`** for detailed usage instructions.

**Basic Workflow:**
1. `python scripts/generate_simple.py` → Generate gap analysis from personas
2. `python scripts/evaluate.py` → Evaluate and score  
3. Repeat → Each cycle produces better results

## System Intelligence

**v3.0 Iterative Learning**: The system learns from every evaluation using the Example Map system:
- **High scores** (8.5+) become quality benchmarks and reference patterns
- **Low scores** teach failure patterns and what to avoid
- **Improvement tags** guide refinement focus for next generation
- **Pattern recognition** improves with accumulated evaluation dataset

**Performance Trajectory:**
- Uses 1-5: Good baseline methodology
- Uses 5-10: Pattern recognition emerges from example map
- Uses 10+: Expert-level strategic insights with proven frameworks

## Technical Notes

- **API**: Claude 3.5 Sonnet via Anthropic API
- **Language**: Python 3.x
- **Dependencies**: Minimal (tkinter, json, pathlib)
- **Encoding**: UTF-8 throughout
- **Platform**: Cross-platform compatible

## Quality Standards

Gap analysis reports are evaluated on:
- **Framework Adherence**: Follows 4-step methodology and required format
- **Quantitative Evidence**: Uses actual percentages and data-driven findings
- **Business Relevance**: Focuses on gaps that impact revenue/growth
- **Gap Clarity**: Clear, specific gap statements using template
- **Strategic Prioritization**: Appropriate ranking by business impact

**Target Score**: 8.5+ for business-ready analysis

## Input Requirements

Expected input:
- **Exactly 2 files**: One brand persona file, one customer persona file
- **Format**: Markdown (.md) files with structured persona data
- **Naming**: Files should indicate source (brand/customer) for auto-identification
- **Content**: Complete persona profiles with demographics, motivations, pain points

## Integration with Agent Pipeline

**Position**: Agent 4 in the strategic pipeline

**Upstream Dependencies:**
- Agent 2: brand_side_persona.md → Brand customer vision
- Agent 3: customer_side_persona.md → Real customer insights

**Downstream Usage:**
- Agent 6: Stakeholder Strategy Decks (strategic insights for internal teams)
- Strategic decision-making and positioning refinement
- Brand messaging alignment recommendations

## Output Format

Generated reports follow this structure:
- **Executive Summary**: Key strategic gaps overview
- **Prioritized Gap Analysis**: Ranked by business impact
- **Gap Statements**: Using proven template format
- **Quantitative Evidence**: Actual percentages and frequencies
- **Strategic Implications**: Business-focused recommendations

---

*A complete, self-improving AI system for strategic gap analysis between brand perception and customer reality.*