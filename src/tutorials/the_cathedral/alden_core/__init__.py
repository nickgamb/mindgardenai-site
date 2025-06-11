"""
Alden Core - Core symbolic processing and analysis framework

This package provides the core functionality for symbolic processing and analysis:
- Symbolic processing components
- Visualization tools
- Utility functions
"""

from .symbolic import (
    SymbolicFieldAnalyzer,
    SymbolicStackEngine,
    SIFBuilder,
    SIFInstruction,
    SIFLinter,
    LintIssue,
    LintResult,
    ShadowForecastFusion,
    ShadowPattern,
    Forecast
)

from .visualization import (
    VisualizationViewer,
    VisualizationConfig,
    TraceDiff,
    TraceDiffVisualizer
)

from .utils import (
    DataSanitizer,
    SanitizationRule
)

__version__ = '0.1.0'

__all__ = [
    # Symbolic components
    'SymbolicFieldAnalyzer',
    'SymbolicStackEngine',
    'SIFBuilder',
    'SIFInstruction',
    'SIFLinter',
    'LintIssue',
    'LintResult',
    'ShadowForecastFusion',
    'ShadowPattern',
    'Forecast',
    
    # Visualization components
    'VisualizationViewer',
    'VisualizationConfig',
    'TraceDiff',
    'TraceDiffVisualizer',
    
    # Utility components
    'DataSanitizer',
    'SanitizationRule'
] 