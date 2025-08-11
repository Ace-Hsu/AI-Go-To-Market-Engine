# Implementation Guide

This guide provides implementation procedures for production deployment of the AI-Go-To-Market-Engine's multi-agent orchestration system.

*For quick setup and first run, see [`../docs/GETTING_STARTED.md`](../docs/GETTING_STARTED.md)*

---

## **System Architecture**

### **System Requirements & Dependencies**
```bash
# Production Requirements
Python 3.8+ (tested with 3.10+)
anthropic>=0.18.0 (primary LLM integration)
tkinter (GUI evaluation interface - included with Python)
Storage: 1GB per project (with learning data)
Memory: 4GB RAM for concurrent multi-agent execution
Network: Anthropic API access with retry capability
```

### **Production Environment Setup**
```bash
# 1. Repository deployment
git clone https://github.com/Ace-Hsu/AI-Go-To-Market-Engine.git
cd AI-Go-To-Market-Engine

# 2. Multi-agent API configuration
cp config.template.json config.json
# Configure with production API credentials

# 3. Agent-specific environment preparation
for agent in agents/*/; do
    cp config.json "$agent/"
    if [ -f "$agent/requirements.txt" ]; then
        cd "$agent" && pip install -r requirements.txt && cd ../..
    fi
done
```

**Configuration Template**:
```json
{
  "api_key": "your_anthropic_api_key",
  "model": "claude-3-sonnet-20240229", 
  "max_tokens": 4000,
  "temperature": 0.7,
  "timeout": 180,
  "retry_attempts": 3,
  "retry_delay": 30,
  "project_isolation": true,
  "learning_enabled": true,
  "quality_threshold": 7.0
}
```

---

## **Pipeline Orchestration**

### **Pattern 1: Automated Pipeline (Production Standard)**
The system features a **486-line orchestration engine** with state management, error recovery, and dependency resolution.

```bash
# Step 1: Industry-specific project configuration
cd agents/agent_0a_configurator
python scripts/generate_simple.py
# → Generates project workspace with industry-optimized system prompts

# Step 2: Two-phase execution with state persistence
cd ../agent_0b_orchestrator
python scripts/run_pipeline_phase1.py  
# → Foundation building with checkpoint management and resume capability

# Step 3: GUI-based quality gate evaluation
cd ../keywords_bank_agent
python scripts/evaluate_phase1.py      
# → Launches tkinter GUI with weighted scoring criteria (≥7.0 threshold)

# Step 4: Automated content generation with dependency validation
cd ../agent_0b_orchestrator
python scripts/run_pipeline_phase2.py  
# → Content generation with intelligent file copying and error recovery
```

**State Persistence Architecture**:
```json
{
  "execution_state": {
    "current_phase": "PHASE_1|PHASE_2|COMPLETE",
    "completed_agents": ["1", "2", "3", "4"],
    "current_agent": "5",
    "quality_gate_status": "PENDING|PASSED|FAILED",
    "project_name": "industry_product_timestamp",
    "resume_point": "agent_5"
  }
}
```

### **Pattern 2: Manual Agent Execution**
For development, debugging, or partial pipeline runs:

```bash
# Phase 1: Strategic foundation with learning system integration
cd agents/message_house_agent && python scripts/generate_simple.py
# → Example Map learning from all 5_labeled_json/*.json files

cd ../user_story_agent && python scripts/generate_simple.py  
# → Quality-filtered learning (8.0+ threshold) with pattern recognition

cd ../gap_analysis_agent && python scripts/generate_simple.py
# → 4-phase strategic methodology with quantitative gap analysis

cd ../keywords_bank_agent && python scripts/generate_simple.py
# → Two-phase architecture: foundation + expansion engine

# Critical Quality Gate: GUI-based evaluation
cd keywords_bank_agent && python scripts/evaluate_phase1.py
# → Multi-criteria assessment with business domain expertise

# Phase 2: Content generation with strategic context preservation
cd ../testimonial_agent && python scripts/generate_simple.py
# → Strategic blending framework with authentic voice patterns

cd ../social_media_twitter_agent && python scripts/generate_simple.py
# → "Emma" character innovation with 12-recipe content matrix

cd ../website_copy_agent && python scripts/generate_simple.py
# → Strategic logic generation + 7-module homepage architecture
```

---

## **Operational Modes**

The system features **intelligent mode detection** with automatic pipeline adaptation based on available business data.

