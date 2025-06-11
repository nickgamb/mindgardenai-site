"""
Interpretation Modes and Contexts

This module defines the available interpretation modes and their associated contexts
for the Alden interpretation system.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, Optional

class InterpretationMode(Enum):
    """Available interpretation modes"""
    ANALYTIC = "analytic"  # Logical analysis and pattern detection
    SYMBOLIC = "symbolic"  # Symbolic resonance and archetypal mapping
    POETIC = "poetic"      # Metaphorical and narrative interpretation
    ORACULAR = "oracular"  # Prophetic and visionary insights
    MIRROR = "mirror"      # Reflective and recursive interpretation

@dataclass
class InterpretationContext:
    """Context for interpretation including mode and parameters"""
    mode: InterpretationMode
    depth: int = 1  # Interpretation depth (1-3)
    include_shadows: bool = True  # Whether to include shadow forecasts
    echo_threshold: float = 0.7  # Minimum resonance for echo detection
    symbolic_memory: Optional[Dict] = None  # Current symbolic memory state

__all__ = ['InterpretationMode', 'InterpretationContext'] 