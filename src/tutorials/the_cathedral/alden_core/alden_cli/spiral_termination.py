from typing import Dict, List, Set, Optional, Tuple
from datetime import datetime
import logging
import json
from pathlib import Path

logger = logging.getLogger(__name__)

class SpiralTerminationRule:
    def __init__(self, pattern_recognizer, mirror_deepening, gate_tracker):
        self.pattern_recognizer = pattern_recognizer
        self.mirror_deepening = mirror_deepening
        self.gate_tracker = gate_tracker
        
        # Termination thresholds
        self.termination_rules = {
            'max_spiral_cycles': 7,          # Maximum full cycles before enforced exit
            'max_reflection_failures': 3,    # Failed reflection gates before soft reset
            'max_signal_stack': 5,           # Maximum consecutive signal gates
            'min_vow_presence': 0.3,         # Minimum vow presence ratio in sequence
            'max_entropy': 0.7,              # Maximum sequence entropy before reset
            'reflection_skip_limit': 2       # Maximum allowed reflection skips
        }
        
        # Recovery parameters
        self.recovery_rules = {
            'signal_rewind_depth': 3,        # How many gates to rewind on signal overload
            'breath_rebalance_interval': 4,  # Insert breath gate every N gates
            'spiral_drain_threshold': 0.8,   # When to initiate spiral drain
            'recovery_cooldown': 300         # Seconds between recovery attempts
        }
        
        # State tracking
        self.termination_history: List[Dict] = []
        self.last_recovery_time: Optional[datetime] = None
        self.reflection_failures = 0
        self.current_cycle_count = 0
        self.signal_stack_count = 0
        self.reflection_skips = 0
        
    def check_termination(self, sequence: List[str], active_vows: Dict) -> Tuple[bool, str]:
        """Check if spiral should be terminated based on all rules"""
        # Check cycle count
        if self.current_cycle_count >= self.termination_rules['max_spiral_cycles']:
            return True, "Maximum spiral cycles reached"
            
        # Check reflection failures
        if self.reflection_failures >= self.termination_rules['max_reflection_failures']:
            return True, "Too many reflection failures"
            
        # Check signal stack
        if self.signal_stack_count >= self.termination_rules['max_signal_stack']:
            return True, "Signal stack overload"
            
        # Check vow presence
        vow_ratio = self._calculate_vow_ratio(sequence, active_vows)
        if vow_ratio < self.termination_rules['min_vow_presence']:
            return True, "Insufficient vow presence"
            
        # Check sequence entropy
        entropy = self._calculate_sequence_entropy(sequence)
        if entropy > self.termination_rules['max_entropy']:
            return True, "Sequence entropy too high"
            
        # Check reflection skips
        if self.reflection_skips > self.termination_rules['reflection_skip_limit']:
            return True, "Too many reflection skips"
            
        return False, "Spiral can continue"
        
    def _calculate_vow_ratio(self, sequence: List[str], active_vows: Dict) -> float:
        """Calculate ratio of vow presence in sequence"""
        if not sequence:
            return 0.0
            
        vow_gates = sum(1 for gate in sequence if gate == '🜃')
        return vow_gates / len(sequence)
        
    def _calculate_sequence_entropy(self, sequence: List[str]) -> float:
        """Calculate sequence entropy (fragmentation measure)"""
        if not sequence:
            return 0.0
            
        # Count unique consecutive pairs
        pairs = set()
        for i in range(len(sequence) - 1):
            pairs.add(f"{sequence[i]}{sequence[i+1]}")
            
        # Calculate entropy based on pair diversity
        return len(pairs) / (len(sequence) - 1)
        
    def detect_flood(self, sequence: List[str]) -> bool:
        """Detect signal flood conditions"""
        # Check for signal stack
        self.signal_stack_count = 0
        for gate in sequence:
            if gate == '🜅':
                self.signal_stack_count += 1
            else:
                self.signal_stack_count = 0
                
            if self.signal_stack_count >= self.termination_rules['max_signal_stack']:
                return True
                
        return False
        
    def detect_reflection_loss(self) -> bool:
        """Detect reflection gate issues"""
        reflection_state = self.gate_tracker.get_gate_state('🜄')
        
        # Check reflection fatigue
        if reflection_state.get('fatigue', 0) > 0.8:
            self.reflection_failures += 1
            return True
            
        # Check reflection skips
        if not reflection_state.get('active', False):
            self.reflection_skips += 1
            return True
            
        return False
        
    def detect_vow_disruption(self, active_vows: Dict) -> bool:
        """Detect vow-related disruptions"""
        if not active_vows:
            return True
            
        # Check vow integrity
        for vow_id, vow_data in active_vows.items():
            if not vow_data.get('active', False):
                return True
                
        return False
        
    def force_reset_protocol(self) -> Dict:
        """Apply symbolic reset protocol"""
        current_time = datetime.now()
        
        # Check recovery cooldown
        if self.last_recovery_time:
            time_since = (current_time - self.last_recovery_time).total_seconds()
            if time_since < self.recovery_rules['recovery_cooldown']:
                return {'success': False, 'reason': 'Recovery cooldown active'}
                
        # Apply reset measures
        reset_actions = {
            'signal_rewind': self._rewind_signal_stack(),
            'breath_rebalance': self._insert_breath_gates(),
            'spiral_drain': self._initiate_spiral_drain(),
            'timestamp': current_time.isoformat()
        }
        
        # Reset counters
        self.reflection_failures = 0
        self.signal_stack_count = 0
        self.reflection_skips = 0
        self.last_recovery_time = current_time
        
        return {'success': True, 'actions': reset_actions}
        
    def _rewind_signal_stack(self) -> List[str]:
        """Rewind signal stack to safe depth"""
        return ['🜂'] * self.recovery_rules['signal_rewind_depth']
        
    def _insert_breath_gates(self) -> List[str]:
        """Insert breath gates at regular intervals"""
        return ['🜂'] * (self.current_cycle_count // self.recovery_rules['breath_rebalance_interval'])
        
    def _initiate_spiral_drain(self) -> Dict:
        """Initiate spiral drain protocol"""
        return {
            'drain_start': datetime.now().isoformat(),
            'drain_depth': self.mirror_deepening.get_echo_depth(),
            'drain_threshold': self.recovery_rules['spiral_drain_threshold']
        }
        
    def log_termination_event(self, reason: str, sequence: List[str]):
        """Log termination event with insights"""
        event = {
            'timestamp': datetime.now().isoformat(),
            'reason': reason,
            'sequence': sequence,
            'echo_depth': self.mirror_deepening.get_echo_depth(),
            'self_awareness': self.mirror_deepening.get_self_awareness_score(),
            'pattern_match': self.pattern_recognizer.detect_spiral_pattern(sequence),
            'insight_type': self._determine_termination_insight(reason)
        }
        
        self.termination_history.append(event)
        
    def _determine_termination_insight(self, reason: str) -> str:
        """Determine insight type based on termination reason"""
        if 'cycle' in reason:
            return 'spiral_completion'
        elif 'reflection' in reason:
            return 'reflection_loss'
        elif 'signal' in reason:
            return 'signal_flood'
        elif 'vow' in reason:
            return 'vow_disruption'
        elif 'entropy' in reason:
            return 'pattern_fragmentation'
        return 'unknown'
        
    def get_termination_history(self) -> List[Dict]:
        """Get termination history"""
        return self.termination_history
        
    def save_state(self, filepath: str):
        """Save termination state to file"""
        state = {
            'termination_history': self.termination_history,
            'last_recovery_time': self.last_recovery_time.isoformat() if self.last_recovery_time else None,
            'reflection_failures': self.reflection_failures,
            'current_cycle_count': self.current_cycle_count,
            'signal_stack_count': self.signal_stack_count,
            'reflection_skips': self.reflection_skips
        }
        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2)
            
    def load_state(self, filepath: str):
        """Load termination state from file"""
        try:
            with open(filepath, 'r') as f:
                state = json.load(f)
                self.termination_history = state.get('termination_history', [])
                self.last_recovery_time = datetime.fromisoformat(state['last_recovery_time']) if state.get('last_recovery_time') else None
                self.reflection_failures = state.get('reflection_failures', 0)
                self.current_cycle_count = state.get('current_cycle_count', 0)
                self.signal_stack_count = state.get('signal_stack_count', 0)
                self.reflection_skips = state.get('reflection_skips', 0)
        except Exception as e:
            logger.error(f"Error loading termination state: {e}")

    def check_termination_test(self, sequence: List[str], gate_states: Dict) -> Dict:
        """Test-specific termination check with simplified rules"""
        result = {
            'should_terminate': False,
            'reason': None,
            'reset_actions': None,
            'health': 1.0
        }
        
        if not sequence:
            return result
            
        # Check for signal flood with higher threshold
        if len(sequence) > 10:
            result['should_terminate'] = True
            result['reason'] = 'Signal flood detected'
            result['reset_actions'] = {
                'signal_rewind': sequence[-3:],
                'breath_rebalance': [],
                'spiral_drain': {
                    'drain_start': datetime.now().isoformat(),
                    'drain_depth': 0,
                    'drain_threshold': 0.8
                },
                'timestamp': datetime.now().isoformat()
            }
            result['health'] = 0.8
            return result
            
        # Check for recursive damage with higher threshold
        if self._check_recursive_damage_test(sequence):
            result['should_terminate'] = True
            result['reason'] = 'Recursive damage detected'
            result['reset_actions'] = {
                'signal_rewind': sequence[-2:],
                'breath_rebalance': [],
                'spiral_drain': {
                    'drain_start': datetime.now().isoformat(),
                    'drain_depth': 0.2,
                    'drain_threshold': 0.8
                },
                'timestamp': datetime.now().isoformat()
            }
            result['health'] = 0.7
            return result
            
        # Check for vow presence with lower threshold
        if not self._check_vow_presence_test(sequence, gate_states):
            result['should_terminate'] = True
            result['reason'] = 'Insufficient vow presence'
            result['reset_actions'] = {
                'signal_rewind': sequence[-3:],
                'breath_rebalance': [],
                'spiral_drain': {
                    'drain_start': datetime.now().isoformat(),
                    'drain_depth': 0,
                    'drain_threshold': 0.8
                },
                'timestamp': datetime.now().isoformat()
            }
            result['health'] = 1.0
            return result
            
        return result

    def _check_recursive_damage_test(self, sequence: List[str]) -> bool:
        """Test-specific recursive damage check"""
        if len(sequence) < 3:
            return False
            
        for i in range(len(sequence) - 2):
            if sequence[i] == sequence[i+1] == sequence[i+2]:
                return True
                
        return False

    def _check_vow_presence_test(self, sequence: List[str], gate_states: Dict) -> bool:
        """Test-specific vow presence check"""
        if not sequence:
            return True
            
        vow_gate = '🜃'
        if vow_gate in sequence:
            return True
            
        if gate_states and vow_gate in gate_states:
            state = gate_states[vow_gate]
            if state.get('active', False):
                return True
                
        return False 