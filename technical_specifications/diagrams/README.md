# System Architecture Diagrams

This folder contains visual documentation for the AI-Go-To-Market-Engine system architecture using Mermaid diagrams.

## 📊 Available Diagrams

### **1. [Pipeline Execution Flow](pipeline_execution_flow.md)**
**Purpose**: Complete system execution flow with orchestration, modes, and phases

**Shows**:
- Agent 0a/0b orchestration system
- Two operational modes (Validation vs Brand)
- Phase 1: Foundation Building → Quality Gate → Phase 2: Content Generation
- Optional enhancement layer (Agent 6, 6.5, 10)
- Complete execution timeline (15-20 minutes)

**When to use**: Understanding overall system workflow and execution sequence

### **2. [File Dependency Flow](file_dependency_flow.md)**
**Purpose**: Agent file transfer dependencies and mode-specific data flows

**Shows**:
- Agent X output → Agent Y input relationships
- Actual file names (message_house.md, keywords_bank.md, etc.)
- Mode-specific fallback logic (Brand Mode vs Validation Mode)
- Critical dependency paths for content generation

**When to use**: Understanding data flow and agent integration requirements

## 🖥️ Viewing Instructions

### **GitHub (Recommended)**
Diagrams render automatically when viewing `.md` files on GitHub.
- Click on any diagram file above
- Diagrams display natively in GitHub interface

### **VS Code**
Install the Mermaid extension for preview:
```bash
ext install bierner.markdown-mermaid
```

### **Mermaid Live Editor**
For editing or standalone viewing:
1. Visit [mermaid.live](https://mermaid.live)
2. Copy diagram code from any `.md` file
3. Paste into editor for interactive viewing

### **Other Markdown Renderers**
Most modern markdown renderers support Mermaid:
- GitLab
- Notion  
- Obsidian
- Typora

## 🏗️ Architecture Overview

### **System Characteristics**
- **11-Agent Pipeline**: Complete marketing asset generation system
- **Two-Phase Execution**: Strategic foundation → Quality gate → Content generation  
- **Mode Flexibility**: Validation Mode (8 agents) vs Brand Mode (6 agents)
- **Quality Control**: Human evaluation checkpoint at ≥7.0 threshold
- **State Persistence**: Resume capability with error recovery

### **Enterprise Features**
- **Multi-Project Isolation**: Concurrent project management
- **Plugin Architecture**: Optional enhancement agents (6, 6.5, 10)
- **API Integration**: Claude 3.5 Sonnet with retry mechanisms
- **Learning System**: Example Map architecture for quality improvement

## 📁 Generated Asset Portfolio

One complete pipeline execution produces:

### **Phase 1 Assets (4 files)**
- `message_house.md` - Strategic messaging foundation
- `brand_side_persona.md` - Brand's ideal customer vision  
- `customer_side_persona.md` - Real customer analysis (Validation Mode only)
- `gap_analysis.md` - Brand vs reality strategic gaps (Validation Mode only)

### **Phase 2 Assets (4 files)**
- `keywords_bank.md` - Strategic keyword foundation + expansion
- `testimonials.md` - Marketing testimonials with authentic voice
- `twitter_posts.md` - Social media content strategy
- `website_copy.md` - Homepage copy with psychology logic

### **Optional Enhancement Assets (2-3 files)**
- `stakeholder_strategy.md` - Internal strategy decks (Agent 6)
- `platform_personas.md` - Platform-specific intelligence (Agent 6.5)
- `consistency_report.md` - Quality validation report (Agent 10)

**Total Output**: 6-10 production-ready marketing assets per pipeline execution

## 🔄 Workflow Integration

### **Development Workflow**
1. **Planning**: Use diagrams to understand agent dependencies
2. **Implementation**: Reference file flows for integration logic  
3. **Testing**: Validate against execution flow patterns
4. **Debugging**: Trace issues through dependency chains

### **Documentation Workflow**
1. **System Changes**: Update diagrams when modifying agent flows
2. **Architecture Reviews**: Use visual documentation for stakeholder alignment
3. **Onboarding**: Start new developers with execution flow overview

---

## 📚 Related Documentation

- **[System Architecture](../system_architecture.md)** - Technical implementation details
- **[Agent Specifications](../agent_specifications.md)** - Individual agent documentation  
- **[Implementation Guide](../implementation_guide.md)** - Production deployment procedures
- **[Main README](../../README.md)** - Project overview and business value

---

*Visual documentation for enterprise-scale AI agent orchestration system*