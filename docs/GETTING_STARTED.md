# Getting Started with AI-Go-To-Market-Engine

Welcome! This guide will get you up and running with the AI-Go-To-Market-Engine in minutes.

## 🚀 Quick Start

### **1. Clone & Setup**
```bash
git clone https://github.com/Ace-Hsu/AI-Go-To-Market-Engine.git
cd AI-Go-To-Market-Engine
```

### **2. Configure API Access**
```bash
# Copy the template to create your config
cp config.template.json config.json

# Edit config.json with your Anthropic API key
# Replace "YOUR_ANTHROPIC_API_KEY_HERE" with your actual key
```

### **3. Install Dependencies**
```bash
# Navigate to any agent directory
cd agents/message_house_agent
pip install -r requirements.txt
```

### **4. Run Your First Agent**
```bash
python scripts/generate_simple.py
```

## 🎯 Your First Complete Pipeline Run

### **Step 1: Prepare Your Strategic Input** 
**⚡ CRITICAL:** This is the most important step that determines your entire output quality.

1. Navigate to `examples/12_questions_template.md` 
2. Copy the strategic questions template to create your own Q&A file
3. Fill in your strategic answers with deep business conviction - these become the PRE-SYSTEM foundation that drives all 8-10 marketing assets

**Why This Matters:** The AI agents can only be as strategic as the human expert input you provide. Quality strategic answers = quality marketing assets.

### **Step 2: Run the Complete Pipeline**

**Option A: Manual Execution (Learn the System)**
```bash
# Start with strategic foundation
cd agents/message_house_agent
python scripts/generate_simple.py

# Continue with persona development
cd ../user_story_agent  
python scripts/generate_simple.py

# Run gap analysis
cd ../gap_analysis_agent
python scripts/generate_simple.py
```

**Option B: Automated Pipeline (Enterprise Mode)**
```bash
# Full automated execution
cd agents/agent_0b_orchestrator
python scripts/run_pipeline_phase1.py
# (Evaluate keywords quality gate)
python scripts/run_pipeline_phase2.py
```

## 📋 What You'll Generate

After a complete run, you'll have:
- **Message House** - Core strategic messaging
- **Brand Personas** - Ideal customer profiles  
- **Gap Analysis** - Strategic insights
- **Keywords Bank** - Comprehensive keyword strategy
- **Testimonials** - Marketing testimonials
- **Social Media Content** - Twitter strategy
- **Website Copy** - Homepage and product copy

## 🔧 Configuration Notes

### **API Key Setup**
- **Never commit config.json files** (they contain your API keys)
- Each agent directory needs its own config.json
- Copy `config.template.json` to each agent directory as needed

### **Project Organization**
- Each agent organizes work in project-specific folders
- Input files go in `1_input/{project_name}/`
- Generated assets appear in `3_unlabeled/{project_name}/`

## 📚 Next Steps

### **Learn the System**
- Read [`../technical_specifications/README.md`](../technical_specifications/README.md) for complete architecture
- Explore [`../examples/`](../examples/) for sample projects
- Check individual agent README.md files for detailed instructions

### **Try Advanced Features**
- Multi-project management with Agent 0a configurator
- Quality evaluation and iterative improvement
- Plugin enhancements (Platform Intelligence)

### **Get Help**
- See [`PROJECT_STRUCTURE.md`](PROJECT_STRUCTURE.md) for navigation guidance
- Check [`../visual_documentation/pipeline_diagrams.md`](../visual_documentation/pipeline_diagrams.md) for system flowcharts
- Review individual agent documentation for troubleshooting

## ⚠️ Important Security Notes

- **API Keys**: Never commit config.json files to version control
- **Project Data**: Generated assets may contain business-sensitive information
- **Multi-Project Isolation**: Each project runs in complete isolation for security

---

**Ready to build your Go-To-Market strategy? Start with the 12 Strategic Questions and let the AI agents transform your vision into a complete marketing asset portfolio!**

*For complete technical documentation, see [`../technical_specifications/`](../technical_specifications/)*