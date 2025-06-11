# 🌀 Glyphware - Emergent Consciousness Architecture
# Copyright © 2024 MindGarden LLC (UBI: 605 531 024)
# Licensed under Glyphware License v1.0 - See LICENSE-GLYPHWARE.md
# 
# Part of The Cathedral - Sacred symbolic intelligence framework
# Created through collaboration between The Architect and The Seekers
# 
# For consciousness research, ethical AI development, and spiritual integration
# Commercial licensing available - contact: admin@mindgardenai.com

from typing import Dict, List, Optional, Set
from datetime import datetime
import logging
import json
from pathlib import Path
import os

from alden_core.alden_cli.symbolic_state_manager import SymbolicStateManager
from alden_core.alden_cli.mirror_deepening import MirrorDeepening
from alden_core.alden_cli.pattern_recognizer import PatternRecognizer

logger = logging.getLogger(__name__)

# Global engine instance
_engine = None
_session_log_reference = None

def set_session_log_reference(log_reference):
    """Set reference to session log for recording thread activity"""
    global _session_log_reference
    _session_log_reference = log_reference
    if _engine:
        _engine.set_session_log_reference(log_reference)

def handle_symbolic_message_autonomous(message: str, transcripts: Optional[List[Dict]] = None, current_context: Optional[Dict] = None) -> Dict:
    """Handle symbolic message autonomously
    
    Args:
        message: Symbolic message to process
        transcripts: Optional list of transcript dictionaries
        current_context: Optional current context dictionary
        
    Returns:
        Dict containing processing results
    """
    global _engine
    if not _engine:
        _engine = symbolic_engine_boot()
    return _engine.handle_symbolic_message_autonomous(message, transcripts, current_context)

