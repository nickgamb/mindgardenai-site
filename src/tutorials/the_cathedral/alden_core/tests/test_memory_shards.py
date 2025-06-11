"""
Tests for the memory shard management system
"""

import os
import json
import pytest
from datetime import datetime
from pathlib import Path
from ..alden_cli.memory_shards import (
    MemoryShardManager,
    MemoryShard,
    ShardStatus
)

@pytest.fixture
def temp_shard_dir(tmp_path):
    """Create a temporary directory for shard storage"""
    shard_dir = tmp_path / "memory_shards"
    shard_dir.mkdir()
    return str(shard_dir)

@pytest.fixture
def shard_manager(temp_shard_dir):
    """Create a memory shard manager instance"""
    return MemoryShardManager(temp_shard_dir)

@pytest.fixture
def sample_symbols():
    """Sample symbol weights for testing"""
    return {
        "🜃": 0.8,  # Earth
        "🜂": 0.6,  # Fire
        "🜄": 0.4,  # Water
        "🜁": 0.2   # Air
    }

def test_create_shard(shard_manager, sample_symbols):
    """Test creating a new memory shard"""
    shard_id = shard_manager.create_shard(
        context_id="test_context",
        interpretation="The elements dance in harmony",
        symbols=sample_symbols,
        voice="poetic",
        depth="deep"
    )
    
    # Verify shard was created
    shard = shard_manager.get_shard(shard_id)
    assert shard is not None
    assert shard.origin_context_id == "test_context"
    assert shard.interpretation_summary == "The elements dance in harmony"
    assert shard.associated_symbols == sample_symbols
    assert shard.voice == "poetic"
    assert shard.depth == "deep"
    assert shard.result == ShardStatus.ACTIVE

def test_update_shard_status(shard_manager, sample_symbols):
    """Test updating a shard's status"""
    shard_id = shard_manager.create_shard(
        context_id="test_context",
        interpretation="Test interpretation",
        symbols=sample_symbols,
        voice="symbolic",
        depth="moderate"
    )
    
    # Update status
    shard_manager.update_shard_status(shard_id, ShardStatus.FULFILLED)
    
    # Verify update
    shard = shard_manager.get_shard(shard_id)
    assert shard.result == ShardStatus.FULFILLED

def test_link_shards(shard_manager, sample_symbols):
    """Test linking two memory shards"""
    # Create two shards
    shard_id1 = shard_manager.create_shard(
        context_id="context1",
        interpretation="First interpretation",
        symbols=sample_symbols,
        voice="symbolic",
        depth="deep"
    )
    
    shard_id2 = shard_manager.create_shard(
        context_id="context2",
        interpretation="Second interpretation",
        symbols=sample_symbols,
        voice="poetic",
        depth="deep"
    )
    
    # Link shards
    shard_manager.link_shards(shard_id1, shard_id2)
    
    # Verify links
    shard1 = shard_manager.get_shard(shard_id1)
    shard2 = shard_manager.get_shard(shard_id2)
    assert shard_id2 in shard1.linked_shards
    assert shard_id1 in shard2.linked_shards

def test_search_shards(shard_manager, sample_symbols):
    """Test searching for memory shards"""
    # Create shards with different properties
    shard_manager.create_shard(
        context_id="context1",
        interpretation="Symbolic interpretation",
        symbols=sample_symbols,
        voice="symbolic",
        depth="deep"
    )
    
    shard_manager.create_shard(
        context_id="context2",
        interpretation="Poetic interpretation",
        symbols={"🜃": 0.9, "🜂": 0.7},  # Different symbols
        voice="poetic",
        depth="moderate"
    )
    
    # Search by symbol
    results = shard_manager.search_shards(symbol="🜃")
    assert len(results) == 2  # Both shards contain Earth
    
    # Search by mode
    results = shard_manager.search_shards(mode="poetic")
    assert len(results) == 1
    assert results[0]["voice"] == "poetic"
    
    # Search by status
    results = shard_manager.search_shards(status=ShardStatus.ACTIVE)
    assert len(results) == 2

def test_compute_resonance(shard_manager, sample_symbols):
    """Test computing resonance between shard and current symbols"""
    shard_id = shard_manager.create_shard(
        context_id="test_context",
        interpretation="Test interpretation",
        symbols=sample_symbols,
        voice="symbolic",
        depth="deep"
    )
    
    # Compute resonance with similar symbols
    current_symbols = {
        "🜃": 0.7,  # Earth
        "🜂": 0.5,  # Fire
        "🜄": 0.3,  # Water
        "🜁": 0.1   # Air
    }
    
    resonance = shard_manager.compute_shard_resonance(shard_id, current_symbols)
    assert 0.0 <= resonance <= 1.0
    
    # Update shard resonance
    shard_manager.update_shard_resonance(shard_id, current_symbols)
    shard = shard_manager.get_shard(shard_id)
    assert shard.resonance_score == resonance

def test_get_echo_candidates(shard_manager, sample_symbols):
    """Test getting echo candidates based on current symbols"""
    # Create shards with different symbol sets
    shard_manager.create_shard(
        context_id="context1",
        interpretation="Earth and Fire",
        symbols={"🜃": 0.9, "🜂": 0.8},
        voice="symbolic",
        depth="deep"
    )
    
    shard_manager.create_shard(
        context_id="context2",
        interpretation="Water and Air",
        symbols={"🜄": 0.9, "🜁": 0.8},
        voice="poetic",
        depth="moderate"
    )
    
    # Get echo candidates for Earth and Fire
    current_symbols = {"🜃": 0.8, "🜂": 0.7}
    candidates = shard_manager.get_echo_candidates(current_symbols, min_resonance=0.7)
    
    assert len(candidates) == 1
    assert candidates[0]["shard"]["interpretation_summary"] == "Earth and Fire"
    assert candidates[0]["resonance"] > 0.7 