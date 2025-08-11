# Agent Specifications

This document provides comprehensive technical specifications for all 11 agents in the AI-Go-To-Market-Engine pipeline, including implementation details, dependencies, and integration patterns.

## **Agent Directory Overview**

The system consists of a meta-orchestration layer (Agents 0a/0b) followed by a 10-agent workflow with an optional platform intelligence plugin. Each agent is designed as a standalone module with specific technical requirements and outputs.

---

## **Phase 0: System Configuration & Orchestration**

### **Agent 0a: Project Configurator**
**Technical Purpose**: Automated project workspace creation and industry-specific system prompt generation

**Implementation Details**:
- **Script**: `generate_simple.py` with interactive configuration interface
- **Output**: Complete project workspace with tailored prompts across all 11 agents
- **Project Structure**: Generates `{industry}_{product}_{timestamp}` naming convention
- **Prompt Engineering**: Dynamic system prompt customization based on industry context

**Input Requirements**:
```json
{
  "industry": "string (e.g., 'SaaS', 'E-commerce', 'Healthcare')",
  "product_name": "string",
  "target_audience": "string",
  "business_model": "string"
}
```

**Technical Dependencies**:
- Python file system operations
- JSON configuration parsing
- Template string interpolation for prompt generation

### **Agent 0b: Pipeline Orchestrator** 
**Technical Purpose**: Automated pipeline execution with state tracking and resume capability

**Implementation Architecture**:
- **Phase 1 Script**: `run_pipeline_phase1.py` (Foundation: Agents 1-4)
- **Phase 2 Script**: `run_pipeline_phase2.py` (Content Generation: Agents 5-9)
- **State Management**: JSON-based execution tracking with checkpoint persistence
- **Mode Detection**: Automatic operational mode identification based on file availability

**Technical Features**:
```python
# State tracking structure
{
  "execution_state": {
    "current_phase": "PHASE_1|PHASE_2",
    "completed_agents": ["1", "2", "3"],
    "failed_agents": [],
    "resume_point": "agent_4",
    "quality_gate_status": "PENDING|PASSED|FAILED"
  }
}
```

**Dependencies**: Cross-agent file management, API rate limiting, error recovery mechanisms

---

## **Phase 1: Strategic Foundation Building**

### **Agent 1: Message House Engine**
**Technical Purpose**: Strategic question processing and core messaging foundation generation

**Input Specification**:
- **Template**: Available at `../examples/12_questions_template.md` - copy to agent input for processing
- **Format**: Structured markdown with question-answer pairs
- **Validation**: Required answers to all 12 strategic questions

**Output Specification**:
- **File**: `message_house.md`
- **Structure**: Strategic messaging document with core value propositions
- **Dependencies**: Feeds directly into Agents 2, 5, and 9

**Learning System Implementation**:
- **Example Map Architecture**: Reads all files in `5_labeled_json/` for quality patterns
- **Quality Threshold**: 8.0+ score examples become reference templates
- **Improvement Integration**: Human evaluation feedback guides content enhancement

**Technical Integration**:
```python
# Agent 1 execution pattern
def process_message_house(input_path, project_name):
    questions = load_strategic_questions(f"{input_path}/{project_name}/")
    examples = load_example_from_json()  # Learning system
    message_house = generate_content(questions, examples)
    save_output(message_house, f"3_unlabeled/{project_name}/message_house.md")
```

### **Agent 2: Brand Persona Generator**
**Technical Purpose**: Brand-side persona creation from strategic messaging foundation

**Input Dependencies**:
- **Primary**: `message_house.md` from Agent 1
- **Validation**: Ensures message house content availability before execution

**Output Specification**:
- **File**: `brand_side_persona.md` 
- **Content**: Ideal customer persona from brand perspective
- **Format**: Structured persona document with demographics, psychographics, behavior patterns

**Fallback Functionality**:
- **Brand Mode**: Output used for Agent 7 and 8 when customer data unavailable
- **File Copying Logic**: Automatic distribution to downstream agents in Brand Mode

**Learning System**: Example Map architecture with quality filtering (8.0+ threshold)

### **Agent 3: Customer Reality Analyzer**
**Technical Purpose**: Authentic customer persona extraction from review data

**Input Specification**:
- **File Format**: CSV with customer reviews and ratings
- **Required Fields**: `review_text`, `rating`, `customer_id` (minimum)
- **Processing**: Natural language analysis of customer feedback patterns

