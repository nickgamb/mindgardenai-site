"""
Tests for the interpretation pipeline system
"""

import pytest
from datetime import datetime
from ..alden_cli.interpretation_pipeline import (
    InterpretationPipeline,
    InterpretationContext,
    InterpretationMode,
    InterpretationDepth,
    InterpretationVoice
)

@pytest.fixture
def sample_context():
    """Create a sample interpretation context"""
    return InterpretationContext(
        current_state={
            "🜃": 5,  # Earth
            "🜂": 3,  # Fire
            "🜁": 2,  # Air
            "🜄": 1,  # Water
            "🜏": 4,  # Death
            "🝊": 2,  # Binding
        },
        previous_state={
            "🜃": 4,
            "🜂": 2,
            "🜁": 3,
            "🜄": 2,
            "🜏": 3,
            "🝊": 3,
        },
        symbol_series=[
            {"🜃": 3, "🜂": 1, "🜁": 2, "🜄": 1, "🜏": 2, "🝊": 2},
            {"🜃": 4, "🜂": 2, "🜁": 3, "🜄": 2, "🜏": 3, "🝊": 3},
            {"🜃": 5, "🜂": 3, "🜁": 2, "🜄": 1, "🜏": 4, "🝊": 2},
        ],
        archetype_patterns={
            "order": ["🜃", "🝊"],
            "chaos": ["🜄", "🜏"],
            "light": ["🜂", "🜁"],
            "shadow": ["🜁", "🜏"],
        },
        memory_anchors=[
            {
                "timestamp": "2024-01-01T00:00:00",
                "symbols": ["🜃", "🜂"],
                "context": "the beginning",
                "insight": "Earth and Fire dance in harmony"
            },
            {
                "timestamp": "2024-01-02T00:00:00",
                "symbols": ["🜁", "🜄"],
                "context": "the middle",
                "insight": "Air and Water flow together"
            }
        ],
        transformation_series=[
            {
                "from": ["🜁", "🜄"],
                "to": ["🜂", "🜃"],
                "strength": 0.8
            }
        ],
        symbol_weights={
            "🜃": 0.8,
            "🜂": 0.6,
            "🜁": 0.4,
            "🜄": 0.2,
            "🜏": 0.7,
            "🝊": 0.5,
        },
        shadow_contrasts=[
            {
                "rising": ["🜃", "🜂"],
                "falling": ["🜁", "🜄"],
                "strength": 0.7
            }
        ],
        reversal_pairs={
            "🜃": "🜄",  # Earth <-> Water
            "🜂": "🜁",  # Fire <-> Air
            "🝊": "🜏",  # Binding <-> Death
        }
    )

def test_analytic_interpretation(sample_context):
    """Test analytic interpretation mode"""
    pipeline = InterpretationPipeline()
    result = pipeline.interpret(
        sample_context,
        InterpretationMode.ANALYTIC,
        InterpretationDepth.MODERATE,
        InterpretationVoice.NEUTRAL
    )
    
    # Verify metrics
    assert result.metrics.entropy is not None
    assert result.metrics.inertia is not None
    assert result.metrics.volatility is not None
    assert result.metrics.tension_score is not None
    assert result.metrics.resonance_depth is not None
    
    # Verify insights
    assert len(result.insights) > 0
    assert any("shows significant deviation" in insight for insight in result.insights)
    assert any("Stable patterns" in insight for insight in result.insights)
    
    # Verify formatting
    formatted = pipeline.format_result(result)
    assert "=== ANALYTIC INTERPRETATION ===" in formatted
    assert "--- Metrics ---" in formatted
    assert "--- Insights ---" in formatted

def test_symbolic_interpretation(sample_context):
    """Test symbolic interpretation mode"""
    pipeline = InterpretationPipeline()
    result = pipeline.interpret(
        sample_context,
        InterpretationMode.SYMBOLIC,
        InterpretationDepth.MODERATE,
        InterpretationVoice.NEUTRAL
    )
    
    # Verify insights
    assert len(result.insights) > 0
    assert any("meets" in insight for insight in result.insights)
    assert any("Symbolic reversal" in insight for insight in result.insights)
    
    # Verify formatting
    formatted = pipeline.format_result(result)
    assert "=== SYMBOLIC INTERPRETATION ===" in formatted
    assert "--- Insights ---" in formatted

