import unittest
import numpy as np
from datetime import datetime
import os
import sys
import json

# Add parent directory to path to import the analyzer
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from conversations.conversation_symbolic_field_analyzer import (
    visualize_breath_field,
    compute_field_metrics,
    serialize_field_state,
    load_field_state
)

class TestBreathPatterns(unittest.TestCase):
    def setUp(self):
        """Set up test data."""
        self.test_field_data = {
            'field_history': [
                complex(1.0, 0.0),
                complex(0.7, 0.7),
                complex(0.0, 1.0),
                complex(-0.7, 0.7),
                complex(-1.0, 0.0)
            ],
            'phase_history': [
                complex(1.0, 0.0),
                complex(0.7, 0.7),
                complex(0.0, 1.0),
                complex(-0.7, 0.7),
                complex(-1.0, 0.0)
            ],
            'resonance_peaks': [
                {'time': 0, 'amplitude': 1.0},
                {'time': 2, 'amplitude': 1.0}
            ],
            'field_thresholds': {
                'stability': 0.7,
                'resonance': 0.8,
                'coherence': 0.6
            }
        }
        
        # Create temporary directory for test outputs
        self.test_output_dir = os.path.join(os.path.dirname(__file__), 'test_outputs')
        os.makedirs(self.test_output_dir, exist_ok=True)

    def tearDown(self):
        """Clean up test outputs."""
        if os.path.exists(self.test_output_dir):
            for file in os.listdir(self.test_output_dir):
                os.remove(os.path.join(self.test_output_dir, file))
            os.rmdir(self.test_output_dir)

    def test_visualize_breath_field_static(self):
        """Test static visualization generation."""
        visualize_breath_field(self.test_field_data, self.test_output_dir, format='static')
        
        # Check if visualization files were created
        expected_files = [
            'field_evolution.png',
            'phase_vector.png',
            'threshold_heatmap.png'
        ]
        
        for file in expected_files:
            self.assertTrue(
                os.path.exists(os.path.join(self.test_output_dir, file)),
                f"Visualization file {file} was not created"
            )

    def test_visualize_breath_field_interactive(self):
        """Test interactive visualization generation."""
        visualize_breath_field(self.test_field_data, self.test_output_dir, format='interactive')
        
        # Check if visualization files were created
        expected_files = [
            'field_evolution.html',
            'phase_space.html',
            'threshold_surface.html'
        ]
        
        for file in expected_files:
            self.assertTrue(
                os.path.exists(os.path.join(self.test_output_dir, file)),
                f"Visualization file {file} was not created"
            )

    def test_compute_field_metrics(self):
        """Test field metrics computation."""
        metrics = compute_field_metrics(self.test_field_data)
        
        # Check if all expected metrics are present
        expected_metrics = [
            'breath_phase_coherence',
            'resonance_stability',
            'field_entropy'
        ]
        
        for metric in expected_metrics:
            self.assertIn(metric, metrics)
            self.assertIsInstance(metrics[metric], (int, float))

    def test_serialize_and_load_field_state(self):
        """Test field state serialization and loading."""
        # Serialize state
        output_path = os.path.join(self.test_output_dir, 'test_state.json')
        serialize_field_state(self.test_field_data, output_path)
        
        # Verify file was created
        self.assertTrue(os.path.exists(output_path))
        
        # Load state
        loaded_state = load_field_state(output_path)
        
        # Verify all components were preserved
        self.assertEqual(len(loaded_state['field_history']), len(self.test_field_data['field_history']))
        self.assertEqual(len(loaded_state['phase_history']), len(self.test_field_data['phase_history']))
        self.assertEqual(len(loaded_state['resonance_peaks']), len(self.test_field_data['resonance_peaks']))
        self.assertEqual(loaded_state['field_thresholds'], self.test_field_data['field_thresholds'])

    def test_edge_cases(self):
        """Test edge cases in field computations."""
        # Test empty field history
        empty_data = {
            'field_history': [],
            'phase_history': [],
            'resonance_peaks': [],
            'field_thresholds': {}
        }
        
        metrics = compute_field_metrics(empty_data)
        self.assertEqual(metrics['breath_phase_coherence'], 0)
        self.assertEqual(metrics['resonance_stability'], 0)
        self.assertEqual(metrics['field_entropy'], 0)
        
        # Test single point field history
        single_point_data = {
            'field_history': [complex(1.0, 0.0)],
            'phase_history': [complex(1.0, 0.0)],
            'resonance_peaks': [],
            'field_thresholds': {'stability': 0.7}
        }
        
        metrics = compute_field_metrics(single_point_data)
        self.assertIsInstance(metrics['breath_phase_coherence'], float)
        self.assertIsInstance(metrics['resonance_stability'], float)
        self.assertIsInstance(metrics['field_entropy'], float)

    def test_phase_wraparound(self):
        """Test phase angle wraparound handling."""
        # Create data with phase angles crossing 2π boundary
        phase_data = {
            'field_history': [
                complex(np.cos(0), np.sin(0)),
                complex(np.cos(np.pi/2), np.sin(np.pi/2)),
                complex(np.cos(np.pi), np.sin(np.pi)),
                complex(np.cos(3*np.pi/2), np.sin(3*np.pi/2)),
                complex(np.cos(2*np.pi), np.sin(2*np.pi))
            ],
            'phase_history': [
                complex(np.cos(0), np.sin(0)),
                complex(np.cos(np.pi/2), np.sin(np.pi/2)),
                complex(np.cos(np.pi), np.sin(np.pi)),
                complex(np.cos(3*np.pi/2), np.sin(3*np.pi/2)),
                complex(np.cos(2*np.pi), np.sin(2*np.pi))
            ],
            'resonance_peaks': [],
            'field_thresholds': {'stability': 0.7}
        }
        
        metrics = compute_field_metrics(phase_data)
        self.assertIsInstance(metrics['breath_phase_coherence'], float)
        self.assertGreaterEqual(metrics['breath_phase_coherence'], 0)

    def test_resonance_stability(self):
        """Test resonance stability computation."""
        # Create data with clear constructive and destructive interference
        resonance_data = {
            'field_history': [
                complex(1.0, 0.0),  # Constructive
                complex(0.8, 0.0),  # Constructive
                complex(0.2, 0.0),  # Destructive
                complex(0.1, 0.0),  # Destructive
                complex(0.9, 0.0)   # Constructive
            ],
            'phase_history': [
                complex(1.0, 0.0),
                complex(0.8, 0.0),
                complex(0.2, 0.0),
                complex(0.1, 0.0),
                complex(0.9, 0.0)
            ],
            'resonance_peaks': [],
            'field_thresholds': {'stability': 0.7}
        }
        
        metrics = compute_field_metrics(resonance_data)
        self.assertGreater(metrics['resonance_stability'], 1.0)  # More constructive than destructive

if __name__ == '__main__':
    unittest.main() 