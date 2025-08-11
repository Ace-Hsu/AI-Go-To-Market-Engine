# Testimonial Agent - Quick Start Guide

## Prerequisites

1. **Python 3.x** installed
2. **Anthropic API key** configured
3. **Upstream agent outputs** available:
   - `brand_side_persona.md` (from Agent 2)
   - `customer_side_persona.md` (from Agent 3) 
   - `keywords_bank.md` (from Agent 5)

## Setup

### 1. Install Dependencies
```bash
cd testimonial_agent
pip install -r requirements.txt
```

### 2. Configure API
Edit `config.json` with your Anthropic API key:
```json
{
    "api_key": "your-anthropic-api-key-here",
    "model": "claude-3-5-sonnet-20241022"
}
```

### 3. Add Input Files
Place required files in `1_input/`:
- Copy `brand_side_persona.md` from `user_story_agent/3_unlabeled/`
- Copy `customer_side_persona.md` from `user_story_real_reviews_agent/3_unlabeled/`
- Copy `keywords_bank_expansion_[timestamp].md` from `keywords_bank_agent/3_unlabeled/`

## Basic Usage

### Step 1: Generate Testimonials
```bash
python scripts/generate_simple.py
```

**Expected Output:**
- New file in `3_unlabeled/`: `testimonials_[timestamp].md`
- Contains multiple testimonial formats blending strategic messaging with authentic voice

### Step 2: Evaluate Quality
```bash
python scripts/evaluate.py
```

**Evaluation Process:**
1. GUI opens with testimonial content
2. Score 5 criteria (1-10 scale):
   - **Authenticity**: Believable customer voice
   - **Strategic Alignment**: Brand positioning alignment
   - **Emotional Resonance**: Connects with audience
   - **Believability**: Sounds like real experiences
   - **Marketing Effectiveness**: Ready for campaigns
3. Add improvement notes if needed
4. Save evaluation

**Target Score:** 8.5+ for business-ready testimonials

## Expected Results

### Sample Testimonial Blending:
**Strategic Messaging**: "Superior absorption technology"
**Customer Voice**: "Can't believe the difference!"
**Authentic Language**: "chronic knee pain", "10k+ steps daily"

**Generated Result**: 
*"I've had chronic knee pain for years, and after trying this superior absorption technology, I can't believe the difference! I'm back to walking 10k+ steps daily without needing breaks every few minutes."*

## File Workflow

```
Input Files:
├── brand_side_persona.md (Agent 2 output)
├── customer_side_persona.md (Agent 3 output) 
└── keywords_bank.md (Agent 5 output)

Generation:
└── testimonials_[timestamp].md (in 3_unlabeled/)

Evaluation:
└── testimonials_[timestamp]_labeled.json (in 5_labeled_json/)
```

## Quality Improvement

### Learning System
- Each evaluation improves future generations
- High-scoring testimonials become templates
- Low scores identify improvement areas
- System learns authentic voice patterns

### Iteration Process
1. Generate → Evaluate → Learn
2. Repeat cycle for continuous improvement
3. Track scores over time
4. Adjust system prompts based on patterns

## Common Issues

### Low Authenticity Scores
- **Cause**: Too much strategic messaging, not enough customer voice
- **Solution**: Increase customer voice pattern usage

### Poor Strategic Alignment
- **Cause**: Missing brand positioning elements
- **Solution**: Strengthen brand persona integration

### Sounds Like Marketing Copy
- **Cause**: Not enough authentic language patterns
- **Solution**: Enhance Vector G customer voice patterns

## Success Metrics

- **8.5+ Overall Score**: Business-ready testimonials
- **Authentic Voice**: Sounds like real customers
- **Strategic Alignment**: Reflects brand positioning
- **Marketing Ready**: Immediate campaign use

## Next Steps

After generating quality testimonials:
1. Use in marketing campaigns
2. Adapt for different channels
3. Test effectiveness in market
4. Feed results back for improvement

---

*Ready to create authentic, strategically-aligned testimonials!*