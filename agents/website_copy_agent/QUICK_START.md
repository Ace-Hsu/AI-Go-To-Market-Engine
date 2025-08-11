# Website Copy Agent - Quick Start Guide

## Prerequisites

1. **Python 3.x** installed
2. **Anthropic API key** set as environment variable
3. **Required input files** from upstream agents

## Setup

### 1. Install Dependencies
```bash
cd website_copy_agent
pip install -r requirements.txt
```

### 2. Set API Key
```bash
# Windows
set ANTHROPIC_API_KEY=your_api_key_here

# Mac/Linux
export ANTHROPIC_API_KEY=your_api_key_here
```

### 3. Prepare Input Files
Place **any 3 .md files** in `1_input/` directory with these content types:
- **Message house/brand strategy** file (any filename containing "message house", "brand strategy", or "positioning")
- **Keywords/vocabulary** file (any filename containing "keywords", "vocabulary", or "seo")
- **Testimonials/reviews** file (any filename containing "testimonial", "review", or "social proof")

**Examples of valid filenames:**
- `messagehouse_20250719_143022.md`
- `keywords_bank_expansion_20250718_101936.md` 
- `marketing_testimonials_final_v03.md`

## Basic Workflow

### Step 1: Generate Website Copy
```bash
python scripts/generate_simple.py
```

**What happens:**
- Analyzes your brand strategy assets
- Creates strategic homepage logic explanation
- Generates 7 content modules in priority order
- Saves output to `3_unlabeled/website_copy_TIMESTAMP.md`

**Expected output:** Strategic website copy with compelling logic explanation

### Step 2: Validate Quality
```bash
python scripts/evaluate.py
```

**What happens:**
- Opens GUI evaluation interface
- Load generated website copy
- Score on 5 criteria (1-10 scale)
- Add validation tags and comments
- Save validation to `5_labeled_json/`

**Target score:** 8.5+ for business-ready website copy

### Step 3: Regenerate (If Needed)
- Review validation feedback
- Adjust input files if needed
- Re-generate with improved strategy
- Each generation creates fresh strategic insights

## Understanding the Output

### Strategic Logic Explanation (Most Important)
This section explains WHY the content should be ordered in a specific way:
- Customer psychology analysis
- Emotional journey reasoning
- Trust-building sequence
- Conversion optimization logic

### Content Modules (7 Strategic Sections)
- **Module A:** Core Emotional Promise (Hero/Tagline)
- **Module B:** Customer Pain Point Narrative 
- **Module C:** Authentic Community Voice (Testimonials)
- **Module D:** Scientific Breakthrough (How it works)
- **Module E:** Quantifiable Proof (Data/Results)
- **Module F:** Aspirational Vision (Lifestyle goals)
- **Module G:** Brand's Deeper Purpose (Mission/Values)

## Quality Scoring Criteria

### Strategic Logic Quality (30%)
- Does the psychology analysis convince you?
- Is the narrative flow reasoning compelling?
- Would you implement this logic?

### Customer Psychology Accuracy (25%)
- Deep understanding of target audience
- Specific insights from input assets
- Realistic customer behavior patterns

### Content Module Effectiveness (20%)
- Quality and relevance of 7 modules
- Authentic customer language
- Strategic alignment with logic

### Narrative Flow (15%)
- Logical progression from empathy to conversion
- Smooth emotional journey
- Clear trust-building sequence

### Business Impact (10%)
- Conversion optimization focus
- Revenue-driven recommendations
- Practical implementation value

## Troubleshooting

### Common Issues

**"Missing required files" or "Could not auto-detect file types"**
- Ensure 3 .md files are in `1_input/` directory
- Check filenames or content contain keywords like "message house", "keywords", "testimonials"
- Rename files if needed to include identifying keywords

**"API key not found"**
- Set ANTHROPIC_API_KEY environment variable
- Restart terminal after setting variable

**"Low quality output"**
- Check input file quality and completeness
- Ensure message house has clear strategy
- Verify testimonials are authentic and detailed

### Getting Better Results

**High-Quality Inputs:**
- Complete message house with clear positioning
- Rich keywords bank with customer language
- Authentic testimonials with emotional stories

**Validation Feedback:**
- Be specific in comments
- Use validation tags consistently
- Score honestly to assess output quality

**Regeneration:**
- Review low-scoring outputs
- Identify areas for input improvement
- Refine input strategy for better results

## File Structure Reference

```
website_copy_agent/
├── 1_input/                    # Input files (3 required)
├── 2_system_assets/           # System prompts and examples
├── 3_unlabeled/              # Generated website copy
├── 5_labeled_json/           # Evaluation data
├── scripts/
│   ├── generate_simple.py    # Generation script
│   └── evaluate.py          # Evaluation GUI
├── config.json              # API configuration
├── requirements.txt         # Dependencies
└── README.md               # Complete documentation
```

## Next Steps

1. **Generate your first website copy** with existing inputs
2. **Validate and score** the output quality
3. **Review the strategic logic** - does it convince you?
4. **Regenerate with refined inputs** if needed
5. **Focus on strategic logic quality** - that's where the real value lies

Each generation creates fresh psychology insights based purely on your brand assets. The strategic logic explanation is the core differentiator.

## Integration with Pipeline

**Upstream Dependencies:**
- Agent 1: message_house.md
- Agent 5: keywords_bank.md  
- Agent 7: marketing_testimonials.md

**Downstream Usage:**
- Website implementation
- Landing page optimization
- Content management systems
- A/B testing frameworks

---

*Start with one generation cycle to understand the output format, then focus on the strategic logic quality - that's where the breakthrough value lies.*