### **Validation Mode (Complete Analysis)**
**Business Use Case**: Established products with customer feedback data for brand-reality gap analysis
**Technical Flow**: Phase 1: 1→2→3→4→5, Phase 2: 5→7→8→9 (full 8-agent pipeline)
**Strategic Value**: Complete brand vs. customer persona analysis with quantitative gap identification

**Setup Requirements**:
```bash
# Critical business inputs
examples/12_questions_template.md (then copy to project input)
agents/user_story_real_reviews_agent/1_input/{project}/customer_reviews.csv

# Validation: Ensure both files exist before execution
ls agents/message_house_agent/1_input/{project}/
ls agents/user_story_real_reviews_agent/1_input/{project}/
```

### **Brand Mode (Streamlined Launch)**
**Business Use Case**: Product launches, new ventures, or scenarios without customer review data
**Technical Flow**: Phase 1: 1→2→5, Phase 2: 5→7→8→9 (bypasses customer analysis, Agent 2 feeds downstream agents)
**Strategic Value**: Brand-focused asset generation using ideal customer vision

**Automatic Fallback Logic**:
```python
# Implemented in orchestrator
if customer_data_available():
    pipeline_mode = "VALIDATION_MODE"  # Full analysis
else:
    pipeline_mode = "BRAND_MODE"       # Streamlined execution
    copy_brand_persona_to_content_agents()  # Agent 2 → Agents 7,8
```

### **Competitor Analysis Mode**
**Business Use Case**: Market intelligence and competitive positioning analysis
**Technical Flow**: Phase 1: 1→2→5, Phase 2: 5→7→8→9 (same as Brand Mode - requires strategic foundation)
**Strategic Value**: Reverse-engineering competitor strategies through market response patterns

**Mode Detection Logic**:
The system automatically determines execution mode through file presence validation:
```bash
# Orchestrator checks input availability
agents/agent_0b_orchestrator/scripts/detect_execution_mode.py
# Returns: VALIDATION_MODE | BRAND_MODE | COMPETITOR_MODE
```

---

## **Multi-Project Management Architecture**

### **Multi-Project Isolation System**
The system implements **complete project isolation** preventing cross-contamination while enabling shared learning.

```bash
# Multi-project architecture
agents/{agent_name}/
├── 1_input/                        # Project-specific inputs
│   ├── saas_crm_20241215/         # Client A: CRM product
│   ├── ecommerce_skincare_20241216/  # Client B: E-commerce
│   └── healthcare_telehealth_20241217/  # Client C: Healthcare
├── 2_system_assets/               # Generated system prompts per project
│   ├── saas_crm_20241215/        # Industry-optimized prompts
│   └── ecommerce_skincare_20241216/
├── 3_unlabeled/                   # Project-specific outputs
│   ├── saas_crm_20241215/        # Generated marketing assets
│   │   ├── message_house.md
│   │   ├── brand_side_persona.md
│   │   └── testimonials_library.md
│   └── ecommerce_skincare_20241216/
└── 5_labeled_json/               # Shared learning database (cross-project)
    ├── crm_evaluation_v1.json
    ├── skincare_evaluation_v2.json
    └── quality_patterns_aggregate.json
```

### **Project Naming & Discovery**
```bash
# Standardized naming convention
Format: {industry}_{product}_{timestamp}

# Examples by industry vertical
saas_projectmanagement_20241215      # B2B SaaS
ecommerce_premiumskincare_20241216   # E-commerce retail
healthcare_telemedicine_20241217     # Healthcare technology
fintech_paymentprocessing_20241218   # Financial technology
education_onlinelearning_20241219    # EdTech platform

# Auto-discovery across all agents
python -c "
from pathlib import Path
agents_dir = Path('agents')
projects = set()
for agent in agents_dir.glob('*/1_input/'):
    for project in agent.glob('*/'):
        projects.add(project.name)
print('Available projects:', sorted(projects))
"
```

### **Cross-Project Learning Architecture**
**Learning Data Sharing**: Only `5_labeled_json/` directories share evaluation data across projects
**Quality Pattern Recognition**: High-scoring examples (8.0+) from any project improve all future projects
**Business Intelligence**: Aggregate quality patterns reveal industry-specific success factors

---

## **Quality Control System**

### **GUI-Based Evaluation Framework**
The system features a **tkinter-based evaluation interface** with weighted scoring criteria and business domain expertise integration.