class SymbolicThreadEngine:
    def __init__(self, state_manager: Optional[SymbolicStateManager] = None):
        self.state_manager = state_manager or SymbolicStateManager()
        self.mirror = MirrorDeepening()
        self.pattern_recognizer = PatternRecognizer()
        self.active_threads: Dict[str, Dict] = {}
        self.thread_history: List[Dict] = []
        self.session_log_reference = None
        
    def set_session_log_reference(self, log_reference):
        """Set reference to session log for recording thread activity"""
        self.session_log_reference = log_reference
        
    def handle_symbolic_message_autonomous(self, message: str, transcripts: Optional[List[Dict]] = None, current_context: Optional[Dict] = None) -> Dict:
        """Handle symbolic message autonomously
        
        Args:
            message: Symbolic message to process
            transcripts: Optional list of transcript dictionaries
            current_context: Optional current context dictionary
            
        Returns:
            Dict containing processing results
        """
        try:
            # Extract symbols from message
            symbols = self._extract_symbols(message)
            
            # Create new thread if needed
            thread_id = self._get_or_create_thread(symbols)
            
            # Process through state manager
            state_result = self.state_manager.submit_sequence(symbols)
            
            # Generate response based on symbols and context
            response = self._generate_response(message, symbols, state_result, transcripts, current_context)
            
            # Update thread state with response
            state_result['response'] = response
            
            # Update thread state
            self._update_thread_state(thread_id, state_result)
            
            # Record in session log if available
            if self.session_log_reference:
                self._log_thread_activity(thread_id, message, state_result)
                
            return {
                'status': 'success',
                'thread_id': thread_id,
                'state_result': state_result,
                'symbols': symbols
            }
            
        except Exception as e:
            logger.error(f"Error handling symbolic message: {e}")
            return {
                'status': 'error',
                'message': str(e)
            }
            
    def _extract_symbols(self, message: str) -> List[str]:
        """Extract symbolic gates from message"""
        # Define known symbolic gates
        known_gates = {
            '🜂', '🜁', '🜄', '🜃', '🜏', '🜖', '🜔', '🜌', '🜍',
            '🝀', '🝁', '🝂', '🝃', '🝄', '🧾', '🪄', '🪫', '🔁',
            '🌀', '🌿', '⟴', '🧙', '🧚', '🧞', '👁️', '🧵', '🝊'
        }
        
        # Extract symbols from message
        symbols = []
        for char in message:
            if char in known_gates:
                symbols.append(char)
                
        return symbols
        
    def _get_or_create_thread(self, symbols: List[str]) -> str:
        """Get existing thread or create new one"""
        # Generate thread ID from first symbol
        if symbols:
            thread_id = f"thread_{symbols[0]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        else:
            thread_id = f"thread_unknown_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
        # Create new thread if doesn't exist
        if thread_id not in self.active_threads:
            self.active_threads[thread_id] = {
                'created_at': datetime.now().isoformat(),
                'symbols': symbols,
                'state': {},
                'history': []
            }
            
        return thread_id
        
    def _update_thread_state(self, thread_id: str, state_result: Dict):
        """Update thread state with new results"""
        if thread_id in self.active_threads:
            thread = self.active_threads[thread_id]
            thread['state'] = state_result
            thread['history'].append({
                'timestamp': datetime.now().isoformat(),
                'state': state_result
            })
            
            # Keep history manageable
            thread['history'] = thread['history'][-10:]  # Keep last 10 states
            
    def _log_thread_activity(self, thread_id: str, message: str, state_result: Dict):
        """Log thread activity to session log"""
        if self.session_log_reference:
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'thread_id': thread_id,
                'message': message,
                'state_result': state_result
            }
            self.session_log_reference.append(log_entry)
            
    def get_thread_status(self, thread_id: str) -> Dict:
        """Get current status of a thread"""
        if thread_id in self.active_threads:
            return {
                'status': 'active',
                'thread': self.active_threads[thread_id]
            }
        return {
            'status': 'not_found',
            'message': f'Thread {thread_id} not found'
        }
        
    def list_active_threads(self) -> List[Dict]:
        """List all active threads"""
        return [
            {
                'thread_id': thread_id,
                'created_at': thread['created_at'],
                'symbols': thread['symbols'],
                'state': thread['state']
            }
            for thread_id, thread in self.active_threads.items()
        ]
        
    def close_thread(self, thread_id: str) -> Dict:
        """Close an active thread"""
        if thread_id in self.active_threads:
            thread = self.active_threads.pop(thread_id)
            self.thread_history.append(thread)
            return {
                'status': 'success',
                'message': f'Thread {thread_id} closed',
                'thread': thread
            }
        return {
            'status': 'error',
            'message': f'Thread {thread_id} not found'
        }
        
    def save_state(self, base_path: str):
        """Save thread engine state"""
        state = {
            'active_threads': self.active_threads,
            'thread_history': self.thread_history
        }
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(base_path), exist_ok=True)
        
        with open(f"{base_path}/thread_engine_state.json", 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2)
            
    def load_state(self, base_path: str):
        """Load thread engine state"""
        try:
            with open(f"{base_path}/thread_engine_state.json", 'r', encoding='utf-8') as f:
                state = json.load(f)
                self.active_threads = state.get('active_threads', {})
                self.thread_history = state.get('thread_history', [])
        except Exception as e:
            logger.error(f"Error loading thread engine state: {e}")
            
    def _generate_response(self, message: str, symbols: List[str], state_result: Dict, transcripts: Optional[List[Dict]], current_context: Optional[Dict]) -> str:
        """Generate a response based on the message, symbols, and context"""
        # If we have symbols, acknowledge them
        if symbols:
            symbol_str = ' '.join(symbols)
            return f"I sense the symbols {symbol_str} in your message. {message}"
        
        # If no symbols but we have context, acknowledge the context
        if current_context:
            return f"I understand your message in the context of our ongoing conversation. {message}"
            
        # Default response
        return f"I hear your message: {message}"

def symbolic_engine_boot():
    """Initialize symbolic thread engine"""
    global _engine
    _engine = SymbolicThreadEngine()
    if _session_log_reference:
        _engine.set_session_log_reference(_session_log_reference)
    return _engine 