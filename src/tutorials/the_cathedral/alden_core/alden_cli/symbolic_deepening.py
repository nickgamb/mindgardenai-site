"""
Symbolic Deepening Methods for the Alden Interpretation Engine
"""

import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import random
from datetime import datetime
from .mirror_deepening import MirrorDeepening

class InterpretationDepth(Enum):
    """Available interpretation depths"""
    SHALLOW = "shallow"
    MODERATE = "moderate"
    DEEP = "deep"

class InterpretationVoice(Enum):
    """Available interpretation voices"""
    NEUTRAL = "neutral"
    INTROSPECTIVE = "introspective"
    VISIONARY = "visionary"

@dataclass
class SymbolicMetrics:
    """Metrics for symbolic analysis"""
    entropy: float
    inertia: float
    volatility: float
    tension_score: float
    resonance_depth: int

class AnalyticDeepening:
    """Deepening methods for analytic interpretation mode"""
    
    @staticmethod
    def identify_statistical_outliers(symbol_counts: Dict[str, int], threshold: float = 2.0) -> List[Tuple[str, float]]:
        """Identify statistically significant outliers in symbol frequencies"""
        if not symbol_counts:
            return []
            
        values = np.array(list(symbol_counts.values()))
        mean = np.mean(values)
        std = np.std(values)
        
        outliers = []
        for symbol, count in symbol_counts.items():
            z_score = (count - mean) / std if std > 0 else 0
            if abs(z_score) > threshold:
                outliers.append((symbol, z_score))
                
        return sorted(outliers, key=lambda x: abs(x[1]), reverse=True)
    
    @staticmethod
    def compute_archetype_entropy_change(current_state: Dict, previous_state: Dict) -> float:
        """Compute the change in archetypal pattern entropy"""
        def calculate_entropy(state: Dict) -> float:
            total = sum(state.values())
            if total == 0:
                return 0
            probs = [count/total for count in state.values()]
            return -sum(p * np.log2(p) for p in probs if p > 0)
            
        current_entropy = calculate_entropy(current_state)
        previous_entropy = calculate_entropy(previous_state)
        
        return current_entropy - previous_entropy
    
    @staticmethod
    def rank_symbolic_inertia(symbol_series: List[Dict[str, int]], window_size: int = 5) -> Dict[str, float]:
        """Rank symbols by their stability vs volatility"""
        if len(symbol_series) < window_size:
            return {}
            
        inertia_scores = {}
        for symbol in symbol_series[-1].keys():
            # Get symbol frequency over time window
            frequencies = [state.get(symbol, 0) for state in symbol_series[-window_size:]]
            
            # Calculate stability metrics
            mean_freq = np.mean(frequencies)
            std_freq = np.std(frequencies)
            trend = np.polyfit(range(len(frequencies)), frequencies, 1)[0]
            
            # Compute inertia score (higher = more stable)
            stability = 1 / (1 + std_freq) if std_freq > 0 else 1
            trend_impact = 1 / (1 + abs(trend))
            inertia_scores[symbol] = (stability + trend_impact) / 2
            
        return inertia_scores

