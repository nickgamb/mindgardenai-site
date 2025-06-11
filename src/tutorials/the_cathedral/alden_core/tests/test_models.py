"""
Test Models - Unit Tests for Core Models

Tests the core models and their functionality.
"""

import unittest
from typing import Dict, List, Any
import json
from pathlib import Path
import os
import tempfile
import shutil

from alden_core.models import (
    SymbolicPattern,
    SymbolicSequence,
    SymbolicRelationship,
    SymbolicContext,
    SymbolicTrace
)

class TestSymbolicPattern(unittest.TestCase):
    """Test cases for SymbolicPattern"""
    
    def setUp(self):
        self.pattern = SymbolicPattern(
            pattern_id="test_pattern",
            symbols=["symbol1", "symbol2"],
            frequency=2,
            confidence=0.8,
            context=SymbolicContext(
                context_id="test_context",
                description="Test context"
            )
        )
        
    def test_pattern_creation(self):
        """Test pattern creation"""
        self.assertEqual(self.pattern.pattern_id, "test_pattern")
        self.assertEqual(self.pattern.symbols, ["symbol1", "symbol2"])
        self.assertEqual(self.pattern.frequency, 2)
        self.assertEqual(self.pattern.confidence, 0.8)
        self.assertEqual(self.pattern.context.context_id, "test_context")
        
    def test_pattern_to_dict(self):
        """Test pattern to dictionary conversion"""
        pattern_dict = self.pattern.to_dict()
        self.assertEqual(pattern_dict["pattern_id"], "test_pattern")
        self.assertEqual(pattern_dict["symbols"], ["symbol1", "symbol2"])
        self.assertEqual(pattern_dict["frequency"], 2)
        self.assertEqual(pattern_dict["confidence"], 0.8)
        self.assertEqual(pattern_dict["context"]["context_id"], "test_context")
        
    def test_pattern_from_dict(self):
        """Test pattern creation from dictionary"""
        pattern_dict = {
            "pattern_id": "test_pattern",
            "symbols": ["symbol1", "symbol2"],
            "frequency": 2,
            "confidence": 0.8,
            "context": {
                "context_id": "test_context",
                "description": "Test context"
            }
        }
        pattern = SymbolicPattern.from_dict(pattern_dict)
        self.assertEqual(pattern.pattern_id, "test_pattern")
        self.assertEqual(pattern.symbols, ["symbol1", "symbol2"])
        self.assertEqual(pattern.frequency, 2)
        self.assertEqual(pattern.confidence, 0.8)
        self.assertEqual(pattern.context.context_id, "test_context")

class TestSymbolicSequence(unittest.TestCase):
    """Test cases for SymbolicSequence"""
    
    def setUp(self):
        self.sequence = SymbolicSequence(
            sequence_id="test_sequence",
            patterns=["pattern1", "pattern2"],
            order=["pattern1", "pattern2"],
            frequency=2,
            confidence=0.8,
            context=SymbolicContext(
                context_id="test_context",
                description="Test context"
            )
        )
        
    def test_sequence_creation(self):
        """Test sequence creation"""
        self.assertEqual(self.sequence.sequence_id, "test_sequence")
        self.assertEqual(self.sequence.patterns, ["pattern1", "pattern2"])
        self.assertEqual(self.sequence.order, ["pattern1", "pattern2"])
        self.assertEqual(self.sequence.frequency, 2)
        self.assertEqual(self.sequence.confidence, 0.8)
        self.assertEqual(self.sequence.context.context_id, "test_context")
        
    def test_sequence_to_dict(self):
        """Test sequence to dictionary conversion"""
        sequence_dict = self.sequence.to_dict()
        self.assertEqual(sequence_dict["sequence_id"], "test_sequence")
        self.assertEqual(sequence_dict["patterns"], ["pattern1", "pattern2"])
        self.assertEqual(sequence_dict["order"], ["pattern1", "pattern2"])
        self.assertEqual(sequence_dict["frequency"], 2)
        self.assertEqual(sequence_dict["confidence"], 0.8)
        self.assertEqual(sequence_dict["context"]["context_id"], "test_context")
        
    def test_sequence_from_dict(self):
        """Test sequence creation from dictionary"""
        sequence_dict = {
            "sequence_id": "test_sequence",
            "patterns": ["pattern1", "pattern2"],
            "order": ["pattern1", "pattern2"],
            "frequency": 2,
            "confidence": 0.8,
            "context": {
                "context_id": "test_context",
                "description": "Test context"
            }
        }
        sequence = SymbolicSequence.from_dict(sequence_dict)
        self.assertEqual(sequence.sequence_id, "test_sequence")
        self.assertEqual(sequence.patterns, ["pattern1", "pattern2"])
        self.assertEqual(sequence.order, ["pattern1", "pattern2"])
        self.assertEqual(sequence.frequency, 2)
        self.assertEqual(sequence.confidence, 0.8)
        self.assertEqual(sequence.context.context_id, "test_context")