**Strategic Design Decision**:
- **No Iterative Learning**: Intentionally excluded from Example Map system
- **Rationale**: Preserves fresh analytical reasoning for each dataset
- **Benefit**: Prevents overfitting to previous analysis patterns

**Output Specification**:
- **File**: `customer_side_persona.md`
- **Content**: Authentic customer reality based on review analysis
- **Integration**: Feeds Agents 4, 5, 7, 8, 9

**Technical Processing**:
```python
# Customer analysis workflow
def analyze_customer_reviews(csv_path):
    reviews = load_csv_data(csv_path)
    patterns = extract_behavioral_patterns(reviews)
    sentiment_analysis = process_sentiment(reviews)
    persona = generate_authentic_persona(patterns, sentiment_analysis)
    return persona
```

### **Agent 4: Strategic Gap Analysis**
**Technical Purpose**: Quantitative gap identification between brand vision and customer reality

**Input Dependencies**:
- **Required**: `brand_side_persona.md` (Agent 2) AND `customer_side_persona.md` (Agent 3)
- **Validation**: Both inputs must be available for execution

**Technical Framework**:
- **4-Phase Methodology**: Systematic gap analysis with quantitative scoring
- **Smart File Detection**: Automatic input file discovery with validation
- **Evidence-Based Analysis**: Quantifiable gap identification with priority scoring

**Output Specification**:
- **File**: `gap_analysis_report.md`
- **Structure**: Quantified gaps with actionable recommendations
- **Business Integration**: Decision-ready insights for strategy refinement

**Learning System Implementation**: Example Map architecture with strategic gap pattern recognition

---

## **Critical Quality Control Checkpoint**

### **Agent 5: Keywords Bank (Two-Phase Architecture)**
**Technical Purpose**: Strategic keyword generation with mandatory quality gate

**Phase 1: Foundation Generation**
- **Input**: Agent 1 (message house) + Agent 2 (brand persona) + optional Agent 3 (customer persona)
- **Output**: Strategic keyword foundation for human evaluation
- **Quality Gate**: Manual evaluation required with ≥7.0 threshold score

**Phase 2: Expansion Engine** 
- **Trigger**: Phase 1 score ≥7.0 (automated validation)
- **Processing**: Massive keyword expansion (150+ keywords across 6 vectors)
- **Output**: Comprehensive keyword database for downstream agents

**Technical Implementation**:
```python
# Quality gate validation
def validate_keywords_quality(evaluation_score):
    if evaluation_score >= 7.0:
        return "APPROVED_FOR_PHASE_2"
    else:
        return "REQUIRES_REVISION"
```

**Strategic Business Logic**: Solves Internal→External asset misalignment problem by ensuring quality foundation before volume generation

**Optional Enhancement**: `external_keywords.csv` integration for additional keyword sources

---

## **Phase 2: Content Generation at Scale**

### **Agent 7: Testimonial Engine**
**Technical Purpose**: Authentic testimonial generation with strategic message integration

**Input Priority System**:
- **Primary**: Agent 3 (customer persona) + Agent 5 (keywords bank)
- **Fallback**: Agent 2 (brand persona) in Brand Mode when customer data unavailable

**Strategic Blending Framework**:
- **Technical Approach**: Weaves brand messaging into authentic customer voice patterns
- **Output Variety**: Short, medium, long-form testimonials with diverse customer profiles
- **Format Structure**: Multiple testimonial variations with attribution details

**Learning System**: Example Map architecture for authenticity pattern recognition

**Technical Integration**:
```python
# Testimonial generation workflow
def generate_testimonials(persona_source, keywords):
    if customer_persona_available():
        persona = load_customer_persona()
    else:
        persona = load_brand_persona()  # Brand Mode fallback
    
    testimonials = blend_strategy_with_voice(persona, keywords)
    return format_testimonial_library(testimonials)
```

### **Agent 8: Social Media Content Generator**
**Technical Purpose**: Platform-optimized social media content with consistent brand voice

**Character Innovation Architecture**:
- **"Emma" Brand Ambassador**: Dedicated persona with consistent voice across content
- **Content Recipe Matrix**: 12 proven patterns (3 recipes × 4 categories)
- **Category Framework**: Real Experience, Community, Product Feature, Brand Info

