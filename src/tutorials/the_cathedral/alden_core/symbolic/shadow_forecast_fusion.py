"""
Shadow Forecast Fusion - Symbolic Pattern Analysis

Analyzes and fuses symbolic patterns to forecast potential shadow
manifestations and their impacts on the system.
"""

from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass
from pathlib import Path
import json
from datetime import datetime
import numpy as np
from collections import defaultdict
import networkx as nx

@dataclass
class ShadowPattern:
    """Represents a detected shadow pattern"""
    pattern_id: str
    symbols: List[str]
    frequency: float
    confidence: float
    impact_score: float
    context: Dict[str, Any]
    metadata: Dict[str, Any]

@dataclass
class Forecast:
    """Represents a shadow forecast"""
    forecast_id: str
    patterns: List[ShadowPattern]
    probability: float
    impact_level: str  # 'low', 'medium', 'high', 'critical'
    timeframe: str  # 'immediate', 'short_term', 'long_term'
    mitigation_suggestions: List[str]
    metadata: Dict[str, Any]

class ShadowForecastFusion:
    """Analyzes and fuses symbolic patterns to forecast shadows"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.patterns: List[ShadowPattern] = []
        self.forecasts: List[Forecast] = []
        self.pattern_graph = nx.Graph()
        
    def add_pattern(self,
                   symbols: List[str],
                   frequency: float,
                   confidence: float,
                   impact_score: float,
                   context: Dict[str, Any],
                   metadata: Optional[Dict[str, Any]] = None) -> str:
        """Add a new shadow pattern"""
        pattern_id = f"pattern_{len(self.patterns)}"
        
        pattern = ShadowPattern(
            pattern_id=pattern_id,
            symbols=symbols,
            frequency=frequency,
            confidence=confidence,
            impact_score=impact_score,
            context=context,
            metadata=metadata or {}
        )
        
        self.patterns.append(pattern)
        
        # Add to pattern graph
        self.pattern_graph.add_node(pattern_id)
        for symbol in symbols:
            if symbol not in self.pattern_graph:
                self.pattern_graph.add_node(symbol)
            self.pattern_graph.add_edge(pattern_id, symbol)
            
        return pattern_id
        
    def analyze_patterns(self) -> List[Tuple[str, float]]:
        """Analyze patterns for correlations and clusters"""
        # Calculate pattern similarity matrix
        n = len(self.patterns)
        similarity = np.zeros((n, n))
        
        for i in range(n):
            for j in range(i + 1, n):
                p1, p2 = self.patterns[i], self.patterns[j]
                
                # Symbol overlap
                symbol_overlap = len(set(p1.symbols) & set(p2.symbols))
                max_symbols = max(len(p1.symbols), len(p2.symbols))
                symbol_similarity = symbol_overlap / max_symbols if max_symbols > 0 else 0
                
                # Context similarity
                context_keys = set(p1.context.keys()) & set(p2.context.keys())
                context_similarity = 0
                if context_keys:
                    context_similarity = sum(
                        1 for k in context_keys
                        if p1.context[k] == p2.context[k]
                    ) / len(context_keys)
                    
                # Combined similarity
                similarity[i, j] = similarity[j, i] = (
                    0.6 * symbol_similarity + 0.4 * context_similarity
                )
                
        # Find clusters
        clusters = []
        visited = set()
        
        for i in range(n):
            if i in visited:
                continue
                
            cluster = [i]
            visited.add(i)
            
            for j in range(n):
                if j not in visited and similarity[i, j] > 0.7:  # High similarity threshold
                    cluster.append(j)
                    visited.add(j)
                    
            if len(cluster) > 1:  # Only keep significant clusters
                clusters.append(cluster)
                
        # Calculate cluster scores
        cluster_scores = []
        for cluster in clusters:
            # Average pattern metrics
            avg_frequency = np.mean([self.patterns[i].frequency for i in cluster])
            avg_confidence = np.mean([self.patterns[i].confidence for i in cluster])
            avg_impact = np.mean([self.patterns[i].impact_score for i in cluster])
            
            # Cluster size factor
            size_factor = min(len(cluster) / 5, 1.0)  # Cap at 5 patterns
            
            # Combined score
            score = (0.4 * avg_frequency + 0.3 * avg_confidence + 0.3 * avg_impact) * (1 + 0.2 * size_factor)
            
            cluster_scores.append((cluster, score))
            
        return cluster_scores
        
    def generate_forecast(self,
                         patterns: List[ShadowPattern],
                         probability: float,
                         impact_level: str,
                         timeframe: str,
                         mitigation_suggestions: List[str],
                         metadata: Optional[Dict[str, Any]] = None) -> str:
        """Generate a new shadow forecast"""
        forecast_id = f"forecast_{len(self.forecasts)}"
        
        forecast = Forecast(
            forecast_id=forecast_id,
            patterns=patterns,
            probability=probability,
            impact_level=impact_level,
            timeframe=timeframe,
            mitigation_suggestions=mitigation_suggestions,
            metadata=metadata or {}
        )
        
        self.forecasts.append(forecast)
        return forecast_id
        
    def analyze_and_forecast(self) -> List[Forecast]:
        """Analyze patterns and generate forecasts"""
        # Clear existing forecasts
        self.forecasts = []
        
        # Analyze patterns
        cluster_scores = self.analyze_patterns()
        
        # Generate forecasts for each cluster
        for cluster, score in cluster_scores:
            patterns = [self.patterns[i] for i in cluster]
            
            # Determine impact level
            avg_impact = np.mean([p.impact_score for p in patterns])
            if avg_impact > 0.8:
                impact_level = 'critical'
            elif avg_impact > 0.6:
                impact_level = 'high'
            elif avg_impact > 0.4:
                impact_level = 'medium'
            else:
                impact_level = 'low'
                
            # Determine timeframe
            if score > 0.8:
                timeframe = 'immediate'
            elif score > 0.6:
                timeframe = 'short_term'
            else:
                timeframe = 'long_term'
                
            # Generate mitigation suggestions
            suggestions = self._generate_mitigation_suggestions(patterns)
            
            # Create forecast
            self.generate_forecast(
                patterns=patterns,
                probability=score,
                impact_level=impact_level,
                timeframe=timeframe,
                mitigation_suggestions=suggestions,
                metadata={'cluster_score': score}
            )
            
        return self.forecasts
        
    def _generate_mitigation_suggestions(self, patterns: List[ShadowPattern]) -> List[str]:
        """Generate mitigation suggestions based on patterns"""
        suggestions = []
        
        # Analyze common symbols
        symbol_counts = defaultdict(int)
        for pattern in patterns:
            for symbol in pattern.symbols:
                symbol_counts[symbol] += 1
                
        # Generate symbol-specific suggestions
        for symbol, count in symbol_counts.items():
            if count > len(patterns) / 2:  # Symbol appears in majority of patterns
                suggestions.append(f"Monitor and analyze occurrences of symbol '{symbol}'")
                
        # Add general suggestions
        if len(patterns) > 2:
            suggestions.append("Implement pattern detection and early warning system")
            suggestions.append("Review and update shadow mitigation protocols")
            
        if any(p.impact_score > 0.7 for p in patterns):
            suggestions.append("Prepare emergency response protocols")
            
        return suggestions
        
    def save_forecasts(self, output_file: str):
        """Save forecasts to file"""
        data = {
            'generated_at': datetime.now().isoformat(),
            'forecasts': [
                {
                    'forecast_id': f.forecast_id,
                    'patterns': [
                        {
                            'pattern_id': p.pattern_id,
                            'symbols': p.symbols,
                            'frequency': p.frequency,
                            'confidence': p.confidence,
                            'impact_score': p.impact_score,
                            'context': p.context,
                            'metadata': p.metadata
                        }
                        for p in f.patterns
                    ],
                    'probability': f.probability,
                    'impact_level': f.impact_level,
                    'timeframe': f.timeframe,
                    'mitigation_suggestions': f.mitigation_suggestions,
                    'metadata': f.metadata
                }
                for f in self.forecasts
            ]
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
            
    @classmethod
    def load_forecasts(cls, input_file: str) -> 'ShadowForecastFusion':
        """Load forecasts from file"""
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        fusion = cls()
        
        for forecast_data in data['forecasts']:
            # Add patterns
            patterns = []
            for pattern_data in forecast_data['patterns']:
                pattern_id = fusion.add_pattern(
                    symbols=pattern_data['symbols'],
                    frequency=pattern_data['frequency'],
                    confidence=pattern_data['confidence'],
                    impact_score=pattern_data['impact_score'],
                    context=pattern_data['context'],
                    metadata=pattern_data.get('metadata', {})
                )
                patterns.append(fusion.patterns[-1])
                
            # Add forecast
            fusion.generate_forecast(
                patterns=patterns,
                probability=forecast_data['probability'],
                impact_level=forecast_data['impact_level'],
                timeframe=forecast_data['timeframe'],
                mitigation_suggestions=forecast_data['mitigation_suggestions'],
                metadata=forecast_data.get('metadata', {})
            )
            
        return fusion 