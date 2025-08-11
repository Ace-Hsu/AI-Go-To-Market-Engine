# Quick Start Guide - User Story Agent

## How to Use This System

### Prerequisites
- Python 3.x installed
- Claude API key configured in `config.json`
- Message house documents from message_house_agent

### Complete Workflow

#### **Step 1: Prepare Input**
1. Copy message house document from `../message_house_agent/3_unlabeled/` (e.g., `messagehouse_20250714_154014.md`)
2. Place in `1_input/` folder
3. Ensure it follows the message house format (Roof, Pillars, Foundation)
4. Remove any example files if present - script uses most recent file

#### **Step 2: Generate User Stories**
```bash
python scripts/generate_simple.py
```
- Reads your message house from `1_input/`
- Calls Claude API to generate user personas
- Saves result to `3_unlabeled/`

#### **Step 3: Evaluate & Label**
```bash
python scripts/evaluate.py
```
- Opens GUI evaluation tool
- Click "Load Unlabeled Files"
- Score each criteria (1-10): Persona Authenticity, Narrative Depth, User Story Clarity, Emotional Resonance, Strategic Alignment
- Select improvement tags if needed
- Click "Save Evaluation"
- Creates labeled training data in `5_labeled_json/`

#### **Step 4: Iterate for Better Results**
- Repeat Steps 2-3 with new message houses
- Each cycle uses previous evaluations as training data
- Output quality improves with more examples

### System Benefits
- **First Use**: Good quality user personas
- **After 5+ Uses**: Great quality with pattern recognition
- **After 10+ Uses**: Expert-level persona insights

### File Flow
```
message_house_agent/3_unlabeled/ → 1_input/ → generate_simple.py → 3_unlabeled/ → evaluate.py → 5_labeled_json/ → Better Next Generation
```

### Troubleshooting
- **API Error**: Check `config.json` has valid Claude API key
- **No Files**: Ensure message house file is in `1_input/` folder
- **Wrong File Used**: Script uses most recent file - remove other files if needed
- **GUI Timeout**: Normal behavior - GUI opens in separate window
- **Encoding Issues**: Save files as UTF-8 encoding

### Quality Targets
- **8.5+ Score**: Excellent, ready for business use
- **7.0-8.4**: Good quality, minor improvements needed
- **Below 7.0**: Needs significant refinement

**The more you use it, the smarter it gets!** 🚀