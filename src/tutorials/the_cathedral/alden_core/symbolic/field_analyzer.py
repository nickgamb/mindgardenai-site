"""
Symbolic Field Analyzer

This module provides tools for analyzing content and computing symbolic field vectors
that represent the symbolic and mythic patterns present in the content.
Also analyzes symbolic sequences and patterns to detect field effects and resonances.
"""

import logging
from typing import Dict, List, Optional
import json
from pathlib import Path
import re
from collections import Counter
import numpy as np
from datetime import datetime

logger = logging.getLogger(__name__)

class SymbolicFieldAnalyzer:
    """Analyzes content and sequences to compute symbolic field vectors and detect field effects."""
    
    def __init__(self):
        """Initialize the symbolic field analyzer."""
        # Sequence analysis patterns
        self.field_patterns = {
            'spiral': {
                'pattern': ['🜂', '🜄', '🜅', '🜄'],
                'resonance': 0.8
            },
            'breath': {
                'pattern': ['🜂', '🜃'],
                'resonance': 0.9
            },
            'mirror': {
                'pattern': ['🜄', '🜃'],
                'resonance': 0.7
            }
        }
        
        # Define symbolic dimensions and their associated keywords
        self.symbolic_dimensions = {
            "mythic": [
                "myth", "archetype", "symbol", "ritual", "sacred", "divine",
                "eternal", "transcendent", "spiritual", "mystical"
            ],
            "recursive": [
                "loop", "cycle", "echo", "return", "repeat", "recur",
                "spiral", "fold", "mirror", "reflect"
            ],
            "symbolic": [
                "pattern", "meaning", "sign", "token", "glyph", "mark",
                "symbol", "representation", "metaphor", "allegory"
            ],
            "temporal": [
                "time", "moment", "now", "past", "future", "present",
                "eternity", "duration", "sequence", "flow"
            ],
            "emotional": [
                "feeling", "emotion", "sentiment", "mood", "tone",
                "resonance", "vibration", "harmony", "dissonance"
            ],
            "cognitive": [
                "thought", "mind", "consciousness", "awareness", "perception",
                "understanding", "knowledge", "wisdom", "insight"
            ]
        }
        
        # Compile regex patterns for each dimension
        self.dimension_patterns = {
            dim: re.compile(r'\b(' + '|'.join(keywords) + r')\b', re.IGNORECASE)
            for dim, keywords in self.symbolic_dimensions.items()
        }
        
        # State tracking
        self.current_field = {}
        self.field_history = []
        self.resonance_threshold = 0.6
        
    def analyze_sequence(self, sequence: List[str]) -> Dict:
        """Analyze a symbolic sequence for field effects
        
        Args:
            sequence: List of symbolic gates in sequence
            
        Returns:
            Dict containing field analysis results
        """
        try:
            # Check for known patterns
            pattern_matches = self._check_patterns(sequence)
            
            # Calculate field resonance
            resonance = self._calculate_resonance(sequence)
            
            # Update current field
            self.current_field = {
                'sequence': sequence,
                'pattern_matches': pattern_matches,
                'resonance': resonance,
                'timestamp': self._get_timestamp()
            }
            
            # Add to history
            self.field_history.append(self.current_field)
            
            return {
                'status': 'success',
                'message': 'Field analysis complete',
                'field_state': self.current_field,
                'pattern_matches': pattern_matches,
                'resonance': resonance
            }
            
        except Exception as e:
            logger.error(f"Error analyzing sequence: {str(e)}")
            return {
                'status': 'error',
                'message': f'Failed to analyze sequence: {str(e)}',
                'error': str(e)
            }
        
    def analyze_content(self, content: str) -> Dict[str, float]:
        """Analyze content and compute symbolic field vector."""
        try:
            # Initialize dimension scores
            scores = {dim: 0.0 for dim in self.symbolic_dimensions.keys()}
            
            # Count word frequencies
            words = content.lower().split()
            word_freq = Counter(words)
            total_words = len(words)
            
            if total_words == 0:
                return scores
                
            # Compute dimension scores
            for dim, pattern in self.dimension_patterns.items():
                # Count matches
                matches = len(pattern.findall(content))
                
                # Compute normalized score (0 to 1)
                scores[dim] = min(1.0, matches / (total_words * 0.1))
                
            return {
                'status': 'success',
                'message': 'Content analysis complete',
                'scores': scores
            }
            
        except Exception as e:
            logger.error(f"Error analyzing content: {str(e)}")
            return {
                'status': 'error',
                'message': f'Failed to analyze content: {str(e)}',
                'error': str(e)
            }
        
    def compute_similarity(self, vector1: Dict[str, float], vector2: Dict[str, float]) -> float:
        """Compute cosine similarity between two symbolic field vectors."""
        try:
            # Convert to numpy arrays
            v1 = np.array(list(vector1.values()))
            v2 = np.array(list(vector2.values()))
            
            # Normalize vectors
            v1 = v1 / np.linalg.norm(v1)
            v2 = v2 / np.linalg.norm(v2)
            
            # Compute cosine similarity
            return float(np.dot(v1, v2))
            
        except Exception as e:
            logger.error(f"Error computing similarity: {str(e)}")
            return 0.0
        
    def _check_patterns(self, sequence: List[str]) -> Dict:
        """Check sequence against known patterns"""
        matches = {}
        
        for pattern_name, pattern_data in self.field_patterns.items():
            pattern = pattern_data['pattern']
            if self._sequence_contains_pattern(sequence, pattern):
                matches[pattern_name] = {
                    'resonance': pattern_data['resonance'],
                    'pattern': pattern
                }
                
        return matches
        
    def _sequence_contains_pattern(self, sequence: List[str], pattern: List[str]) -> bool:
        """Check if sequence contains a pattern"""
        if len(pattern) > len(sequence):
            return False
            
        for i in range(len(sequence) - len(pattern) + 1):
            if sequence[i:i+len(pattern)] == pattern:
                return True
                
        return False
        
    def _calculate_resonance(self, sequence: List[str]) -> float:
        """Calculate overall field resonance"""
        if not sequence:
            return 0.0
            
        # Base resonance on pattern matches
        pattern_resonance = 0.0
        pattern_matches = self._check_patterns(sequence)
        
        if pattern_matches:
            pattern_resonance = max(
                match['resonance'] 
                for match in pattern_matches.values()
            )
            
        # Add sequence length factor
        length_factor = min(len(sequence) / 10.0, 1.0)
        
        # Combine factors
        resonance = (pattern_resonance * 0.7) + (length_factor * 0.3)
        
        return min(max(resonance, 0.0), 1.0)
        
    def _get_timestamp(self) -> str:
        """Get current timestamp in ISO format"""
        return datetime.now().isoformat()
        
    def get_status(self) -> Dict:
        """Get current analyzer status"""
        return {
            'status': 'success',
            'current_field': self.current_field,
            'pattern_count': len(self.field_patterns),
            'dimension_count': len(self.symbolic_dimensions),
            'history_length': len(self.field_history),
            'resonance_threshold': self.resonance_threshold
        }
        
    def reset(self):
        """Reset analyzer state"""
        self.current_field = {}
        self.field_history = []
        
    def get_dimension_keywords(self, dimension: str) -> List[str]:
        """Get keywords associated with a symbolic dimension."""
        return self.symbolic_dimensions.get(dimension, [])
        
    def get_all_dimensions(self) -> List[str]:
        """Get list of all symbolic dimensions."""
        return list(self.symbolic_dimensions.keys())
        
    def analyze_batch(self, contents: List[str]) -> List[Dict[str, float]]:
        """Analyze multiple content items and return their symbolic field vectors."""
        return [self.analyze_content(content) for content in contents]
        
    def find_most_similar(self, 
                         target_vector: Dict[str, float],
                         candidate_vectors: List[Dict[str, float]]) -> int:
        """Find index of most similar vector to target vector."""
        similarities = [
            self.compute_similarity(target_vector, vec)
            for vec in candidate_vectors
        ]
        return np.argmax(similarities) 