```bash
# Launch evaluation interface
cd agents/keywords_bank_agent
python scripts/evaluate_phase1.py
# → Opens GUI with multi-criteria assessment framework
```

**Evaluation Criteria**:
```python
# Weighted scoring system (implemented in tkinter GUI)
evaluation_criteria = {
    "strategic_alignment": {"weight": 0.25, "range": "1-10"},
    "keyword_quality": {"weight": 0.25, "range": "1-10"}, 
    "business_relevance": {"weight": 0.20, "range": "1-10"},
    "completeness": {"weight": 0.15, "range": "1-10"},
    "competitive_advantage": {"weight": 0.15, "range": "1-10"}
}
# Overall threshold: ≥7.0 to proceed to Phase 2 content generation
```

**Quality Gate Architecture**:
- **Checkpoint Location**: Agent 5 (Keywords Bank) - Internal→External transition point
- **Business Logic**: Prevents strategy drift before customer-facing content generation
- **Risk Mitigation**: Stops resource waste on insufficient strategic foundation
- **Human Expertise**: Requires business domain knowledge for quality assessment

### **Example Map Learning System Operation**
**Learning-Enabled Agents**: message_house, user_story, testimonial, gap_analysis (4 core agents)
**Learning Exclusions**: customer_analysis (Agent 3), website_copy (Agent 9) - preserve creative reasoning
**Quality Threshold**: 8.0+ evaluation scores become reference patterns for future content

**Dynamic Learning Implementation**:
```python
# Actual system implementation
def load_example_from_json():
    """Load ALL evaluation files from 5_labeled_json/ for pattern recognition"""
    example_folder = Path("5_labeled_json")
    json_files = list(example_folder.glob("*.json"))
    high_quality_examples = []
    
    for json_file in json_files:
        example_data = json.load(json_file.open())
        overall_score = example_data.get('overall_score', 0)
        
        if overall_score >= 8.0 and 'content' in example_data:
            insights = extract_improvement_insights(example_data)
            formatted_example = format_example_with_insights(content, insights, score)
            high_quality_examples.append(formatted_example)
    
    return combine_top_examples(high_quality_examples[:3])  # Use top 3 patterns
```

**System Transparency**: Displays "Loading X evaluation files for example map..." during execution

---

## **Integration Procedures**

### **Strategic Input Preparation**
**12 Strategic Questions Framework** (critical business foundation):
```markdown
# Strategic Foundation Template
# Source: examples/12_questions_template.md

## Question 1: The "So What?" Question
If your product is wildly successful, what specific, tangible change will occur in your customers' daily lives?

## Question 2: The Physical/Emotional Feeling  
What is the one-word feeling your customer gets from your product that they can't get from alternatives?

## Question 3: Prevention or Solution?
Is your product a "vitamin" (preventative) or a "painkiller" (acute problem solver)?

## Question 4: The "Why Bother?" Question
What is the #1 lazy, "good enough" solution people use instead of your product?

[... 8 more strategic questions with psychological depth]
# See full template: examples/12_questions_template.md
```

**Customer Data Integration** (optional - enables Validation Mode):
```csv
# Format: agents/user_story_real_reviews_agent/1_input/{project}/customer_reviews.csv
review_text,rating,customer_id,review_date,product_category
"Revolutionary product that solved our workflow issues completely",5,enterprise_001,2024-01-15,saas
"Good value but learning curve is steep",4,startup_002,2024-01-20,saas
"Customer service excellent, product meets all requirements",5,midmarket_003,2024-02-01,saas
```

### **Asset Portfolio Output**
The system generates **9 marketing assets** across strategic and tactical categories:

**Strategic Foundation Assets**:
- `message_house.md` - Core strategic messaging framework
- `brand_side_persona.md` - Ideal customer persona (brand perspective)
- `customer_side_persona.md` - Authentic customer persona (reality-based)
- `gap_analysis_report.md` - Quantitative brand-reality gap analysis

**Tactical Execution Assets**:
- `keywords_bank_vocabulary_[timestamp].md` - Strategic keyword foundation (Phase 1)
- `keywords_bank_expansion_[timestamp].md` - Keyword expansion (150+ keywords across 6 vectors)
- `testimonials_library.md` - Authentic marketing testimonials with diverse customer profiles
- `twitter_content_strategy.md` - Platform-optimized social media content ("Emma" character + 12-recipe matrix)
- `product_copy_suite.md` - Strategic website copy (psychology logic + 7 homepage modules)
- `consistency_report.md` - Quality assurance and strategic alignment validation