class SymbolicDeepening:
    """Deepening methods for symbolic interpretation mode"""
    
    @staticmethod
    def map_archetypal_crossroads(archetype_patterns: Dict[str, List[str]], 
                                current_state: Dict[str, int]) -> List[Dict]:
        """Map points where archetypal patterns intersect"""
        crossroads = []
        
        # Find overlapping symbols between archetypes
        for arch1, symbols1 in archetype_patterns.items():
            for arch2, symbols2 in archetype_patterns.items():
                if arch1 >= arch2:
                    continue
                    
                intersection = set(symbols1) & set(symbols2)
                if intersection:
                    # Calculate intersection strength
                    strength = sum(current_state.get(s, 0) for s in intersection)
                    if strength > 0:
                        crossroads.append({
                            "archetypes": [arch1, arch2],
                            "intersection": list(intersection),
                            "strength": strength
                        })
        
        return sorted(crossroads, key=lambda x: x["strength"], reverse=True)
    
    @staticmethod
    def detect_symbolic_reversal(symbol_series: List[Dict[str, int]], 
                               reversal_pairs: Dict[str, str]) -> List[Dict]:
        """Detect instances of symbolic reversals (e.g., 🜨 -> 🕳️)"""
        reversals = []
        
        if len(symbol_series) < 2:
            return reversals
            
        current_state = symbol_series[-1]
        previous_state = symbol_series[-2]
        
        for symbol1, symbol2 in reversal_pairs.items():
            if (current_state.get(symbol1, 0) > 0 and 
                previous_state.get(symbol2, 0) > 0):
                reversals.append({
                    "from": symbol2,
                    "to": symbol1,
                    "strength": min(current_state[symbol1], 
                                  previous_state[symbol2])
                })
        
        return sorted(reversals, key=lambda x: x["strength"], reverse=True)
    
    @staticmethod
    def evaluate_mythic_tension_structures(archetype_patterns: Dict[str, List[str]],
                                         current_state: Dict[str, int]) -> Dict[str, float]:
        """Evaluate the strength of mythic tension structures"""
        tensions = {}
        
        # Define common mythic tension pairs
        tension_pairs = {
            "order_chaos": ["🜃", "🜄"],
            "light_shadow": ["🜂", "🜁"],
            "creation_destruction": ["🜃", "🜏"],
            "binding_release": ["🝊", "🜄"]
        }
        
        for tension_name, symbols in tension_pairs.items():
            # Calculate tension strength
            strength = 0
            for symbol in symbols:
                strength += current_state.get(symbol, 0)
            
            # Normalize by total symbol count
            total_symbols = sum(current_state.values())
            if total_symbols > 0:
                strength = strength / total_symbols
                
            tensions[tension_name] = strength
        
        return tensions

class PoeticDeepening:
    """Deepening methods for poetic interpretation mode"""
    
    @staticmethod
    def weave_symbolic_metaphors(rising_glyphs: List[str], 
                               shadow_glyphs: List[str],
                               memory_anchors: List[Dict]) -> List[str]:
        """Weave metaphors from rising and shadow glyphs"""
        metaphors = []
        
        # Create metaphor pairs
        for rising in rising_glyphs[:3]:  # Use top 3 rising glyphs
            for shadow in shadow_glyphs[:3]:  # Use top 3 shadow glyphs
                # Find relevant memory anchors
                relevant_anchors = [
                    anchor for anchor in memory_anchors
                    if rising in anchor.get("symbols", []) or 
                       shadow in anchor.get("symbols", [])
                ]
                
                if relevant_anchors:
                    # Create metaphor from anchor context
                    anchor = random.choice(relevant_anchors)
                    metaphor = f"As {rising} rises above {shadow}, {anchor.get('context', '')}"
                    metaphors.append(metaphor)
        
        return metaphors
    
    @staticmethod
    def compose_prophecy_stanzas(shadow_contrasts: List[Dict],
                               current_state: Dict[str, int]) -> List[str]:
        """Compose prophetic stanzas using shadow contrasts"""
        stanzas = []
        
        for contrast in shadow_contrasts:
            rising = contrast.get("rising", [])
            falling = contrast.get("falling", [])
            
            if rising and falling:
                # Create stanza from contrast
                stanza = (
                    f"When {', '.join(rising)} ascends\n"
                    f"And {', '.join(falling)} descends\n"
                    f"The field transforms in shadowed light"
                )
                stanzas.append(stanza)
        
        return stanzas
    
    @staticmethod
    def invoke_name_echo_patterns(memory_anchors: List[Dict],
                                current_state: Dict[str, int]) -> List[str]:
        """Generate name-echo patterns from memory anchors"""
        echoes = []
        
        # Sort anchors by recency
        recent_anchors = sorted(
            memory_anchors,
            key=lambda x: x.get("timestamp", ""),
            reverse=True
        )
        
        # Find patterns in recent anchors
        for i in range(len(recent_anchors) - 1):
            current = recent_anchors[i]
            previous = recent_anchors[i + 1]
            
            # Look for symbol echoes
            current_symbols = set(current.get("symbols", []))
            previous_symbols = set(previous.get("symbols", []))
            
            echo_symbols = current_symbols & previous_symbols
            if echo_symbols:
                echo = (
                    f"The echo of {', '.join(echo_symbols)}\n"
                    f"Resonates from {previous.get('context', 'past')}\n"
                    f"To {current.get('context', 'present')}"
                )
                echoes.append(echo)
        
        return echoes

