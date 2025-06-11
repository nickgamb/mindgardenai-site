"""
Interpretation System

This package contains the core interpretation system components:
- Engine: Main interpretation engine
- Modes: Interpretation modes and contexts
"""

from .engine import RecursiveInterpreter
from .modes import InterpretationMode, InterpretationContext

__all__ = [
    'RecursiveInterpreter',
    'InterpretationMode',
    'InterpretationContext'
] 