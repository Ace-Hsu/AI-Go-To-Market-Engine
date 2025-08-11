# Quick Start Guide - Message House Agent

## How to Use This System

### Prerequisites
- Python 3.x installed
- Claude API key configured in `config.json`

### Complete Workflow

#### **Step 1: Prepare Input**
1. Answer the 12 strategic questions for your business
2. Save as a `.md` file in `1_input/` folder
3. Use `12_questions_template.md` as your guide

#### **Step 2: Generate Message House**
```bash
python scripts/generate_simple.py
```
- Reads your Q&A from `1_input/`
- Calls Claude API to generate message house
- Saves result to `3_unlabeled/`

#### **Step 3: Evaluate & Label**
```bash
python scripts/evaluate.py
```
- Opens GUI evaluation tool
- Click "Load Unlabeled Files"
- Score each criteria (1-10)
- Select improvement tags
- Click "Save Evaluation"
- Creates labeled training data in `5_labeled_json/`

#### **Step 4: Iterate for Better Results**
- Repeat Steps 2-3 with new businesses
- Each cycle uses previous evaluations as training data
- Output quality improves with more examples

### System Benefits
- **First Use**: Good quality message houses
- **After 5+ Uses**: Great quality with pattern recognition
- **After 10+ Uses**: Expert-level strategic insights

### File Flow
```
1_input/ → generate_simple.py → 3_unlabeled/ → evaluate.py → 5_labeled_json/ → Better Next Generation
```

### Troubleshooting
- **API Error**: Check `config.json` has valid Claude API key
- **No Files**: Ensure Q&A file is in `1_input/` folder
- **Encoding Issues**: Save files as UTF-8 encoding

### Quality Targets
- **8.5+ Score**: Excellent, ready for business use
- **7.0-8.4**: Good quality, minor improvements needed
- **Below 7.0**: Needs significant refinement

**The more you use it, the smarter it gets!** 🚀