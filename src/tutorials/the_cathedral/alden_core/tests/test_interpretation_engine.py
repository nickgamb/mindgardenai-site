"""
Tests for the Alden Interpretation Engine
"""

import unittest
from alden_cli.interpretation_engine import InterpretationEngine, InterpretationMode

class TestInterpretationEngine(unittest.TestCase):
    def setUp(self):
        self.engine = InterpretationEngine()
        
    def test_mode_setting(self):
        """Test setting different interpretation modes"""
        for mode in InterpretationMode:
            self.engine.set_mode(mode)
            self.assertEqual(self.engine.current_mode, mode)
            
    def test_interpretation_generation(self):
        """Test generating interpretations in different modes"""
        test_content = "The Loom weaves patterns of light and shadow"
        
        # Test each mode
        for mode in InterpretationMode:
            self.engine.set_mode(mode)
            interpretation = self.engine.interpret(test_content)
            
            # Verify interpretation structure
            self.assertIn("timestamp", interpretation)
            self.assertIn("mode", interpretation)
            self.assertIn("content", interpretation)
            self.assertIn("analysis", interpretation)
            self.assertIn("symbols", interpretation)
            self.assertIn("shadows", interpretation)
            
            # Verify mode-specific analysis
            analysis = interpretation["analysis"]
            if mode == InterpretationMode.ANALYTIC:
                self.assertIn("patterns", analysis)
                self.assertIn("structure", analysis)
                self.assertIn("key_phrases", analysis)
            elif mode == InterpretationMode.SYMBOLIC:
                self.assertIn("archetypes", analysis)
                self.assertIn("symbolic_flow", analysis)
                self.assertIn("resonance_map", analysis)
            elif mode == InterpretationMode.POETIC:
                self.assertIn("metaphors", analysis)
                self.assertIn("narrative_arc", analysis)
                self.assertIn("emotional_tone", analysis)
            elif mode == InterpretationMode.ORACULAR:
                self.assertIn("portents", analysis)
                self.assertIn("visionary_elements", analysis)
                self.assertIn("temporal_echoes", analysis)
            elif mode == InterpretationMode.MIRROR:
                self.assertIn("recursive_patterns", analysis)
                self.assertIn("self_reference", analysis)
                self.assertIn("echo_depth", analysis)
                
    def test_shadow_forecast(self):
        """Test shadow forecast generation"""
        test_content = "The shadows dance between the threads of memory"
        
        # Enable shadow forecasts
        self.engine.context.include_shadows = True
        
        interpretation = self.engine.interpret(test_content)
        shadows = interpretation["shadows"]
        
        # Verify shadow forecast structure
        self.assertIn("potential_paths", shadows)
        self.assertIn("shadow_elements", shadows)
        self.assertIn("transformation_points", shadows)
        
        # Verify shadow forecasts are being tracked
        self.assertTrue(len(self.engine.shadow_forecasts) > 0)
        
    def test_context_integration(self):
        """Test integration with symbolic memory context"""
        test_content = "The Guardian's Flame illuminates the path"
        test_context = {
            "symbolic_memory": {
                "Guardian": {"resonance": 0.8, "context": "protection"},
                "Flame": {"resonance": 0.9, "context": "illumination"}
            }
        }
        
        interpretation = self.engine.interpret(test_content, test_context)
        
        # Verify context was integrated
        self.assertEqual(self.engine.context.symbolic_memory, test_context["symbolic_memory"])
        
if __name__ == "__main__":
    unittest.main() 