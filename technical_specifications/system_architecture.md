# System Architecture

## **Core Vision & Principles**

The AI-Go-To-Market-Engine is a modular, self-improving AI ecosystem designed to translate high-level strategy into a suite of actionable marketing assets. The system transforms strategic business input into comprehensive content through an orchestrated pipeline of specialized AI agents.

### **Foundational Principles**

**Modular Agent Architecture**
Each agent is a standalone, self-contained workflow with a specific function. This design enables flexibility, simplifies maintenance, and allows for system expansion without disrupting existing functionality.

**Human-in-the-Loop Quality Control**
Human intelligence is integrated at two critical points: providing high-quality strategic input at the beginning and evaluating AI output at the end. This ensures relevance, accuracy, and strategic alignment throughout the pipeline.

**Self-Improving System Architecture**
Every agent learns from human evaluation through structured feedback loops. Evaluation data is stored as JSON and used to refine future outputs, creating a system that becomes more effective with each use.

**Asset-Driven Pipeline Design**
The system operates as a connected pipeline where each agent's output document becomes input for downstream agents. This creates a cohesive workflow that maintains strategic consistency across all generated assets.

---

## **System Blueprint: Implementation Architecture**

*For detailed agent capabilities and business innovations, see [Main README.md](../README.md#technical-architecture-deep-dive)*

### **Pipeline Execution Flow**

**Phase 0: System Configuration & Orchestration**
- **Agent 0a** → Project workspace setup, multi-project isolation, system prompt generation
- **Agent 0b** → Two-phase execution management, state persistence, dependency validation

**Phase 1: Strategic Foundation Building**  
- **Agent 1** → Strategic input processing (12-question template → message house)
- **Agent 2** → Brand persona generation (message house → brand-side persona)
- **Agent 3** → Customer analysis (CSV reviews → customer-side persona)  
- **Agent 4** → Gap analysis (brand persona + customer persona → strategic gaps)

**Critical Quality Control Checkpoint**
- **Agent 5** → Keywords generation with ≥7.0 quality gate threshold

**Phase 2: Content Generation at Scale**
- **Agent 7** → Testimonial generation (customer persona + keywords → testimonials)
- **Agent 8** → Social media content (keywords + customer persona → social posts)
- **Agent 9** → Website copy generation (message house + keywords + customer persona → website modules)

**Optional Enhancement Layer**
- **Agent 6** → Stakeholder strategy decks (conditional execution)
- **Agent 6.5** → Platform-specific intelligence (plugin architecture)
- **Agent 10** → Final consistency validation (all assets → consistency report)

### **Dependency Matrix**

| Agent | Required Inputs | Optional Inputs | Output Dependencies |
|-------|----------------|----------------|-------------------|
| 1 | 12-question Q&A | - | → 2, 5, 9 |
| 2 | Agent 1 output | - | → 4, 5, 6 (Brand Mode: → 7, 8) |
| 3 | Customer CSV data | - | → 4, 5, 7, 8, 9 |
| 4 | Agent 2 + Agent 3 | - | → 6 |
| 5 | Agent 1, Agent 2 | Agent 3 (Validation Mode) | → 7, 8, 9 |
| 7 | Agent 5 | Agent 3 (Validation), Agent 2 (Brand Mode) | → 8, 9 |
| 8 | Agent 1, Agent 2, Agent 5, Agent 7 | Agent 6.5 | → 10 |
| 9 | Agent 1, Agent 5, Agent 7 | - | → 10 |

---

## **Operational Modes: Technical Implementation**

### **Mode Detection Logic**
```python
# Simplified mode detection algorithm
def detect_execution_mode(project_path):
    has_message_house = check_file_exists(f"{project_path}/message_house_input.md")
    has_customer_data = check_file_exists(f"{project_path}/customer_reviews.csv")
    
    if has_message_house and has_customer_data:
        return "VALIDATION_MODE"  # Full pipeline
    elif has_message_house:
        return "BRAND_MODE"       # Streamlined pipeline
    else:
        return "COMPETITOR_MODE"  # Manual configuration
```

### **Pipeline Execution Patterns**

**Validation Mode Technical Flow**
```
Input Validation → Agent 1 → Agent 2 → Agent 3 → Agent 4 → Agent 5 (Quality Gate) 
                                                                    ↓ (≥7.0 score)
Agent 10 ← Agent 9 ← Agent 8 ← Agent 7 ← Agent 6 (Optional) ←─────┘
```

**Brand Mode Technical Flow**  
```
Input Validation → Agent 1 → Agent 2 → Agent 5 (Quality Gate)
                                           ↓ (≥7.0 score)  
Agent 10 ← Agent 9 ← Agent 8 ← Agent 7 ←───┘
```

**File Transfer Logic**: Agent 2 output copied to Agent 7, 8 input directories in Brand Mode

---

## **Current System Capabilities: Technical Implementation**

### **Multi-Project Data Architecture**
**Folder Structure Pattern**:
```
{agent_name}/
├── 1_input/{project_name}/           ← Isolated project inputs
├── 2_system_assets/{project_name}/   ← Generated system prompts  
├── 3_unlabeled/{project_name}/       ← Project-specific outputs
├── 5_labeled_json/                   ← Shared learning database
```

**Project Detection Algorithm**: Cross-agent project validation with timestamp-based naming
**Isolation Mechanism**: Filesystem-level separation preventing cross-project contamination

### **Iterative Learning System: Technical Architecture**

**Example Map Implementation**:
```python
def load_example_from_json():
    """Dynamic learning from ALL evaluation files"""
    json_files = glob("5_labeled_json/*.json")
    high_quality_examples = []
    
    for file in json_files:
        data = json.load(file)
        if data.get('overall_score', 0) >= 8.0:
            high_quality_examples.append(format_example(data))
    
    return combine_top_examples(high_quality_examples[:3])
```

**Learning Integration**: System prompts dynamically enhanced with quality-filtered examples
**Backward Compatibility**: Graceful degradation from 0 to 100+ evaluation files

### **Two-Phase Pipeline Orchestration: Technical Details**

**State Management**:
```json
{
  "execution_state": {
    "current_phase": "PHASE_1",
    "completed_agents": ["1", "2", "3", "4"],
    "current_agent": "5",
    "quality_gate_status": "PENDING_EVALUATION"
  }
}
```

**Resume Capability**: JSON-based checkpoint system with agent-level granularity
**Error Handling**: Retry logic with exponential backoff and state preservation

---

## **Technical Implementation Details**

### **Agent Execution Environment**
**Runtime**: Python 3.x with standard library dependencies
**API Integration**: Claude API via HTTP requests with retry logic
**File Operations**: Atomic file operations with backup creation
**Configuration Management**: JSON-based agent configuration with project-specific overrides

### **Quality Control Implementation**
**Human Evaluation Interface**: 
- Structured JSON scoring system (overall_score, detailed_feedback)
- 10-point scoring with threshold-based quality gates
- Evaluation persistence in `5_labeled_json/` directories

**Automated Consistency Checking**:
- Cross-asset content analysis for messaging alignment
- Strategic consistency validation across all generated content
- Automated scoring with human review integration

### **Plugin Architecture: Technical Framework**
**Agent 6.5 Integration Pattern**:
```python
def enhance_with_platform_intelligence(base_content, platform_data=None):
    if platform_data and agent_6_5_available():
        return apply_platform_optimization(base_content, platform_data)
    return base_content  # Graceful degradation
```

**Extensibility Design**: Standardized plugin interface for new agent integration
**Optional Enhancement Pattern**: Core system functionality preserved without plugins

---

## **Integration Architecture: Technical Specifications**

### **External API Dependencies**
- **Anthropic Claude API**: Primary LLM integration with rate limiting and error handling
- **File System**: Local storage for all data persistence and state management
- **JSON Processing**: Structured data handling for configuration and learning systems

### **Data Flow Architecture**
**Input Processing**: Markdown template parsing with validation
**Asset Generation**: Structured markdown output with consistent formatting  
**Learning Data**: JSON serialization of evaluation data with metadata
**State Persistence**: JSON-based execution tracking with recovery mechanisms

### **Performance Characteristics**
**Execution Time**: ~15-30 minutes for full Validation Mode pipeline
**Resource Usage**: Moderate memory footprint with file-based storage
**Scalability**: Linear scaling with project count, agent-level parallelization possible
**Reliability**: Checkpoint-based resume capability with comprehensive error handling

---

*For agent-specific technical details and API specifications, see [`agent_specifications.md`](agent_specifications.md)*  
*For deployment and operational procedures, see [`implementation_guide.md`](implementation_guide.md)*