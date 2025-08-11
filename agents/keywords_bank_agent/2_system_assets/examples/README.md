# Examples Directory

This directory points to examples stored in `5_labeled_json/` for system learning and quality benchmarking.

## Two-Phase Example System

### Phase 1 Examples (Vocabulary Foundation)
Examples stored in `5_labeled_json/` for human-evaluated vocabulary foundations:

- **High-Quality Examples (8.5+ Score)**
  - Demonstrates strategic alignment with message house
  - Complete persona language extraction
  - Creative semantic variations beyond synonyms
  - Insightful thematic cluster analysis
  - Clear structure for expansion engine usage

- **Learning Examples (7.0-8.4 Score)**
  - Approved foundations with improvement areas
  - Good strategic extraction with minor gaps
  - Adequate creative expansion
  - Solid foundation for Phase 2 expansion

### Phase 2 Examples (Expansion Engine)
**No evaluation examples needed** - Phase 2 outputs feed directly to downstream agents:

- Agent 7 (Testimonial): Uses Creative Vectors D, E, F
- Agent 8 (Social Media): Uses Vectors E, F, A  
- Agent 9 (Website Copy): Uses SEO Vectors A, B, C

## Usage in System Learning

### Phase 1 Learning
The system pulls examples from `5_labeled_json/` to show the LLM:
- Success patterns from high-scoring vocabulary foundations
- Strategic extraction quality standards
- Creative expansion depth requirements
- Structural consistency for expansion engine usage

### Phase 2 Pattern Recognition
Phase 2 generation improves based on:
- Approved Phase 1 vocabulary quality
- Vector-specific optimization patterns
- Agent-specific content requirements
- Strategic consistency maintenance

## Example Format

All Phase 1 examples in `5_labeled_json/` include:
- **Evaluation Metadata**: 5-criteria scores and overall rating
- **Approval Status**: Pass/fail for Phase 2 progression
- **Complete Vocabulary**: Full keyword bank foundation
- **Strategic Traceability**: Connection to input assets
- **Learning Patterns**: What made it succeed/fail

## Quality Benchmarks

### Phase 1 Foundation Standards
- **Strategic Alignment**: Clear message house extraction
- **Completeness**: All persona themes captured
- **Creative Depth**: Semantic variations beyond synonyms  
- **Insightfulness**: Thematic synthesis quality
- **Actionability**: Clear expansion engine readiness

### Phase 2 Output Standards
- **Volume**: 150+ keywords across 6 vectors
- **Diversity**: Agent-specific optimization
- **Consistency**: Strategic alignment with approved foundation
- **Actionability**: Immediate content generation readiness

## Learning Trajectory

**Uses 1-5**: Basic vocabulary generation with human guidance
**Uses 5-10**: Pattern recognition emerges for strategic extraction
**Uses 10+**: Expert-level keyword banking with minimal human correction

The more Phase 1 evaluations accumulated, the better the vocabulary foundation quality becomes.