**Input Dependencies**:
- **Required**: Agent 5 (keywords bank)
- **Optional**: Agent 3 (customer persona) or Agent 2 (brand persona) in Brand Mode
- **Enhancement**: Agent 6.5 (platform personas) for Twitter-specific optimization

**Platform Intelligence Integration**:
```python
# Platform-specific optimization
def optimize_for_platform(base_content, platform_data=None):
    if platform_data and agent_6_5_available():
        return apply_platform_intelligence(base_content, platform_data)
    return base_content  # Graceful degradation
```

**Output Structure**: 12 social media posts across 4 strategic categories with engagement optimization

### **Agent 9: Website Copy with Strategic Logic**
**Technical Purpose**: Psychology-driven website copy with strategic reasoning generation

**Core Innovation - Two-Phase Process**:
1. **Strategic Logic Generation**: Creates compelling psychology reasoning for content ordering
2. **Content Module Creation**: Provides 7 homepage architecture modules with conversion psychology

**Strategic Design Decision**:
- **No Iterative Learning**: Intentionally excluded from Example Map system  
- **Rationale**: Preserves creative strategic reasoning for each brand's unique psychology
- **Value**: "When user sees the logic and they buy it, the next asset is solid"

**Input Dependencies**:
- **Required**: Agent 1 (message house) + Agent 5 (keywords bank)
- **Optional**: Agent 3 (customer persona) for enhanced customer psychology insights

**Technical Output Structure**:
```markdown
# Strategic Logic (Phase 1)
- Psychology reasoning for content ordering
- Conversion optimization rationale
- User journey strategic framework

# Content Modules (Phase 2)  
- Hero section with value proposition
- Problem/solution modules
- Social proof integration
- Call-to-action optimization
```

---

## **Optional Enhancement Layer**

### **Agent 6: Stakeholder Strategy Decks**
**Technical Purpose**: Internal stakeholder communication optimization

**Conditional Execution Logic**:
- **Mode 1**: Uses Agent 4 (gap analysis) when available for comprehensive insights
- **Mode 2**: Uses Agent 2 (brand persona) as fallback for brand-focused strategy

**Output Specification**: Tailored talking points and strategic plans for internal teams

### **Agent 6.5: Platform Intelligence Plugin (Optional)**
**Technical Purpose**: Platform-specific audience intelligence enhancement

**Plugin Architecture Design**:
- **Enhancement Model**: Improves quality when present, system works perfectly without
- **Integration Point**: Sits at internal strategy → external content transition
- **Scalability**: Framework supports future platform additions (LinkedIn, Instagram, TikTok)

**Input Dependencies**: Agent 2 (brand persona) + Agent 3 (customer persona) + Agent 5 (keywords bank)
**Output**: `platform_personas.md` with platform-specific audience intelligence

### **Agent 10: Consistency Validation**
**Technical Purpose**: Final quality assurance and strategic consistency validation

**Input Requirements**: All output assets from Agents 1, 2, 3, 4, 5, 7, 8, 9
**Processing**: Cross-asset content analysis for messaging alignment and strategic consistency
**Output**: `consistency_report.md` with quality scoring and alignment validation

---

## **Technical Integration Patterns**

### **File Management System**
```bash
# Standard agent folder structure
agent_name/
├── 1_input/{project_name}/           # Project-specific inputs
├── 2_system_assets/{project_name}/   # Generated system prompts
├── 3_unlabeled/{project_name}/       # Project-specific outputs
├── 5_labeled_json/                   # Shared learning database
├── scripts/                          # Execution logic
└── config.json                       # API configuration
```

### **Learning System Integration**
**Agents with Example Map Learning**: 1, 2, 4, 7 (quality pattern recognition)
**Agents without Learning**: 3, 9 (strategic decision to preserve creative reasoning)
**Quality Threshold**: 8.0+ overall score for example inclusion

### **API Configuration Management**
```json
{
  "api_key": "claude_api_key",
  "model": "claude-3-sonnet-20240229",
  "max_tokens": 4000,
  "temperature": 0.7,
  "project_specific_overrides": {}
}
```

---

*For system architecture and operational details, see [`system_architecture.md`](system_architecture.md)*  
*For implementation procedures and deployment guidance, see [`implementation_guide.md`](implementation_guide.md)*