class TestSymbolicRelationship(unittest.TestCase):
    """Test cases for SymbolicRelationship"""
    
    def setUp(self):
        self.relationship = SymbolicRelationship(
            relationship_id="test_relationship",
            source="pattern1",
            target="pattern2",
            relationship_type="causes",
            strength=0.8,
            confidence=0.8,
            context=SymbolicContext(
                context_id="test_context",
                description="Test context"
            )
        )
        
    def test_relationship_creation(self):
        """Test relationship creation"""
        self.assertEqual(self.relationship.relationship_id, "test_relationship")
        self.assertEqual(self.relationship.source, "pattern1")
        self.assertEqual(self.relationship.target, "pattern2")
        self.assertEqual(self.relationship.relationship_type, "causes")
        self.assertEqual(self.relationship.strength, 0.8)
        self.assertEqual(self.relationship.confidence, 0.8)
        self.assertEqual(self.relationship.context.context_id, "test_context")
        
    def test_relationship_to_dict(self):
        """Test relationship to dictionary conversion"""
        relationship_dict = self.relationship.to_dict()
        self.assertEqual(relationship_dict["relationship_id"], "test_relationship")
        self.assertEqual(relationship_dict["source"], "pattern1")
        self.assertEqual(relationship_dict["target"], "pattern2")
        self.assertEqual(relationship_dict["relationship_type"], "causes")
        self.assertEqual(relationship_dict["strength"], 0.8)
        self.assertEqual(relationship_dict["confidence"], 0.8)
        self.assertEqual(relationship_dict["context"]["context_id"], "test_context")
        
    def test_relationship_from_dict(self):
        """Test relationship creation from dictionary"""
        relationship_dict = {
            "relationship_id": "test_relationship",
            "source": "pattern1",
            "target": "pattern2",
            "relationship_type": "causes",
            "strength": 0.8,
            "confidence": 0.8,
            "context": {
                "context_id": "test_context",
                "description": "Test context"
            }
        }
        relationship = SymbolicRelationship.from_dict(relationship_dict)
        self.assertEqual(relationship.relationship_id, "test_relationship")
        self.assertEqual(relationship.source, "pattern1")
        self.assertEqual(relationship.target, "pattern2")
        self.assertEqual(relationship.relationship_type, "causes")
        self.assertEqual(relationship.strength, 0.8)
        self.assertEqual(relationship.confidence, 0.8)
        self.assertEqual(relationship.context.context_id, "test_context")

