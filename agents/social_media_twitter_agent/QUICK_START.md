# Quick Start Guide - Twitter Agent

## Prerequisites
- Python 3.x installed
- Anthropic API key configured in `config.json`
- Required input files from upstream agents

## Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Verify API Configuration**
   - Check that `config.json` contains your valid Anthropic API key
   - Model should be set to `claude-3-5-sonnet-20241022`

## Input Files Required

Place these files in the `1_input/` directory:

### **Required Files:**
- `messagehouse_[timestamp].md` (from Agent 1)
- `userstories_[timestamp].md` (from Agent 2) 
- `userstories_reviews_[timestamp].md` (from Agent 3)
- `keywords_bank_[timestamp].md` (from Agent 5)
- `testimonials_[timestamp].md` (from Agent 7)

### **Optional Files:**
- `platform_personas_[timestamp].md` (from Agent 6.5)

**Note:** The script auto-detects these timestamped files, so exact filenames will vary.

## Usage

### **Step 1: Generate Twitter Content**
```bash
python scripts/generate_simple.py
```

**What this does:**
- Auto-detects input files in `1_input/`
- Maps them to the content recipe system
- Generates 12 Twitter posts using Emma's character
- Saves output to `3_unlabeled/twitter_posts_[timestamp].md`

### **Step 2: Evaluate Content Quality**
```bash
python scripts/evaluate.py
```

**What this does:**
- Opens GUI evaluation tool
- Loads generated Twitter content
- Provides scoring interface (5 criteria)
- Saves evaluations to `5_labeled_json/`

## Content Framework

The agent generates content using the **Universal 4-Category System**:

1. **Real Experience & Use Case** (25%)
   - Customer success stories
   - Educational use cases  
   - Transformation narratives

2. **Community** (25%)
   - Engagement questions
   - Polls and choices
   - Conversation starters

3. **Product Feature** (25%)  
   - Feature spotlights
   - Educational explanations
   - Benefit focus

4. **Brand Info** (25%)
   - Values statements
   - Quality/process info
   - Purpose/mission content

## Character Approach

**Emma** - Your dedicated Twitter brand ambassador:
- Owns the account completely
- Has access to full brand library
- Maintains consistent authentic voice
- Builds community relationships

## Quality Standards

Target scores for platform-ready content:
- **Overall Score**: 8.0+ out of 10
- **Platform Authenticity**: Sounds natural on Twitter
- **Strategic Alignment**: Reflects brand messaging
- **Engagement Potential**: Drives interactions
- **Recipe Execution**: Follows content frameworks
- **Voice Consistency**: Maintains Emma's character

## Troubleshooting

### **Common Issues:**

**Missing Input Files**
- Ensure all required files are in `1_input/`
- Check file naming patterns match expected formats

**API Errors**
- Verify API key in `config.json`
- Check internet connection
- Ensure sufficient API credits

**Empty Output**
- Check that input files contain content
- Verify system prompt loads correctly

### **File Structure Check:**
```
social_media_twitter_agent/
├── 1_input/               # Input files from upstream agents
├── 2_system_assets/       # System prompt and templates  
├── 3_unlabeled/          # Generated content
├── 5_labeled_json/       # Evaluations
├── scripts/              # Generation and evaluation tools
├── config.json           # API configuration
└── requirements.txt      # Dependencies
```

## Best Practices

1. **Always evaluate content** before using
2. **Aim for 8.0+ scores** for platform posting
3. **Mix content categories** for balanced feed
4. **Maintain Emma's voice** across all posts
5. **Use evaluations** to improve future generations

## Next Steps

After generating and evaluating content:
1. Select highest-scoring posts (8.0+)
2. Schedule for Twitter posting
3. Monitor engagement and results
4. Use feedback to improve future generations

---

For detailed system documentation, see `README.md`