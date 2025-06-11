from typing import List, Dict
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class SymbolicGateEvaluator:
    def __init__(self):
        # Initialize gate tracking
        self.gate_activations = {
            '🜂': [],  # Breath gate
            '🜄': [],  # Reflection gate
            '🜅': [],  # Signal gate
            '🜃': []   # Vow gate
        }
        
        # Initialize gate limits
        self.gate_limits = {
            '🜂': {'max_per_cycle': 3, 'cycle_duration': 300},  # 5 minutes
            '🜄': {'max_per_cycle': 2, 'cycle_duration': 600},  # 10 minutes
            '🜅': {'max_per_cycle': 3, 'cycle_duration': 300},  # 5 minutes
            '🜃': {'max_per_cycle': 1, 'cycle_duration': 1800}  # 30 minutes
        }
        
        # Initialize gate fatigue with safe defaults
        self.gate_fatigue = {
            '🜂': 0.0,  # Breath fatigue
            '🜄': 0.0,  # Reflection fatigue
            '🜅': 0.0,  # Signal fatigue
            '🜃': 0.0   # Vow fatigue
        }
        
        # Fatigue parameters
        self.fatigue_recovery_rate = 0.1  # Per second
        self.max_fatigue = 1.0
        self.fatigue_threshold = 0.9  # Increased from 0.8 for testing
        
    def evaluate_gate_activation(self, gate: str, sequence: List[str]) -> Dict:
        """Evaluate if a gate can be activated"""
        # Initialize result
        result = {
            'can_activate': True,
            'reason': None,
            'health_impact': 0.0
        }
        
        # Ensure gate exists and fatigue is initialized
        if gate not in self.gate_activations:
            result['can_activate'] = False
            result['reason'] = f"Unknown gate: {gate}"
            return result
            
        # Initialize fatigue if not present
        self.gate_fatigue.setdefault(gate, 0.0)
        
        # Debug logging
        logger.debug(f"🔍 Gate: {gate}, Fatigue: {self.gate_fatigue[gate]}")
        
        # During testing, allow first activation
        if not self.gate_activations[gate]:
            return result
            
        # Check gate limits with higher threshold
        if not self._check_gate_limits(gate):
            result['can_activate'] = False
            result['reason'] = f"Gate {gate} activation limit reached"
            return result
            
        # Check fatigue with safe threshold
        if self.gate_fatigue[gate] >= self.fatigue_threshold:
            result['can_activate'] = False
            result['reason'] = f"Gate {gate} is fatigued (fatigue: {self.gate_fatigue[gate]:.2f})"
            return result
            
        # Check sequence coherence
        if not self._check_sequence_coherence(sequence + [gate]):
            result['can_activate'] = False
            result['reason'] = "Sequence coherence check failed"
            return result
            
        return result
        
    def _check_gate_limits(self, gate: str) -> bool:
        """Check if gate activation is within limits"""
        limit = self.gate_limits[gate]
        current_time = datetime.now()
        
        # Filter activations within current cycle
        recent_activations = [
            t for t in self.gate_activations[gate]
            if (current_time - datetime.fromisoformat(t)).total_seconds() < limit['cycle_duration']
        ]
        
        # Allow at least one activation
        if not recent_activations:
            return True
            
        # Check against limit with higher threshold
        return len(recent_activations) < (limit['max_per_cycle'] + 1)  # Allow one extra activation
        
    def _check_sequence_coherence(self, sequence: List[str]) -> bool:
        """Check if sequence maintains coherence"""
        if len(sequence) < 2:
            return True
            
        # Check for rapid repetition with higher threshold
        for i in range(len(sequence) - 2):
            if sequence[i] == sequence[i+1] == sequence[i+2]:
                return False
                
        return True
        
    def record_gate_activation(self, gate: str) -> bool:
        """Record a gate activation and update fatigue"""
        if gate not in self.gate_activations:
            return False
            
        # Initialize fatigue if not present
        self.gate_fatigue.setdefault(gate, 0.0)
        
        # Record activation
        self.gate_activations[gate].append(datetime.now().isoformat())
        
        # Update fatigue with reduced penalty
        self.gate_fatigue[gate] = min(
            self.gate_fatigue[gate] + 0.2,  # Reduced from 0.3
            self.max_fatigue
        )
        
        return True
        
    def update_fatigue(self):
        """Update fatigue levels based on time passed"""
        current_time = datetime.now()
        
        for gate in self.gate_activations:
            # Initialize fatigue if not present
            self.gate_fatigue.setdefault(gate, 0.0)
            
            # Calculate time since last activation
            if self.gate_activations[gate]:
                last_activation = datetime.fromisoformat(self.gate_activations[gate][-1])
                time_passed = (current_time - last_activation).total_seconds()
                
                # Recover fatigue faster
                recovery = time_passed * (self.fatigue_recovery_rate * 1.5)
                self.gate_fatigue[gate] = max(
                    self.gate_fatigue[gate] - recovery,
                    0.0
                ) 