# Quick Start Guide - Keywords Bank Agent

## How to Use This Two-Phase System

### Prerequisites
- Python 3.x installed
- Claude API key configured in `config.json`
- Required input files from upstream agents

### Complete Workflow

#### **Step 1: Prepare Input Files**
Place these files in `1_input/` folder:
- `message_house_[timestamp].md` (from Agent 1)
- `brand_side_persona_[timestamp].md` (from Agent 2)
- `customer_side_persona_[timestamp].md` (from Agent 3)
- `external_keywords.csv` (optional - if you have external keyword data)

#### **Step 2: Generate Phase 1 Vocabulary**
```bash
python scripts/generate_phase1.py
```
- Reads input files from `1_input/`
- Calls Claude API to generate keyword bank vocabulary
- Saves result to `3_unlabeled/keywords_bank_vocabulary_[timestamp].md`

#### **Step 3: Evaluate Phase 1 (Human Quality Control)**
```bash
python scripts/evaluate_phase1.py
```
- Opens GUI evaluation tool
- Click "Refresh" then "Load File"
- Score each of 5 criteria (1-10 scale):
  - Strategic Alignment (25%)
  - Completeness (20%)
  - Creative Expansion (20%)
  - Insightfulness (20%)
  - Actionability (15%)
- Click "Update Score" to see overall score
- **If score ≥ 7.0**: Click "Approve & Continue to Phase 2"
- **If score < 7.0**: Click "Reject & Regenerate"

#### **Step 4: Generate Phase 2 Expansion (If Approved)**
```bash
python scripts/generate_phase2.py
```
- Automatically finds approved Phase 1 vocabulary
- Generates 150+ keywords across 6 strategic vectors
- Saves result to `3_unlabeled/keywords_bank_expansion_[timestamp].md`
- **No evaluation needed** - feeds directly to downstream agents

### Two-Phase Quality Philosophy

**Phase 1**: High-quality foundation with human evaluation
- Focus on strategic alignment and completeness
- Human judgment ensures quality foundation
- Approval threshold: 7.0+ required

**Phase 2**: Massive expansion with no evaluation
- Generates 150+ keywords across 6 vectors
- Trust Phase 1 quality for volume generation
- Quality control happens at downstream agents

### Output Structure

**Phase 1 Output** (`keywords_bank_vocabulary_[timestamp].md`):
- Externally Validated Keywords (if CSV provided)
- Core Brand Vocabulary & Creative Variations
- Foundational Language (from personas)
- Thematic Clusters & Core Pains

**Phase 2 Output** (`keywords_bank_expansion_[timestamp].md`):
- **SEO Vectors**: Question-based, Modifier-based, Intent-based
- **Creative Vectors**: Quote starters, Social hooks, Benefit angles

### Integration with Agent Pipeline

**Feeds Into:**
- Agent 7 (Testimonial): Uses Creative Vectors D, E, F
- Agent 8 (Social Media): Uses Vectors E, F, A
- Agent 9 (Website Copy): Uses SEO Vectors A, B, C

### File Flow
```
1_input/ → generate_phase1.py → 3_unlabeled/ → evaluate_phase1.py → 5_labeled_json/
                                                      ↓ (if approved)
                                               generate_phase2.py → 3_unlabeled/ → Agents 7,8,9
```

### Troubleshooting

**API Error**: Check `config.json` has valid Claude API key
**No Input Files**: Ensure message house & personas are in `1_input/`
**Phase 2 Won't Run**: Must have approved Phase 1 file (score ≥7.0)
**GUI Issues**: Ensure tkinter is available (comes with Python)

### Quality Targets

**Phase 1 Scores:**
- **8.5+ Score**: Excellent foundation, proceed with confidence
- **7.0-8.4**: Good quality, approved for Phase 2
- **Below 7.0**: Needs regeneration with input improvements

**Phase 2 Output:**
- **Target**: 150+ keywords across 6 vectors
- **Quality**: Strategic consistency with approved foundation
- **Purpose**: Immediate use by downstream content agents

### Success Metrics

**Phase 1 Success**: Human evaluator approves vocabulary foundation
**Phase 2 Success**: Massive, structured keyword output ready for content agents
**System Success**: Downstream agents (7,8,9) produce high-quality content

**The foundation quality determines everything else!** 🎯