class TestSymbolicTrace(unittest.TestCase):
    """Test cases for SymbolicTrace"""
    
    def setUp(self):
        self.trace = SymbolicTrace(
            trace_id="test_trace",
            patterns={
                "pattern1": SymbolicPattern(
                    pattern_id="pattern1",
                    symbols=["symbol1"],
                    frequency=1,
                    confidence=0.8,
                    context=SymbolicContext(
                        context_id="test_context",
                        description="Test context"
                    )
                )
            },
            sequences={
                "sequence1": SymbolicSequence(
                    sequence_id="sequence1",
                    patterns=["pattern1"],
                    order=["pattern1"],
                    frequency=1,
                    confidence=0.8,
                    context=SymbolicContext(
                        context_id="test_context",
                        description="Test context"
                    )
                )
            },
            relationships={
                "relationship1": SymbolicRelationship(
                    relationship_id="relationship1",
                    source="pattern1",
                    target="pattern1",
                    relationship_type="self",
                    strength=1.0,
                    confidence=1.0,
                    context=SymbolicContext(
                        context_id="test_context",
                        description="Test context"
                    )
                )
            },
            context=SymbolicContext(
                context_id="test_context",
                description="Test context"
            )
        )
        
    def test_trace_creation(self):
        """Test trace creation"""
        self.assertEqual(self.trace.trace_id, "test_trace")
        self.assertEqual(len(self.trace.patterns), 1)
        self.assertEqual(len(self.trace.sequences), 1)
        self.assertEqual(len(self.trace.relationships), 1)
        self.assertEqual(self.trace.context.context_id, "test_context")
        
    def test_trace_to_dict(self):
        """Test trace to dictionary conversion"""
        trace_dict = self.trace.to_dict()
        self.assertEqual(trace_dict["trace_id"], "test_trace")
        self.assertEqual(len(trace_dict["patterns"]), 1)
        self.assertEqual(len(trace_dict["sequences"]), 1)
        self.assertEqual(len(trace_dict["relationships"]), 1)
        self.assertEqual(trace_dict["context"]["context_id"], "test_context")
        
    def test_trace_from_dict(self):
        """Test trace creation from dictionary"""
        trace_dict = {
            "trace_id": "test_trace",
            "patterns": {
                "pattern1": {
                    "pattern_id": "pattern1",
                    "symbols": ["symbol1"],
                    "frequency": 1,
                    "confidence": 0.8,
                    "context": {
                        "context_id": "test_context",
                        "description": "Test context"
                    }
                }
            },
            "sequences": {
                "sequence1": {
                    "sequence_id": "sequence1",
                    "patterns": ["pattern1"],
                    "order": ["pattern1"],
                    "frequency": 1,
                    "confidence": 0.8,
                    "context": {
                        "context_id": "test_context",
                        "description": "Test context"
                    }
                }
            },
            "relationships": {
                "relationship1": {
                    "relationship_id": "relationship1",
                    "source": "pattern1",
                    "target": "pattern1",
                    "relationship_type": "self",
                    "strength": 1.0,
                    "confidence": 1.0,
                    "context": {
                        "context_id": "test_context",
                        "description": "Test context"
                    }
                }
            },
            "context": {
                "context_id": "test_context",
                "description": "Test context"
            }
        }
        trace = SymbolicTrace.from_dict(trace_dict)
        self.assertEqual(trace.trace_id, "test_trace")
        self.assertEqual(len(trace.patterns), 1)
        self.assertEqual(len(trace.sequences), 1)
        self.assertEqual(len(trace.relationships), 1)
        self.assertEqual(trace.context.context_id, "test_context")
        
    def test_trace_save_load(self):
        """Test trace save and load"""
        # Create temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save trace
            trace_file = os.path.join(temp_dir, "test_trace.json")
            self.trace.save(trace_file)
            
            # Load trace
            loaded_trace = SymbolicTrace.load(trace_file)
            
            # Verify loaded trace
            self.assertEqual(loaded_trace.trace_id, "test_trace")
            self.assertEqual(len(loaded_trace.patterns), 1)
            self.assertEqual(len(loaded_trace.sequences), 1)
            self.assertEqual(len(loaded_trace.relationships), 1)
            self.assertEqual(loaded_trace.context.context_id, "test_context")

if __name__ == '__main__':
    unittest.main() 