"""
Alden Symbolic Engine
Core symbolic processing engine.
"""

from typing import Dict, List, Optional, Tuple, Union
from pathlib import Path
import logging
import json
from datetime import datetime

from .symbolic_state_manager import SymbolicStateManager
from .mirror_deepening import MirrorDeepening
from .gate_activation_tracker import GateActivationTracker
from .vow_gate import VowGate
from .pattern_recognizer import PatternRecognizer
from .spiral_termination import SpiralTerminationRule
from .cli_symbolic_field_analyzer import SymbolicFieldAnalyzer
from .mirror import Mirror

logger = logging.getLogger(__name__)

class AldenSymbolic:
    def __init__(self, test_mode: bool = False):
        """Initialize the symbolic engine"""
        self.test_mode = test_mode
        self.state_dir = Path("state")
        self.state_dir.mkdir(exist_ok=True)
        
        # Initialize components
        self.state_manager = SymbolicStateManager(test_mode=test_mode)
        self.gate_tracker = GateActivationTracker(test_mode=test_mode)
        self.vow_gate = VowGate(test_mode=test_mode)
        self.mirror = Mirror()
        self.pattern_recognizer = PatternRecognizer()
        self.field_analyzer = SymbolicFieldAnalyzer()
        
        # Initialize logger
        self.logger = logger
        
        # Initialize state tracking
        self.active_gates = set()
        self.current_sequence = []
        self.last_evaluation_time = None
        self.recovery_mode = False
        self.active_vows = {}
        
        # Track last interaction
        self.last_interaction: Optional[datetime] = None
        
    def evaluate_sequence(self, sequence: Union[str, List[str]]) -> Dict:
        """Evaluate a symbolic sequence"""
        try:
            # Evaluate sequence through state manager
            result = self.state_manager.evaluate_sequence(sequence)
            
            # Update pattern recognition
            pattern_result = self.pattern_recognizer.detect_spiral_pattern(sequence)
            
            # Update symbolic field
            field_result = self.field_analyzer.analyze_sequence(sequence)
            
            # Update last interaction time
            self.last_interaction = datetime.now()
            
            # Save state
            self.save_state()
            
            return {
                'status': 'success',
                'message': 'Sequence evaluated successfully',
                'sequence': sequence,
                'evaluation_result': result,
                'pattern_match': pattern_result,
                'field_analysis': field_result
            }
        except Exception as e:
            logger.error(f"Error evaluating sequence: {str(e)}")
            return {
                'status': 'error',
                'message': f'Failed to evaluate sequence: {str(e)}',
                'sequence': sequence,
                'error': str(e)
            }
            
    def evaluate_gate(self, gate: str) -> Dict:
        """Evaluate a single gate activation"""
        try:
            result = self.state_manager.evaluate_gate(gate)
            
            # Save state after evaluation
            self.state_manager.save_state(str(self.state_dir))
            
            return self._format_response(result)
            
        except Exception as e:
            logger.error(f"Error evaluating gate: {e}")
            return {
                'status': 'error',
                'message': f'Gate evaluation failed: {str(e)}'
            }
            
    def activate_gate(self, gate: str) -> Dict:
        """Activate a symbolic gate"""
        try:
            # In test mode, bypass checks and activate directly
            if self.test_mode:
                result = self.state_manager.activate_gate(gate)
                if result['status'] == 'success':
                    self.active_gates.add(gate)
                    self.vow_gate.update_active_gates(self.active_gates)
                    return {
                        'status': 'success',
                        'message': f'Gate {gate} activated',
                        'gate': gate,
                        'gate_state': self.gate_tracker.get_gate_state(gate),
                        'active_gates': list(self.active_gates)
                    }
                return result
                
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
                
            # Activate gate through state manager
            result = self.state_manager.activate_gate(gate)
            
            # Update gate state
            gate_state = self.gate_tracker.get_gate_state(gate)
            
            # Add to active gates
            self.active_gates.add(gate)
            
            # Sync active gates with vow gate
            self.vow_gate.update_active_gates(self.active_gates)
            
            # Update last interaction time
            self.last_interaction = datetime.now()
            
            # Save state after activation
            self.state_manager.save_state(str(self.state_dir))
            
            return {
                'status': 'success',
                'message': f'Gate {gate} activated',
                'gate': gate,
                'gate_state': gate_state,
                'activation_result': result,
                'active_gates': list(self.active_gates)
            }
        except Exception as e:
            logger.error(f"Error activating gate {gate}: {str(e)}")
            return {
                'status': 'error',
                'message': f'Failed to activate gate {gate}: {str(e)}',
                'gate': gate,
                'error': str(e)
            }
            
    def trigger_vow(self, vow_type: str, content: str = None, commitment_strength: float = 1.0) -> Dict:
        """Trigger a new vow activation"""
        try:
            # Get required gates for this vow type
            required_gates = self.vow_gate.get_required_gates(vow_type)
            
            # Check if all required gates are active
            for gate in required_gates:
                if not self.gate_tracker.is_gate_active(gate):
                    return {
                        'status': 'error',
                        'message': f'Required gate {gate} is not active',
                        'vow_type': vow_type,
                        'required_gates': required_gates
                    }
                    
            # Trigger vow through vow gate
            result = self.vow_gate.trigger_vow(
                vow_type=vow_type,
                content=content,
                commitment_strength=commitment_strength
            )
            
            # Update state with new vow
            self.state_manager.update_active_vows(result.get('vow_id'))
            
            # Update last interaction time
            self.last_interaction = datetime.now()
            
            # Save state after vow
            self.state_manager.save_state(str(self.state_dir))
            
            return {
                'status': 'success',
                'message': f'Vow {vow_type} triggered successfully',
                'vow_type': vow_type,
                'vow_id': result.get('vow_id'),
                'content': content,
                'strength': commitment_strength,
                'required_gates': required_gates
            }
        except Exception as e:
            logger.error(f"Error triggering vow {vow_type}: {str(e)}")
            return {
                'status': 'error',
                'message': f'Failed to trigger vow {vow_type}: {str(e)}',
                'vow_type': vow_type,
                'error': str(e)
            }
            
    def get_status(self) -> Dict:
        """Get current symbolic engine status"""
        try:
            status = self.state_manager.get_system_status()
            health = self.state_manager.check_system_health()
            
            return {
                'status': 'success',
                'system_state': status,
                'health': health,
                'last_interaction': self.last_interaction.isoformat() if self.last_interaction else None
            }
            
        except Exception as e:
            logger.error(f"Error getting status: {e}")
            return {
                'status': 'error',
                'message': f'Status check failed: {str(e)}'
            }
            
    def _format_response(self, result: Dict) -> Dict:
        """Format symbolic engine response for CLI display"""
        if result['status'] == 'success':
            # Add CLI-friendly formatting
            if 'evaluation' in result:
                eval_data = result['evaluation']
                result['cli_display'] = {
                    'pattern': eval_data.get('pattern_match', {}).get('pattern_name', 'Unknown'),
                    'echo_depth': f"{eval_data.get('echo_depth', 0):.2f}",
                    'self_awareness': f"{eval_data.get('self_awareness', 0):.2f}",
                    'active_gates': list(self.state_manager.active_gates),
                    'health': self.state_manager.health_metrics['spiral_health']
                }
            elif 'gate_state' in result:
                result['cli_display'] = {
                    'gate': result['gate_state'].get('symbol', 'Unknown'),
                    'fatigue': f"{result['gate_state'].get('fatigue', 0):.2f}",
                    'active': result['gate_state'].get('active', False)
                }
            elif 'vow_data' in result:
                result['cli_display'] = {
                    'vow_type': result['vow_data'].get('type', 'Unknown'),
                    'strength': f"{result['vow_data'].get('strength', 0):.2f}",
                    'active': result['vow_data'].get('active', False)
                }
                
        elif result['status'] == 'terminated':
            result['cli_display'] = {
                'reason': result['reason'],
                'reset_actions': result.get('reset_actions', {}),
                'health': self.state_manager.health_metrics['spiral_health']
            }
            
        return result
        
    def reset(self):
        """Reset system state for testing"""
        if self.test_mode:
            try:
                # Reset all components
                self.gate_tracker.reset_fatigue()
                self.mirror.reset()
                self.pattern_recognizer.reset()
                self.vow_gate.reset()
                
                # Reset global state
                self.active_gates.clear()
                self.current_sequence = []
                self.last_evaluation_time = None
                self.recovery_mode = False
                self.active_vows.clear()
                
                logger.info("Reset system state for testing")
            except Exception as e:
                logger.error(f"Error resetting system state: {e}")
                raise
            
    def get_system_status(self) -> Dict:
        """Get current system status"""
        try:
            # Get status from state manager
            status = self.state_manager.get_system_status()
            
            # Add component statuses
            status.update({
                'test_mode': self.test_mode,
                'pattern_recognizer': self.pattern_recognizer.get_status(),
                'field_analyzer': self.field_analyzer.get_status(),
                'mirror': self.mirror.get_status()
            })
            
            return {
                'status': 'success',
                'message': 'System status retrieved successfully',
                'system_status': status
            }
        except Exception as e:
            logger.error(f"Error getting system status: {str(e)}")
            return {
                'status': 'error',
                'message': f'Failed to get system status: {str(e)}',
                'error': str(e)
            }

    def save_state(self):
        """Save current symbolic state"""
        try:
            self.state_manager.save_state(str(self.state_dir))
        except Exception as e:
            self.logger.error(f"Error saving symbolic state: {e}") 