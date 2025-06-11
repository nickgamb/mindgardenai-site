"""
Trace Diff - Symbolic Trace Comparison

Compares and visualizes differences between symbolic traces,
highlighting changes in patterns, sequences, and relationships.
"""

from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass
from pathlib import Path
import json
from datetime import datetime
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns
from difflib import SequenceMatcher

@dataclass
class TraceDiff:
    """Represents differences between two traces"""
    added_patterns: List[str]
    removed_patterns: List[str]
    modified_patterns: List[Tuple[str, str, float]]  # (pattern_id, change_type, similarity)
    sequence_changes: List[Tuple[int, int, str]]  # (position, length, change_type)
    relationship_changes: List[Tuple[str, str, str]]  # (source, target, change_type)

class TraceDiffVisualizer:
    """Visualizes differences between symbolic traces"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.trace1: Dict[str, Any] = {}
        self.trace2: Dict[str, Any] = {}
        self.diff: Optional[TraceDiff] = None
        
    def load_traces(self, trace1_file: str, trace2_file: str):
        """Load two traces for comparison"""
        with open(trace1_file, 'r', encoding='utf-8') as f:
            self.trace1 = json.load(f)
            
        with open(trace2_file, 'r', encoding='utf-8') as f:
            self.trace2 = json.load(f)
            
    def compute_diff(self) -> TraceDiff:
        """Compute differences between traces"""
        # Compare patterns
        patterns1 = set(self.trace1['patterns'].keys())
        patterns2 = set(self.trace2['patterns'].keys())
        
        added_patterns = list(patterns2 - patterns1)
        removed_patterns = list(patterns1 - patterns2)
        
        # Compare modified patterns
        modified_patterns = []
        common_patterns = patterns1 & patterns2
        
        for pattern_id in common_patterns:
            p1 = self.trace1['patterns'][pattern_id]
            p2 = self.trace2['patterns'][pattern_id]
            
            # Compute similarity
            similarity = self._compute_pattern_similarity(p1, p2)
            
            if similarity < 1.0:
                change_type = 'modified'
                modified_patterns.append((pattern_id, change_type, similarity))
                
        # Compare sequences
        sequence_changes = self._compute_sequence_changes(
            self.trace1['sequence'],
            self.trace2['sequence']
        )
        
        # Compare relationships
        relationship_changes = self._compute_relationship_changes(
            self.trace1['relationships'],
            self.trace2['relationships']
        )
        
        self.diff = TraceDiff(
            added_patterns=added_patterns,
            removed_patterns=removed_patterns,
            modified_patterns=modified_patterns,
            sequence_changes=sequence_changes,
            relationship_changes=relationship_changes
        )
        
        return self.diff
        
    def _compute_pattern_similarity(self, pattern1: Dict[str, Any], pattern2: Dict[str, Any]) -> float:
        """Compute similarity between two patterns"""
        # Compare symbols
        symbols1 = set(pattern1['symbols'])
        symbols2 = set(pattern2['symbols'])
        
        symbol_similarity = len(symbols1 & symbols2) / len(symbols1 | symbols2) if symbols1 | symbols2 else 1.0
        
        # Compare metadata
        metadata1 = pattern1.get('metadata', {})
        metadata2 = pattern2.get('metadata', {})
        
        metadata_keys = set(metadata1.keys()) | set(metadata2.keys())
        metadata_similarity = 0.0
        
        if metadata_keys:
            matches = sum(1 for k in metadata_keys
                         if k in metadata1 and k in metadata2
                         and metadata1[k] == metadata2[k])
            metadata_similarity = matches / len(metadata_keys)
            
        # Combined similarity
        return 0.7 * symbol_similarity + 0.3 * metadata_similarity
        
    def _compute_sequence_changes(self,
                                sequence1: List[str],
                                sequence2: List[str]) -> List[Tuple[int, int, str]]:
        """Compute changes between two sequences"""
        changes = []
        matcher = SequenceMatcher(None, sequence1, sequence2)
        
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag != 'equal':
                changes.append((i1, i2 - i1, tag))
                
        return changes
        
    def _compute_relationship_changes(self,
                                    rel1: Dict[str, List[str]],
                                    rel2: Dict[str, List[str]]) -> List[Tuple[str, str, str]]:
        """Compute changes between relationship sets"""
        changes = []
        
        # Compare relationships
        for source in set(rel1.keys()) | set(rel2.keys()):
            targets1 = set(rel1.get(source, []))
            targets2 = set(rel2.get(source, []))
            
            # Added relationships
            for target in targets2 - targets1:
                changes.append((source, target, 'added'))
                
            # Removed relationships
            for target in targets1 - targets2:
                changes.append((source, target, 'removed'))
                
        return changes
        
    def visualize_diff(self,
                      output_file: Optional[str] = None,
                      format: str = 'png') -> Optional[plt.Figure]:
        """Create a visualization of the differences"""
        if not self.diff:
            self.compute_diff()
            
        # Create figure with subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        # Plot pattern changes
        pattern_changes = {
            'Added': len(self.diff.added_patterns),
            'Removed': len(self.diff.removed_patterns),
            'Modified': len(self.diff.modified_patterns)
        }
        
        ax1.bar(pattern_changes.keys(), pattern_changes.values())
        ax1.set_title('Pattern Changes')
        ax1.set_ylabel('Count')
        
        # Plot sequence changes
        sequence_changes = {
            'Replace': sum(1 for _, _, t in self.diff.sequence_changes if t == 'replace'),
            'Delete': sum(1 for _, _, t in self.diff.sequence_changes if t == 'delete'),
            'Insert': sum(1 for _, _, t in self.diff.sequence_changes if t == 'insert')
        }
        
        ax2.bar(sequence_changes.keys(), sequence_changes.values())
        ax2.set_title('Sequence Changes')
        ax2.set_ylabel('Count')
        
        # Plot relationship changes
        relationship_changes = {
            'Added': sum(1 for _, _, t in self.diff.relationship_changes if t == 'added'),
            'Removed': sum(1 for _, _, t in self.diff.relationship_changes if t == 'removed')
        }
        
        ax3.bar(relationship_changes.keys(), relationship_changes.values())
        ax3.set_title('Relationship Changes')
        ax3.set_ylabel('Count')
        
        # Plot pattern similarity distribution
        similarities = [s for _, _, s in self.diff.modified_patterns]
        if similarities:
            ax4.hist(similarities, bins=10, range=(0, 1))
            ax4.set_title('Pattern Similarity Distribution')
            ax4.set_xlabel('Similarity')
            ax4.set_ylabel('Count')
            
        plt.tight_layout()
        
        # Save or return figure
        if output_file:
            plt.savefig(output_file, format=format, bbox_inches='tight')
            plt.close()
            return None
        else:
            return fig
            
    def visualize_sequence_diff(self,
                              output_file: Optional[str] = None,
                              format: str = 'png') -> Optional[plt.Figure]:
        """Create a visualization of sequence differences"""
        if not self.diff:
            self.compute_diff()
            
        # Create figure
        plt.figure(figsize=(15, 8))
        
        # Plot sequences
        sequence1 = self.trace1['sequence']
        sequence2 = self.trace2['sequence']
        
        # Create color map for changes
        colors = {'equal': 'lightgray',
                 'replace': 'red',
                 'delete': 'blue',
                 'insert': 'green'}
        
        # Plot sequence 1
        y1 = 0
        for i, symbol in enumerate(sequence1):
            color = colors['equal']
            for pos, length, change_type in self.diff.sequence_changes:
                if i >= pos and i < pos + length:
                    color = colors[change_type]
                    break
            plt.barh(y1, 1, color=color, alpha=0.5)
            plt.text(i, y1, symbol, ha='center', va='center')
            
        # Plot sequence 2
        y2 = 1
        for i, symbol in enumerate(sequence2):
            color = colors['equal']
            for pos, length, change_type in self.diff.sequence_changes:
                if i >= pos and i < pos + length:
                    color = colors[change_type]
                    break
            plt.barh(y2, 1, color=color, alpha=0.5)
            plt.text(i, y2, symbol, ha='center', va='center')
            
        # Configure plot
        plt.title('Sequence Differences')
        plt.yticks([0, 1], ['Trace 1', 'Trace 2'])
        plt.legend([plt.Rectangle((0, 0), 1, 1, color=c) for c in colors.values()],
                  colors.keys())
        
        # Save or return figure
        if output_file:
            plt.savefig(output_file, format=format, bbox_inches='tight')
            plt.close()
            return None
        else:
            return plt.gcf()
            
    def visualize_relationship_diff(self,
                                  output_file: Optional[str] = None,
                                  format: str = 'png') -> Optional[plt.Figure]:
        """Create a visualization of relationship differences"""
        if not self.diff:
            self.compute_diff()
            
        # Create figure
        plt.figure(figsize=(12, 8))
        
        # Create graph
        G = nx.DiGraph()
        
        # Add nodes
        nodes = set()
        for source, target, _ in self.diff.relationship_changes:
            nodes.add(source)
            nodes.add(target)
            
        G.add_nodes_from(nodes)
        
        # Add edges with attributes
        for source, target, change_type in self.diff.relationship_changes:
            G.add_edge(source, target, change_type=change_type)
            
        # Get layout
        pos = nx.spring_layout(G)
        
        # Draw nodes
        nx.draw_networkx_nodes(G, pos,
                             node_size=1000,
                             node_color='lightblue',
                             alpha=0.8)
        
        # Draw edges with different colors
        edge_colors = {'added': 'green', 'removed': 'red'}
        for change_type in edge_colors:
            edges = [(u, v) for u, v, d in G.edges(data=True)
                    if d['change_type'] == change_type]
            nx.draw_networkx_edges(G, pos,
                                 edgelist=edges,
                                 edge_color=edge_colors[change_type],
                                 width=2,
                                 alpha=0.8)
            
        # Draw labels
        nx.draw_networkx_labels(G, pos)
        
        # Add legend
        plt.legend([plt.Line2D([0], [0], color=c) for c in edge_colors.values()],
                  edge_colors.keys())
        
        # Configure plot
        plt.title('Relationship Changes')
        plt.axis('off')
        
        # Save or return figure
        if output_file:
            plt.savefig(output_file, format=format, bbox_inches='tight')
            plt.close()
            return None
        else:
            return plt.gcf()
            
    def save_diff(self, output_file: str):
        """Save diff results to file"""
        if not self.diff:
            self.compute_diff()
            
        data = {
            'generated_at': datetime.now().isoformat(),
            'trace1_id': self.trace1.get('trace_id', 'unknown'),
            'trace2_id': self.trace2.get('trace_id', 'unknown'),
            'added_patterns': self.diff.added_patterns,
            'removed_patterns': self.diff.removed_patterns,
            'modified_patterns': [
                {
                    'pattern_id': p[0],
                    'change_type': p[1],
                    'similarity': p[2]
                }
                for p in self.diff.modified_patterns
            ],
            'sequence_changes': [
                {
                    'position': c[0],
                    'length': c[1],
                    'change_type': c[2]
                }
                for c in self.diff.sequence_changes
            ],
            'relationship_changes': [
                {
                    'source': c[0],
                    'target': c[1],
                    'change_type': c[2]
                }
                for c in self.diff.relationship_changes
            ]
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2) 