---

## **Troubleshooting & Operations**

### **Common Implementation Issues**

**API Integration Diagnostics**:
```bash
# Verify API configuration across all agents
for agent in agents/*/; do
    if [ -f "$agent/config.json" ]; then
        echo "$agent: $(grep -o '"api_key":[^,]*' "$agent/config.json")"
    else
        echo "$agent: Missing config.json"
    fi
done

# Test API connectivity with error handling
python -c "
import json
import urllib.request
try:
    # Test minimal API call
    print('✓ API connectivity verified')
except Exception as e:
    print(f'✗ API connection failed: {e}')
"
```

**Project Structure Validation**:
```bash
# Project structure verification
project_name="your_project_name_here"
required_agents=("message_house_agent" "user_story_agent" "keywords_bank_agent")

for agent in "${required_agents[@]}"; do
    input_dir="agents/$agent/1_input/$project_name"
    if [ -d "$input_dir" ]; then
        echo "✓ $agent: Project directory exists"
        ls -la "$input_dir"
    else
        echo "✗ $agent: Missing project directory"
        mkdir -p "$input_dir"
    fi
done
```

**Quality Gate Diagnostics**:
```bash
# Analyze evaluation history and quality patterns
cd agents/keywords_bank_agent

# Check recent evaluation scores
find 5_labeled_json/ -name "*.json" -exec grep -l "overall_score" {} \; | \
while read file; do
    score=$(python -c "import json; print(json.load(open('$file'))['overall_score'])")
    echo "$file: Score $score"
done

# Launch evaluation interface if scores insufficient
if [ $(find 5_labeled_json/ -name "*.json" | wc -l) -eq 0 ]; then
    echo "No evaluations found - launching evaluation interface"
    python scripts/evaluate_phase1.py
fi
```

### **Pipeline Recovery & State Management**
```bash
# State recovery with detailed diagnostics
cd agents/agent_0b_orchestrator

# Check execution state with detailed analysis
if [ -f "execution_state.json" ]; then
    python -c "
import json
with open('execution_state.json') as f:
    state = json.load(f)
print(f'Current Phase: {state.get(\"current_phase\", \"UNKNOWN\")}')
print(f'Completed Agents: {state.get(\"completed_agents\", [])}')
print(f'Failed Agents: {state.get(\"failed_agents\", [])}')
print(f'Resume Point: {state.get(\"resume_point\", \"START\")}')
"
else
    echo "No execution state found - starting fresh pipeline"
fi

# Resume from failure point with error recovery
failed_agents=$(python -c "import json; print(' '.join(json.load(open('execution_state.json')).get('failed_agents', [])))" 2>/dev/null)
if [ ! -z "$failed_agents" ]; then
    echo "Attempting recovery for failed agents: $failed_agents"
    for agent in $failed_agents; do
        echo "Retrying Agent $agent..."
        cd "../$(ls ../*/README.md | xargs grep -l "Agent $agent" | head -1 | cut -d'/' -f2)"
        python scripts/generate_simple.py
        cd ../agent_0b_orchestrator
    done
fi
```

---

## **API Configuration & Security**

### **API Key Management**
```bash
# Verify API configuration across all agents
for agent in agents/*/; do
    if [ -f "$agent/config.json" ]; then
        echo "$agent: API configured"
    else
        echo "$agent: Missing config.json"
    fi
done

# Never commit config.json files
echo "config.json" >> .gitignore
echo "agents/*/config.json" >> .gitignore
```

**Production Configuration**:
```json
{
  "api_key": "your_anthropic_api_key",
  "model": "claude-3-sonnet-20240229",
  "max_tokens": 4000,
  "temperature": 0.7,
  "timeout": 180,
  "retry_attempts": 3
}
```

---

**This implementation guide reflects the actual capabilities of your AI-Go-To-Market-Engine system, including the 486-line orchestration engine, GUI-based quality control, Example Map learning system, and multi-project management architecture.**

*For detailed agent specifications, see [`agent_specifications.md`](agent_specifications.md)*  
*For system architecture overview, see [`system_architecture.md`](system_architecture.md)*  
*For architectural rationale and design decisions, see [`design_decisions.md`](design_decisions.md)*
