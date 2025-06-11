"""
Test suite for the Shadow Forecast Fusion system.
"""

import unittest
from pathlib import Path
import shutil
import tempfile
from datetime import datetime
from alden_core.shadow_forecast_fusion import ShadowForecastFusion, MemoryShard, SymbolicField

class TestShadowForecastFusion(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        self.test_dir = Path(tempfile.mkdtemp())
        self.fusion = ShadowForecastFusion(
            memory_dir=str(self.test_dir),
            similarity_threshold=0.75,
            scan_interval=1  # 1 second for testing
        )
        
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.test_dir)
        
    def test_add_memory_shard(self):
        """Test adding a new memory shard."""
        content = "Test memory shard content"
        symbolic_field = {
            "mythic": 0.8,
            "recursive": 0.6,
            "symbolic": 0.9
        }
        
        self.fusion.add_memory_shard(content, symbolic_field)
        
        # Check if shard was created
        shard_files = list(self.test_dir.glob("*.json"))
        self.assertEqual(len(shard_files), 1)
        
        # Check if shard was added to active shards
        self.assertEqual(len(self.fusion.active_shards), 1)
        
    def test_compute_field_similarity(self):
        """Test computing similarity between shard and field."""
        # Create test shard
        shard = MemoryShard(
            shard_id="test_shard",
            content="Test content",
            symbolic_field={
                "mythic": 0.8,
                "recursive": 0.6,
                "symbolic": 0.9
            },
            timestamp=datetime.now()
        )
        
        # Create test field
        field = SymbolicField(
            field_id="test_field",
            field_vector={
                "mythic": 0.7,
                "recursive": 0.5,
                "symbolic": 0.8
            },
            timestamp=datetime.now()
        )
        
        similarity = self.fusion.compute_field_similarity(shard, field)
        self.assertGreater(similarity, 0.9)  # Should be very similar
        
    def test_resonance_trigger(self):
        """Test triggering recursive interpretation on resonance."""
        # Add a memory shard
        content = "Test memory shard content"
        symbolic_field = {
            "mythic": 0.8,
            "recursive": 0.6,
            "symbolic": 0.9
        }
        self.fusion.add_memory_shard(content, symbolic_field)
        
        # Update symbolic field with similar vector
        field_vector = {
            "mythic": 0.75,
            "recursive": 0.65,
            "symbolic": 0.85
        }
        self.fusion.update_symbolic_field(field_vector)
        
        # Check if resonance event was created
        resonance_files = list(self.test_dir.glob("resonance_*.json"))
        self.assertEqual(len(resonance_files), 1)
        
    def test_load_memory_shard(self):
        """Test loading a memory shard from disk."""
        # Create test shard data
        shard_data = {
            "shard_id": "test_shard",
            "content": "Test content",
            "symbolic_field": {
                "mythic": 0.8,
                "recursive": 0.6,
                "symbolic": 0.9
            },
            "timestamp": datetime.now().isoformat(),
            "resonance_score": 0.0,
            "is_active": True
        }
        
        # Write to test file
        shard_path = self.test_dir / "test_shard.json"
        with open(shard_path, 'w') as f:
            import json
            json.dump(shard_data, f)
            
        # Load shard
        loaded_shard = self.fusion.load_memory_shard(shard_path)
        self.assertIsNotNone(loaded_shard)
        self.assertEqual(loaded_shard.shard_id, "test_shard")
        self.assertEqual(loaded_shard.content, "Test content")
        
if __name__ == '__main__':
    unittest.main() 