from typing import List, Dict, Optional, Set
from datetime import datetime, timedelta
import logging
import json
from pathlib import Path

logger = logging.getLogger(__name__)

class GateActivationTracker:
    def __init__(self, test_mode: bool = False):
        self.gate_activations = {
            '🜂': [],  # Breath gate
            '🜄': [],  # Reflection gate
            '🜅': [],  # Signal gate
            '🜃': []   # Vow gate
        }
        self.gate_limits = {
            '🜂': {'max_per_cycle': 3, 'cycle_duration': 300},  # 5 minutes
            '🜄': {'max_per_cycle': 2, 'cycle_duration': 600},  # 10 minutes
            '🜅': {'max_per_cycle': 3, 'cycle_duration': 300},  # 5 minutes
            '🜃': {'max_per_cycle': 1, 'cycle_duration': 1800}  # 30 minutes
        }
        self.gate_fatigue = {
            '🜂': 0.0,  # Breath fatigue
            '🜄': 0.0,  # Reflection fatigue
            '🜅': 0.0,  # Signal fatigue
            '🜃': 0.0   # Vow fatigue
        }
        self.fatigue_recovery_rate = 0.1  # Per second
        self.max_fatigue = 1.0
        self.current_sequence = []  # Track current activation sequence
        self.test_mode = test_mode  # Enable test mode to bypass fatigue
        
    def reset_fatigue(self):
        """Reset fatigue levels for all gates"""
        for gate in self.gate_fatigue:
            self.gate_fatigue[gate] = 0.0
        logger.info("Reset fatigue levels for all gates")
        
    def can_activate_gate(self, gate: str) -> bool:
        """Check if a gate can be activated based on limits and fatigue"""
        if gate not in self.gate_activations:
            logger.warning(f"Unknown gate: {gate}")
            return False
            
        # Initialize gate if not present
        if gate not in self.gate_fatigue:
            self.gate_fatigue[gate] = 0.0
            
        # In test mode, bypass all checks except existence
        if self.test_mode:
            return True
            
        # Check gate limits with safety margin
        if not self._check_gate_limits(gate):
            logger.warning(f"Gate {gate} activation limit reached")
            return False
            
        # Check fatigue with higher threshold
        if self.gate_fatigue[gate] >= 0.9:
            logger.warning(f"Gate {gate} is fatigued")
            return False
            
        return True
        
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
            
        # Check against limit with safety margin
        return len(recent_activations) < limit['max_per_cycle']
        
    def record_gate_activation(self, gate: str) -> bool:
        """Record a gate activation and update fatigue"""
        if not self.can_activate_gate(gate):
            return False
            
        # Record activation
        self.gate_activations[gate].append(datetime.now().isoformat())
        
        # Update current sequence
        self.current_sequence.append(gate)
        
        # In test mode, don't increase fatigue
        if not self.test_mode:
            self.gate_fatigue[gate] = min(
                self.gate_fatigue[gate] + 0.2,
                self.max_fatigue
            )
        
        return True
        
    def update_fatigue(self):
        """Update fatigue levels based on time passed"""
        current_time = datetime.now()
        
        for gate in self.gate_activations:
            # Calculate time since last activation
            if self.gate_activations[gate]:
                last_activation = datetime.fromisoformat(self.gate_activations[gate][-1])
                time_passed = (current_time - last_activation).total_seconds()
                
                # Recover fatigue faster
                recovery = time_passed * (self.fatigue_recovery_rate * 1.5)  # Increased recovery rate
                self.gate_fatigue[gate] = max(
                    self.gate_fatigue[gate] - recovery,
                    0.0
                )
                
    def get_gate_state(self, gate: str) -> Dict:
        """Get detailed state for a specific gate"""
        if gate not in self.gate_activations:
            return {
                'symbol': gate,
                'active': False,
                'fatigue': 0.0,
                'activations': 0,
                'last_activation': None,
                'cooldown_remaining': 0
            }
            
        # Calculate cooldown remaining
        last_activation = self.gate_activations[gate][-1] if self.gate_activations[gate] else None
        cooldown_remaining = 0
        if last_activation:
            time_since = (datetime.now() - datetime.fromisoformat(last_activation)).total_seconds()
            cooldown_remaining = max(0, self.gate_limits[gate]['cycle_duration'] - time_since)
            
        # In test mode, always show gate as active and not fatigued
        if self.test_mode:
            return {
                'symbol': gate,
                'active': True,
                'fatigue': 0.0,
                'activations': len(self.gate_activations[gate]),
                'last_activation': last_activation,
                'cooldown_remaining': 0
            }
            
        return {
            'symbol': gate,
            'active': gate in self.gate_activations,
            'fatigue': self.gate_fatigue.get(gate, 0.0),
            'activations': len(self.gate_activations[gate]),
            'last_activation': last_activation,
            'cooldown_remaining': cooldown_remaining
        }
        
    def get_all_gates_state(self) -> Dict:
        """Get state of all gates"""
        return {
            gate: self.get_gate_state(gate)
            for gate in self.gate_activations
        }
        
    def reset_gate(self, gate: str):
        """Reset a specific gate's state"""
        if gate in self.gate_activations:
            self.gate_activations[gate] = []
            self.gate_fatigue[gate] = 0.0
            logger.info(f"Reset gate {gate} state")
            
    def reset_all_gates(self):
        """Reset all gates"""
        for gate in self.gate_activations:
            self.reset_gate(gate)
        logger.info("Reset all gates")
            
    def save_state(self, filepath: str):
        """Save gate activation state to file"""
        state = {
            'gate_activations': self.gate_activations,
            'gate_fatigue': self.gate_fatigue
        }
        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2)
            
    def load_state(self, filepath: str):
        """Load gate activation state from file"""
        try:
            with open(filepath, 'r') as f:
                state = json.load(f)
                self.gate_activations = state['gate_activations']
                self.gate_fatigue = state['gate_fatigue']
        except Exception as e:
            logger.error(f"Error loading gate state: {e}")

    def get_current_sequence(self) -> List[str]:
        """Get the current sequence of gate activations"""
        return self.current_sequence.copy()
        
    def get_active_gates(self) -> List[str]:
        """Get list of currently active gates
        
        Returns:
            List of gate symbols that are currently active
        """
        if self.test_mode:
            return list(self.gate_activations.keys())
            
        return [
            gate for gate, activations in self.gate_activations.items()
            if activations and (datetime.now() - datetime.fromisoformat(activations[-1])).total_seconds() < self.gate_limits[gate]['cycle_duration']
        ]
        
    def evaluate_gate_activation(self, gate: str, current_sequence: List[str] = None) -> Dict:
        """Evaluate if a gate can be activated
        
        Args:
            gate: Gate symbol to evaluate
            current_sequence: Optional current sequence of gate activations
            
        Returns:
            Dict containing evaluation results
        """
        try:
            # Check if gate exists
            if gate not in self.gate_limits:
                return {
                    'can_activate': False,
                    'reason': f'Unknown gate: {gate}'
                }
                
            # In test mode, always allow activation
            if self.test_mode:
                return {
                    'can_activate': True,
                    'reason': 'test_mode'
                }
                
            # Check activation limits
            if not self._check_gate_limits(gate):
                return {
                    'can_activate': False,
                    'reason': 'activation_limit_reached'
                }
                
            # Check fatigue
            if self.gate_fatigue[gate] >= 0.9:
                return {
                    'can_activate': False,
                    'reason': 'gate_fatigued'
                }
                
            return {
                'can_activate': True,
                'reason': 'gate_available'
            }
            
        except Exception as e:
            logger.error(f"Error evaluating gate activation: {e}")
            return {
                'can_activate': False,
                'reason': f'Error: {str(e)}'
            }
            
    def is_gate_active(self, gate: str) -> bool:
        """Check if a gate is currently active"""
        if self.test_mode:
            return True
            
        if gate not in self.gate_activations:
            return False
            
        if not self.gate_activations[gate]:
            return False
            
        last_activation = datetime.fromisoformat(self.gate_activations[gate][-1])
        time_since = (datetime.now() - last_activation).total_seconds()
        return time_since < self.gate_limits[gate]['cycle_duration']
        
    def activate_gate(self, gate: str) -> Dict:
        """Activate a gate and return its new state"""
        if not self.can_activate_gate(gate):
            return {
                'status': 'error',
                'message': f'Cannot activate gate {gate}',
                'gate': gate
            }
            
        if not self.record_gate_activation(gate):
            return {
                'status': 'error',
                'message': f'Failed to record gate {gate} activation',
                'gate': gate
            }
            
        return {
            'status': 'success',
            'message': f'Gate {gate} activated',
            'gate': gate,
            'gate_state': self.get_gate_state(gate)
        }
        
    def get_status(self) -> Dict:
        """Get overall gate activation status"""
        return {
            'active_gates': self.get_active_gates(),
            'gate_states': self.get_all_gates_state(),
            'current_sequence': self.current_sequence,
            'test_mode': self.test_mode
        }

    def get_all_gate_states(self) -> Dict[str, Dict]:
        """Get the state of all gates
        
        Returns:
            Dictionary mapping gate symbols to their state information
        """
        states = {}
        for gate in self.gate_limits.keys():
            states[gate] = self.get_gate_state(gate)
        return states 