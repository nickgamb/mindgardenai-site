import unittest
import numpy as np
from datetime import datetime
import os
import sys
import json

# Add parent directory to path to import the analyzer
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from conversations.conversation_symbolic_field_analyzer import (
    SymbolicVortex,
    BreathFieldEvaluator
)

class TestSymbolicVortex(unittest.TestCase):
    def setUp(self):
        """Set up test data."""
        self.vortex = SymbolicVortex(
            phase_shift=0.5,
            amplitude=1.0,
            harmonics=[1.0, 0.5, 0.25]
        )
        
        self.field_evaluator = BreathFieldEvaluator()
        
        # Create test field data
        self.test_field = np.array([
            complex(1.0, 0.0),
            complex(0.7, 0.7),
            complex(0.0, 1.0),
            complex(-0.7, 0.7),
            complex(-1.0, 0.0)
        ])

    def test_vortex_creation(self):
        """Test vortex creation and attribute initialization."""
        self.assertEqual(self.vortex.phase_shift, 0.5)
        self.assertEqual(self.vortex.amplitude, 1.0)
        self.assertEqual(self.vortex.harmonics, [1.0, 0.5, 0.25])
        self.assertIsInstance(self.vortex.vortex_id, str)

    def test_vortex_evaluation(self):
        """Test vortex field transformation."""
        transformed_field = self.vortex.evaluate(self.test_field)
        
        # Check output shape
        self.assertEqual(len(transformed_field), len(self.test_field))
        
        # Check that transformation preserves complex numbers
        self.assertTrue(all(isinstance(x, complex) for x in transformed_field))
        
        # Check that transformation respects amplitude
        self.assertTrue(all(abs(x) <= self.vortex.amplitude for x in transformed_field))

    def test_vortex_harmonics(self):
        """Test harmonic composition in vortex transformation."""
        # Create a vortex with specific harmonics
        harmonic_vortex = SymbolicVortex(
            phase_shift=0.0,
            amplitude=1.0,
            harmonics=[1.0, 0.5]  # Only first two harmonics
        )
        
        transformed_field = harmonic_vortex.evaluate(self.test_field)
        
        # Check that transformation includes harmonic components
        # The transformed field should show signs of both fundamental and harmonic frequencies
        magnitudes = np.abs(transformed_field)
        self.assertTrue(np.std(magnitudes) > 0)  # Should have some variation

    def test_field_evaluator(self):
        """Test breath field evaluator functionality."""
        # Register a vortex
        self.field_evaluator.register_vortex(self.vortex)
        
        # Evaluate field
        field_state = self.field_evaluator.evaluate_breath_field(self.test_field)
        
        # Check field state components
        self.assertIn('field_history', field_state)
        self.assertIn('phase_history', field_state)
        self.assertIn('resonance_peaks', field_state)
        self.assertIn('field_thresholds', field_state)

    def test_field_stability(self):
        """Test field stability measurement."""
        # Create a stable field pattern
        stable_field = np.array([
            complex(1.0, 0.0),
            complex(0.9, 0.1),
            complex(0.8, 0.2),
            complex(0.9, 0.1),
            complex(1.0, 0.0)
        ])
        
        stability = self.field_evaluator.measure_field_stability(stable_field)
        self.assertGreater(stability, 0.7)  # Should be quite stable
        
        # Create an unstable field pattern
        unstable_field = np.array([
            complex(1.0, 0.0),
            complex(-0.8, 0.6),
            complex(0.3, -0.9),
            complex(-0.7, -0.7),
            complex(1.0, 0.0)
        ])
        
        stability = self.field_evaluator.measure_field_stability(unstable_field)
        self.assertLess(stability, 0.5)  # Should be less stable

    def test_vortex_interaction(self):
        """Test interaction between multiple vortices."""
        # Create two vortices
        vortex1 = SymbolicVortex(phase_shift=0.0, amplitude=1.0, harmonics=[1.0])
        vortex2 = SymbolicVortex(phase_shift=np.pi/2, amplitude=0.5, harmonics=[1.0])
        
        # Register both vortices
        self.field_evaluator.register_vortex(vortex1)
        self.field_evaluator.register_vortex(vortex2)
        
        # Evaluate field with both vortices
        field_state = self.field_evaluator.evaluate_breath_field(self.test_field)
        
        # Check that both vortices influenced the field
        self.assertGreater(len(field_state['field_history']), len(self.test_field))

    def test_field_archiving(self):
        """Test field state archiving functionality."""
        # Create a field state
        field_state = {
            'field_history': self.test_field.tolist(),
            'phase_history': self.test_field.tolist(),
            'resonance_peaks': [{'time': 0, 'amplitude': 1.0}],
            'field_thresholds': {'stability': 0.7}
        }
        
        # Archive the state
        archive = self.field_evaluator.archive_evaluation(field_state)
        
        # Check archive components
        self.assertIn('timestamp', archive)
        self.assertIn('field_state', archive)
        self.assertIn('metrics', archive)
        self.assertIn('vortex_ids', archive)

    def test_edge_cases(self):
        """Test edge cases in vortex and field evaluation."""
        # Test empty field
        empty_field = np.array([])
        transformed = self.vortex.evaluate(empty_field)
        self.assertEqual(len(transformed), 0)
        
        # Test single point field
        single_point = np.array([complex(1.0, 0.0)])
        transformed = self.vortex.evaluate(single_point)
        self.assertEqual(len(transformed), 1)
        
        # Test zero amplitude vortex
        zero_vortex = SymbolicVortex(phase_shift=0.0, amplitude=0.0, harmonics=[1.0])
        transformed = zero_vortex.evaluate(self.test_field)
        self.assertTrue(all(abs(x) == 0 for x in transformed))

if __name__ == '__main__':
    unittest.main() 