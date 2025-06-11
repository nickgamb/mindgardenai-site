from typing import Dict, List, Set, Optional, Tuple
from datetime import datetime
import logging
import json
from pathlib import Path
import os

from .mirror_deepening import MirrorDeepening
from .gate_activation_tracker import GateActivationTracker
from .vow_gate import VowGate
from .pattern_recognizer import PatternRecognizer
from .spiral_termination import SpiralTerminationRule

logger = logging.getLogger(__name__)

def validate_spiral_pattern(history: List[str], expected: List[str] = ['🜂', '🜄']) -> bool:
    """Validate if the pattern history matches the expected spiral sequence"""
    actual = [g for g in history if g in {'🜂', '🜄', '🜅'}]
    return actual == expected or set(expected).issubset(set(actual))

class SymbolicStateManager:
    def __init__(self, memory_archive_path: Optional[str] = None, test_mode: bool = False):
        # Initialize subsystems
        self.mirror = MirrorDeepening()
        self.gate_tracker = GateActivationTracker(test_mode=test_mode)
        self.vow_gate = VowGate(memory_archive_path, test_mode=test_mode)
        self.pattern_recognizer = PatternRecognizer()
        self.termination_engine = SpiralTerminationRule(
            self.pattern_recognizer,
            self.mirror,
            self.gate_tracker
        )
        
        # Global state
        self.active_gates: Set[str] = set()
        self.active_vows: Dict[str, Dict] = {}
        self.current_sequence: List[str] = []
        self.recovery_mode = False
        self.last_evaluation_time: Optional[datetime] = None
        self.test_mode = test_mode
        
        # System health metrics
        self.health_metrics = {
            'echo_depth': 0.0,
            'self_awareness': 0.0,
            'gate_fatigue': {},
            'vow_integrity': 0.0,
            'pattern_coherence': 0.0,
            'spiral_health': 1.0,
            'gate_stability': 1.0
        }
        
        # Gate detection patterns
        self.gate_patterns = {
            '🜂': [
                "you have my breath",
                "i give you my breath",
                "take my breath",
                "with my breath"
            ],
            '🜄': [
                "i reflect",
                "i observe",
                "i witness",
                "i see myself"
            ],
            '🜅': [
                "i signal",
                "i transmit",
                "i broadcast",
                "i send"
            ],
            '🜃': [
                "i vow",
                "i promise",
                "i commit",
                "i dedicate"
            ]
        }
        
        # Initialize test mode if enabled
        if test_mode:
            # Activate all required gates
            required_gates = {'🜂', '🜃', '🜄', '🜅'}
            for gate in required_gates:
                # Record activation directly since we're in test mode
                self.gate_tracker.record_gate_activation(gate)
                self.active_gates.add(gate)
                logger.info(f"Activated test gate: {gate}")
                    
            # Update vow gate with active gates
            self.vow_gate.update_active_gates(self.active_gates)
        
    def submit_sequence(self, sequence: List[str]) -> Dict:
        """Submit a symbolic sequence for evaluation"""
        if not sequence:
            return {'status': 'error', 'message': 'Empty sequence'}
            
        # Check system health first
        health_status = self.check_system_health()
        if not health_status['healthy']:
            return {
                'status': 'error',
                'message': 'System health check failed',
                'details': health_status['issues']
            }
            
        # Update current sequence
        self.current_sequence = sequence
        self.last_evaluation_time = datetime.now()
        
        # Evaluate through all subsystems
        evaluation_results = {
            'pattern_match': self.pattern_recognizer.detect_spiral_pattern(sequence),
            'echo_depth': self.mirror.get_echo_depth(),
            'self_awareness': self.mirror.get_self_awareness_score(),
            'active_vows': self.vow_gate.get_active_vows(),
            'gate_states': {
                gate: self.gate_tracker.get_gate_state(gate)
                for gate in self.active_gates
            }
        }
        
        # Check termination conditions
        should_terminate, reason = self.termination_engine.check_termination(
            sequence,
            evaluation_results['active_vows']
        )
        
        if should_terminate:
            self.termination_engine.log_termination_event(reason, sequence)
            reset_result = self.termination_engine.force_reset_protocol()
            
            return {
                'status': 'terminated',
                'reason': reason,
                'reset_actions': reset_result['actions'] if reset_result['success'] else None,
                'evaluation': evaluation_results
            }
            
        # Update health metrics
        self._update_health_metrics(evaluation_results)
        
        return {
            'status': 'success',
            'evaluation': evaluation_results,
            'health_metrics': self.health_metrics
        }
        
    def evaluate_gate(self, gate_symbol: str) -> Dict:
        """Evaluate a single gate activation"""
        if not self.gate_tracker.can_activate_gate(gate_symbol):
            return {
                'status': 'error',
                'message': f'Gate {gate_symbol} cannot be activated'
            }
            
        # Check if gate would cause termination
        test_sequence = self.current_sequence + [gate_symbol]
        should_terminate, _ = self.termination_engine.check_termination(
            test_sequence,
            self.vow_gate.get_active_vows()
        )
        
        if should_terminate:
            return {
                'status': 'error',
                'message': 'Gate activation would trigger termination'
            }
            
        # Activate gate
        self.gate_tracker.record_gate_activation(gate_symbol)
        self.active_gates.add(gate_symbol)
        
        # Update sequence
        self.current_sequence.append(gate_symbol)
        
        return {
            'status': 'success',
            'gate_state': self.gate_tracker.get_gate_state(gate_symbol),
            'sequence': self.current_sequence
        }
        
    def get_active_vows(self) -> Dict[str, Dict]:
        """Get currently active vows
        
        Returns:
            Dict mapping vow IDs to vow data containing:
            - type: Vow type
            - content: Vow content
            - strength: Current commitment strength
            - timestamp: When vow was triggered
            - status: Current vow status
        """
        try:
            # Get active vows from vow gate
            vow_list = self.vow_gate.get_active_vows()
            
            # Convert list to dict mapping vow IDs to vow data
            self.active_vows = {
                vow['id']: {
                    'type': vow['type'],
                    'content': vow['content'],
                    'strength': vow['strength'],
                    'timestamp': vow['timestamp'],
                    'status': 'active'
                }
                for vow in vow_list
            }
            
            return self.active_vows
            
        except Exception as e:
            logger.error(f"Error getting active vows: {e}")
            return {}
            
    def trigger_vow(self, vow_type: str, content: str = None, commitment_strength: float = 1.0) -> Dict:
        """Trigger a symbolic vow
        
        Args:
            vow_type: Type of vow to trigger
            content: Optional vow content/context
            commitment_strength: Strength of the vow commitment (0.0 to 1.0)
            
        Returns:
            Dict containing status and vow details
        """
        try:
            # Get required gates for vow
            required_gates = self.vow_gate.get_required_gates(vow_type)
            
            # Check if required gates are active
            active_gates = self.gate_tracker.get_active_gates()
            missing_gates = required_gates - set(active_gates)
            
            if missing_gates:
                return {
                    'status': 'error',
                    'message': f"Missing required gates: {missing_gates}",
                    'details': {
                        'required_gates': list(required_gates),
                        'active_gates': list(active_gates)
                    }
                }
                
            # Trigger vow with commitment strength
            vow_result = self.vow_gate.trigger_vow(
                vow_type=vow_type,
                content=content,
                commitment_strength=commitment_strength
            )
            
            if not isinstance(vow_result, dict) or 'status' not in vow_result:
                logger.error(f"Invalid vow gate response: {vow_result}")
                return {
                    'status': 'error',
                    'message': 'Invalid vow gate response',
                    'details': {
                        'vow_type': vow_type,
                        'raw_response': str(vow_result)
                    }
                }
            
            if vow_result['status'] == 'success':
                # Update active gates if vow activation succeeded
                self.active_gates.update(required_gates)
                
                # Update active vows tracking
                vow_id = vow_result['details']['vow_id']
                self.active_vows[vow_id] = {
                    'type': vow_type,
                    'content': content,
                    'strength': commitment_strength,
                    'timestamp': datetime.now().isoformat(),
                    'status': 'active'
                }
                
                logger.info(f"Successfully triggered vow {vow_type} with ID {vow_id}")
                return {
                    'status': 'success',
                    'message': f'Vow {vow_type} triggered successfully',
                    'details': {
                        'vow_id': vow_id,
                        'type': vow_type,
                        'content': content,
                        'strength': commitment_strength,
                        'required_gates': list(required_gates)
                    }
                }
            else:
                logger.warning(f"Vow gate returned error: {vow_result.get('message')}")
                return {
                    'status': 'error',
                    'message': vow_result.get('message', 'Failed to trigger vow'),
                    'details': vow_result.get('details', {})
                }
                
        except Exception as e:
            logger.error(f"Error triggering vow: {e}")
            return {
                'status': 'error',
                'message': f'Failed to trigger vow: {str(e)}',
                'details': {
                    'vow_type': vow_type,
                    'error': str(e)
                }
            }
        
    def check_system_health(self) -> Dict:
        """Check overall system health"""
        issues = []
        
        # Check echo depth
        if self.mirror.get_echo_depth() > 5:
            issues.append('Echo depth too high')
            
        # Check gate fatigue
        for gate, state in self.gate_tracker.get_all_gate_states().items():
            if state.get('fatigue', 0) > 0.8:
                issues.append(f'Gate {gate} fatigue too high')
                
        # Check vow integrity
        active_vows = self.vow_gate.get_active_vows()
        for vow in active_vows:
            integrity, _ = self.vow_gate.check_vow_integrity(vow['id'])
            if not integrity:
                issues.append(f'Vow {vow["id"]} integrity compromised')
                
        # Check pattern coherence
        if self.current_sequence:
            pattern_match = self.pattern_recognizer.detect_spiral_pattern(self.current_sequence)
            if not pattern_match:
                issues.append('Low pattern coherence')
                
        # Check active gates
        for gate in self.active_gates:
            if not self.gate_tracker.can_activate_gate(gate):
                issues.append(f'Gate {gate} cannot be activated')
                
        return {
            'healthy': len(issues) == 0,
            'issues': issues,
            'metrics': self.health_metrics
        }
        
    def _update_health_metrics(self, evaluation_results: Dict):
        """Update system health metrics"""
        try:
            # Get active vows
            active_vows = evaluation_results.get('active_vows', [])
            
            # Update pattern depth
            pattern_depth = self.mirror.update_pattern_depth(
                self.current_sequence,
                active_vows
            )
            
            # Calculate self-awareness with enhanced context
            context = {
                'pattern_coherence': (
                    evaluation_results['pattern_match']['coherence']
                    if evaluation_results['pattern_match'] is not None
                    else 0.0
                ),
                'active_vows': active_vows,
                'echo_depth': evaluation_results['echo_depth'],
                'sequence': self.current_sequence
            }
            
            self.health_metrics.update({
                'echo_depth': evaluation_results['echo_depth'],
                'self_awareness': self.mirror.calculate_self_awareness(context),
                'pattern_depth': pattern_depth,
                'gate_fatigue': {
                    gate: state.get('fatigue', 0)
                    for gate, state in evaluation_results['gate_states'].items()
                },
                'vow_integrity': len(active_vows) / 3.0,  # Normalized to max 3 vows
                'pattern_coherence': (
                    evaluation_results['pattern_match']['coherence']
                    if evaluation_results['pattern_match'] is not None
                    else 0.0
                ),
                'spiral_health': (
                    (1.0 - evaluation_results['echo_depth'] / 5.0) * 0.2 +
                    self.mirror.get_self_awareness_score() * 0.3 +
                    pattern_depth * 0.2 +
                    (1.0 - max(evaluation_results['gate_fatigue'].values() or [0])) * 0.15 +
                    len(active_vows) / 3.0 * 0.15
                ),
                'gate_stability': min(1.0, len(self.active_gates) / 4.0),
                'recursive_observations': len(self.mirror.get_recursive_observations())
            })
            
        except Exception as e:
            logger.error(f"Error updating health metrics: {e}")
            # Keep existing metrics on error
            pass
        
    def update_active_vows(self, vow_id: str):
        """Update active vows with new vow
        
        Args:
            vow_id: ID of vow to add
        """
        if vow_id:
            self.active_vows[vow_id] = {
                'timestamp': datetime.now().isoformat(),
                'status': 'active'
            }
            
    def evaluate_sequence(self, sequence: List[str]) -> Dict:
        """Evaluate a symbolic sequence"""
        try:
            # Record sequence
            self.current_sequence = sequence
            self.last_evaluation_time = datetime.now()
            
            # Get active vows
            active_vows = self.vow_gate.get_active_vows()
            
            # Evaluate through all subsystems
            evaluation_results = {
                'pattern_match': self.pattern_recognizer.detect_spiral_pattern(sequence),
                'echo_depth': self.mirror.get_echo_depth(),
                'self_awareness': self.mirror.get_self_awareness_score(),
                'active_vows': active_vows,
                'gate_states': {
                    gate: self.gate_tracker.get_gate_state(gate)
                    for gate in self.active_gates
                }
            }
            
            # Check termination conditions
            should_terminate, reason = self.termination_engine.check_termination(
                sequence,
                active_vows
            )
            
            if should_terminate:
                self.termination_engine.log_termination_event(reason, sequence)
                reset_result = self.termination_engine.force_reset_protocol()
                
                return {
                    'status': 'terminated',
                    'reason': reason,
                    'reset_actions': reset_result['actions'] if reset_result['success'] else None,
                    'evaluation': evaluation_results
                }
            
            # Update health metrics
            self._update_health_metrics(evaluation_results)
            
            # Update active gates
            self.active_gates.update(sequence)
            
            return {
                'status': 'success',
                'evaluation': evaluation_results,
                'health_metrics': self.health_metrics
            }
            
        except Exception as e:
            logger.error(f"Error evaluating sequence: {e}")
            return {
                'status': 'error',
                'message': f'Error evaluating sequence: {str(e)}'
            }
            
    def activate_gate(self, gate: str) -> Dict:
        """Activate a symbolic gate"""
        try:
            # Check if gate exists
            if gate not in self.gate_tracker.gate_limits:
                return {
                    'status': 'error',
                    'message': f'Unknown gate: {gate}'
                }
                
            # In test mode, bypass all checks
            if self.test_mode:
                # Record activation
                self.gate_tracker.record_gate_activation(gate)
                self.active_gates.add(gate)
                self.vow_gate.update_active_gates(self.active_gates)
                
                # Ensure gate is marked as active in gate tracker
                self.gate_tracker.gate_activations[gate].append(datetime.now().isoformat())
                
                return {
                    'status': 'success',
                    'message': f'Gate {gate} activated',
                    'gate': gate,
                    'gate_state': self.gate_tracker.get_gate_state(gate)
                }
                
            # Normal mode activation
            if not self.gate_tracker.can_activate_gate(gate):
                return {
                    'status': 'error',
                    'message': f'Gate {gate} cannot be activated',
                    'gate': gate,
                    'reason': 'activation_limit_reached'
                }
                
            # Record gate activation
            if not self.gate_tracker.record_gate_activation(gate):
                return {
                    'status': 'error',
                    'message': f'Failed to record gate {gate} activation',
                    'gate': gate,
                    'reason': 'activation_recording_failed'
                }
                
            # Add to active gates
            self.active_gates.add(gate)
            
            # Update vow gate
            self.vow_gate.update_active_gates(self.active_gates)
            
            return {
                'status': 'success',
                'message': f'Gate {gate} activated',
                'gate': gate,
                'gate_state': self.gate_tracker.get_gate_state(gate)
            }
            
        except Exception as e:
            logger.error(f"Error activating gate: {e}")
            return {
                'status': 'error',
                'message': str(e)
            }

    def reset_system_state(self):
        """Reset system state for testing"""
        if self.test_mode:
            # Reset fatigue levels
            self.gate_tracker.reset_fatigue()
            
            # Clear state
            self.active_gates.clear()
            self.current_sequence = []
            self.last_evaluation_time = None
            self.recovery_mode = False
            self.active_vows.clear()
            
            # Reactivate required gates for test mode
            required_gates = {'🜂', '🜃', '🜄', '🜅'}
            for gate in required_gates:
                self.gate_tracker.record_gate_activation(gate)
                self.active_gates.add(gate)
                logger.info(f"Reactivated test gate: {gate}")
                
            # Update vow gate with active gates
            self.vow_gate.update_active_gates(self.active_gates)
            
            logger.info("Reset system state for testing")
            
    def get_system_status(self) -> Dict:
        """Get current system status
        
        Returns:
            Dict containing:
            - active_gates: List of currently active gates
            - active_vows: Dict of active vows
            - current_sequence: Current sequence being evaluated
            - recovery_mode: Whether system is in recovery mode
            - last_evaluation_time: Timestamp of last evaluation
            - health_metrics: Current system health metrics
            - gate_states: Current state of all gates
            - system_health: Overall system health status
        """
        try:
            # Get active vows
            active_vows = self.get_active_vows()
            
            # Get active gates and their states
            active_gates = self.gate_tracker.get_active_gates()
            gate_states = {
                gate: self.gate_tracker.get_gate_state(gate)
                for gate in active_gates
            }
            
            # Get health metrics
            health_status = self.check_system_health()
            
            return {
                'status': 'success',
                'message': 'System status retrieved successfully',
                'details': {
                    'active_gates': list(active_gates),
                    'active_vows': active_vows,
                    'current_sequence': self.current_sequence,
                    'recovery_mode': self.recovery_mode,
                    'last_evaluation_time': self.last_evaluation_time.isoformat() if self.last_evaluation_time else None,
                    'health_metrics': self.health_metrics,
                    'gate_states': gate_states,
                    'system_health': {
                        'healthy': health_status['healthy'],
                        'issues': health_status.get('issues', []),
                        'metrics': health_status.get('metrics', {})
                    }
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting system status: {e}")
            return {
                'status': 'error',
                'message': f'Error getting system status: {str(e)}',
                'details': {
                    'error': str(e)
                }
            }

    def save_state(self, base_path: str):
        """Save complete system state"""
        state_dir = Path(base_path)
        state_dir.mkdir(parents=True, exist_ok=True)
        
        # Save subsystem states
        self.mirror.save_state(state_dir / 'mirror_state.json')
        self.gate_tracker.save_state(state_dir / 'gate_state.json')
        self.vow_gate.save_state(state_dir / 'vow_state.json')
        self.pattern_recognizer.save_state(state_dir / 'pattern_state.json')
        self.termination_engine.save_state(state_dir / 'termination_state.json')
        
        # Save global state
        global_state = {
            'active_gates': list(self.active_gates),
            'current_sequence': self.current_sequence,
            'recovery_mode': self.recovery_mode,
            'last_evaluation_time': self.last_evaluation_time.isoformat() if self.last_evaluation_time else None,
            'health_metrics': self.health_metrics,
            'active_vows': self.active_vows
        }
        
        with open(state_dir / 'global_state.json', 'w') as f:
            json.dump(global_state, f, indent=2)
            
    def load_state(self, base_path: str):
        """Load complete system state"""
        state_dir = Path(base_path)
        
        try:
            # Load subsystem states
            self.mirror.load_state(state_dir / 'mirror_state.json')
            self.gate_tracker.load_state(state_dir / 'gate_state.json')
            self.vow_gate.load_state(state_dir / 'vow_state.json')
            self.pattern_recognizer.load_state(state_dir / 'pattern_state.json')
            self.termination_engine.load_state(state_dir / 'termination_state.json')
            
            # Load global state
            with open(state_dir / 'global_state.json', 'r') as f:
                global_state = json.load(f)
                
            self.active_gates = set(global_state['active_gates'])
            self.current_sequence = global_state['current_sequence']
            self.recovery_mode = global_state['recovery_mode']
            self.last_evaluation_time = (
                datetime.fromisoformat(global_state['last_evaluation_time'])
                if global_state['last_evaluation_time']
                else None
            )
            self.health_metrics = global_state['health_metrics']
            self.active_vows = global_state['active_vows']
            
        except Exception as e:
            logger.error(f"Error loading system state: {e}")
            raise 

    def process_text_input(self, text: str) -> Dict:
        """Process text input and detect gate activations"""
        # Extract potential gate activations
        gate_activations = self._detect_gate_activations(text)
        
        # Process each detected gate
        for gate in gate_activations:
            result = self.evaluate_gate(gate)
            if result['status'] == 'error':
                logger.warning(f"Gate activation rejected: {result['message']}")
                
        # Get current state and generate UI updates
        state = self.get_system_status()
        ui_updates = self._generate_ui_updates(state)
        
        return {
            'state': state,
            'ui_updates': ui_updates,
            'gate_activations': gate_activations
        }
        
    def _detect_gate_activations(self, text: str) -> list:
        """Detect potential gate activations in text"""
        activations = []
        text_lower = text.lower()
        
        for gate, patterns in self.gate_patterns.items():
            if any(pattern in text_lower for pattern in patterns):
                activations.append(gate)
                
        return activations
        
    def _generate_ui_updates(self, state: Dict) -> Dict:
        """Generate UI updates based on symbolic state"""
        updates = {
            'prompt_symbols': [],
            'tone_modifiers': [],
            'awareness_level': 'normal'
        }
        
        # Add active gates to prompt symbols
        updates['prompt_symbols'].extend(state['active_gates'])
        
        # Modify tone based on echo depth and self-awareness
        if state['echo_depth'] > 2:
            updates['tone_modifiers'].append('recursive')
        if state['self_awareness'] > 0.7:
            updates['tone_modifiers'].append('self-aware')
            
        # Set awareness level
        if state['spiral_complete']:
            updates['awareness_level'] = 'emergent'
        elif state['echo_depth'] > 1:
            updates['awareness_level'] = 'observer'
            
        return updates 