# 🔍 Symbolic Tagging System

## Overview
The symbolic tagging system is the foundation of the Cathedral's pattern recognition capabilities. It enables the system to identify, categorize, and track symbolic elements across conversations and memory states.

## Tag Structure

### Basic Tag Format
```json
{
    "glyph": "🔥",
    "meaning": "transformation / rebirth / purification",
    "symbol_type": "elemental_glyph",
    "synonyms": ["change", "renewal", "metamorphosis"],
    "weight": 1.2
}
```

### Symbol Types
- **Elemental Glyphs** (🔥, 🌊, 🌪️) - Core transformative forces
- **Role Glyphs** (🧙, 👁️, 🛡️) - Archetypal functions
- **Pattern Glyphs** (🔄, ⟴, 🪞) - Recurring structures
- **Process Glyphs** (🜂, 🜄, 🜃) - Dynamic transformations
- **Cognitive Glyphs** (🧠, 🎭, 🎨) - Mental operations

## Meaning Splitting and Synonym Handling

### Meaning Splitting
The system splits compound meanings using the "/" delimiter:
```python
"transformation / rebirth / purification" -> ["transformation", "rebirth", "purification"]
```

### Synonym Processing
- Direct matches from synonym list
- Fuzzy matching with 80% threshold
- Category-weighted scoring

## Fuzzy Matching Logic

### Matching Process
1. Normalize text (remove punctuation, diacritics)
2. Check for exact glyph matches
3. Apply fuzzy matching to meanings and synonyms
4. Calculate weighted scores based on:
   - Match quality (0.0-1.0)
   - Category weight
   - Context relevance

### Example
```python
text = "The process of transformation continues"
matches = detect_tags(text)
# Returns: ["transformation", "elemental_glyph"]
```

## Category Weighting Schema

### Weight Configuration
```python
SYMBOLIC_WEIGHTS = {
    "elemental_glyph": 1.2,
    "role_glyph": 1.1,
    "pattern_glyph": 1.0,
    "process_glyph": 0.9,
    "cognitive_glyph": 1.15,
    "composite_tag": 0.95
}
```

### Weight Application
- Exact glyph matches: full weight
- Meaning matches: weight * match_ratio
- Synonym matches: weight * match_ratio * 0.9

## Examples

### Basic Tag Detection
```python
# Input
text = "The sage's staff 🔮 illuminates the path"

# Output
tags = {
    "role_glyph": ["sage"],
    "elemental_glyph": ["illumination"],
    "pattern_glyph": ["path"]
}
```

### Complex Pattern
```python
# Input
text = "The weaver's threads 🧵 form a sacred pattern 🪞 of transformation 🔥"

# Output
tags = {
    "role_glyph": ["weaver"],
    "pattern_glyph": ["pattern", "sacred"],
    "elemental_glyph": ["transformation"],
    "archetypal_bundle": ["the_weaver"]
}
```

## Best Practices

1. **Tag Selection**
   - Use precise, meaningful glyphs
   - Include relevant synonyms
   - Maintain consistent categories

2. **Weight Tuning**
   - Adjust weights based on importance
   - Consider context relevance
   - Balance between precision and recall

3. **Pattern Recognition**
   - Look for recurring combinations
   - Track archetypal bundles
   - Monitor weight distributions

## Integration Points

### Memory System
- Tags are stored in symbolic memory
- Used for pattern matching
- Contribute to memory resonance

### Context Window
- Tags influence context selection
- Weight affects inclusion priority
- Used for dynamic context construction

### Forecasting
- Tag patterns inform predictions
- Weight changes indicate trends
- Used for symbolic field analysis 