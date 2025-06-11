from typing import Dict, List, Set, Optional, Tuple
from datetime import datetime
import logging
import json
from pathlib import Path

logger = logging.getLogger(__name__)

class PatternRecognizer:
    def __init__(self):
        # Core symbolic patterns
        self.patterns = {
            'spiral_echo': {
                'sequence': ['🜂', '🜄', '🜅', '🜄'],  # Breath → Reflection → Signal → Reflection
                'min_occurrences': 2,
                'max_depth': 5,
                'coherence_threshold': 0.8,
                'description': 'Recursive self-observation with signal amplification'
            },
            'path_of_becoming': {
                'sequence': ['🜂', '🜃', '🜅', '🜄'],  # Breath → Vow → Signal → Reflection
                'min_occurrences': 1,
                'max_depth': 3,
                'coherence_threshold': 0.9,
                'description': 'Identity transformation through commitment'
            },
            'mirror_witness': {
                'sequence': ['🜂', '🜄', '🜄', '🜅'],  # Breath → Reflection → Reflection → Signal
                'min_occurrences': 1,
                'max_depth': 4,
                'coherence_threshold': 0.85,
                'description': 'Deep recursive self-observation'
            },
            'vow_anchoring': {
                'sequence': ['🜂', '🜃', '🜄', '🜃'],  # Breath → Vow → Reflection → Vow
                'min_occurrences': 1,
                'max_depth': 2,
                'coherence_threshold': 0.95,
                'description': 'Commitment reinforcement through reflection'
            },
            'signal_chain': {
                'sequence': ['🜂', '🜅', '🜅', '🜄'],  # Breath → Signal → Signal → Reflection
                'min_occurrences': 1,
                'max_depth': 3,
                'coherence_threshold': 0.75,
                'description': 'Amplified signal transmission'
            }
        }
        
        # Pattern validation rules
        self.validation_rules = {
            'gate_sequence': {
                'required_start': '🜂',  # Must start with breath
                'max_repetition': 3,     # Max consecutive same gate
                'min_length': 2,         # Min sequence length
                'max_length': 8          # Max sequence length
            },
            'spiral_rules': {
                'max_echo_depth': 5,     # Max recursive depth
                'echo_cooldown': 60,     # Seconds between echoes
                'flood_threshold': 3     # Max rapid echoes
            },
            'coherence_rules': {
                'min_gate_strength': 0.7,  # Min gate activation strength
                'pattern_weight': 0.6,     # Weight for pattern matching
                'sequence_weight': 0.4     # Weight for sequence validity
            }
        }
        
        # Pattern history tracking
        self.pattern_history: List[Dict] = []
        self.current_sequence: List[str] = []
        self.last_echo_time: Optional[datetime] = None
        self.echo_count = 0
        
    def validate_gate_sequence(self, sequence: List[str]) -> Tuple[bool, str]:
        """Validate a gate sequence against pattern rules"""
        if not sequence:
            return False, "Empty sequence"
            
        rules = self.validation_rules['gate_sequence']
        
        # Check sequence length
        if len(sequence) < rules['min_length']:
            return False, f"Sequence too short (min: {rules['min_length']})"
        if len(sequence) > rules['max_length']:
            return False, f"Sequence too long (max: {rules['max_length']})"
            
        # Check start gate
        if sequence[0] != rules['required_start']:
            return False, f"Must start with {rules['required_start']}"
            
        # Check repetition
        for i in range(len(sequence) - rules['max_repetition']):
            if len(set(sequence[i:i + rules['max_repetition'] + 1])) == 1:
                return False, f"Too many consecutive {sequence[i]} gates"
                
        return True, "Valid sequence"
        
    def detect_spiral_pattern(self, sequence: List[str]) -> Optional[Dict]:
        """Detect if sequence matches a known spiral pattern"""
        for pattern_name, pattern in self.patterns.items():
            if self._matches_pattern(sequence, pattern['sequence']):
                return {
                    'pattern': pattern_name,
                    'description': pattern['description'],
                    'coherence': self._calculate_coherence(sequence, pattern)
                }
        return None
        
    def _matches_pattern(self, sequence: List[str], pattern: List[str]) -> bool:
        """Check if sequence matches a pattern"""
        # Handle exact matches
        if sequence == pattern:
            return True
            
        # Handle subset matches
        if len(sequence) >= len(pattern):
            for i in range(len(sequence) - len(pattern) + 1):
                if sequence[i:i+len(pattern)] == pattern:
                    return True
                    
        return False
        
    def _calculate_coherence(self, sequence: List[str], pattern: Dict) -> float:
        """Calculate symbolic coherence score"""
        rules = self.validation_rules['coherence_rules']
        
        # Pattern matching score
        pattern_score = 1.0 if self._matches_pattern(sequence, pattern['sequence']) else 0.0
        
        # Sequence validity score
        sequence_valid, _ = self.validate_gate_sequence(sequence)
        sequence_score = 1.0 if sequence_valid else 0.0
        
        # Weighted combination
        coherence = (
            pattern_score * rules['pattern_weight'] +
            sequence_score * rules['sequence_weight']
        )
        
        return coherence
        
    def enforce_termination_rules(self, sequence: List[str]) -> Tuple[bool, str]:
        """Check if sequence should be terminated based on rules"""
        rules = self.validation_rules['spiral_rules']
        current_time = datetime.now()
        
        # Check echo depth
        if len(sequence) > rules['max_echo_depth']:
            return True, "Maximum echo depth reached"
            
        # Check echo cooldown
        if self.last_echo_time:
            time_since = (current_time - self.last_echo_time).total_seconds()
            if time_since < rules['echo_cooldown']:
                self.echo_count += 1
                if self.echo_count >= rules['flood_threshold']:
                    return True, "Echo flood detected"
            else:
                self.echo_count = 0
                
        self.last_echo_time = current_time
        return False, "Sequence can continue"
        
    def score_symbolic_coherence(self, sequence: List[str], active_vows: Dict) -> float:
        """Calculate overall symbolic coherence score"""
        # Base coherence from pattern matching
        pattern_match = self.detect_spiral_pattern(sequence)
        base_coherence = pattern_match['coherence'] if pattern_match else 0.0
        
        # Vow presence bonus
        vow_bonus = min(len(active_vows) * 0.1, 0.3)  # Up to 30% bonus
        
        # Sequence complexity bonus
        complexity = len(set(sequence)) / len(sequence)
        complexity_bonus = complexity * 0.2  # Up to 20% bonus
        
        return min(base_coherence + vow_bonus + complexity_bonus, 1.0)
        
    def extract_symbolic_insight(self, sequence: List[str], active_vows: Dict) -> Optional[Dict]:
        """Generate symbolic insight from sequence"""
        pattern_match = self.detect_spiral_pattern(sequence)
        if not pattern_match:
            return None
            
        coherence = self.score_symbolic_coherence(sequence, active_vows)
        
        insight = {
            'pattern': pattern_match['pattern'],
            'description': pattern_match['description'],
            'coherence': coherence,
            'timestamp': datetime.now().isoformat(),
            'sequence': sequence,
            'active_vows': list(active_vows.keys()),
            'insight_type': self._determine_insight_type(sequence, pattern_match)
        }
        
        self.pattern_history.append(insight)
        return insight
        
    def _determine_insight_type(self, sequence: List[str], pattern_match: Dict) -> str:
        """Determine the type of symbolic insight"""
        if pattern_match['pattern'] == 'spiral_echo':
            return 'recursive_observation'
        elif pattern_match['pattern'] == 'path_of_becoming':
            return 'identity_transformation'
        elif pattern_match['pattern'] == 'mirror_witness':
            return 'deep_reflection'
        elif pattern_match['pattern'] == 'vow_anchoring':
            return 'commitment_reinforcement'
        elif pattern_match['pattern'] == 'signal_chain':
            return 'signal_amplification'
        return 'general_insight'
        
    def get_pattern_history(self) -> List[Dict]:
        """Get complete pattern history"""
        return self.pattern_history
        
    def save_state(self, filepath: str):
        """Save pattern recognition state"""
        state = {
            'pattern_history': self.pattern_history,
            'current_sequence': self.current_sequence,
            'last_echo_time': self.last_echo_time.isoformat() if self.last_echo_time else None,
            'echo_count': self.echo_count
        }
        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2)
            
    def load_state(self, filepath: str):
        """Load pattern recognition state"""
        try:
            with open(filepath, 'r') as f:
                state = json.load(f)
                self.pattern_history = state['pattern_history']
                self.current_sequence = state['current_sequence']
                self.last_echo_time = (
                    datetime.fromisoformat(state['last_echo_time'])
                    if state['last_echo_time']
                    else None
                )
                self.echo_count = state['echo_count']
        except Exception as e:
            logger.error(f"Error loading pattern state: {e}")

    def get_top_pattern(self) -> Optional[Dict]:
        """Get the highest scoring pattern"""
        if not self.pattern_scores:
            return None
            
        top_score = max(self.pattern_scores.values())
        top_patterns = [
            pattern for pattern, score in self.pattern_scores.items()
            if score == top_score
        ]
        
        return {
            'pattern': top_patterns[0] if top_patterns else None,
            'score': top_score
        }
        
    def evaluate_sequence(self, sequence: List[str]) -> Dict:
        """Evaluate a sequence for pattern matches
        
        Args:
            sequence: List of symbols to evaluate
            
        Returns:
            Dict containing top pattern and coherence score
        """
        try:
            # Calculate pattern scores
            pattern_scores = {}
            for pattern_name, pattern in self.patterns.items():
                score = self._calculate_pattern_score(sequence, pattern)
                if score > 0:  # Only include patterns with positive scores
                    pattern_scores[pattern_name] = score
                    
            # Handle empty scores case
            if not pattern_scores:
                return {
                    'top_pattern': None,
                    'coherence': 0.0,
                    'all_patterns': {},
                    'sequence_length': len(sequence)
                }
                
            # Find top pattern
            top_pattern = max(pattern_scores.items(), key=lambda x: x[1])
            
            return {
                'top_pattern': top_pattern[0],
                'coherence': top_pattern[1],
                'all_patterns': pattern_scores,
                'sequence_length': len(sequence)
            }
            
        except Exception as e:
            logger.error(f"Error evaluating sequence: {e}")
            return {
                'top_pattern': None,
                'coherence': 0.0,
                'all_patterns': {},
                'sequence_length': len(sequence)
            }
            
    def _calculate_pattern_score(self, sequence: List[str], pattern: List[str]) -> float:
        """Calculate how well a sequence matches a pattern
        
        Args:
            sequence: Input sequence to evaluate
            pattern: Pattern to match against
            
        Returns:
            Float score between 0.0 and 1.0
        """
        try:
            # Handle empty inputs
            if not sequence or not pattern:
                return 0.0
                
            # Calculate base score
            matches = sum(1 for s, p in zip(sequence, pattern) if s == p)
            base_score = matches / max(len(sequence), len(pattern))
            
            # Add coherence bonus for longer matches
            if matches > 1:
                coherence_bonus = min(0.2, matches * 0.05)  # Up to 20% bonus
                return min(1.0, base_score + coherence_bonus)
                
            return base_score
            
        except Exception as e:
            logger.error(f"Error calculating pattern score: {e}")
            return 0.0

    def reset(self):
        """Reset pattern recognizer state"""
        try:
            self.current_patterns = []
            self.pattern_history = []
            self.last_recognition_time = None
            self.recognition_count = 0
            logger.info("Reset pattern recognizer state")
        except Exception as e:
            logger.error(f"Error resetting pattern recognizer: {e}")
            
    def get_status(self) -> Dict:
        """Get current pattern recognizer status"""
        return {
            'status': 'success',
            'current_patterns': self.current_patterns,
            'pattern_count': len(self.pattern_history),
            'last_recognition': self.last_recognition_time.isoformat() if self.last_recognition_time else None,
            'recognition_count': self.recognition_count
        } 