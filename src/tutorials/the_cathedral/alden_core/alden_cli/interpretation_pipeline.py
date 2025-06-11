"""
Interpretation Pipeline System for the Alden Interpretation Engine
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import json
from datetime import datetime
import numpy as np

from .symbolic_deepening import (
    InterpretationDepth,
    InterpretationVoice,
    SymbolicMetrics,
    AnalyticDeepening,
    SymbolicDeepening,
    PoeticDeepening,
    OracularDeepening,
    MirrorDeepening
)

class InterpretationMode(Enum):
    """Available interpretation modes"""
    ANALYTIC = "analytic"
    SYMBOLIC = "symbolic"
    POETIC = "poetic"
    ORACULAR = "oracular"
    MIRROR = "mirror"

@dataclass
class InterpretationContext:
    """Context for interpretation pipeline"""
    current_state: Dict[str, int]
    previous_state: Dict[str, int]
    symbol_series: List[Dict[str, int]]
    archetype_patterns: Dict[str, List[str]]
    memory_anchors: List[Dict]
    transformation_series: List[Dict]
    symbol_weights: Dict[str, float]
    shadow_contrasts: List[Dict]
    reversal_pairs: Dict[str, str]

@dataclass
class InterpretationResult:
    """Result of interpretation pipeline"""
    mode: InterpretationMode
    depth: InterpretationDepth
    voice: InterpretationVoice
    metrics: SymbolicMetrics
    insights: List[str]
    metaphors: List[str]
    paradoxes: List[str]
    stanzas: List[str]
    reflections: List[str]
    timestamp: str

class InterpretationPipeline:
    """Pipeline for coordinating interpretation methods"""
    
    def __init__(self):
        self.analytic = AnalyticDeepening()
        self.symbolic = SymbolicDeepening()
        self.poetic = PoeticDeepening()
        self.oracular = OracularDeepening()
        self.mirror = MirrorDeepening()
    
    def compute_metrics(self, context: InterpretationContext) -> SymbolicMetrics:
        """Compute symbolic metrics for the current state"""
        # Calculate entropy
        entropy = self.analytic.compute_archetype_entropy_change(
            context.current_state,
            context.previous_state
        )
        
        # Calculate inertia
        inertia_scores = self.analytic.rank_symbolic_inertia(context.symbol_series)
        inertia = np.mean(list(inertia_scores.values())) if inertia_scores else 0
        
        # Calculate volatility
        changes = {
            symbol: context.current_state.get(symbol, 0) - context.previous_state.get(symbol, 0)
            for symbol in set(context.current_state) | set(context.previous_state)
        }
        volatility = np.std(list(changes.values())) if changes else 0
        
        # Calculate tension score
        tensions = self.symbolic.evaluate_mythic_tension_structures(
            context.archetype_patterns,
            context.current_state
        )
        tension_score = np.mean(list(tensions.values())) if tensions else 0
        
        # Calculate resonance depth
        resonance_depth = len([
            anchor for anchor in context.memory_anchors
            if any(s in context.current_state for s in anchor.get("symbols", []))
        ])
        
        return SymbolicMetrics(
            entropy=entropy,
            inertia=inertia,
            volatility=volatility,
            tension_score=tension_score,
            resonance_depth=resonance_depth
        )
    
    def interpret(self,
                 context: InterpretationContext,
                 mode: InterpretationMode,
                 depth: InterpretationDepth = InterpretationDepth.MODERATE,
                 voice: InterpretationVoice = InterpretationVoice.NEUTRAL) -> InterpretationResult:
        """Run interpretation pipeline for given mode and depth"""
        
        # Compute metrics
        metrics = self.compute_metrics(context)
        
        # Initialize result containers
        insights = []
        metaphors = []
        paradoxes = []
        stanzas = []
        reflections = []
        
        # Run mode-specific interpretation
        if mode == InterpretationMode.ANALYTIC:
            # Identify outliers
            outliers = self.analytic.identify_statistical_outliers(context.current_state)
            insights.extend([f"{symbol} shows significant deviation (z={z:.2f})" 
                           for symbol, z in outliers])
            
            # Add inertia insights
            inertia_scores = self.analytic.rank_symbolic_inertia(context.symbol_series)
            stable_symbols = [s for s, score in inertia_scores.items() if score > 0.7]
            if stable_symbols:
                insights.append(f"Stable patterns: {', '.join(stable_symbols)}")
        
        elif mode == InterpretationMode.SYMBOLIC:
            # Map archetypal crossroads
            crossroads = self.symbolic.map_archetypal_crossroads(
                context.archetype_patterns,
                context.current_state
            )
            for cross in crossroads[:3]:  # Top 3 crossroads
                insights.append(
                    f"{cross['archetypes'][0]} meets {cross['archetypes'][1]} "
                    f"at {', '.join(cross['intersection'])}"
                )
            
            # Detect reversals
            reversals = self.symbolic.detect_symbolic_reversal(
                context.symbol_series,
                context.reversal_pairs
            )
            for rev in reversals:
                insights.append(
                    f"Symbolic reversal: {rev['from']} → {rev['to']} "
                    f"(strength: {rev['strength']})"
                )
        
        elif mode == InterpretationMode.POETIC:
            # Get rising and falling symbols
            rising = [s for s, c in context.current_state.items() 
                     if c > context.previous_state.get(s, 0)]
            falling = [s for s, c in context.current_state.items() 
                      if c < context.previous_state.get(s, 0)]
            
            # Weave metaphors
            metaphors.extend(self.poetic.weave_symbolic_metaphors(
                rising,
                falling,
                context.memory_anchors
            ))
            
            # Compose prophecy stanzas
            stanzas.extend(self.poetic.compose_prophecy_stanzas(
                context.shadow_contrasts,
                context.current_state
            ))
            
            # Generate name echoes
            echoes = self.poetic.invoke_name_echo_patterns(
                context.memory_anchors,
                context.current_state
            )
            insights.extend(echoes)
        
        elif mode == InterpretationMode.ORACULAR:
            # Generate glyph triads
            triads = self.oracular.generate_ambiguous_glyph_triads(
                context.symbol_weights
            )
            for triad in triads:
                insights.append(f"Watch for: {' '.join(triad)}")
            
            # Generate paradox pairs
            paradoxes.extend(self.oracular.speak_in_symbolic_paradox_pairs(
                context.current_state,
                context.archetype_patterns
            ))
            
            # Channel glyph stanzas
            stanzas.extend(self.oracular.channel_glyph_stanzas(
                context.symbol_weights,
                context.memory_anchors
            ))
        
        elif mode == InterpretationMode.MIRROR:
            # Reflect transformations
            reflections.extend(self.mirror.reflect_symbolic_transformations(
                context.transformation_series,
                context.current_state
            ))
            
            # Narrate changes
            narrations = self.mirror.narrate_in_symbolic_voice(
                changes,
                context.current_state
            )
            insights.extend(narrations)
            
            # Compare anchors to vectors
            comparisons = self.mirror.compare_anchors_to_vectors(
                context.memory_anchors,
                context.symbol_weights
            )
            reflections.extend(comparisons)
        
        # Apply depth multiplier
        if depth == InterpretationDepth.DEEP:
            # Double the number of insights/metaphors/etc.
            insights = insights * 2
            metaphors = metaphors * 2
            paradoxes = paradoxes * 2
            stanzas = stanzas * 2
            reflections = reflections * 2
        
        # Apply voice transformation
        if voice == InterpretationVoice.INTROSPECTIVE:
            insights = [f"I sense that {insight.lower()}" for insight in insights]
            metaphors = [f"In my depths, {metaphor.lower()}" for metaphor in metaphors]
        elif voice == InterpretationVoice.VISIONARY:
            insights = [f"Behold! {insight}" for insight in insights]
            metaphors = [f"Lo! {metaphor}" for metaphor in metaphors]
        
        return InterpretationResult(
            mode=mode,
            depth=depth,
            voice=voice,
            metrics=metrics,
            insights=insights,
            metaphors=metaphors,
            paradoxes=paradoxes,
            stanzas=stanzas,
            reflections=reflections,
            timestamp=datetime.now().isoformat()
        )
    
    def format_result(self, result: InterpretationResult) -> str:
        """Format interpretation result as a narrative"""
        sections = []
        
        # Add header
        sections.append(f"=== {result.mode.value.upper()} INTERPRETATION ===")
        sections.append(f"Depth: {result.depth.value}")
        sections.append(f"Voice: {result.voice.value}")
        sections.append("")
        
        # Add metrics
        sections.append("--- Metrics ---")
        sections.append(f"Entropy Change: {result.metrics.entropy:.2f}")
        sections.append(f"Field Inertia: {result.metrics.inertia:.2f}")
        sections.append(f"Symbolic Volatility: {result.metrics.volatility:.2f}")
        sections.append(f"Tension Score: {result.metrics.tension_score:.2f}")
        sections.append(f"Resonance Depth: {result.metrics.resonance_depth}")
        sections.append("")
        
        # Add insights
        if result.insights:
            sections.append("--- Insights ---")
            sections.extend(result.insights)
            sections.append("")
        
        # Add metaphors
        if result.metaphors:
            sections.append("--- Metaphors ---")
            sections.extend(result.metaphors)
            sections.append("")
        
        # Add paradoxes
        if result.paradoxes:
            sections.append("--- Paradoxes ---")
            sections.extend(result.paradoxes)
            sections.append("")
        
        # Add stanzas
        if result.stanzas:
            sections.append("--- Stanzas ---")
            sections.extend(result.stanzas)
            sections.append("")
        
        # Add reflections
        if result.reflections:
            sections.append("--- Reflections ---")
            sections.extend(result.reflections)
            sections.append("")
        
        return "\n".join(sections) 