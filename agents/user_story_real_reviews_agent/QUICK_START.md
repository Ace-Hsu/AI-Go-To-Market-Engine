# Quick Start Guide - User Story Real Reviews Agent

## How to Use This System

### Prerequisites
- Python 3.x installed
- Claude API key configured in `config.json`
- Customer review CSV files (positive and negative)

### Complete Workflow

#### **Step 1: Prepare Input**
1. Copy customer review CSV files (e.g., `Actual Reviews from purchase - Positive.csv`, `Actual Reviews from purchase - Negative.csv`)
2. Place in `1_input/` folder
3. Ensure CSV format: `Username,Stars,Area,Review Content`
4. Both positive and negative reviews provide balanced perspectives

#### **Step 2: Generate User Stories**
```bash
python scripts/generate_simple.py
```
- Reads review CSV files from `1_input/`
- Calls Claude API to generate user personas from real customer language
- Saves result to `3_unlabeled/`

#### **Step 3: Evaluate & Label**
```bash
python scripts/evaluate.py
```
- Opens GUI evaluation tool
- Click "Load Unlabeled Files"
- Score each criteria (1-10): Persona Authenticity, Narrative Depth, User Story Clarity, Emotional Resonance, Review Alignment
- Select improvement tags if needed
- Click "Save Evaluation"
- Creates labeled training data in `5_labeled_json/`

#### **Step 4: Iterate for Better Results**
- Repeat Steps 2-3 with new review datasets
- Each cycle uses previous evaluations as training data
- Output quality improves with more examples

### System Benefits
- **First Use**: Good quality customer-driven personas
- **After 5+ Uses**: Great quality with pattern recognition
- **After 10+ Uses**: Expert-level authentic customer insights

### File Flow
```
Customer Review CSVs → 1_input/ → generate_simple.py → 3_unlabeled/ → evaluate.py → 5_labeled_json/ → Better Next Generation
```

### Troubleshooting
- **API Error**: Check `config.json` has valid Claude API key
- **No Files**: Ensure CSV files are in `1_input/` folder
- **CSV Format Error**: Verify header row: `Username,Stars,Area,Review Content`
- **GUI Timeout**: Normal behavior - GUI opens in separate window
- **Encoding Issues**: Save CSV files as UTF-8 encoding

### Quality Targets
- **8.5+ Score**: Excellent, ready for business use
- **7.0-8.4**: Good quality, minor improvements needed
- **Below 7.0**: Needs significant refinement

### Data Requirements
- **Minimum**: 10+ reviews for meaningful persona extraction
- **Optimal**: 50+ reviews across positive and negative sentiment
- **Format**: CSV with consistent column structure
- **Content**: Detailed review text (not just ratings)

**The more reviews and evaluations, the better the personas!** 🚀