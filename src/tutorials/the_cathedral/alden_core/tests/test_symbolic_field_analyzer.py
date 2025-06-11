"""
Test suite for the Symbolic Field Analyzer.
"""

import unittest
from typing import Dict, List
import json
from pathlib import Path

from alden_core.symbolic.field_analyzer import SymbolicFieldAnalyzer

class TestSymbolicFieldAnalyzer(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        self.analyzer = SymbolicFieldAnalyzer()
        
    def test_analyze_content(self):
        """Test content analysis and vector computation."""
        content = """
        The mythic patterns echo through the sacred ritual,
        as the eternal symbols reflect in the mirror of time.
        The mind perceives the deeper meaning,
        while emotions resonate with the divine truth.
        """
        
        vector = self.analyzer.analyze_content(content)
        
        # Check if all dimensions are present
        self.assertEqual(set(vector.keys()), set(self.analyzer.get_all_dimensions()))
        
        # Check if scores are between 0 and 1
        for score in vector.values():
            self.assertGreaterEqual(score, 0.0)
            self.assertLessEqual(score, 1.0)
            
        # Check if mythic dimension has high score
        self.assertGreater(vector["mythic"], 0.5)
        
    def test_compute_similarity(self):
        """Test similarity computation between vectors."""
        vector1 = {
            "mythic": 0.8,
            "recursive": 0.6,
            "symbolic": 0.9,
            "temporal": 0.3,
            "emotional": 0.4,
            "cognitive": 0.5
        }
        
        vector2 = {
            "mythic": 0.7,
            "recursive": 0.5,
            "symbolic": 0.8,
            "temporal": 0.4,
            "emotional": 0.3,
            "cognitive": 0.6
        }
        
        similarity = self.analyzer.compute_similarity(vector1, vector2)
        
        # Check if similarity is between 0 and 1
        self.assertGreaterEqual(similarity, 0.0)
        self.assertLessEqual(similarity, 1.0)
        
        # Check if similar vectors have high similarity
        self.assertGreater(similarity, 0.8)
        
    def test_find_most_similar(self):
        """Test finding most similar vector."""
        target = {
            "mythic": 0.8,
            "recursive": 0.6,
            "symbolic": 0.9,
            "temporal": 0.3,
            "emotional": 0.4,
            "cognitive": 0.5
        }
        
        candidates = [
            {
                "mythic": 0.7,
                "recursive": 0.5,
                "symbolic": 0.8,
                "temporal": 0.4,
                "emotional": 0.3,
                "cognitive": 0.6
            },
            {
                "mythic": 0.2,
                "recursive": 0.3,
                "symbolic": 0.1,
                "temporal": 0.8,
                "emotional": 0.7,
                "cognitive": 0.6
            },
            {
                "mythic": 0.9,
                "recursive": 0.7,
                "symbolic": 0.8,
                "temporal": 0.2,
                "emotional": 0.3,
                "cognitive": 0.4
            }
        ]
        
        most_similar_idx = self.analyzer.find_most_similar(target, candidates)
        
        # The third vector should be most similar
        self.assertEqual(most_similar_idx, 2)
        
    def test_analyze_batch(self):
        """Test batch analysis of multiple content items."""
        contents = [
            "The mythic symbols echo through time.",
            "The mind perceives patterns in the sacred ritual.",
            "Emotions resonate with eternal truth."
        ]
        
        vectors = self.analyzer.analyze_batch(contents)
        
        # Check if we got the right number of vectors
        self.assertEqual(len(vectors), len(contents))
        
        # Check if each vector has all dimensions
        for vector in vectors:
            self.assertEqual(set(vector.keys()), set(self.analyzer.get_all_dimensions()))
            
    def test_empty_content(self):
        """Test analysis of empty content."""
        vector = self.analyzer.analyze_content("")
        
        # Check if all dimensions are present with zero scores
        self.assertEqual(set(vector.keys()), set(self.analyzer.get_all_dimensions()))
        for score in vector.values():
            self.assertEqual(score, 0.0)
            
if __name__ == '__main__':
    unittest.main() 