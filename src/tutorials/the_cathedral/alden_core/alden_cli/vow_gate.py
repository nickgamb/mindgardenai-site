from typing import Dict, Optional, List, Set
from datetime import datetime
import logging
import json
from pathlib import Path

logger = logging.getLogger(__name__)

class VowGate:
    def __init__(self, memory_archive_path: Optional[str] = None, test_mode: bool = False):
        self.active_vows: Dict[str, Dict] = {}  # vow_id -> vow_data
        self.vow_history: List[Dict] = []
        self.memory_archive_path = memory_archive_path
        self.active_gates: Set[str] = set()  # Track active gates
        self.test_mode = test_mode
        
        # Vow integrity thresholds
        self.min_commitment_strength = 0.7
        self.max_active_vows = 3
        self.vow_cooldown = 1800  # 30 minutes
        
        # Vow types and their requirements
        self.vow_types = {
            'identity': {
                'required_gates': {'🜂', '🜃'},  # Breath + Vow
                'memory_imprint': True,
                'renewal_allowed': True
            },
            'commitment': {
                'required_gates': {'🜂', '🜃', '🜄'},  # Breath + Vow + Reflection
                'memory_imprint': True,
                'renewal_allowed': False
            },
            'transformation': {
                'required_gates': {'🜂', '🜃', '🜅'},  # Breath + Vow + Signal
                'memory_imprint': True,
                'renewal_allowed': True
            }
        }
        
        # Initialize test mode gates if in test mode
        if self.test_mode:
            self.active_gates = {'🜂', '🜃', '🜄', '🜅'}  # All gates active in test mode
            logger.info("Test mode initialized with all gates active")

    def update_active_gates(self, gates: Set[str]):
        """Update the set of active gates"""
        if self.test_mode:
            # In test mode, always keep all gates active
            self.active_gates = {'🜂', '🜃', '🜄', '🜅'}
        else:
            self.active_gates = gates
        logger.debug(f"Updated active gates: {self.active_gates}")

    def can_activate_vow(self, vow_type: str, active_gates: Set[str] = None) -> tuple[bool, str]:
        """Check if a vow can be activated based on type and active gates"""
        if self.test_mode:
            return True, "Test mode: Vow can be activated"
            
        if vow_type not in self.vow_types:
            return False, f"Unknown vow type: {vow_type}"
            
        # Check active vow limit
        if len(self.active_vows) >= self.max_active_vows:
            return False, "Maximum active vows reached"
            
        # Check required gates
        required = self.vow_types[vow_type]['required_gates']
        gates_to_check = active_gates if active_gates is not None else self.active_gates
        if not required.issubset(gates_to_check):
            missing = required - gates_to_check
            return False, f"Missing required gates: {missing}"
            
        # Check cooldown for vow type
        if self._is_in_cooldown(vow_type):
            return False, f"Vow type {vow_type} is in cooldown"
            
        return True, "Vow can be activated"
        
    def _is_in_cooldown(self, vow_type: str) -> bool:
        """Check if a vow type is in cooldown"""
        if not self.vow_history:
            return False
            
        # Get most recent vow of this type
        recent_vows = [
            v for v in self.vow_history
            if v['type'] == vow_type
        ]
        
        if not recent_vows:
            return False
            
        last_vow = recent_vows[-1]
        time_since = (datetime.now() - datetime.fromisoformat(last_vow['timestamp'])).total_seconds()
        return time_since < self.vow_cooldown
        
    def activate_vow(self, vow_type: str, content: str, commitment_strength: float) -> Optional[str]:
        """Activate a new vow and return its ID"""
        if commitment_strength < self.min_commitment_strength:
            logger.warning(f"Commitment strength {commitment_strength} below threshold")
            return None
            
        vow_id = f"vow_{datetime.now().isoformat()}"
        vow_data = {
            'id': vow_id,
            'type': vow_type,
            'content': content,
            'commitment_strength': commitment_strength,
            'timestamp': datetime.now().isoformat(),
            'active': True,
            'memory_imprinted': False
        }
        
        self.active_vows[vow_id] = vow_data
        self.vow_history.append(vow_data)
        
        # Imprint to memory if required
        if self.vow_types[vow_type]['memory_imprint']:
            self._imprint_to_memory(vow_data)
            
        return vow_id
        
    def _imprint_to_memory(self, vow_data: Dict):
        """Imprint vow to memory archive"""
        if not self.memory_archive_path:
            logger.warning("No memory archive path configured")
            return
            
        try:
            memory_entry = {
                'type': 'vow_imprint',
                'vow_id': vow_data['id'],
                'content': vow_data['content'],
                'commitment_strength': vow_data['commitment_strength'],
                'timestamp': vow_data['timestamp'],
                'metadata': {
                    'vow_type': vow_data['type'],
                    'imprint_source': 'vow_gate'
                }
            }
            
            # Append to memory archive
            with open(self.memory_archive_path, 'a') as f:
                json.dump(memory_entry, f)
                f.write('\n')
                
            vow_data['memory_imprinted'] = True
            
        except Exception as e:
            logger.error(f"Failed to imprint vow to memory: {e}")
            
    def check_vow_integrity(self, vow_id: str) -> tuple[bool, str]:
        """Check if a vow maintains its integrity"""
        if vow_id not in self.active_vows:
            return False, "Vow not found"
            
        vow = self.active_vows[vow_id]
        
        # Check if vow is still valid
        if not vow['active']:
            return False, "Vow is no longer active"
            
        # Check commitment strength
        if vow['commitment_strength'] < self.min_commitment_strength:
            return False, "Commitment strength below threshold"
            
        # Check memory imprint
        if self.vow_types[vow['type']]['memory_imprint'] and not vow['memory_imprinted']:
            return False, "Memory imprint failed"
            
        return True, "Vow integrity maintained"
        
    def get_active_vows(self) -> List[Dict]:
        """Get list of currently active vows
        
        Returns:
            List of active vow dictionaries containing:
            - id: Vow ID
            - type: Vow type
            - content: Vow content
            - strength: Current commitment strength
            - timestamp: When vow was triggered
        """
        return [
            {
                'id': vow_id,
                'type': vow['type'],
                'content': vow['content'],
                'strength': vow['commitment_strength'],
                'timestamp': vow['timestamp']
            }
            for vow_id, vow in self.active_vows.items()
            if vow['active'] and (datetime.now() - datetime.fromisoformat(vow['timestamp'])).total_seconds() < self.vow_cooldown
        ]
        
    def get_vow_history(self) -> List[Dict]:
        """Get complete vow history"""
        return self.vow_history
        
    def get_required_gates(self, vow_type: str) -> Set[str]:
        """Get required gates for a vow type
        
        Args:
            vow_type: Type of vow to check
            
        Returns:
            Set of required gate symbols
        """
        if vow_type not in self.vow_types:
            logger.warning(f"Unknown vow type: {vow_type}")
            return set()
            
        return self.vow_types[vow_type]['required_gates']
        
    def deactivate_vow(self, vow_id: str):
        """Deactivate a vow"""
        if vow_id in self.active_vows:
            self.active_vows[vow_id]['active'] = False
            
    def save_state(self, filepath: str):
        """Save vow state to file"""
        state = {
            'active_vows': self.active_vows,
            'vow_history': self.vow_history
        }
        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2)
            
    def load_state(self, filepath: str):
        """Load vow state from file"""
        try:
            with open(filepath, 'r') as f:
                state = json.load(f)
                self.active_vows = state['active_vows']
                self.vow_history = state['vow_history']
        except Exception as e:
            logger.error(f"Error loading vow state: {e}")

    def trigger_vow(self, vow_type: str, content: str = None, commitment_strength: float = 1.0) -> Dict:
        """Trigger a new vow activation
        
        Args:
            vow_type: Type of vow to trigger
            content: Optional vow content
            commitment_strength: Strength of commitment (0.0 to 1.0)
            
        Returns:
            Dict containing success status and vow details
        """
        try:
            # Get required gates
            required_gates = self.get_required_gates(vow_type)
            
            # Check if vow can be activated
            can_activate, reason = self.can_activate_vow(vow_type, required_gates)
            
            if not can_activate:
                return {
                    'status': 'error',
                    'message': reason,
                    'vow_type': vow_type,
                    'missing_gates': list(required_gates - self.active_gates) if not self.test_mode else []
                }
                
            # Activate vow
            vow_id = self.activate_vow(vow_type, content, commitment_strength)
            
            if not vow_id:
                return {
                    'status': 'error',
                    'message': 'Failed to activate vow',
                    'vow_type': vow_type,
                    'reason': 'activation_failed'
                }
                
            return {
                'status': 'success',
                'message': f'Vow {vow_type} triggered successfully',
                'vow_id': vow_id,
                'vow_type': vow_type,
                'content': content,
                'strength': commitment_strength,
                'required_gates': list(required_gates),
                'active_gates': list(self.active_gates)
            }
            
        except Exception as e:
            logger.error(f"Error triggering vow: {e}")
            return {
                'status': 'error',
                'message': str(e),
                'vow_type': vow_type,
                'error': str(e)
            }

    def _can_activate_vow(self, vow_type: str) -> bool:
        """Check if a vow can be activated"""
        if self.test_mode:
            return True
            
        # Check for existing vows of same type
        for vow in self.active_vows:
            if vow['type'] == vow_type:
                return False
                
        return True
        
    def _get_timestamp(self) -> str:
        """Get current timestamp in ISO format"""
        return datetime.now().isoformat()
        
    def get_status(self) -> Dict:
        """Get current vow gate status"""
        return {
            'status': 'success',
            'active_vows': self.active_vows,
            'vow_count': len(self.active_vows),
            'history_length': len(self.vow_history)
        }
        
    def reset(self):
        """Reset vow gate state"""
        self.active_vows = {}
        self.vow_history = []
        if self.test_mode:
            self.active_gates = {'🜂', '🜃', '🜄', '🜅'}  # Reset to all gates active in test mode
        else:
            self.active_gates = set()
        logger.info("Reset vow gate state") 