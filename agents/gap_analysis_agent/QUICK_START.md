# Quick Start Guide - Gap Analysis Agent

## How to Use This System

### Prerequisites
- Python 3.x installed
- Claude API key configured in `config.json`
- Two persona files (brand-side and customer-side)

### Complete Workflow

#### **Step 1: Prepare Input**
1. Copy your brand persona file (e.g., from `user_story_agent/3_unlabeled/`)
2. Copy your customer persona file (e.g., from `user_story_real_reviews_agent/3_unlabeled/`)
3. Place both files in `1_input/` folder
4. Ensure you have exactly 2 .md files
5. Files should be named to indicate source (brand/customer/review) for auto-identification

#### **Step 2: Generate Gap Analysis**
```bash
python scripts/generate_simple.py
```
- Automatically identifies brand vs customer files
- Applies Strategic Gap Analysis Framework
- Calls Claude API to generate comprehensive analysis
- Saves result to `3_unlabeled/`

#### **Step 3: Evaluate & Label**
```bash
python scripts/evaluate.py
```
- Opens GUI evaluation tool
- Click "Load Unlabeled Files"
- Score each criteria (1-10): Framework Adherence, Quantitative Evidence, Business Relevance, Gap Clarity, Strategic Prioritization
- Select improvement tags if needed
- Click "Save Evaluation"
- Creates labeled training data in `5_labeled_json/`

#### **Step 4: Iterate for Better Results**
- Repeat Steps 2-3 with different persona pairs
- Each cycle uses previous evaluations as training data
- Output quality improves with more examples

### System Benefits
- **First Use**: Good structured analysis using proven framework
- **After 5+ Uses**: Great quality with pattern recognition
- **After 10+ Uses**: Expert-level strategic insights

### File Flow
```
Brand Personas + Customer Personas → 1_input/ → generate_simple.py → 3_unlabeled/ → evaluate.py → 5_labeled_json/ → Better Next Generation
```

### Strategic Gap Analysis Framework

The system follows a proven 4-step methodology:

**Step 1**: Extract data into 5-feature comparison table
- Income & Price
- Primary Motivation  
- Lifestyle
- Product Experience
- Key Pain Points

**Step 2**: Identify thematic patterns (brand vs customer)

**Step 3**: Quantify differences with percentages

**Step 4**: Generate prioritized gap statements using template

### Troubleshooting
- **API Error**: Check `config.json` has valid Claude API key
- **Wrong File Count**: Ensure exactly 2 .md files in `1_input/`
- **File Identification**: Name files with "brand"/"customer"/"review" keywords
- **GUI Timeout**: Normal behavior - GUI opens in separate window
- **Encoding Issues**: Save files as UTF-8 encoding

### Quality Targets
- **8.5+ Score**: Excellent, ready for strategic decisions
- **7.0-8.4**: Good quality, minor methodology improvements needed
- **Below 7.0**: Needs significant framework adherence work

### Expected Output Format

Gap analysis reports include:
- **Executive Summary**: Key strategic gaps overview
- **Prioritized Gap Analysis**: Ranked by business impact
- **Gap Statements**: "Brand believes X, but customers actually Y. We know this because Z."
- **Quantitative Evidence**: Actual percentages from persona data
- **Strategic Implications**: Business-focused recommendations

### Data Requirements
- **Minimum**: 2 persona files with 3+ personas each
- **Optimal**: 5+ personas per file for statistical significance
- **Format**: Structured persona data with demographics, motivations, pain points
- **Content**: Detailed persona profiles with quotes and specifics

**The more personas and evaluations, the better the strategic insights!** 🚀