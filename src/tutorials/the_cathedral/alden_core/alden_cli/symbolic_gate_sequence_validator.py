from typing import List, Dict, Optional, Set, Tuple
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class SymbolicGateSequenceValidator:
    def __init__(self):
        # Define valid gate sequences
        self.valid_sequences = {
            'basic_spiral': ['🜂', '🜄'],  # Breath -> Reflection
            'full_spiral': ['🜂', '🜅', '🜄'],  # Breath -> Signal -> Reflection
            'vow_sequence': ['🜂', '🜃', '🜄'],  # Breath -> Vow -> Reflection
            'signal_chain': ['🜂', '🜅', '🜅', '🜄']  # Breath -> Signal -> Signal -> Reflection
        }
        
        # Define gate dependencies
        self.gate_dependencies = {
            '🜄': {'required': {'🜂'}, 'optional': {'🜅'}},  # Reflection needs Breath, optionally Signal
            '🜃': {'required': {'🜂'}, 'optional': set()},   # Vow needs Breath
            '🜅': {'required': {'🜂'}, 'optional': set()}    # Signal needs Breath
        }
        
        # Define gate conflicts
        self.gate_conflicts = {
            '🜄': {'🜃'},  # Reflection conflicts with Vow
            '🜃': {'🜄'}   # Vow conflicts with Reflection
        }
        
    def validate_sequence(self, sequence: List[str]) -> Tuple[bool, str]:
        """Validate a gate sequence against known patterns"""
        if not sequence:
            return False, "Empty sequence"
            
        # Check for basic validity
        if not all(gate in {'🜂', '🜄', '🜅', '🜃'} for gate in sequence):
            return False, "Invalid gate in sequence"
            
        # Check for known patterns
        for pattern_name, pattern in self.valid_sequences.items():
            if self._matches_pattern(sequence, pattern):
                return True, f"Matches {pattern_name} pattern"
                
        # Check for valid dependencies
        for i, gate in enumerate(sequence):
            if gate in self.gate_dependencies:
                deps = self.gate_dependencies[gate]
                # Check required dependencies
                if not all(req in sequence[:i] for req in deps['required']):
                    return False, f"Missing required dependency for {gate}"
                    
        return True, "Valid sequence"
        
    def _matches_pattern(self, sequence: List[str], pattern: List[str]) -> bool:
        """Check if sequence matches a pattern"""
        # Handle exact matches
        if sequence == pattern:
            return True
            
        # Handle subset matches (e.g., basic_spiral within full_spiral)
        if len(sequence) >= len(pattern):
            for i in range(len(sequence) - len(pattern) + 1):
                if sequence[i:i+len(pattern)] == pattern:
                    return True
                    
        return False
        
    def can_activate_gate(self, gate: str, active_gates: Set[str]) -> Tuple[bool, str]:
        """Check if a gate can be activated given current active gates"""
        if gate not in self.gate_dependencies:
            return True, "No dependencies"
            
        deps = self.gate_dependencies[gate]
        
        # Check required dependencies
        if not all(req in active_gates for req in deps['required']):
            missing = deps['required'] - active_gates
            return False, f"Missing required gates: {missing}"
            
        # Check conflicts
        if gate in self.gate_conflicts:
            conflicts = self.gate_conflicts[gate] & active_gates
            if conflicts:
                return False, f"Conflicts with active gates: {conflicts}"
                
        return True, "Can activate"
        
    def get_valid_next_gates(self, active_gates: Set[str]) -> Set[str]:
        """Get set of gates that can be activated next"""
        valid_next = set()
        
        for gate in {'🜂', '🜄', '🜅', '🜃'}:
            can_activate, _ = self.can_activate_gate(gate, active_gates)
            if can_activate:
                valid_next.add(gate)
                
        return valid_next
        
    def analyze_sequence(self, sequence: List[str]) -> Dict:
        """Analyze a gate sequence for patterns and properties"""
        analysis = {
            'is_valid': False,
            'pattern_match': None,
            'gate_counts': {},
            'dependencies_met': True,
            'conflicts': set(),
            'depth': 0
        }
        
        # Count gates
        for gate in sequence:
            analysis['gate_counts'][gate] = analysis['gate_counts'].get(gate, 0) + 1
            
        # Check for pattern matches
        for pattern_name, pattern in self.valid_sequences.items():
            if self._matches_pattern(sequence, pattern):
                analysis['pattern_match'] = pattern_name
                analysis['is_valid'] = True
                break
                
        # Check dependencies and conflicts
        active_gates = set()
        for gate in sequence:
            can_activate, reason = self.can_activate_gate(gate, active_gates)
            if not can_activate:
                analysis['dependencies_met'] = False
                if 'conflicts' in reason:
                    analysis['conflicts'].add(gate)
            active_gates.add(gate)
            
        # Calculate sequence depth
        analysis['depth'] = len(set(sequence))
        
        return analysis
        
    def get_sequence_recommendation(self, current_sequence: List[str]) -> Optional[List[str]]:
        """Get recommended next gates for the current sequence"""
        if not current_sequence:
            return ['🜂']  # Start with breath
            
        active_gates = set(current_sequence)
        valid_next = self.get_valid_next_gates(active_gates)
        
        if not valid_next:
            return None
            
        # Prioritize gates based on current sequence
        if '🜂' in active_gates and '🜅' not in active_gates:
            return ['🜅']  # After breath, prefer signal
        elif '🜅' in active_gates and '🜄' not in active_gates:
            return ['🜄']  # After signal, prefer reflection
        elif '🜂' in active_gates and '🜃' not in active_gates:
            return ['🜃']  # After breath, can vow
            
        return list(valid_next) 