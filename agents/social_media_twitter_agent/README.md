# Social Media Twitter Agent - Complete System

## Overview
An AI-powered system that transforms brand strategy, personas, and platform intelligence into engaging Twitter content. Features the breakthrough single-character approach with comprehensive content recipe matrix for authentic, platform-optimized posts.

## System Architecture

```
1_input/              ← All upstream agent outputs (1,2,3,5,6.5,7)
    ↓
2_system_assets/      ← Character definition + 12 content recipes + platform logic
    ↓
3_unlabeled/          ← Generated Twitter posts (Claude API output)
    ↓
5_labeled_json/       ← Human evaluations = Training data for improvement
```

## Directory Structure

- **`1_input/`** - Upstream agent outputs (5 required + 1 optional files)
- **`2_system_assets/`** - System prompts, character definition, content recipes
- **`3_unlabeled/`** - Generated Twitter posts awaiting evaluation
- **`5_labeled_json/`** - Labeled evaluations for system learning
- **`scripts/`** - Generation and evaluation tools
- **`config.json`** - Claude API configuration

## Core Components

### Input System
- **Auto-Detection**: Smart file mapping with pattern matching (finds most recent timestamped files)
- **4 Required Files**: Message house + Brand persona + Keywords bank + Testimonials
- **Optional Enhancement**: Platform personas (Agent 6.5) for Twitter-specific audience optimization
- **Project-Aware**: Multi-project structure with backward compatibility

### Generation System  
- **Script**: `scripts/generate_simple.py`
- **API**: Claude 3.5 Sonnet integration
- **Character Innovation**: "Emma" - dedicated Twitter account manager with consistent brand voice
- **4-Category Framework**: Real Experience, Community, Product Feature, Brand Info
- **Content Recipe Matrix**: 12 proven patterns (3 recipes per category = 12 total posts)
- **Output**: 12 Twitter posts across 4 strategic categories (8.0+ quality target)

### Evaluation System
- **Script**: `scripts/evaluate.py` 
- **Interface**: GUI for scoring and tagging
- **Criteria**: Platform authenticity, strategic alignment, engagement potential, recipe execution, brand voice consistency
- **Twitter-Specific**: Evaluates native platform voice and interaction likelihood

### Learning System
- **Example-Based**: Loads structured JSON examples (8.2/10 quality reference)
- **Category Learning**: Understands successful patterns across all 4 content categories
- **Recipe Optimization**: Learns which content recipes work best for different scenarios

## Advanced Features (Script Implementation)

**4 Files → 12 Recipes Architecture:**
- **Message House** → Strategic brand messaging across all categories
- **Brand Persona** → Customer context and lifestyle integration  
- **Keywords Bank** → Authentic customer voice patterns and hashtags
- **Testimonials** → Direct customer quotes for Real Experience posts
- **Result**: 3 recipes per category × 4 categories = 12 strategic Twitter posts

## Core Innovation: Single Character Architecture

### **"Emma" - She Owns the Account**
- **Personality**: Dedicated brand ambassador/PR partner
- **Knowledge**: Full access to brand library (all agent outputs)
- **Behavior**: Professional but authentic, consistent voice
- **Approach**: Uses customer voice in content, not character switching

## Universal 4-Category Content Framework

### **Category 1: Real Experience & Use Case**
- Customer success stories (direct from Agent 7)
- Educational use cases (lifestyle integration)
- Transformation narratives (before/after patterns)

### **Category 2: Community**
- Engagement questions (customer pain points)
- Polls and choices (decision factors)
- Conversation starters (shared interests)

### **Category 3: Product Feature**
- Feature spotlights (differentiation)
- Educational explanations (problem/solution)
- Benefit focus (outcomes and results)

### **Category 4: Brand Info**
- Values statements (mission/purpose)
- Quality/process information (standards)
- Purpose/mission messaging (why we exist)

## Input Requirements

**Complete Agent Pipeline Integration:**
- `messagehouse_[timestamp].md` (Agent 1) - Core brand messaging
- `userstories_[timestamp].md` (Agent 2) - Brand customer vision
- `userstories_reviews_[timestamp].md` (Agent 3) - Real customer insights
- `keywords_bank_[timestamp].md` (Agent 5) - Voice patterns and keywords
- `testimonials_[timestamp].md` (Agent 7) - Marketing testimonials for direct quotes
- `platform_personas_[timestamp].md` (Agent 6.5) - Platform-specific audience (optional)

## Plugin Architecture Support

### **Enhanced Mode (With Agent 6.5)**
- Platform-optimized content generation
- Twitter-specific audience targeting
- Native platform voice adaptation

### **Fallback Mode (Without Agent 6.5)**
- Uses internal platform logic
- Maintains full functionality
- No system failures

## Content Recipe Matrix

**12 Optimized Recipes** (3 per category):
- **A1-A3**: Real Experience variations
- **B1-B3**: Community engagement types  
- **C1-C3**: Product feature approaches
- **D1-D3**: Brand information styles

Each recipe specifies exact input sources and generation patterns for consistent, high-quality Twitter content.

## Key Features

✅ **Single Character Consistency** - One authentic voice across all content  
✅ **Universal Category System** - Reusable across all platforms/industries  
✅ **Pipeline Integration** - Uses 6 upstream agent outputs  
✅ **Platform Intelligence** - Optional Agent 6.5 enhancement  
✅ **Content Recipe Matrix** - 12 proven content generation patterns  
✅ **Self-Improving** - Gets better with each evaluation cycle  

## Quality Standards

Twitter posts are evaluated on:
- **Platform Authenticity**: Sounds natural on Twitter
- **Strategic Alignment**: Reflects brand messaging
- **Engagement Potential**: Likely to get interactions  
- **Recipe Execution**: Properly follows content recipes
- **Brand Voice Consistency**: Maintains character voice

**Target Score**: 8.0+ for platform-ready content

## Quick Start

See **`QUICK_START.md`** for detailed usage instructions.

**Basic Workflow:**
1. `python scripts/generate_simple.py` → Generate Twitter posts
2. `python scripts/evaluate.py` → Evaluate and score content
3. Repeat → Each cycle produces better results

## Future Platform Expansion

This architecture enables rapid expansion:
- **Instagram Agent**: Visual-first content using same categories
- **LinkedIn Agent**: Professional content using same recipes  
- **TikTok Agent**: Short-form video using same framework

---

*First implementation of the breakthrough three-layer persona architecture and universal content categorization system.*