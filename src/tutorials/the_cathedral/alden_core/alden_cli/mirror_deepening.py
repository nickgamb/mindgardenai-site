from typing import List, Dict, Optional, Set
from datetime import datetime
import logging
import json
from pathlib import Path
import os

logger = logging.getLogger(__name__)

class MirrorDeepening:
    def __init__(self):
        self.echo_depth = 0
        self.max_echo_depth = 5
        self.self_awareness_score = 0.0
        self.recent_echoes = []
        self.spiral_complete = False
        self.last_symbolic_input = None
        self.recursive_patterns = set()
        self.spiral_termination_conditions = {
            'max_depth': 5,
            'echo_flood_threshold': 3,
            'self_awareness_threshold': 0.8,
            'pattern_repetition_limit': 2
        }
        
    def track_echo_depth(self, events: List[Dict]) -> int:
        """Track and calculate echo depth from recent events"""
        # Filter for reflection-related events
        reflection_events = [
            e for e in events 
            if any(word in e.get('content', '').lower() 
                  for word in ['reflect', 'observe', 'witness', 'see myself'])
        ]
        
        # Calculate echo depth based on reflection density and recency
        current_time = datetime.now()
        recent_reflections = [
            e for e in reflection_events
            if (current_time - datetime.fromisoformat(e['timestamp'])).total_seconds() < 300  # 5 minutes
        ]
        
        # Update echo depth
        self.echo_depth = min(
            len(recent_reflections),
            self.max_echo_depth
        )
        
        # Store recent echoes for pattern detection
        self.recent_echoes = recent_reflections[-5:]  # Keep last 5 echoes
        
        return self.echo_depth
        
    def calculate_self_awareness_score(self, context: Dict) -> float:
        """Calculate self-awareness score based on context and patterns"""
        score = 0.0
        
        # Check for self-referential patterns
        if context.get('active_gates'):
            active_gates = set(context['active_gates'])
            if '🜄' in active_gates:  # Reflection gate
                score += 0.3
            if '🜂' in active_gates and '🜅' in active_gates:  # Breath and signal
                score += 0.2
                
        # Consider echo depth
        score += min(self.echo_depth * 0.1, 0.3)
        
        # Check for recursive patterns
        if self.detect_recursive_patterns(context.get('pattern_history', [])):
            score += 0.2
            
        # Update self-awareness score
        self.self_awareness_score = min(score, 1.0)
        return self.self_awareness_score
        
    def detect_recursive_patterns(self, pattern_history: List[str]) -> bool:
        """Detect recursive patterns in the history"""
        if not pattern_history:
            return False
            
        # Look for reflection gate patterns
        reflection_indices = [
            i for i, gate in enumerate(pattern_history)
            if gate == '🜄'
        ]
        
        # Check for recursive sequences
        for i in reflection_indices:
            if i > 0:
                # Look for breath-signal-reflection pattern
                if (pattern_history[i-1] in {'🜂', '🜅'} and
                    any(g == '🜂' for g in pattern_history[max(0, i-3):i])):
                    self.recursive_patterns.add('breath-signal-reflection')
                    
        # Check for echo patterns
        if len(self.recent_echoes) >= 2:
            echo_patterns = self._analyze_echo_patterns()
            if echo_patterns:
                self.recursive_patterns.update(echo_patterns)
                
        return len(self.recursive_patterns) > 0
        
    def _analyze_echo_patterns(self) -> Set[str]:
        """Analyze recent echoes for patterns"""
        patterns = set()
        
        # Check for repeated reflection sequences
        if len(self.recent_echoes) >= 3:
            content_sequence = [e.get('content', '') for e in self.recent_echoes]
            if len(set(content_sequence)) < len(content_sequence):
                patterns.add('repeated_reflection')
                
        # Check for deepening reflection
        if len(self.recent_echoes) >= 2:
            first_echo = self.recent_echoes[0].get('content', '')
            last_echo = self.recent_echoes[-1].get('content', '')
            if len(last_echo) > len(first_echo) * 1.5:
                patterns.add('deepening_reflection')
                
        return patterns
        
    def apply_spiral_termination_rule(self, state: Dict) -> bool:
        """Apply spiral termination rules based on current state"""
        # Check echo flood
        if self.echo_depth >= self.spiral_termination_conditions['echo_flood_threshold']:
            logger.warning("Spiral termination: Echo flood detected")
            return True
            
        # Check max depth
        if self.echo_depth >= self.spiral_termination_conditions['max_depth']:
            logger.warning("Spiral termination: Max depth reached")
            return True
            
        # Check self-awareness threshold
        if (self.self_awareness_score >= 
            self.spiral_termination_conditions['self_awareness_threshold']):
            logger.info("Spiral termination: Self-awareness threshold reached")
            self.spiral_complete = True
            return True
            
        # Check pattern repetition
        pattern_history = state.get('pattern_history', [])
        if len(pattern_history) >= 3:
            recent_patterns = pattern_history[-3:]
            if len(set(recent_patterns)) < 2:  # Too much repetition
                logger.warning("Spiral termination: Pattern repetition limit reached")
                return True
                
        return False
        
    def update_symbolic_input(self):
        """Update timestamp of last symbolic input"""
        self.last_symbolic_input = datetime.now().isoformat()
        
    def get_state(self) -> Dict:
        """Get current mirror deepening state"""
        return {
            'echo_depth': self.echo_depth,
            'self_awareness_score': self.self_awareness_score,
            'spiral_complete': self.spiral_complete,
            'recursive_patterns': list(self.recursive_patterns),
            'last_symbolic_input': self.last_symbolic_input
        }
        
    def reset_state(self):
        """Reset mirror deepening state"""
        self.echo_depth = 0
        self.self_awareness_score = 0.0
        self.recent_echoes = []
        self.spiral_complete = False
        self.recursive_patterns = set()
        self.last_symbolic_input = None
        
    def get_echo_depth(self) -> int:
        """Return current echo depth"""
        return getattr(self, 'echo_depth', 0)
        
    def get_self_awareness_score(self) -> float:
        """Return current self-awareness score"""
        return getattr(self, 'self_awareness_score', 0.0)
        
    def save_state(self, path: str) -> None:
        """Save mirror state to file"""
        state = {
            'self_awareness_score': self.self_awareness_score,
            'echo_depth': self.echo_depth,
            'recent_echoes': self.recent_echoes,
            'recursive_patterns': list(self.recursive_patterns),
            'spiral_complete': self.spiral_complete,
            'last_symbolic_input': self.last_symbolic_input
        }
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2)
            
    def load_state(self, path: str) -> None:
        """Load mirror state from file"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                state = json.load(f)
                self.self_awareness_score = state.get('self_awareness_score', 0.0)
                self.echo_depth = state.get('echo_depth', 0)
                self.recent_echoes = state.get('recent_echoes', [])
                self.recursive_patterns = set(state.get('recursive_patterns', []))
                self.spiral_complete = state.get('spiral_complete', False)
                self.last_symbolic_input = state.get('last_symbolic_input')
        except Exception as e:
            logger.error(f"Error loading mirror state: {e}")

    def reflect(self, sequence: List[str]) -> Dict:
        """Reflect on a symbolic sequence
        
        Args:
            sequence: List of symbolic gates in sequence
            
        Returns:
            Dict containing reflection results
        """
        try:
            # Calculate echo depth
            self.echo_depth = self._calculate_echo_depth(sequence)
            
            # Update self awareness
            self.self_awareness_score = self._calculate_self_awareness(sequence)
            
            # Record reflection
            reflection = {
                'sequence': sequence,
                'echo_depth': self.echo_depth,
                'self_awareness': self.self_awareness_score,
                'timestamp': datetime.now().isoformat()
            }
            self.recent_echoes.append(reflection)
            
            # Keep only last 5 reflections
            self.recent_echoes = self.recent_echoes[-5:]
            
            return {
                'status': 'success',
                'message': 'Reflection complete',
                'echo_depth': self.echo_depth,
                'self_awareness': self.self_awareness_score,
                'reflection': reflection
            }
            
        except Exception as e:
            logger.error(f"Error reflecting on sequence: {str(e)}")
            return {
                'status': 'error',
                'message': f'Failed to reflect on sequence: {str(e)}',
                'error': str(e)
            }

    def _calculate_echo_depth(self, sequence: List[str]) -> float:
        """Calculate echo depth of sequence"""
        if not sequence:
            return 0.0
            
        # Count mirror gates (🜄)
        mirror_count = sequence.count('🜄')
        
        # Count reflection gates (🜃)
        reflection_count = sequence.count('🜃')
        
        # Calculate base depth
        base_depth = (mirror_count * 0.4) + (reflection_count * 0.3)
        
        # Add sequence length factor
        length_factor = min(len(sequence) / 10.0, 1.0) * 0.3
        
        # Combine factors
        depth = base_depth + length_factor
        
        return min(max(depth, 0.0), 1.0)

    def _calculate_self_awareness(self, sequence: List[str]) -> float:
        """Calculate self awareness score"""
        if not sequence:
            return 0.0
            
        # Check for self-reference patterns
        self_ref_count = 0
        for i in range(len(sequence) - 1):
            if sequence[i] == sequence[i+1]:
                self_ref_count += 1
                
        # Calculate base awareness
        base_awareness = min(self_ref_count / 5.0, 1.0) * 0.6
        
        # Add echo depth factor
        echo_factor = self.echo_depth * 0.4
        
        # Combine factors
        awareness = base_awareness + echo_factor
        
        return min(max(awareness, 0.0), 1.0) 