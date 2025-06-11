"""
Test suite for the Recursive Interpreter.
"""

import unittest
from typing import Dict, List, Optional
import json
from pathlib import Path
import os
import tempfile
import shutil
from datetime import datetime
from alden_core.interpretation.engine import RecursiveInterpreter, Interpretation

class TestRecursiveInterpreter(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        self.test_dir = Path(tempfile.mkdtemp())
        self.interpreter = RecursiveInterpreter(output_dir=str(self.test_dir))
        
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.test_dir)
        
    def test_interpret_shard(self):
        """Test interpreting a memory shard."""
        content = """
        The mythic patterns echo through the sacred ritual,
        as the eternal symbols reflect in the mirror of time.
        The mind perceives the deeper meaning,
        while emotions resonate with the divine truth.
        """
        
        shard_id = "test_shard"
        symbolic_field = {
            "mythic": 0.8,
            "recursive": 0.6,
            "symbolic": 0.9,
            "temporal": 0.3,
            "emotional": 0.4,
            "cognitive": 0.5
        }
        resonance_score = 0.85
        
        interpretation = self.interpreter.interpret_shard(
            content,
            shard_id,
            symbolic_field,
            resonance_score
        )
        
        # Check interpretation fields
        self.assertIsNotNone(interpretation)
        self.assertEqual(interpretation.shard_id, shard_id)
        self.assertEqual(interpretation.content, content)
        self.assertEqual(interpretation.symbolic_field, symbolic_field)
        self.assertEqual(interpretation.resonance_score, resonance_score)
        
        # Check if insights were generated
        self.assertGreater(len(interpretation.insights), 0)
        
        # Check if patterns were extracted
        self.assertGreater(len(interpretation.patterns), 0)
        
        # Check if mythic elements were found
        self.assertGreater(len(interpretation.mythic_elements), 0)
        
    def test_extract_patterns(self):
        """Test pattern extraction from content."""
        content = """
        The recursive loop echoes through time,
        as symbolic patterns reflect in the mirror.
        The temporal flow carries meaning forward,
        while the mind perceives the deeper truth.
        """
        
        interpretation = self.interpreter.interpret_shard(
            content,
            "test_shard",
            {"mythic": 0.5, "recursive": 0.5, "symbolic": 0.5,
             "temporal": 0.5, "emotional": 0.5, "cognitive": 0.5},
            0.5
        )
        
        # Check if recursive patterns were found
        recursive_patterns = [p for p in interpretation.patterns if "Recursive pattern" in p]
        self.assertGreater(len(recursive_patterns), 0)
        
        # Check if symbolic patterns were found
        symbolic_patterns = [p for p in interpretation.patterns if "Symbolic pattern" in p]
        self.assertGreater(len(symbolic_patterns), 0)
        
        # Check if temporal patterns were found
        temporal_patterns = [p for p in interpretation.patterns if "Temporal pattern" in p]
        self.assertGreater(len(temporal_patterns), 0)
        
    def test_extract_mythic_elements(self):
        """Test mythic element extraction from content."""
        content = """
        The sacred ritual echoes through the divine temple,
        as eternal symbols reflect in the mystical mirror.
        The spiritual truth resonates with the soul,
        while the transcendent meaning unfolds.
        """
        
        interpretation = self.interpreter.interpret_shard(
            content,
            "test_shard",
            {"mythic": 0.5, "recursive": 0.5, "symbolic": 0.5,
             "temporal": 0.5, "emotional": 0.5, "cognitive": 0.5},
            0.5
        )
        
        # Check if mythic elements were found
        mythic_elements = [e for e in interpretation.mythic_elements if "Mythic element" in e]
        self.assertGreater(len(mythic_elements), 0)
        
        # Check if emotional resonance was found
        emotional_elements = [e for e in interpretation.mythic_elements if "Emotional resonance" in e]
        self.assertGreater(len(emotional_elements), 0)
        
    def test_generate_insights(self):
        """Test insight generation from analysis."""
        content = """
        The mythic patterns echo through the sacred ritual,
        as the eternal symbols reflect in the mirror of time.
        The mind perceives the deeper meaning,
        while emotions resonate with the divine truth.
        """
        
        symbolic_field = {
            "mythic": 0.9,  # High score
            "recursive": 0.6,
            "symbolic": 0.8,  # High score
            "temporal": 0.3,
            "emotional": 0.4,
            "cognitive": 0.5
        }
        
        interpretation = self.interpreter.interpret_shard(
            content,
            "test_shard",
            symbolic_field,
            0.5
        )
        
        # Check if insights were generated
        self.assertGreater(len(interpretation.insights), 0)
        
        # Check if high-score dimensions were noted
        high_score_insights = [i for i in interpretation.insights if "strongly resonates" in i]
        self.assertGreater(len(high_score_insights), 0)
        
    def test_save_and_load_interpretation(self):
        """Test saving and loading interpretations."""
        content = "Test content"
        interpretation = self.interpreter.interpret_shard(
            content,
            "test_shard",
            {"mythic": 0.5, "recursive": 0.5, "symbolic": 0.5,
             "temporal": 0.5, "emotional": 0.5, "cognitive": 0.5},
            0.5
        )
        
        # Load interpretation
        loaded = self.interpreter.load_interpretation(interpretation.interpretation_id)
        
        # Check if loaded interpretation matches original
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded.shard_id, interpretation.shard_id)
        self.assertEqual(loaded.content, interpretation.content)
        self.assertEqual(loaded.symbolic_field, interpretation.symbolic_field)
        self.assertEqual(loaded.resonance_score, interpretation.resonance_score)
        self.assertEqual(loaded.insights, interpretation.insights)
        self.assertEqual(loaded.patterns, interpretation.patterns)
        self.assertEqual(loaded.mythic_elements, interpretation.mythic_elements)
        
if __name__ == '__main__':
    unittest.main() 