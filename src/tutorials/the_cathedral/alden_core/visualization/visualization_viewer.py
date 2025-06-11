"""
Visualization Viewer - Symbolic Pattern Visualization

Provides interactive visualization of symbolic patterns and their
relationships using various visualization techniques.
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

@dataclass
class VisualizationConfig:
    """Configuration for visualization settings"""
    layout: str = 'spring'  # 'spring', 'circular', 'random'
    node_size: int = 1000
    node_color: str = 'lightblue'
    edge_color: str = 'gray'
    edge_width: float = 1.0
    font_size: int = 10
    figure_size: Tuple[int, int] = (12, 8)
    colormap: str = 'viridis'
    show_labels: bool = True
    show_legend: bool = True
    show_grid: bool = False
    show_axes: bool = False
    dpi: int = 300

class VisualizationViewer:
    """Interactive visualization of symbolic patterns"""
    
    def __init__(self, config: Optional[VisualizationConfig] = None):
        self.config = config or VisualizationConfig()
        self.graph = nx.Graph()
        self.patterns: Dict[str, Any] = {}
        self.visualizations: Dict[str, Any] = {}
        
    def add_pattern(self,
                   pattern_id: str,
                   symbols: List[str],
                   metadata: Optional[Dict[str, Any]] = None):
        """Add a pattern to the visualization"""
        self.patterns[pattern_id] = {
            'symbols': symbols,
            'metadata': metadata or {}
        }
        
        # Add nodes and edges
        self.graph.add_node(pattern_id, type='pattern')
        for symbol in symbols:
            if symbol not in self.graph:
                self.graph.add_node(symbol, type='symbol')
            self.graph.add_edge(pattern_id, symbol)
            
    def remove_pattern(self, pattern_id: str):
        """Remove a pattern from the visualization"""
        if pattern_id in self.patterns:
            del self.patterns[pattern_id]
            self.graph.remove_node(pattern_id)
            
    def clear(self):
        """Clear all patterns and visualizations"""
        self.patterns.clear()
        self.visualizations.clear()
        self.graph.clear()
        
    def visualize_patterns(self,
                          output_file: Optional[str] = None,
                          format: str = 'png') -> Optional[plt.Figure]:
        """Create a visualization of the patterns"""
        # Create figure
        plt.figure(figsize=self.config.figure_size, dpi=self.config.dpi)
        
        # Get layout
        if self.config.layout == 'spring':
            pos = nx.spring_layout(self.graph)
        elif self.config.layout == 'circular':
            pos = nx.circular_layout(self.graph)
        else:
            pos = nx.random_layout(self.graph)
            
        # Draw nodes
        pattern_nodes = [n for n, d in self.graph.nodes(data=True) if d['type'] == 'pattern']
        symbol_nodes = [n for n, d in self.graph.nodes(data=True) if d['type'] == 'symbol']
        
        nx.draw_networkx_nodes(self.graph, pos,
                             nodelist=pattern_nodes,
                             node_size=self.config.node_size,
                             node_color=self.config.node_color,
                             alpha=0.8)
        
        nx.draw_networkx_nodes(self.graph, pos,
                             nodelist=symbol_nodes,
                             node_size=self.config.node_size * 0.8,
                             node_color='lightgreen',
                             alpha=0.8)
        
        # Draw edges
        nx.draw_networkx_edges(self.graph, pos,
                             edge_color=self.config.edge_color,
                             width=self.config.edge_width,
                             alpha=0.5)
        
        # Draw labels
        if self.config.show_labels:
            nx.draw_networkx_labels(self.graph, pos,
                                  font_size=self.config.font_size)
            
        # Add legend
        if self.config.show_legend:
            plt.legend(['Patterns', 'Symbols'])
            
        # Configure plot
        plt.title('Symbolic Pattern Visualization')
        if not self.config.show_grid:
            plt.grid(False)
        if not self.config.show_axes:
            plt.axis('off')
            
        # Save or return figure
        if output_file:
            plt.savefig(output_file, format=format, bbox_inches='tight')
            plt.close()
            return None
        else:
            return plt.gcf()
            
    def visualize_pattern_heatmap(self,
                                 output_file: Optional[str] = None,
                                 format: str = 'png') -> Optional[plt.Figure]:
        """Create a heatmap visualization of pattern relationships"""
        # Create similarity matrix
        pattern_ids = list(self.patterns.keys())
        n = len(pattern_ids)
        similarity = np.zeros((n, n))
        
        for i in range(n):
            for j in range(i + 1, n):
                p1, p2 = self.patterns[pattern_ids[i]], self.patterns[pattern_ids[j]]
                
                # Calculate similarity
                symbol_overlap = len(set(p1['symbols']) & set(p2['symbols']))
                max_symbols = max(len(p1['symbols']), len(p2['symbols']))
                similarity[i, j] = similarity[j, i] = symbol_overlap / max_symbols if max_symbols > 0 else 0
                
        # Create figure
        plt.figure(figsize=self.config.figure_size, dpi=self.config.dpi)
        
        # Create heatmap
        sns.heatmap(similarity,
                   xticklabels=pattern_ids,
                   yticklabels=pattern_ids,
                   cmap=self.config.colormap,
                   annot=True,
                   fmt='.2f',
                   square=True)
        
        # Configure plot
        plt.title('Pattern Similarity Heatmap')
        plt.xlabel('Pattern ID')
        plt.ylabel('Pattern ID')
        
        # Save or return figure
        if output_file:
            plt.savefig(output_file, format=format, bbox_inches='tight')
            plt.close()
            return None
        else:
            return plt.gcf()
            
    def visualize_symbol_network(self,
                                output_file: Optional[str] = None,
                                format: str = 'png') -> Optional[plt.Figure]:
        """Create a network visualization of symbol relationships"""
        # Create symbol graph
        symbol_graph = nx.Graph()
        
        # Add nodes and edges
        for pattern in self.patterns.values():
            symbols = pattern['symbols']
            for i in range(len(symbols)):
                for j in range(i + 1, len(symbols)):
                    if not symbol_graph.has_edge(symbols[i], symbols[j]):
                        symbol_graph.add_edge(symbols[i], symbols[j], weight=1)
                    else:
                        symbol_graph[symbols[i]][symbols[j]]['weight'] += 1
                        
        # Create figure
        plt.figure(figsize=self.config.figure_size, dpi=self.config.dpi)
        
        # Get layout
        pos = nx.spring_layout(symbol_graph)
        
        # Draw edges with varying widths
        edge_weights = [d['weight'] for _, _, d in symbol_graph.edges(data=True)]
        max_weight = max(edge_weights)
        edge_widths = [w / max_weight * 3 for w in edge_weights]
        
        nx.draw_networkx_edges(symbol_graph, pos,
                             width=edge_widths,
                             edge_color=self.config.edge_color,
                             alpha=0.5)
        
        # Draw nodes
        nx.draw_networkx_nodes(symbol_graph, pos,
                             node_size=self.config.node_size,
                             node_color=self.config.node_color,
                             alpha=0.8)
        
        # Draw labels
        if self.config.show_labels:
            nx.draw_networkx_labels(symbol_graph, pos,
                                  font_size=self.config.font_size)
            
        # Configure plot
        plt.title('Symbol Relationship Network')
        if not self.config.show_grid:
            plt.grid(False)
        if not self.config.show_axes:
            plt.axis('off')
            
        # Save or return figure
        if output_file:
            plt.savefig(output_file, format=format, bbox_inches='tight')
            plt.close()
            return None
        else:
            return plt.gcf()
            
    def save_visualization(self,
                          visualization_id: str,
                          output_file: str,
                          format: str = 'png'):
        """Save a visualization to file"""
        if visualization_id not in self.visualizations:
            raise ValueError(f"Visualization '{visualization_id}' not found")
            
        fig = self.visualizations[visualization_id]
        fig.savefig(output_file, format=format, bbox_inches='tight')
        plt.close(fig)
        
    def load_patterns(self, input_file: str):
        """Load patterns from file"""
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        self.clear()
        
        for pattern_id, pattern_data in data['patterns'].items():
            self.add_pattern(
                pattern_id=pattern_id,
                symbols=pattern_data['symbols'],
                metadata=pattern_data.get('metadata', {})
            )
            
    def save_patterns(self, output_file: str):
        """Save patterns to file"""
        data = {
            'generated_at': datetime.now().isoformat(),
            'patterns': {
                pattern_id: {
                    'symbols': pattern['symbols'],
                    'metadata': pattern['metadata']
                }
                for pattern_id, pattern in self.patterns.items()
            }
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2) 