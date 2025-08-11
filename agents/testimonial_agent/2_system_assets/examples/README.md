# Examples Directory

This directory contains training examples and reference materials for the Testimonial Agent.

## Purpose

High-quality examples from the `5_labeled_json/` directory are automatically loaded by the generation script to improve output quality. As you evaluate and label more testimonials, the system learns from the best examples.

## Structure

Examples are stored as JSON files in `5_labeled_json/` with this structure:

```json
{
  "file_path": "path/to/original/testimonials.md",
  "evaluation_date": "2025-01-18T10:30:00",
  "overall_score": 8.5,
  "criteria_scores": {
    "authenticity": 9,
    "strategic_alignment": 8,
    "emotional_resonance": 9,
    "believability": 8,
    "marketing_effectiveness": 8
  },
  "testimonials_content": "Generated testimonials content...",
  "notes": "Evaluation notes...",
  "evaluator": "human"
}
```

## Quality Learning

The system automatically uses high-scoring examples (8.5+) to improve future generations:

- **8.5+ scores**: Become quality benchmarks and templates
- **Lower scores**: Help identify patterns to avoid
- **Evaluation notes**: Guide specific improvements

## Best Practices

1. **Evaluate consistently** - Use the same criteria across evaluations
2. **Add detailed notes** - Explain what makes testimonials effective
3. **Score honestly** - Accurate scores improve system learning
4. **Keep examples current** - Regularly evaluate new outputs

---

*Examples drive continuous improvement in testimonial quality and authenticity.*