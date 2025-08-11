# Technical Specifications

This directory contains comprehensive technical documentation for the AI-Go-To-Market-Engine system architecture, implementation details, and design specifications.

## 📋 Documentation Overview

### **System Architecture & Design**
- **[`system_architecture.md`](system_architecture.md)** → Complete system design, core principles, and current capabilities
- **[`agent_specifications.md`](agent_specifications.md)** → Detailed specifications for all 11 agents and their dependencies
- **[`design_decisions.md`](design_decisions.md)** → Architectural rationale and design philosophy

### **Implementation & Integration**
- **[`implementation_guide.md`](implementation_guide.md)** → Setup, deployment, and system extension guide
- **[`data_store_specification.md`](data_store_specification.md)** → Multi-project data architecture and storage patterns

### **Visual Documentation**
- **[`diagrams/pipeline_diagrams.md`](diagrams/pipeline_diagrams.md)** → System flowcharts and visual architecture (Mermaid format)
- **[`diagrams/screenshots/`](diagrams/screenshots/)** → Visual system documentation and flowchart assets

### **Historical Reference**
- **[`archive/design_evolution.md`](archive/design_evolution.md)** → Strategic evolution history and version milestones

---

## 🎯 Quick Navigation by Technical Need

### **"I Need Complete System Understanding"**
**Primary Path**: `system_architecture.md` → `agent_specifications.md` → `diagrams/pipeline_diagrams.md`

**Use Case**: Architecture review, system evaluation, technical due diligence

### **"I'm Implementing/Deploying the System"**
**Primary Path**: `implementation_guide.md` → `data_store_specification.md` → `agent_specifications.md`

**Use Case**: Production deployment, system setup, operational configuration

### **"I'm Extending/Contributing to the System"**
**Primary Path**: [`../contrib/`](../contrib/) → `design_decisions.md` → `agent_specifications.md`

**Use Case**: Feature development, agent creation, system enhancement

### **"I Need Visual System Overview"**
**Primary Path**: `diagrams/pipeline_diagrams.md` → `system_architecture.md`

**Use Case**: Presentations, system demos, architectural discussions

---

## 🏗️ System Architecture Summary

The AI-Go-To-Market-Engine is a **modular, self-improving AI pipeline** that transforms strategic business input into comprehensive marketing assets through an 11-agent orchestrated workflow.

### **Core Architecture Principles**
- **Modular Agent Design**: Each agent is self-contained with specific function
- **Human-in-the-Loop**: Quality control at strategic input and output evaluation points
- **Self-Improving System**: Agents learn from human evaluation feedback
- **Asset-Driven Pipeline**: Connected workflow where agent outputs become downstream inputs

### **System Components**
- **Meta-Orchestration**: Project configuration and pipeline execution (Agents 0a/0b)
- **Strategic Foundation**: Message house, personas, and gap analysis (Agents 1-4)
- **Content Generation**: Keywords, testimonials, social media, website copy (Agents 5-9)
- **Quality Assurance**: Consistency validation and system learning (Agent 10)

### **Operational Modes**
- **Validation Mode**: Complete brand vs customer analysis with gap identification
- **Brand Mode**: Streamlined execution for products without customer review data
- **Competitor Analysis Mode**: Reverse-engineering competitor strategies

---

## 📊 Technical Specifications at a Glance

| Component | Implementation | Documentation Reference |
|-----------|----------------|-------------------------|
| **Agent System** | Python-based modular architecture | `agent_specifications.md` |
| **Data Storage** | Multi-project isolation with JSON learning | `data_store_specification.md` |
| **Pipeline Orchestration** | Two-phase execution with state tracking | `implementation_guide.md` |
| **Quality Control** | Human evaluation + automated consistency | `system_architecture.md` |
| **Learning System** | Example Map architecture with quality filtering | `design_decisions.md` |

---

## 🔗 Integration Points

### **External System Integration**
- **API Configuration**: `../config.template.json` for Claude API integration
- **Input Templates**: `../examples/12_questions_template.md` for strategic input
- **Output Assets**: Generated marketing content in agent `3_unlabeled/` folders

### **Development Integration**
- **Extension Framework**: `../contrib/` for agent development and contribution
- **Usage Examples**: `../examples/` for implementation patterns and templates

---

*For user-facing documentation and quick start guides, see [`../docs/`](../docs/)*