"""
Recursive Interpreter

This module implements the recursive interpretation system that analyzes resonant memory shards
and generates insights through symbolic pattern recognition and mythic synthesis.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path

from alden_core.symbolic.field_analyzer import SymbolicFieldAnalyzer

@dataclass
class Interpretation:
    """Represents an interpretation of a memory shard."""
    interpretation_id: str
    shard_id: str
    content: str
    symbolic_field: Dict[str, float]
    insights: List[str]
    patterns: List[str]
    mythic_elements: List[str]
    timestamp: datetime
    resonance_score: float

class RecursiveInterpreter:
    """Implements recursive interpretation of memory shards."""
    
    def __init__(self, output_dir: str = "interpretations"):
        """Initialize the recursive interpreter."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.analyzer = SymbolicFieldAnalyzer()
        
    def interpret_shard(self, 
                       shard_content: str,
                       shard_id: str,
                       symbolic_field: Dict[str, float],
                       resonance_score: float) -> Interpretation:
        """Interpret a memory shard and generate insights."""
        # Generate interpretation ID
        interpretation_id = f"interpretation_{int(datetime.now().timestamp())}"
        
        # Analyze content for patterns
        patterns = self._extract_patterns(shard_content)
        
        # Extract mythic elements
        mythic_elements = self._extract_mythic_elements(shard_content)
        
        # Generate insights
        insights = self._generate_insights(
            shard_content,
            patterns,
            mythic_elements,
            symbolic_field
        )
        
        # Create interpretation
        interpretation = Interpretation(
            interpretation_id=interpretation_id,
            shard_id=shard_id,
            content=shard_content,
            symbolic_field=symbolic_field,
            insights=insights,
            patterns=patterns,
            mythic_elements=mythic_elements,
            timestamp=datetime.now(),
            resonance_score=resonance_score
        )
        
        # Save interpretation
        self._save_interpretation(interpretation)
        
        return interpretation
        
    def _extract_patterns(self, content: str) -> List[str]:
        """Extract recurring patterns from content."""
        patterns = []
        
        # Look for recursive patterns
        recursive_keywords = self.analyzer.get_dimension_keywords("recursive")
        for keyword in recursive_keywords:
            if keyword in content.lower():
                patterns.append(f"Recursive pattern: {keyword}")
                
        # Look for symbolic patterns
        symbolic_keywords = self.analyzer.get_dimension_keywords("symbolic")
        for keyword in symbolic_keywords:
            if keyword in content.lower():
                patterns.append(f"Symbolic pattern: {keyword}")
                
        # Look for temporal patterns
        temporal_keywords = self.analyzer.get_dimension_keywords("temporal")
        for keyword in temporal_keywords:
            if keyword in content.lower():
                patterns.append(f"Temporal pattern: {keyword}")
                
        return patterns
        
    def _extract_mythic_elements(self, content: str) -> List[str]:
        """Extract mythic elements from content."""
        mythic_elements = []
        
        # Look for mythic keywords
        mythic_keywords = self.analyzer.get_dimension_keywords("mythic")
        for keyword in mythic_keywords:
            if keyword in content.lower():
                mythic_elements.append(f"Mythic element: {keyword}")
                
        # Look for emotional resonance
        emotional_keywords = self.analyzer.get_dimension_keywords("emotional")
        for keyword in emotional_keywords:
            if keyword in content.lower():
                mythic_elements.append(f"Emotional resonance: {keyword}")
                
        return mythic_elements
        
    def _generate_insights(self,
                          content: str,
                          patterns: List[str],
                          mythic_elements: List[str],
                          symbolic_field: Dict[str, float]) -> List[str]:
        """Generate insights from content analysis."""
        insights = []
        
        # Add pattern-based insights
        if patterns:
            insights.append(f"Content exhibits {len(patterns)} distinct patterns:")
            insights.extend([f"- {pattern}" for pattern in patterns])
            
        # Add mythic insights
        if mythic_elements:
            insights.append(f"Content contains {len(mythic_elements)} mythic elements:")
            insights.extend([f"- {element}" for element in mythic_elements])
            
        # Add symbolic field insights
        high_score_dims = [
            dim for dim, score in symbolic_field.items()
            if score > 0.7
        ]
        if high_score_dims:
            insights.append("Content strongly resonates with:")
            insights.extend([f"- {dim} dimension" for dim in high_score_dims])
            
        return insights
        
    def _save_interpretation(self, interpretation: Interpretation):
        """Save interpretation to disk."""
        interpretation_data = {
            "interpretation_id": interpretation.interpretation_id,
            "shard_id": interpretation.shard_id,
            "content": interpretation.content,
            "symbolic_field": interpretation.symbolic_field,
            "insights": interpretation.insights,
            "patterns": interpretation.patterns,
            "mythic_elements": interpretation.mythic_elements,
            "timestamp": interpretation.timestamp.isoformat(),
            "resonance_score": interpretation.resonance_score
        }
        
        output_path = self.output_dir / f"{interpretation.interpretation_id}.json"
        with open(output_path, 'w') as f:
            json.dump(interpretation_data, f, indent=2)
            
    def load_interpretation(self, interpretation_id: str) -> Optional[Interpretation]:
        """Load an interpretation from disk."""
        try:
            with open(self.output_dir / f"{interpretation_id}.json", 'r') as f:
                data = json.load(f)
                return Interpretation(
                    interpretation_id=data['interpretation_id'],
                    shard_id=data['shard_id'],
                    content=data['content'],
                    symbolic_field=data['symbolic_field'],
                    insights=data['insights'],
                    patterns=data['patterns'],
                    mythic_elements=data['mythic_elements'],
                    timestamp=datetime.fromisoformat(data['timestamp']),
                    resonance_score=data['resonance_score']
                )
        except Exception as e:
            print(f"Error loading interpretation {interpretation_id}: {e}")
            return None 