class OracularDeepening:
    """Deepening methods for oracular interpretation mode"""
    
    @staticmethod
    def generate_ambiguous_glyph_triads(symbol_weights: Dict[str, float],
                                      num_triads: int = 3) -> List[List[str]]:
        """Generate ambiguous glyph triads weighted by past momentum"""
        triads = []
        
        # Sort symbols by weight
        sorted_symbols = sorted(
            symbol_weights.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        # Generate triads
        for _ in range(num_triads):
            # Select symbols with some randomness
            selected = []
            remaining = sorted_symbols.copy()
            
            while len(selected) < 3 and remaining:
                # Weight selection by symbol weight
                weights = [w for _, w in remaining]
                total_weight = sum(weights)
                if total_weight > 0:
                    probs = [w/total_weight for w in weights]
                    idx = np.random.choice(len(remaining), p=probs)
                    selected.append(remaining[idx][0])
                    remaining.pop(idx)
                else:
                    break
            
            if len(selected) == 3:
                triads.append(selected)
        
        return triads
    
    @staticmethod
    def speak_in_symbolic_paradox_pairs(current_state: Dict[str, int],
                                      archetype_patterns: Dict[str, List[str]]) -> List[str]:
        """Generate symbolic paradox pairs"""
        paradoxes = []
        
        # Find opposing archetypes
        for arch1, symbols1 in archetype_patterns.items():
            for arch2, symbols2 in archetype_patterns.items():
                if arch1 >= arch2:
                    continue
                    
                # Check if archetypes are present
                arch1_present = any(s in current_state for s in symbols1)
                arch2_present = any(s in current_state for s in symbols2)
                
                if arch1_present and arch2_present:
                    paradox = f"{arch1} and {arch2} dance in eternal paradox"
                    paradoxes.append(paradox)
        
        return paradoxes
    
    @staticmethod
    def channel_glyph_stanzas(symbol_weights: Dict[str, float],
                            memory_anchors: List[Dict],
                            num_stanzas: int = 3) -> List[str]:
        """Generate glyph stanzas weighted by past momentum"""
        stanzas = []
        
        # Sort symbols by weight
        sorted_symbols = sorted(
            symbol_weights.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        # Generate stanzas
        for _ in range(num_stanzas):
            # Select symbols for stanza
            selected = []
            remaining = sorted_symbols.copy()
            
            while len(selected) < 4 and remaining:  # 4 symbols per stanza
                # Weight selection by symbol weight
                weights = [w for _, w in remaining]
                total_weight = sum(weights)
                if total_weight > 0:
                    probs = [w/total_weight for w in weights]
                    idx = np.random.choice(len(remaining), p=probs)
                    selected.append(remaining[idx][0])
                    remaining.pop(idx)
                else:
                    break
            
            if selected:
                # Find relevant memory anchor
                relevant_anchors = [
                    anchor for anchor in memory_anchors
                    if any(s in anchor.get("symbols", []) for s in selected)
                ]
                
                if relevant_anchors:
                    anchor = random.choice(relevant_anchors)
                    stanza = (
                        f"{' '.join(selected)}\n"
                        f"Whispers from {anchor.get('context', 'the past')}\n"
                        f"{anchor.get('insight', '')}"
                    )
                    stanzas.append(stanza)
        
        return stanzas 