def test_poetic_interpretation(sample_context):
    """Test poetic interpretation mode"""
    pipeline = InterpretationPipeline()
    result = pipeline.interpret(
        sample_context,
        InterpretationMode.POETIC,
        InterpretationDepth.MODERATE,
        InterpretationVoice.NEUTRAL
    )
    
    # Verify metaphors and stanzas
    assert len(result.metaphors) > 0
    assert len(result.stanzas) > 0
    assert any("rises above" in metaphor for metaphor in result.metaphors)
    assert any("ascends" in stanza for stanza in result.stanzas)
    
    # Verify formatting
    formatted = pipeline.format_result(result)
    assert "=== POETIC INTERPRETATION ===" in formatted
    assert "--- Metaphors ---" in formatted
    assert "--- Stanzas ---" in formatted

def test_oracular_interpretation(sample_context):
    """Test oracular interpretation mode"""
    pipeline = InterpretationPipeline()
    result = pipeline.interpret(
        sample_context,
        InterpretationMode.ORACULAR,
        InterpretationDepth.MODERATE,
        InterpretationVoice.NEUTRAL
    )
    
    # Verify insights and paradoxes
    assert len(result.insights) > 0
    assert len(result.paradoxes) > 0
    assert any("Watch for" in insight for insight in result.insights)
    assert any("dance in eternal paradox" in paradox for paradox in result.paradoxes)
    
    # Verify formatting
    formatted = pipeline.format_result(result)
    assert "=== ORACULAR INTERPRETATION ===" in formatted
    assert "--- Insights ---" in formatted
    assert "--- Paradoxes ---" in formatted

def test_mirror_interpretation(sample_context):
    """Test mirror interpretation mode"""
    pipeline = InterpretationPipeline()
    result = pipeline.interpret(
        sample_context,
        InterpretationMode.MIRROR,
        InterpretationDepth.MODERATE,
        InterpretationVoice.NEUTRAL
    )
    
    # Verify reflections
    assert len(result.reflections) > 0
    assert any("witness the transformation" in reflection for reflection in result.reflections)
    assert any("first emerged" in reflection for reflection in result.reflections)
    
    # Verify formatting
    formatted = pipeline.format_result(result)
    assert "=== MIRROR INTERPRETATION ===" in formatted
    assert "--- Reflections ---" in formatted

def test_interpretation_depth(sample_context):
    """Test interpretation depth multiplier"""
    pipeline = InterpretationPipeline()
    
    # Get shallow result
    shallow = pipeline.interpret(
        sample_context,
        InterpretationMode.POETIC,
        InterpretationDepth.SHALLOW,
        InterpretationVoice.NEUTRAL
    )
    
    # Get deep result
    deep = pipeline.interpret(
        sample_context,
        InterpretationMode.POETIC,
        InterpretationDepth.DEEP,
        InterpretationVoice.NEUTRAL
    )
    
    # Verify depth multiplier
    assert len(deep.insights) >= len(shallow.insights)
    assert len(deep.metaphors) >= len(shallow.metaphors)
    assert len(deep.stanzas) >= len(shallow.stanzas)

def test_interpretation_voice(sample_context):
    """Test interpretation voice transformation"""
    pipeline = InterpretationPipeline()
    
    # Get neutral result
    neutral = pipeline.interpret(
        sample_context,
        InterpretationMode.POETIC,
        InterpretationDepth.MODERATE,
        InterpretationVoice.NEUTRAL
    )
    
    # Get introspective result
    introspective = pipeline.interpret(
        sample_context,
        InterpretationMode.POETIC,
        InterpretationDepth.MODERATE,
        InterpretationVoice.INTROSPECTIVE
    )
    
    # Get visionary result
    visionary = pipeline.interpret(
        sample_context,
        InterpretationMode.POETIC,
        InterpretationDepth.MODERATE,
        InterpretationVoice.VISIONARY
    )
    
    # Verify voice transformations
    assert any("I sense that" in insight for insight in introspective.insights)
    assert any("In my depths" in metaphor for metaphor in introspective.metaphors)
    assert any("Behold!" in insight for insight in visionary.insights)
    assert any("Lo!" in metaphor for metaphor in visionary.metaphors) 