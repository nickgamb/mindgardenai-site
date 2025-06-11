import json
from typing import Dict, List, Set, Optional, Any, Callable
from dataclasses import dataclass
from collections import defaultdict
import re
from datetime import datetime
from pathlib import Path
import os
import time

@dataclass
class GateExecution:
    glyph: str
    name: str
    gate_type: str
    result: bool
    function: str
    depth: int
    state_snapshot: Dict[str, bool]

@dataclass
class ExecutionTrace:
    """Represents a single step in symbolic execution"""
    step: int
    gate: str
    name: str
    type: str
    input_state: Dict[str, Any]
    mutation: Dict[str, Any]
    depth: Optional[int] = None
    pattern: Optional[str] = None
    threshold: Optional[int] = None
    timestamp: str = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert trace to dictionary format"""
        return {
            "step": self.step,
            "gate": self.gate,
            "name": self.name,
            "type": self.type,
            "input_state": self.input_state,
            "mutation": self.mutation,
            "depth": self.depth,
            "pattern": self.pattern,
            "threshold": self.threshold,
            "timestamp": self.timestamp
        }

class LogicGate:
    def __init__(self, glyph: str, name: str, gate_type: str, trigger: str, function: str, state_modifiers: Dict[str, str] = None):
        self.glyph = glyph
        self.name = name
        self.gate_type = gate_type
        self.trigger = trigger
        self.function = function
        self.state_modifiers = state_modifiers or {}
        self.activation_count = 0
    
    def evaluate(self, state: Dict[str, bool], depth: int = 0) -> bool:
        try:
            if self.gate_type == 'XOR':
                # XOR: exactly one condition must be true
                conditions = self.trigger.split(' or ')
                true_count = sum(1 for c in conditions if eval(c, {}, state))
                result = true_count == 1
            elif self.gate_type == 'IMPLY':
                # A => B: if A is true, B must be true
                a, b = self.trigger.split(' => ')
                result = not eval(a, {}, state) or eval(b, {}, state)
            elif self.gate_type == 'NAND':
                # NAND: opposite of AND
                result = not eval(self.trigger, {}, state)
            elif self.gate_type == 'THRESHOLD':
                # THRESHOLD: N of K conditions must be true
                match = re.match(r'(\d+) of (\d+): (.+)', self.trigger)
                if match:
                    n, k, conditions = match.groups()
                    conditions = conditions.split(' and ')
                    true_count = sum(1 for c in conditions if eval(c, {}, state))
                    result = true_count >= int(n)
                else:
                    result = False
            else:
                # Standard gates (AND, OR, NOT)
                result = eval(self.trigger, {}, state)

            print(f"{'  ' * depth}🜂 Gate {self.name} ({self.glyph}) [{self.gate_type}] => {'✔' if result else '✘'}")
            return result
        except Exception as e:
            print(f"{'  ' * depth}⚠️ Error evaluating gate {self.name}: {e}")
            return False

    def execute(self, state: Dict[str, bool], depth: int = 0) -> Optional[str]:
        if self.evaluate(state, depth):
            self.activation_count += 1
            return f"{self.function}()"
        return None

    def modify_state(self, state: Dict[str, bool], execution: GateExecution) -> None:
        """Apply state modifications based on gate execution"""
        for modifier in self.state_modifiers.values():
            try:
                # Parse and execute state modification
                if '=' in modifier:
                    var, expr = modifier.split('=')
                    var = var.strip()
                    expr = expr.strip()
                    state[var] = eval(expr, {}, state)
                elif modifier.startswith('toggle:'):
                    var = modifier.split(':')[1].strip()
                    state[var] = not state.get(var, False)
                elif modifier.startswith('set:'):
                    var, val = modifier.split(':')[1].split('=')
                    state[var.strip()] = val.strip().lower() == 'true'
            except Exception as e:
                print(f"⚠️ Error applying state modifier {modifier}: {e}")

class PatternEchoInterface:
    """Interface for loading and processing pattern echoes from conversations and CLI logs"""
    def __init__(self):
        self.pattern_sources = {
            "omni": "omni_conversations/",
            "cli": "alden_cli_session.log",
            "transcripts": "transcripts/"
        }
        self.gate_patterns = {
            "breath": ["🜂", "breath", "inhale", "exhale"],
            "reflection": ["🜄", "reflect", "mirror", "echo"],
            "ethics": ["🜃", "ethics", "virtue", "integrity"],
            "signal": ["🜅", "signal", "resonance", "vibration"],
            "origin": ["🜁", "origin", "source", "beginning"]
        }
        self.pattern_history = []
        self.last_pattern = None
        self.pattern_confidence = 0.0
        self.pattern_context = {}
        self.pattern_weights = {
            "omni": 0.4,
            "cli": 0.3,
            "transcripts": 0.3
        }
        self.min_confidence = 0.6
        self.max_history = 100
        self.pattern_cache = {}
        self.pattern_stats = defaultdict(int)
        self.pattern_transitions = defaultdict(int)
        self.pattern_echoes = defaultdict(list)
        self.pattern_activations = defaultdict(int)
        self.pattern_cooldowns = defaultdict(int)
        self.pattern_priorities = defaultdict(float)
        self.pattern_weights = defaultdict(float)
        self.pattern_scores = defaultdict(float)
        self.pattern_thresholds = defaultdict(int)
        self.pattern_echo_states = defaultdict(bool)
        self.pattern_memory_states = defaultdict(dict)
        self.pattern_signal_states = defaultdict(bool)
        self.pattern_breath_states = defaultdict(int)
        self.pattern_reflection_states = defaultdict(bool)
        self.pattern_ethics_states = defaultdict(int)
        self.pattern_origin_states = defaultdict(bool)
        self.pattern_activation_history = []
        self.pattern_echo_history = []
        self.pattern_memory_history = []
        self.pattern_signal_history = []
        self.pattern_breath_history = []
        self.pattern_reflection_history = []
        self.pattern_ethics_history = []
        self.pattern_origin_history = []
        self.pattern_confidence_history = []
        self.pattern_context_history = []
        self.pattern_weight_history = []
        self.pattern_score_history = []
        self.pattern_threshold_history = []
        self.pattern_echo_state_history = []
        self.pattern_memory_state_history = []
        self.pattern_signal_state_history = []
        self.pattern_breath_state_history = []
        self.pattern_reflection_state_history = []
        self.pattern_ethics_state_history = []
        self.pattern_origin_state_history = []

    def load_patterns_from_source(self, source: str) -> List[str]:
        """Load patterns from a specific source"""
        patterns = []
        try:
            if source == "omni":
                patterns.extend(self._load_from_omni())
            elif source == "cli":
                patterns.extend(self._load_from_cli())
            elif source == "transcripts":
                patterns.extend(self._load_from_transcripts())
        except Exception as e:
            print(f"⚠️ Error loading patterns from {source}: {e}")
        return patterns

    def _load_from_omni(self) -> List[str]:
        """Load patterns from omni conversations"""
        patterns = []
        try:
            omni_dir = Path(self.pattern_sources["omni"])
            if not omni_dir.exists():
                return patterns

            for file in omni_dir.glob("*.json"):
                with open(file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        # Extract patterns from conversation content
                        content = data.get("content", "")
                        patterns.extend(self._extract_patterns(content))
        except Exception as e:
            print(f"⚠️ Error loading from omni: {e}")
        return patterns

    def _load_from_cli(self) -> List[str]:
        """Load patterns from CLI session log"""
        patterns = []
        try:
            cli_log = Path(self.pattern_sources["cli"])
            if not cli_log.exists():
                return patterns

            with open(cli_log, "r", encoding="utf-8") as f:
                for line in f:
                    patterns.extend(self._extract_patterns(line))
        except Exception as e:
            print(f"⚠️ Error loading from CLI: {e}")
        return patterns

    def _load_from_transcripts(self) -> List[str]:
        """Load patterns from transcript files"""
        patterns = []
        try:
            transcript_dir = Path(self.pattern_sources["transcripts"])
            if not transcript_dir.exists():
                return patterns

            for file in transcript_dir.glob("*.txt"):
                with open(file, "r", encoding="utf-8") as f:
                    content = f.read()
                    patterns.extend(self._extract_patterns(content))
        except Exception as e:
            print(f"⚠️ Error loading from transcripts: {e}")
        return patterns

    def _extract_patterns(self, content: str) -> List[str]:
        """Extract patterns from text content"""
        patterns = []
        
        # Extract explicit glyph patterns
        glyph_pattern = re.compile(r'[🜂🜄🜃🜅🜁🜏]')
        patterns.extend(glyph_pattern.findall(content))
        
        # Extract implicit patterns from keywords
        for gate, keywords in self.gate_patterns.items():
            for keyword in keywords:
                if keyword in content.lower():
                    patterns.append(self._get_gate_glyph(gate))
        
        return patterns

    def _get_gate_glyph(self, gate: str) -> str:
        """Get the glyph for a gate type"""
        return self.gate_patterns[gate][0]

    def process_patterns(self, patterns: List[str]) -> Dict[str, Any]:
        """Process extracted patterns and return pattern context"""
        if not patterns:
            return {}

        # Update pattern statistics
        for pattern in patterns:
            self.pattern_stats[pattern] += 1
            if self.last_pattern:
                self.pattern_transitions[(self.last_pattern, pattern)] += 1
            self.last_pattern = pattern

        # Calculate pattern confidence
        total_patterns = sum(self.pattern_stats.values())
        self.pattern_confidence = sum(self.pattern_stats.values()) / (total_patterns or 1)

        # Update pattern context
        context = {
            "patterns": patterns,
            "confidence": self.pattern_confidence,
            "stats": dict(self.pattern_stats),
            "transitions": dict(self.pattern_transitions)
        }

        # Update pattern history
        self.pattern_history.extend(patterns)
        if len(self.pattern_history) > self.max_history:
            self.pattern_history = self.pattern_history[-self.max_history:]

        return context

    def get_pattern_context(self) -> Dict[str, Any]:
        """Get current pattern context"""
        return {
            "history": self.pattern_history,
            "confidence": self.pattern_confidence,
            "stats": dict(self.pattern_stats),
            "transitions": dict(self.pattern_transitions),
            "last_pattern": self.last_pattern
        }

    def inject_pattern(self, pattern: str, source: str = "external") -> None:
        """Inject a pattern from an external source"""
        if pattern in self.gate_patterns.values():
            self.pattern_history.append(pattern)
            self.pattern_stats[pattern] += 1
            if self.last_pattern:
                self.pattern_transitions[(self.last_pattern, pattern)] += 1
            self.last_pattern = pattern
            print(f"🔄 Injected pattern {pattern} from {source}")

    def get_expected_pattern(self) -> List[str]:
        """Get the expected pattern based on history and confidence"""
        if not self.pattern_history:
            return ['🜂', '🜄']  # Default pattern

        # Get most common pattern
        pattern_counts = defaultdict(int)
        for i in range(len(self.pattern_history) - 1):
            pattern = (self.pattern_history[i], self.pattern_history[i + 1])
            pattern_counts[pattern] += 1

        if pattern_counts:
            most_common = max(pattern_counts.items(), key=lambda x: x[1])[0]
            return list(most_common)

        return ['🜂', '🜄']  # Fallback to default

class SymbolicStackEngine:
    def __init__(self, symbol_tags: Dict[str, Any], trace_output: Optional[str] = None):
        self.gates: Dict[str, LogicGate] = self.load_gates(symbol_tags)
        self.max_depth = 10  # Maximum recursion depth
        self.MAX_RECURSION_DEPTH = 5  # Maximum allowed recursion depth for pattern validation
        self.execution_history: List[GateExecution] = []
        self.activation_counts: Dict[str, int] = defaultdict(int)
        self.state_history: List[Dict[str, bool]] = []
        self.trace_output = trace_output
        self.current_step = 0
        self.trace_log = []
        self.pattern_history: List[str] = []  # Track pattern activation order
        self.activation_window: Dict[str, List[int]] = defaultdict(list)  # Sliding window for loop detection
        self.recent_activations: Set[str] = set()  # Track recently activated gates
        self.loop_counter: Dict[str, int] = defaultdict(int)  # Count loops per gate
        self.pattern_window_size = 5  # Size of window for pattern matching
        self.gate_activation_counts: Dict[str, int] = defaultdict(int)  # Track activations per gate
        self.RECURSION_LIMIT = 3  # Maximum allowed activations without state change
        self.state_changes: Dict[str, Dict[str, Any]] = {}  # Track state mutations
        self.gate_cooldowns: Dict[str, int] = defaultdict(int)  # Track gate cooldowns
        self.gate_priorities: Dict[str, int] = defaultdict(lambda: 1)  # Track gate priorities
        self.current_tick = 0  # Track current processing tick
        self.emotional_state = 'neutral'  # Track emotional context
        self.spiral_tension = 0  # Track spiral pattern tension
        self.threshold_pairs: Dict[tuple, int] = defaultdict(int)  # Track gate pair activations
        self.reflection_ready = False  # Track if reflection gate is ready to activate
        self.breath_activation_count = 0  # Track breath gate activations per tick
        self.MAX_BREATH_ACTIVATIONS = 3  # Maximum breath activations per tick
        self.unique_gate_activations: Set[str] = set()  # Track unique gate activations
        self.spiral_begun = False  # Track if spiral pattern has begun
        self.last_gate = None  # Track last activated gate
        self.MAX_REACTIVATIONS = 5  # Maximum reactivations per gate per cycle
        self.MAX_SPIRAL_WINDOW = 10  # Maximum window size for spiral pattern detection
        self.MIN_UNIQUE_GATES = 3  # Minimum unique gates required for valid spiral
        self.gate_reactivation_counts: Dict[str, int] = defaultdict(int)  # Track gate reactivations per cycle
        self.ethics_activation_count = 0  # Track ethics gate activations
        self.MAX_ETHICS_ACTIVATIONS = 3  # Maximum ethics activations before forcing reflection
        self.pattern_cycle_start = 0  # Track start of current pattern cycle
        self.pattern_cycle_gates: Set[str] = set()  # Track gates in current pattern cycle
        self.core_gates = {'🜂', '🜄'}  # Core gates for spiral pattern
        self.secondary_gates = {'🜃', '🜅', '🜁', '🜏'}  # Secondary gates
        self.last_core_activation = None  # Track last core gate activation
        self.test_mode = False  # Test mode flag for isolation
        self.spiral_complete = False  # Track if spiral pattern is complete
        self.echo_state = False  # Track echo state
        self.pattern_echo = PatternEchoInterface()  # Initialize pattern echo interface
        self.external_patterns = []  # Store patterns from external sources
        self.pattern_confidence = 0.0  # Track pattern confidence
        self.pattern_context = {}  # Store pattern context
        self.pattern_weights = {}  # Store pattern weights
        self.pattern_scores = {}  # Store pattern scores
        self.pattern_thresholds = {}  # Store pattern thresholds
        self.pattern_echo_states = {}  # Store pattern echo states
        self.pattern_memory_states = {}  # Store pattern memory states
        self.pattern_signal_states = {}  # Store pattern signal states
        self.pattern_breath_states = {}  # Store pattern breath states
        self.pattern_reflection_states = {}  # Store pattern reflection states
        self.pattern_ethics_states = {}  # Store pattern ethics states
        self.pattern_origin_states = {}  # Store pattern origin states
        self.pattern_activation_history = []  # Store pattern activation history
        self.pattern_echo_history = []  # Store pattern echo history
        self.pattern_memory_history = []  # Store pattern memory history
        self.pattern_signal_history = []  # Store pattern signal history
        self.pattern_breath_history = []  # Store pattern breath history
        self.pattern_reflection_history = []  # Store pattern reflection history
        self.pattern_ethics_history = []  # Store pattern ethics history
        self.pattern_origin_history = []  # Store pattern origin history
        self.pattern_confidence_history = []  # Store pattern confidence history
        self.pattern_context_history = []  # Store pattern context history
        self.pattern_weight_history = []  # Store pattern weight history
        self.pattern_score_history = []  # Store pattern score history
        self.pattern_threshold_history = []  # Store pattern threshold history
        self.pattern_echo_state_history = []  # Store pattern echo state history
        self.pattern_memory_state_history = []  # Store pattern memory state history
        self.pattern_signal_state_history = []  # Store pattern signal state history
        self.pattern_breath_state_history = []  # Store pattern breath state history
        self.pattern_reflection_state_history = []  # Store pattern reflection state history
        self.pattern_ethics_state_history = []  # Store pattern ethics state history
        self.pattern_origin_state_history = []  # Store pattern origin state history
        # Initialize error tracking
        self.error_trace = {}  # Track errors and mismatches
        self.recursion_stack = []  # Track recursion stack
        self.memory_mutations = []  # Track memory mutations
        self.recursion_depth = 0  # Track actual recursion depth
        self.recursion_pattern = []  # Track recursion pattern
        self.recursion_threshold = 0  # Track recursion threshold
        self.recursion_echo = False  # Track recursion echo state
        self.recursion_memory = {}  # Track recursion memory state
        self.recursion_gates = set()  # Track gates in current recursion
        self.recursion_start = None  # Track recursion start time
        self.recursion_complete = False  # Track if recursion is complete
        self.recursion_valid = False  # Track if recursion is valid
        self.recursion_correction_needed = False  # Track if recursion needs correction
        self.recursion_correction_applied = False  # Track if correction was applied
        self.recursion_correction_history = []  # Track correction history
        self.recursion_correction_pattern = []  # Track correction pattern
        self.recursion_correction_state = {}  # Track correction state
        self.recursion_correction_gates = set()  # Track correction gates
        self.recursion_correction_depth = 0  # Track correction depth
        self.recursion_correction_threshold = 0  # Track correction threshold
        self.recursion_correction_echo = False  # Track correction echo
        self.recursion_correction_memory = {}  # Track correction memory
        self.recursion_correction_complete = False  # Track if correction is complete
        self.recursion_correction_valid = False  # Track if correction is valid
        self.recursion_correction_start = None  # Track correction start time
        self.recursion_correction_end = None  # Track correction end time
        self.recursion_correction_duration = 0  # Track correction duration
        self.recursion_correction_count = 0  # Track correction count
        self.recursion_correction_limit = 3  # Track correction limit
        self.recursion_correction_timeout = 1000  # Track correction timeout
        self.recursion_correction_interval = 100  # Track correction interval
        self.recursion_correction_last = None  # Track last correction time
        self.recursion_correction_next = None  # Track next correction time
        self.recursion_correction_active = False  # Track if correction is active
        self.recursion_correction_pending = False  # Track if correction is pending
        self.recursion_correction_queued = False  # Track if correction is queued
        self.recursion_correction_priority = 0  # Track correction priority
        self.recursion_correction_weight = 0  # Track correction weight
        self.recursion_correction_score = 0  # Track correction score
        self.recursion_correction_threshold_score = 0  # Track correction threshold score
        self.recursion_correction_echo_score = 0  # Track correction echo score
        self.recursion_correction_memory_score = 0  # Track correction memory score
        self.recursion_correction_pattern_score = 0  # Track correction pattern score
        self.recursion_correction_gate_score = 0  # Track correction gate score
        self.recursion_correction_depth_score = 0  # Track correction depth score
        self.recursion_correction_time_score = 0  # Track correction time score
        self.recursion_correction_state_score = 0  # Track correction state score
        self.recursion_correction_total_score = 0  # Track correction total score
        self.recursion_correction_best_score = 0  # Track correction best score
        self.recursion_correction_best_pattern = []  # Track correction best pattern
        self.recursion_correction_best_state = {}  # Track correction best state
        self.recursion_correction_best_gates = set()  # Track correction best gates
        self.recursion_correction_best_depth = 0  # Track correction best depth
        self.recursion_correction_best_threshold = 0  # Track correction best threshold
        self.recursion_correction_best_echo = False  # Track correction best echo
        self.recursion_correction_best_memory = {}  # Track correction best memory
        self.recursion_correction_best_time = None  # Track correction best time
        self.recursion_correction_best_duration = 0  # Track correction best duration
        self.recursion_correction_best_count = 0  # Track correction best count
        self.recursion_correction_best_threshold_score = 0  # Track correction best threshold score
        self.recursion_correction_best_echo_score = 0  # Track correction best echo score
        self.recursion_correction_best_memory_score = 0  # Track correction best memory score
        self.recursion_correction_best_pattern_score = 0  # Track correction best pattern score
        self.recursion_correction_best_gate_score = 0  # Track correction best gate score
        self.recursion_correction_best_depth_score = 0  # Track correction best depth score
        self.recursion_correction_best_time_score = 0  # Track correction best time score
        self.recursion_correction_best_state_score = 0  # Track correction best state score
        self.recursion_correction_best_total_score = 0  # Track correction best total score
        self.memory_bootstrapped = False  # Track if memory has been bootstrapped
        self.pattern_lock = False  # Track if pattern is locked
        self.signal_activation_count = 0  # Track signal gate activations
        self.breath_count = 0  # Track breath count
        self.reflection_activated = False  # Track if reflection has been activated
        self.pattern_correction_needed = False  # Track if pattern correction is needed
        self.last_valid_pattern = None  # Track last valid pattern
        self.temporal_depth = 0  # Track temporal depth
        self.expected_pattern = ['🜂', '🜄']  # Default expected pattern
        self.valid_spirals = [  # Define valid spiral patterns
            ['🜂', '🜄'],  # Basic breath-reflection
            ['🜂', '🜃', '🜄'],  # Breath-ethics-reflection
            ['🜂', '🜅', '🜄'],  # Breath-signal-reflection
            ['🜂', '🜁', '🜄'],  # Breath-origin-reflection
            ['🜂', '🜃', '🜅', '🜄'],  # Breath-ethics-signal-reflection
            ['🜂', '🜃', '🜁', '🜄'],  # Breath-ethics-origin-reflection
            ['🜂', '🜅', '🜁', '🜄'],  # Breath-signal-origin-reflection
            ['🜂', '🜃', '🜅', '🜁', '🜄']  # Complete spiral
        ]
        self.simple_mode = True  # Use simple mode by default
        self.MAX_SIGNAL_ACTIVATIONS = 3  # Maximum signal activations
        self.REQUIRED_BREATH_COUNT = 2  # Required breath count for reflection
        self.memory_state = {
            'breath': False,
            'reflection': False,
            'ethics': False,
            'signal': False,
            'origin': False,
            'active': False
        }
        self.pattern_context = None
        self.pattern_confidence = 0.0

    @property
    def default_patterns(self) -> Dict[str, List[str]]:
        """Default symbolic patterns used when no external sources are available"""
        return {
            "spiral": ["🜂", "🜄", "🜂", "🜅"],  # Basic spiral with signal
            "echo_loop": ["🜁", "🜄", "🜁"],  # Origin-reflection-origin loop
            "breath_cycle": ["🜂", "🜃", "🜄"],  # Breath-ethics-reflection
            "signal_chain": ["🜂", "🜅", "🜄", "🜅"],  # Breath-signal-reflection-signal
            "origin_spiral": ["🜂", "🜁", "🜄", "🜁"],  # Breath-origin-reflection-origin
            "ethics_loop": ["🜂", "🜃", "🜄", "🜃"],  # Breath-ethics-reflection-ethics
            "complete_spiral": ["🜂", "🜃", "🜅", "🜁", "🜄"],  # Complete spiral pattern
            "simple_breath": ["🜂", "🜄"],  # Minimal breath-reflection
            "signal_echo": ["🜂", "🜅", "🜄", "🜅", "🜄"],  # Signal echo pattern
            "ethics_chain": ["🜂", "🜃", "🜄", "🜃", "🜄"],  # Ethics chain pattern
            "origin_echo": ["🜂", "🜁", "🜄", "🜁", "🜄"],  # Origin echo pattern
            "breath_signal": ["🜂", "🜅", "🜄"],  # Breath-signal-reflection
            "breath_ethics": ["🜂", "🜃", "🜄"],  # Breath-ethics-reflection
            "breath_origin": ["🜂", "🜁", "🜄"],  # Breath-origin-reflection
            "signal_ethics": ["🜂", "🜅", "🜃", "🜄"],  # Signal-ethics pattern
            "origin_ethics": ["🜂", "🜁", "🜃", "🜄"],  # Origin-ethics pattern
            "signal_origin": ["🜂", "🜅", "🜁", "🜄"],  # Signal-origin pattern
            "triple_echo": ["🜂", "🜄", "🜂", "🜄", "🜂", "🜄"],  # Triple breath-reflection
            "quad_echo": ["🜂", "🜄", "🜂", "🜄", "🜂", "🜄", "🜂", "🜄"],  # Quad breath-reflection
            "penta_echo": ["🜂", "🜄", "🜂", "🜄", "🜂", "🜄", "🜂", "🜄", "🜂", "🜄"],  # Penta breath-reflection
            "hexa_echo": ["🜂", "🜄", "🜂", "🜄", "🜂", "🜄", "🜂", "🜄", "🜂", "🜄", "🜂", "🜄"]  # Hexa breath-reflection
        }

    def preload_symbolic_patterns(self):
        """Load known patterns from memory sources"""
        print("🔄 Preloading symbolic patterns...")
        known = []
        sources_loaded = 0
        
        for source in self.pattern_echo.pattern_weights.keys():
            try:
                if not os.path.exists(source):
                    print(f"ℹ️ Source not found: {source}")
                    continue
                    
                if source.endswith('.json'):
                    with open(source, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        if isinstance(data, dict):
                            patterns = data.get('spiral_pattern', [])
                            if patterns:
                                known.extend(patterns)
                                sources_loaded += 1
                elif source.endswith('.log'):
                    with open(source, "r", encoding="utf-8") as f:
                        for line in f:
                            # Look for pattern markers in log
                            if '🜂' in line or '🜄' in line:
                                pattern = re.findall(r'[🜂🜄🜃🜅🜁🜏]', line)
                                if pattern:
                                    known.append(pattern)
                                    sources_loaded += 1
                elif source.endswith('.py'):
                    with open(source, "r", encoding="utf-8") as f:
                        content = f.read()
                        # Find pattern definitions
                        pattern_matches = re.findall(r'\[.*?\]', content)
                        for match in pattern_matches:
                            if '🜂' in match or '🜄' in match:
                                pattern = re.findall(r'[🜂🜄🜃🜅🜁🜏]', match)
                                if pattern:
                                    known.append(pattern)
                                    sources_loaded += 1
            except Exception as e:
                print(f"⚠️ Error loading patterns from {source}: {e}")
                continue
                
        # If no sources loaded, use default patterns
        if sources_loaded == 0:
            print("ℹ️ No sources loaded, using default patterns")
            known = self.default_patterns
                
        self.bootstrap_patterns = known
        print(f"🔄 Loaded {len(known)} patterns from {sources_loaded} sources")
        return known

    def inject_bootstrap_patterns(self, state: Dict[str, bool]):
        """Inject preloaded patterns into the current state"""
        if not self.memory_bootstrapped and self.bootstrap_patterns:
            print("🔄 Injecting bootstrap patterns...")
            
            # Add patterns to state
            if 'pattern_history' not in state:
                state['pattern_history'] = []
                
            # Add valid patterns to history
            for pattern in self.bootstrap_patterns:
                if self.is_valid_spiral(pattern):
                    state['pattern_history'].extend(pattern)
                    print(f"🔄 Injected pattern: {pattern}")
                    
            # Mark as bootstrapped
            self.memory_bootstrapped = True
            state['memory_bootstrapped'] = True
            print("🔄 Memory bootstrapped with patterns")
            
            # Initialize memory state
            state['memory'] = True
            state['temporal_awareness'] = True
            state['pattern_memory'] = True
            print("🧠 Memory state initialized")

    def mutate_memory_state(self, gate: str, state: Dict[str, bool]) -> None:
        """Mutate memory state based on gate activation"""
        # Track memory mutations
        mutation = {
            'gate': gate,
            'timestamp': time.time(),
            'state_before': state.copy()
        }

        # Update memory state based on gate type
        if gate == '🜂':  # Breath gate
            self.memory_state['breath'] = True
            self.memory_state['active'] = True
            state['memory'] = True
            state['echo'] = True
            # Update recursion state
            self.recursion_memory['memory'] = True
            self.recursion_memory['echo'] = True
            mutation['memory_state'] = self.memory_state.copy()
            mutation['recursion_memory'] = self.recursion_memory.copy()

        elif gate == '🜄':  # Reflection gate
            self.memory_state['reflection'] = True
            self.memory_state['active'] = True
            state['memory'] = True
            state['echo'] = True
            # Update recursion state
            self.recursion_memory['memory'] = True
            self.recursion_memory['echo'] = True
            mutation['memory_state'] = self.memory_state.copy()
            mutation['recursion_memory'] = self.recursion_memory.copy()

        elif gate == '🜃':  # Ethics gate
            self.memory_state['ethics'] = True
            self.memory_state['active'] = True
            state['memory'] = True
            # Update recursion state
            self.recursion_memory['memory'] = True
            mutation['memory_state'] = self.memory_state.copy()
            mutation['recursion_memory'] = self.recursion_memory.copy()

        elif gate == '🜅':  # Signal gate
            self.memory_state['signal'] = True
            self.memory_state['active'] = True
            state['memory'] = True
            state['signal'] = True
            # Update recursion state
            self.recursion_memory['memory'] = True
            self.recursion_memory['signal'] = True
            mutation['memory_state'] = self.memory_state.copy()
            mutation['recursion_memory'] = self.recursion_memory.copy()

        elif gate == '🜁':  # Origin gate
            self.memory_state['origin'] = True
            self.memory_state['active'] = True
            state['memory'] = True
            # Update recursion state
            self.recursion_memory['memory'] = True
            mutation['memory_state'] = self.memory_state.copy()
            mutation['recursion_memory'] = self.recursion_memory.copy()

        # Store mutation in history
        self.memory_mutations.append(mutation)

        # Log memory mutation
        self._log_error('memory.mutation', mutation['memory_state'], mutation['state_before'])

        # Update pattern context if needed
        if self.pattern_context and self.pattern_confidence > 0.8:
            self.pattern_context['memory_state'] = self.memory_state.copy()
            self.pattern_context['recursion_memory'] = self.recursion_memory.copy()

    def _log_error(self, key: str, expected: Any, actual: Any) -> None:
        """Log an error or mismatch in the error trace"""
        self.error_trace[key] = {
            "expected": expected,
            "actual": actual,
            "timestamp": datetime.now().isoformat()
        }
        print(f"⚠️ Error logged: {key} - Expected {expected}, got {actual}")

    def correct_pattern(self, state: Dict[str, bool]) -> None:
        """Correct malformed pattern by forcing reflection gate and ensuring memory persistence"""
        if not self.pattern_correction_needed:
            return
            
        print("🔄 Correcting malformed pattern...")
        
        # Force reflection gate to be ready
        self.reflection_ready = True
        
        # Reset secondary gate counts
        self.signal_activation_count = 0
        self.ethics_activation_count = 0
        
        # Clear recent activations to allow reflection
        self.recent_activations.clear()
        
        # Update state to indicate correction
        state['pattern_correcting'] = True
        
        # Ensure memory state is set
        state['memory'] = True
        state['echo'] = True
        state['signal'] = True
        
        # Update pattern history with correction
        if 'pattern_history' not in state:
            state['pattern_history'] = []
            
        # Add core gates if missing
        if '🜂' not in state['pattern_history']:
            state['pattern_history'].append('🜂')
            self._log_error('pattern_history.breath', 'present', 'missing')
            
        if '🜄' not in state['pattern_history']:
            state['pattern_history'].append('🜄')
            self._log_error('pattern_history.reflection', 'present', 'missing')
            
        # Update active gates
        if 'active_gates' not in state:
            state['active_gates'] = []
        state['active_gates'].extend(['🜂', '🜄'])
        
        # Update recursion state
        self.recursion_echo = True
        self.recursion_memory['memory'] = True
        self.recursion_memory['signal'] = True
        self.recursion_threshold += 1
        
        # Log correction
        self._log_error('pattern_correction', 'applied', 'needed')
        print("🔄 Pattern correction applied with memory persistence")
        
        # Update pattern context
        self.pattern_context = self.pattern_echo.process_patterns(state['pattern_history'])
        self.pattern_confidence = self.pattern_context.get("confidence", 0.0)
        
        # Mark correction as complete
        self.pattern_correction_needed = False
        self.recursion_correction_complete = True
        self.recursion_correction_valid = True
        
        # Update correction history
        self.recursion_correction_history.append({
            'pattern': state['pattern_history'].copy(),
            'memory': state.get('memory', False),
            'echo': state.get('echo', False),
            'signal': state.get('signal', False),
            'timestamp': datetime.now().isoformat()
        })
        
        print("🔄 Pattern correction complete with memory persistence")

    def load_gates(self, tags: Dict) -> Dict[str, LogicGate]:
        """Load gates from symbol tags into a dictionary keyed by glyph"""
        gates = {}
        for glyph, data in tags.items():
            if 'logic_gate' in data and 'trigger_condition' in data:
                gates[glyph] = LogicGate(
                    glyph=glyph,
                    name=data.get('meaning', 'unknown'),
                    gate_type=data.get('logic_gate'),
                    trigger=data.get('trigger_condition'),
                    function=data.get('function', f"function_for_{glyph}"),
                    state_modifiers=data.get('state_modifiers', {})
                )
        return gates

    def reset_gate_states(self):
        """Reset gate states for a new test or tick"""
        self.activation_counts.clear()
        self.activation_window.clear()
        self.recent_activations.clear()
        self.loop_counter.clear()
        self.gate_activation_counts.clear()
        self.gate_cooldowns.clear()
        self.gate_priorities.clear()
        self.pattern_history.clear()
        self.state_changes.clear()
        self.current_tick += 1
        self.emotional_state = 'neutral'
        self.spiral_tension = 0
        self.reflection_ready = False
        self.breath_activation_count = 0
        self.unique_gate_activations.clear()
        self.spiral_begun = False
        self.last_gate = None
        self.gate_reactivation_counts.clear()
        self.ethics_activation_count = 0
        self.pattern_cycle_start = len(self.pattern_history)
        self.pattern_cycle_gates.clear()
        self.last_core_activation = None
        self.spiral_complete = False
        self.echo_state = False
        self.pattern_lock = False
        self.signal_activation_count = 0
        self.breath_count = 0
        self.reflection_activated = False
        self.pattern_correction_needed = False
        self.last_valid_pattern = None
        self.temporal_depth = 0
        self.error_trace.clear()
        self.memory_mutations.clear()
        self.recursion_stack.clear()
        # Update expected pattern from context
        self.expected_pattern = self.pattern_echo.get_expected_pattern()
        self.recursion_depth = 0  # Track actual recursion depth
        self.recursion_pattern = []  # Track recursion pattern
        self.recursion_threshold = 0  # Track recursion threshold
        self.recursion_echo = False  # Track recursion echo state
        self.recursion_memory = {}  # Track recursion memory state
        self.recursion_gates = set()  # Track gates in current recursion
        self.recursion_start = None  # Track recursion start time
        self.recursion_complete = False  # Track if recursion is complete
        self.recursion_valid = False  # Track if recursion is valid
        self.recursion_correction_needed = False  # Track if recursion needs correction
        self.recursion_correction_applied = False  # Track if correction was applied
        self.recursion_correction_history = []  # Track correction history
        self.recursion_correction_pattern = []  # Track correction pattern
        self.recursion_correction_state = {}  # Track correction state
        self.recursion_correction_gates = set()  # Track correction gates
        self.recursion_correction_depth = 0  # Track correction depth
        self.recursion_correction_threshold = 0  # Track correction threshold
        self.recursion_correction_echo = False  # Track correction echo
        self.recursion_correction_memory = {}  # Track correction memory
        self.recursion_correction_complete = False  # Track if correction is complete
        self.recursion_correction_valid = False  # Track if correction is valid
        self.recursion_correction_start = None  # Track correction start time
        self.recursion_correction_end = None  # Track correction end time
        self.recursion_correction_duration = 0  # Track correction duration
        self.recursion_correction_count = 0  # Track correction count
        self.recursion_correction_limit = 3  # Track correction limit
        self.recursion_correction_timeout = 1000  # Track correction timeout
        self.recursion_correction_interval = 100  # Track correction interval
        self.recursion_correction_last = None  # Track last correction time
        self.recursion_correction_next = None  # Track next correction time
        self.recursion_correction_active = False  # Track if correction is active
        self.recursion_correction_pending = False  # Track if correction is pending
        self.recursion_correction_queued = False  # Track if correction is queued
        self.recursion_correction_priority = 0  # Track correction priority
        self.recursion_correction_weight = 0  # Track correction weight
        self.recursion_correction_score = 0  # Track correction score
        self.recursion_correction_threshold_score = 0  # Track correction threshold score
        self.recursion_correction_echo_score = 0  # Track correction echo score
        self.recursion_correction_memory_score = 0  # Track correction memory score
        self.recursion_correction_pattern_score = 0  # Track correction pattern score
        self.recursion_correction_gate_score = 0  # Track correction gate score
        self.recursion_correction_depth_score = 0  # Track correction depth score
        self.recursion_correction_time_score = 0  # Track correction time score
        self.recursion_correction_state_score = 0  # Track correction state score
        self.recursion_correction_total_score = 0  # Track correction total score
        self.recursion_correction_best_score = 0  # Track correction best score
        self.recursion_correction_best_pattern = []  # Track correction best pattern
        self.recursion_correction_best_state = {}  # Track correction best state
        self.recursion_correction_best_gates = set()  # Track correction best gates
        self.recursion_correction_best_depth = 0  # Track correction best depth
        self.recursion_correction_best_threshold = 0  # Track correction best threshold
        self.recursion_correction_best_echo = False  # Track correction best echo
        self.recursion_correction_best_memory = {}  # Track correction best memory
        self.recursion_correction_best_time = None  # Track correction best time
        self.recursion_correction_best_duration = 0  # Track correction best duration
        self.recursion_correction_best_count = 0  # Track correction best count
        self.recursion_correction_best_threshold_score = 0  # Track correction best threshold score
        self.recursion_correction_best_echo_score = 0  # Track correction best echo score
        self.recursion_correction_best_memory_score = 0  # Track correction best memory score
        self.recursion_correction_best_pattern_score = 0  # Track correction best pattern score
        self.recursion_correction_best_gate_score = 0  # Track correction best gate score
        self.recursion_correction_best_depth_score = 0  # Track correction best depth score
        self.recursion_correction_best_time_score = 0  # Track correction best time score
        self.recursion_correction_best_state_score = 0  # Track correction best state score
        self.recursion_correction_best_total_score = 0  # Track correction best total score
        self.memory_bootstrapped = False  # Track if memory has been bootstrapped
        self.pattern_lock = False  # Track if pattern is locked
        self.signal_activation_count = 0  # Track signal gate activations
        self.breath_count = 0  # Track breath count
        self.reflection_activated = False  # Track if reflection has been activated
        self.pattern_correction_needed = False  # Track if pattern correction is needed
        self.last_valid_pattern = None  # Track last valid pattern
        self.temporal_depth = 0  # Track temporal depth
        self.expected_pattern = ['🜂', '🜄']  # Default expected pattern
        self.valid_spirals = [  # Define valid spiral patterns
            ['🜂', '🜄'],  # Basic breath-reflection
            ['🜂', '🜃', '🜄'],  # Breath-ethics-reflection
            ['🜂', '🜅', '🜄'],  # Breath-signal-reflection
            ['🜂', '🜁', '🜄'],  # Breath-origin-reflection
            ['🜂', '🜃', '🜅', '🜄'],  # Breath-ethics-signal-reflection
            ['🜂', '🜃', '🜁', '🜄'],  # Breath-ethics-origin-reflection
            ['🜂', '🜅', '🜁', '🜄'],  # Breath-signal-origin-reflection
            ['🜂', '🜃', '🜅', '🜁', '🜄']  # Complete spiral
        ]
        self.simple_mode = True  # Use simple mode by default
        self.MAX_SIGNAL_ACTIVATIONS = 3  # Maximum signal activations
        self.REQUIRED_BREATH_COUNT = 2  # Required breath count for reflection
        self.memory_state = {
            'breath': False,
            'reflection': False,
            'ethics': False,
            'signal': False,
            'origin': False,
            'active': False
        }
        self.pattern_context = None
        self.pattern_confidence = 0.0

    def check_spiral_tension(self) -> bool:
        """Check if conditions are right for reflection gate activation"""
        breath_count = self.pattern_history.count('🜂')
        reflection_count = self.pattern_history.count('🜄')
        
        # Update spiral tension based on pattern
        if breath_count > reflection_count:
            self.spiral_tension += 1
        else:
            self.spiral_tension = max(0, self.spiral_tension - 1)
            
        # Activate reflection when tension is high enough
        return (self.spiral_tension >= 3 and 
                '🜄' not in self.pattern_history[-3:] and 
                breath_count >= 3)

    def has_threshold_pairs(self, gate_a: str, gate_b: str, count: int) -> bool:
        """Check if a pair of gates has been activated enough times"""
        pair = (gate_a, gate_b)
        return self.threshold_pairs[pair] >= count

    def update_threshold_pairs(self, gate: str):
        """Update threshold pair counts when a gate activates"""
        if len(self.pattern_history) > 0:
            prev_gate = self.pattern_history[-1]
            pair = (prev_gate, gate)
            self.threshold_pairs[pair] += 1

    def check_pattern_match(self, pattern_history: List[str]) -> bool:
        """Check if the pattern history matches the expected spiral pattern using fuzzy matching"""
        if len(pattern_history) < 2:
            return False
            
        # Check for presence of both breath and reflection gates
        has_breath = '🜂' in pattern_history
        has_reflection = '🜄' in pattern_history
        
        if not (has_breath and has_reflection):
            return False
            
        # Check that breath appears before reflection
        breath_index = pattern_history.index('🜂')
        reflection_index = pattern_history.index('🜄')
        
        if breath_index >= reflection_index:
            return False
            
        # Check for minimum number of unique gates activated
        if len(self.unique_gate_activations) < 2:
            return False
            
        # Verify the pattern is valid for echo
        required_pattern = ['🜂', '🜄']
        if not all(g in pattern_history for g in required_pattern):
            return False
            
        # Log pattern matching details
        print(f"🜂 Pattern check: breath at {breath_index}, reflection at {reflection_index}")
        print(f"🜂 Unique gates: {self.unique_gate_activations}")
        print(f"🜂 Pattern history: {pattern_history}")
        
        return True

    def is_valid_spiral(self, pattern: List[str]) -> bool:
        """Check if a pattern matches any valid spiral form"""
        # Filter out secondary gates for comparison
        core_pattern = [gate for gate in pattern if gate in self.core_gates]
        
        # Check against valid spirals
        for valid_spiral in self.valid_spirals:
            if core_pattern == valid_spiral:
                return True
                
        # Check if pattern contains a valid spiral as a subsequence
        for valid_spiral in self.valid_spirals:
            if self.contains_subsequence(pattern, valid_spiral):
                return True
                
        return False

    def contains_subsequence(self, pattern: List[str], subsequence: List[str]) -> bool:
        """Check if pattern contains subsequence in order"""
        if not subsequence:
            return True
        if not pattern:
            return False
            
        # Find first occurrence of first element
        try:
            start = pattern.index(subsequence[0])
            # Recursively check rest of subsequence
            return self.contains_subsequence(pattern[start+1:], subsequence[1:])
        except ValueError:
            return False

    def check_spiral_pattern(self, state: Dict[str, bool]) -> bool:
        """Check if the current state matches the spiral pattern requirements"""
        # Early termination if already detected
        if self.spiral_complete or self.pattern_lock:
            print("🌀 Spiral pattern already complete and locked")
            return True

        # Get recent pattern history
        recent = state.get('pattern_history', [])[-self.MAX_SPIRAL_WINDOW:]
        
        # Check if pattern needs correction
        if not self.is_valid_spiral(recent):
            print("⚠️ Malformed pattern detected")
            self.pattern_correction_needed = True
            self.correct_pattern(state)
            return False

        # Check for minimum unique gates
        unique_gates = set(recent)
        if len(unique_gates) < self.MIN_UNIQUE_GATES:
            print(f"⚠️ Insufficient unique gates: {len(unique_gates)} < {self.MIN_UNIQUE_GATES}")
            return False

        # Check for excessive ethics gate activations
        if recent.count('🜃') > self.MAX_ETHICS_ACTIVATIONS:
            print(f"⚠️ Excessive ethics gate activations detected: {recent.count('🜃')} > {self.MAX_ETHICS_ACTIVATIONS}")
            self.pattern_correction_needed = True
            self.correct_pattern(state)
            return False

        # Check for core spiral pattern
        core_sequence = [gate for gate in recent if gate in self.core_gates]
        if len(core_sequence) >= 2:
            # Verify breath appears before reflection
            breath_index = core_sequence.index('🜂')
            reflection_index = core_sequence.index('🜄')
            if breath_index < reflection_index:
                # In simple mode, only accept the minimal pattern
                if self.simple_mode:
                    if len(core_sequence) == 2 and core_sequence == self.expected_pattern:
                        print(f"🌀 Simple spiral pattern complete: {core_sequence}")
                        self.spiral_complete = True
                        self.pattern_lock = True
                        self.last_valid_pattern = core_sequence
                        # Update pattern history
                        self.pattern_echo.update_pattern_history(core_sequence)
                        return True
                else:
                    # In complex mode, accept any valid spiral
                    if self.is_valid_spiral(core_sequence):
                        print(f"🌀 Complex spiral pattern complete: {core_sequence}")
                        self.spiral_complete = True
                        self.pattern_lock = True
                        self.last_valid_pattern = core_sequence
                        # Update pattern history
                        self.pattern_echo.update_pattern_history(core_sequence)
                        return True

        return False

    def should_activate_gate(self, gate: str, state: Dict[str, bool]) -> bool:
        """Determine if a gate should activate based on symbolic context"""
        # Skip if pattern is locked
        if self.pattern_lock:
            print("🔒 Pattern locked: skipping gate activation")
            return False

        # Skip secondary gates in test mode
        if self.test_mode and gate in self.secondary_gates:
            print(f"⏭️ Skipping secondary gate {gate} in test mode")
            return False

        # Check if spiral is already complete
        if self.spiral_complete:
            print("🌀 Spiral complete: skipping gate activation")
            return False

        # Check cooldown
        if self.gate_cooldowns[gate] > self.current_tick:
            print(f"⏸️ Gate {gate} in cooldown until tick {self.gate_cooldowns[gate]}")
            return False

        # Check reactivation count
        if self.gate_reactivation_counts[gate] >= self.MAX_REACTIVATIONS:
            print(f"⏸️ Gate {gate} exceeded max reactivations ({self.MAX_REACTIVATIONS})")
            return False

        # Special handling for reflection gate
        if gate == '🜄':
            # Skip if reflection has already been activated in this cycle
            if self.reflection_activated:
                print("⏭️ Skipping reflection gate - already activated in this cycle")
                return False
            # Activate reflection if we have enough breath activations
            if self.breath_count >= self.REQUIRED_BREATH_COUNT:
                print("🜄 Activating reflection gate - breath count reached")
                self.reflection_activated = True
                return True
            # Activate reflection if signal or ethics limits reached
            if self.signal_activation_count >= self.MAX_SIGNAL_ACTIVATIONS or self.ethics_activation_count >= self.MAX_ETHICS_ACTIVATIONS:
                print("🜄 Activating reflection gate - secondary gate limits reached")
                self.reflection_activated = True
                return True
            # Activate reflection if pattern correction is needed
            if self.pattern_correction_needed:
                print("🜄 Activating reflection gate - pattern correction needed")
                self.reflection_activated = True
                return True
            return False

        # Special handling for breath gate
        if gate == '🜂':
            if self.breath_activation_count >= self.MAX_BREATH_ACTIVATIONS:
                print(f"⏸️ Breath gate activation limit reached ({self.breath_activation_count})")
                return False
            # Skip redundant breath gate if spiral has begun and we're waiting for reflection
            if self.spiral_begun and self.last_gate == '🜂' and not self.reflection_activated:
                print(f"⏭️ Skipping redundant breath gate after spiral begun")
                return False
            self.breath_activation_count += 1
            self.breath_count += 1
            return True

        # Special handling for signal gate
        if gate == '🜅':
            if self.signal_activation_count >= self.MAX_SIGNAL_ACTIVATIONS:
                print(f"⏸️ Signal gate activation limit reached ({self.signal_activation_count})")
                return False
            # Skip signal gate if we have enough breath activations and reflection is pending
            if self.breath_count >= self.REQUIRED_BREATH_COUNT and not self.reflection_activated:
                print("⏭️ Skipping signal gate - enough breath activations")
                return False
            self.signal_activation_count += 1
            return True

        # Special handling for ethics gate
        if gate == '🜃':
            if self.ethics_activation_count >= self.MAX_ETHICS_ACTIVATIONS:
                print(f"⏸️ Ethics gate activation limit reached ({self.ethics_activation_count})")
                return False
            # Skip ethics gate in simple mode
            if self.simple_mode:
                print("⏭️ Skipping ethics gate in simple mode")
                return False
            # Only allow ethics gate if a core gate has activated since last ethics activation
            if self.last_gate == '🜃' and self.last_core_activation != '🜂':
                print("⏭️ Skipping ethics gate - no core gate activation since last ethics")
                return False
            self.ethics_activation_count += 1
            return True

        # Check recent pattern history
        if len(self.pattern_history) >= 3 and gate in self.pattern_history[-3:]:
            print(f"⏭️ Gate {gate} recently activated")
            return False

        # Gate-specific symbolic context checks
        if gate == '🜂':  # Breath gate
            return self.emotional_state in ['calm', 'neutral']
        elif gate == '🜃':  # Ethics gate
            return state.get('breath', False) and self.emotional_state != 'chaotic'
        elif gate == '🜄':  # Reflection gate
            return self.reflection_ready or ('🜃' in state.get('active_gates', []) and not self.reflection_ready)
        elif gate == '🜏':  # Creativity gate
            return state.get('reflection', False) and self.emotional_state != 'stagnant'
        elif gate == '🜖':  # Persistence gate
            return state.get('creativity', False) and self.gate_priorities[gate] > 0
        elif gate == '🜁':  # Origin gate
            return not (state.get('memory', False) and state.get('signal', False))

        return True

    def detect_loops(self, current_gate: str, current_state: Dict[str, bool], new_state: Dict[str, bool]) -> bool:
        """Detect if a gate has been activated too many times using a sliding window and state change detection"""
        current_time = len(self.state_history)
        
        # Update activation window
        self.activation_window[current_gate].append(current_time)
        
        # Remove activations older than window size
        window_size = 5  # Allow more activations before detecting loops
        if self.state_history and self.state_history[-1].get('pattern') == 'spiral':
            window_size = 8  # Even more lenient for spiral patterns
        
        self.activation_window[current_gate] = [
            t for t in self.activation_window[current_gate] 
            if current_time - t < window_size
        ]
        
        # Check if state actually changed
        state_changed = False
        for key in set(current_state.keys()) | set(new_state.keys()):
            if current_state.get(key) != new_state.get(key):
                state_changed = True
                break
        
        if not state_changed:
            self.gate_activation_counts[current_gate] += 1
            if self.gate_activation_counts[current_gate] > self.RECURSION_LIMIT:
                # Instead of halting, reduce priority and add cooldown
                self.gate_priorities[current_gate] -= 1
                self.gate_cooldowns[current_gate] = self.current_tick + 3
                print(f"{'  ' * len(self.state_history)}⚠️ Throttling {current_gate} due to state stagnation")
                return True
        else:
            # Reset activation count and restore priority on valid state change
            self.gate_activation_counts[current_gate] = 0
            self.gate_priorities[current_gate] = 1
            
        # Check activation frequency in window
        if len(self.activation_window[current_gate]) > window_size - 1:
            self.loop_counter[current_gate] += 1
            print(f"{'  ' * len(self.state_history)}⚠️ Loop detected for gate {self.gates[current_gate].name} ({current_gate}) - {len(self.activation_window[current_gate])} activations in window")
            
            # Instead of halting, add cooldown
            if self.loop_counter[current_gate] > 2:
                self.gate_cooldowns[current_gate] = self.current_tick + 5
                self.gate_priorities[current_gate] = max(0, self.gate_priorities[current_gate] - 1)
                print(f"{'  ' * len(self.state_history)}⏸️ Cooling down {current_gate} for 5 ticks")
                return True
                
            return True
            
        return False

    def log_trace(self, gate: str, name: str, gate_type: str, 
                 input_state: Dict[str, Any], mutation: Dict[str, Any],
                 depth: Optional[int] = None, pattern: Optional[str] = None,
                 threshold: Optional[int] = None) -> None:
        """Log a single execution trace"""
        trace = ExecutionTrace(
            step=self.current_step,
            gate=gate,
            name=name,
            type=gate_type,
            input_state=input_state.copy(),
            mutation=mutation.copy(),
            depth=depth,
            pattern=pattern,
            threshold=threshold
        )
        self.trace_log.append(trace)
        self.current_step += 1

    def save_trace(self) -> None:
        """Save execution trace to file"""
        if not self.trace_output:
            return

        trace_data = [trace.to_dict() for trace in self.trace_log]
        with open(self.trace_output, 'w', encoding='utf-8') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "traces": trace_data
            }, f, indent=2)

    def check_recursion_pattern(self, state: Dict[str, bool]) -> bool:
        """Check if the current recursion pattern is valid"""
        # Initialize recursion pattern if needed
        if not hasattr(self, 'recursion_pattern'):
            self.recursion_pattern = []
        if not hasattr(self, 'recursion_depth'):
            self.recursion_depth = 0
        if not hasattr(self, 'recursion_memory'):
            self.recursion_memory = {'memory': False, 'echo': False, 'signal': False}

        # Check if we have a valid pattern
        if not self.recursion_pattern:
            self._log_error('recursion.pattern', 'valid', 'empty')
            return False

        # Check for minimum pattern length
        if len(self.recursion_pattern) < 2:
            self._log_error('recursion.pattern', 'valid', 'too_short')
            return False

        # Check for maximum recursion depth
        if self.recursion_depth > self.MAX_RECURSION_DEPTH:
            self._log_error('recursion.depth', self.MAX_RECURSION_DEPTH, self.recursion_depth)
            return False

        # Check for core gates
        has_breath = '🜂' in self.recursion_pattern
        has_reflection = '🜄' in self.recursion_pattern
        if not (has_breath and has_reflection):
            self._log_error('recursion.core_gates', 'present', 'missing')
            return False

        # Check for valid gate sequence
        for i in range(len(self.recursion_pattern) - 1):
            current = self.recursion_pattern[i]
            next_gate = self.recursion_pattern[i + 1]
            
            # Check for invalid consecutive gates
            if current == next_gate:
                self._log_error('recursion.consecutive', 'different', 'same')
                return False
            
            # Check for invalid gate transitions
            if current == '🜄' and next_gate == '🜂':  # Reflection -> Breath
                self._log_error('recursion.transition', 'valid', 'invalid')
                return False
            if current == '🜅' and next_gate == '🜃':  # Signal -> Ethics
                self._log_error('recursion.transition', 'valid', 'invalid')
                return False

        # Check memory state
        if not self.recursion_memory['memory']:
            self._log_error('recursion.memory', 'active', 'inactive')
            return False

        # Check echo state for reflection gate
        if '🜄' in self.recursion_pattern and not self.recursion_memory['echo']:
            self._log_error('recursion.echo', 'active', 'inactive')
            return False

        # Check signal state for signal gate
        if '🜅' in self.recursion_pattern and not self.recursion_memory['signal']:
            self._log_error('recursion.signal', 'active', 'inactive')
            return False

        # Pattern is valid
        return True

    def correct_recursion_pattern(self, state: Dict[str, bool]) -> None:
        """Correct the recursion pattern if needed"""
        if not self.recursion_correction_needed:
            return

        # Log correction attempt
        self._log_error('recursion.correction', 'started', 'needed')

        # Initialize correction state if needed
        if not hasattr(self, 'recursion_correction_applied'):
            self.recursion_correction_applied = False
        if not hasattr(self, 'recursion_correction_score'):
            self.recursion_correction_score = 0.0

        # Check if correction is already applied
        if self.recursion_correction_applied:
            self._log_error('recursion.correction', 'already_applied', 'duplicate')
            return

        # Ensure we have a valid pattern to correct
        if not self.recursion_pattern:
            # Initialize with default pattern if empty
            self.recursion_pattern = ['🜂', '🜄']
            self._log_error('recursion.correction', 'initialized', 'empty')
            corrections_applied = True
        else:
            corrections_applied = False

        # Store original pattern for comparison
        original_pattern = self.recursion_pattern.copy()
        original_depth = self.recursion_depth
        original_memory = self.recursion_memory.copy()

        # Apply corrections based on error trace
        # Fix missing core gates
        if '🜂' not in self.recursion_pattern:
            self.recursion_pattern.insert(0, '🜂')
            corrections_applied = True
            self._log_error('recursion.correction', 'added_breath', 'missing')

        if '🜄' not in self.recursion_pattern:
            self.recursion_pattern.append('🜄')
            corrections_applied = True
            self._log_error('recursion.correction', 'added_reflection', 'missing')

        # Fix invalid gate transitions
        i = 0
        while i < len(self.recursion_pattern) - 1:
            current = self.recursion_pattern[i]
            next_gate = self.recursion_pattern[i + 1]
            
            if current == next_gate:
                # Remove duplicate gate
                self.recursion_pattern.pop(i + 1)
                corrections_applied = True
                self._log_error('recursion.correction', 'removed_duplicate', 'found')
                continue
            
            if current == '🜄' and next_gate == '🜂':
                # Swap invalid transition
                self.recursion_pattern[i], self.recursion_pattern[i + 1] = self.recursion_pattern[i + 1], self.recursion_pattern[i]
                corrections_applied = True
                self._log_error('recursion.correction', 'fixed_transition', 'invalid')
                continue
            
            if current == '🜅' and next_gate == '🜃':
                # Swap invalid transition
                self.recursion_pattern[i], self.recursion_pattern[i + 1] = self.recursion_pattern[i + 1], self.recursion_pattern[i]
                corrections_applied = True
                self._log_error('recursion.correction', 'fixed_transition', 'invalid')
                continue
            
            i += 1

        # Fix memory state
        if not self.recursion_memory['memory']:
            self.recursion_memory['memory'] = True
            state['memory'] = True
            corrections_applied = True
            self._log_error('recursion.correction', 'fixed_memory', 'inactive')

        # Fix echo state for reflection gate
        if '🜄' in self.recursion_pattern and not self.recursion_memory['echo']:
            self.recursion_memory['echo'] = True
            state['echo'] = True
            corrections_applied = True
            self._log_error('recursion.correction', 'fixed_echo', 'inactive')

        # Fix signal state for signal gate
        if '🜅' in self.recursion_pattern and not self.recursion_memory['signal']:
            self.recursion_memory['signal'] = True
            state['signal'] = True
            corrections_applied = True
            self._log_error('recursion.correction', 'fixed_signal', 'inactive')

        # Update recursion depth if needed
        if self.recursion_depth > self.MAX_RECURSION_DEPTH:
            self.recursion_depth = self.MAX_RECURSION_DEPTH
            corrections_applied = True
            self._log_error('recursion.correction', 'fixed_depth', 'exceeded')

        # Calculate correction score
        if corrections_applied:
            # Calculate similarity between original and corrected pattern
            pattern_similarity = 0.0
            if original_pattern and self.recursion_pattern:
                intersection = len(set(original_pattern) & set(self.recursion_pattern))
                union = len(set(original_pattern) | set(self.recursion_pattern))
                pattern_similarity = intersection / union if union > 0 else 0.0
            
            # Calculate memory state similarity
            memory_similarity = 0.0
            if original_memory and self.recursion_memory:
                matching_keys = sum(1 for k in original_memory if k in self.recursion_memory and original_memory[k] == self.recursion_memory[k])
                total_keys = len(set(original_memory.keys()) | set(self.recursion_memory.keys()))
                memory_similarity = matching_keys / total_keys if total_keys > 0 else 0.0
            
            # Calculate depth similarity
            depth_similarity = 0.0
            if original_depth > 0 or self.recursion_depth > 0:
                max_depth = max(original_depth, self.recursion_depth)
                depth_similarity = 1.0 - abs(original_depth - self.recursion_depth) / max_depth if max_depth > 0 else 0.0
            
            # Combine scores with weights
            self.recursion_correction_score = (
                0.4 * pattern_similarity +
                0.4 * memory_similarity +
                0.2 * depth_similarity
            )
            
            # Mark correction as applied
            self.recursion_correction_applied = True
            self.recursion_correction_needed = False
            
            # Log successful correction
            self._log_error('recursion.correction', 'completed', {
                'score': self.recursion_correction_score,
                'original_pattern': original_pattern,
                'corrected_pattern': self.recursion_pattern,
                'original_depth': original_depth,
                'corrected_depth': self.recursion_depth,
                'original_memory': original_memory,
                'corrected_memory': self.recursion_memory
            })
        else:
            # Log no corrections needed
            self._log_error('recursion.correction', 'no_changes', 'needed')

    def evaluate_gate(self, gate: str, state: Dict[str, bool], depth: int = 0) -> Dict[str, bool]:
        """Evaluate a single logic gate and return state changes"""
        if gate not in self.gates:
            print(f"{'  ' * depth}⚠️ Gate {gate} not found")
            self._log_error('gate.evaluation', 'found', 'not_found')
            return {}

        # Skip if pattern is locked
        if self.pattern_lock:
            print(f"{'  ' * depth}🔒 Pattern locked: skipping gate evaluation")
            return {}

        # Skip if gate was recently activated
        if gate in self.recent_activations:
            print(f"{'  ' * depth}⏭️ Skipping recently activated gate {gate}")
            return {}

        # Ensure state has required fields
        if 'active_gates' not in state:
            state['active_gates'] = []
        if 'pattern_history' not in state:
            state['pattern_history'] = []
        if 'pattern' not in state:
            state['pattern'] = 'spiral'  # Default to spiral pattern
        if 'threshold_count' not in state:
            state['threshold_count'] = 0
        if 'echo' not in state:
            state['echo'] = False
        if 'memory' not in state:
            state['memory'] = False
        if 'signal' not in state:
            state['signal'] = False

        # Bootstrap memory if needed
        if not self.memory_bootstrapped:
            self.preload_symbolic_patterns()
            self.inject_bootstrap_patterns(state)

        # Update temporal depth
        self.temporal_depth = depth
        self.recursion_stack.append(gate)

        gate_info = self.gates[gate]
        gate_type = gate_info.gate_type
        name = gate_info.name
        
        # Log pre-evaluation state
        self.log_trace(
            gate=gate,
            name=name,
            gate_type=gate_type,
            input_state=state.copy(),
            mutation={},
            depth=depth
        )

        # First evaluate if the gate should activate
        if not gate_info.evaluate(state, depth):
            return {}

        # Add to recent activations and unique gates
        self.recent_activations.add(gate)
        self.unique_gate_activations.add(gate)
        self.last_gate = gate
        self.gate_reactivation_counts[gate] += 1
        self.pattern_cycle_gates.add(gate)

        # Update last core activation if this is a core gate
        if gate in self.core_gates:
            self.last_core_activation = gate

        # Gate activated - apply mutations based on type
        mutation = {}
        state_changes = {}  # Track state changes for this gate

        # Handle memory mutations
        self.mutate_memory_state(gate, state)

        # Special handling for reflection gate (🜄)
        if gate == '🜄':
            # Ensure reflection gate is added to active gates and pattern history
            if gate not in state['active_gates']:
                state['active_gates'].append(gate)
                state_changes['active_gates'] = {'added': gate}
            if not state['pattern_history'] or state['pattern_history'][-1] != gate:
                state['pattern_history'].append(gate)
                state_changes['pattern_history'] = {'added': gate}
            mutation['active_gates'] = state['active_gates'].copy()
            mutation['pattern_history'] = state['pattern_history'].copy()
            # Reset reflection ready flag and ethics count
            self.reflection_ready = False
            self.ethics_activation_count = 0
            # Update recursion state
            self.recursion_echo = True
            self.recursion_memory['memory'] = True
            self.recursion_memory['signal'] = True
            # Ensure memory state is set
            state['memory'] = True
            state['echo'] = True
            state['signal'] = True
            print(f"{'  ' * depth}🜂 Reflection gate activated: {state['pattern_history']}")

        # For spiral pattern, include all activated gates in active_gates
        if state.get('pattern') == 'spiral':
            if gate not in state['active_gates']:
                state['active_gates'].append(gate)
                state_changes['active_gates'] = {'added': gate}
            mutation['active_gates'] = state['active_gates'].copy()
            mutation['pattern'] = 'spiral'
            
            # Update pattern history, ensuring no consecutive duplicates
            if not state['pattern_history'] or state['pattern_history'][-1] != gate:
                state['pattern_history'].append(gate)
                state_changes['pattern_history'] = {'added': gate}
                # Update threshold pairs
                self.update_threshold_pairs(gate)
            mutation['pattern_history'] = state['pattern_history'].copy()
            
            # Mark spiral as begun when breath gate activates
            if gate == '🜂':
                self.spiral_begun = True
                # Update recursion state
                self.recursion_threshold += 1
                self.recursion_memory['memory'] = True
                # Ensure memory state is set
                state['memory'] = True
                state['echo'] = True
            
            # Check for pattern match using window
            if self.check_spiral_pattern(state):
                mutation['spiral_complete'] = True
                state_changes['spiral_complete'] = {'from': False, 'to': True}
                # Set echo to true when spiral pattern is complete
                mutation['echo'] = True
                state_changes['echo'] = {'from': False, 'to': True}
                self.echo_state = True
                # Update recursion state
                self.recursion_complete = True
                self.recursion_valid = True
                # Ensure memory state is set
                state['memory'] = True
                state['signal'] = True
                print(f"{'  ' * depth}🜂 Spiral pattern complete: {state['pattern_history']}")
                print(f"{'  ' * depth}🜂 Echo state set to true")
                return mutation  # Return immediately when spiral is complete

        # Apply state modifications from the gate's state_modifiers
        for modifier in gate_info.state_modifiers.values():
            try:
                if isinstance(modifier, dict):
                    # Handle dictionary-style modifiers
                    for key, value in modifier.items():
                        if key == 'inputs' or key == 'outputs':
                            continue
                        # Don't overwrite pattern state if it's spiral
                        if key == 'pattern' and state.get('pattern') == 'spiral':
                            continue
                        if state.get(key) != value:
                            mutation[key] = value
                            state_changes[key] = {'from': state.get(key), 'to': value}
                elif isinstance(modifier, str):
                    # Handle string-style modifiers
                    if '=' in modifier:
                        var, expr = modifier.split('=')
                        var = var.strip()
                        expr = expr.strip()
                        
                        # Don't overwrite pattern state if it's spiral
                        if var == 'pattern' and state.get('pattern') == 'spiral':
                            continue
                        
                        # Handle boolean literals
                        if expr.lower() == 'true':
                            new_value = True
                        elif expr.lower() == 'false':
                            new_value = False
                        else:
                            # Try to evaluate as a Python expression
                            try:
                                new_value = eval(expr, {}, state)
                            except:
                                # If evaluation fails, use the string value
                                new_value = expr
                                
                        if state.get(var) != new_value:
                            mutation[var] = new_value
                            state_changes[var] = {'from': state.get(var), 'to': new_value}
                    elif modifier.startswith('toggle:'):
                        var = modifier.split(':')[1].strip()
                        new_value = not state.get(var, False)
                        mutation[var] = new_value
                        state_changes[var] = {'from': state.get(var, False), 'to': new_value}
                    elif modifier.startswith('set:'):
                        var, val = modifier.split(':')[1].split('=')
                        var = var.strip()
                        val = val.strip()
                        
                        # Don't overwrite pattern state if it's spiral
                        if var == 'pattern' and state.get('pattern') == 'spiral':
                            continue
                        
                        # Handle boolean literals
                        if val.lower() == 'true':
                            new_value = True
                        elif val.lower() == 'false':
                            new_value = False
                        else:
                            # Try to evaluate as a Python expression
                            try:
                                new_value = eval(val, {}, state)
                            except:
                                # If evaluation fails, use the string value
                                new_value = val
                                
                        if state.get(var) != new_value:
                            mutation[var] = new_value
                            state_changes[var] = {'from': state.get(var), 'to': new_value}
            except Exception as e:
                print(f"{'  ' * depth}⚠️ Error applying state modifier {modifier}: {e}")
                self.error_trace.append({
                    'gate': gate,
                    'modifier': modifier,
                    'error': str(e),
                    'depth': depth
                })

        # Store state changes for this gate
        if state_changes:
            self.state_changes[gate] = state_changes

        # Log post-evaluation state with enriched trace data
        self.log_trace(
            gate=gate,
            name=name,
            gate_type=gate_type,
            input_state=state.copy(),
            mutation=mutation.copy(),
            depth=depth,
            pattern=gate_info.state_modifiers.get('pattern'),
            threshold=gate_info.state_modifiers.get('threshold')
        )

        # Attempt pattern correction if needed
        if self.test_mode and self.error_trace:
            self.correct_pattern_on_failure(state)

        # Update recursion tracking
        self.recursion_depth = depth
        self.recursion_pattern.append(gate)
        self.recursion_gates.add(gate)

        # Check recursion pattern
        if not self.check_recursion_pattern(state):
            self.recursion_correction_needed = True
            self.correct_recursion_pattern(state)

        # Update pattern context
        if gate in self.external_patterns:
            self.pattern_context = self.pattern_echo.process_patterns([gate])
            self.pattern_confidence = self.pattern_context.get("confidence", 0.0)
            print(f"🔄 Updated pattern context with confidence {self.pattern_confidence:.2f}")

        return mutation

    def run(self, input_state: Dict[str, bool], depth: int = 0) -> List[str]:
        if depth > self.max_depth:
            print(f"{'  ' * depth}⚠️ Maximum recursion depth reached")
            return []

        # Reset gate states at the start of each run
        if depth == 0:
            self.reset_gate_states()

        # Initialize pattern state if not present
        if 'pattern' not in input_state:
            input_state['pattern'] = 'spiral'  # Default to spiral pattern
        if 'active_gates' not in input_state:
            input_state['active_gates'] = []
        if 'pattern_history' not in input_state:
            input_state['pattern_history'] = []

        # Check if spiral pattern is already complete
        if self.spiral_complete or self.pattern_lock:
            print(f"{'  ' * depth}🜂 Spiral pattern already complete and locked, terminating")
            return []

        # Clear recent activations at start of each recursion level
        self.recent_activations.clear()

        activated = []
        for gate in self.gates.values():
            # Skip if pattern is locked
            if self.pattern_lock:
                print(f"{'  ' * depth}🔒 Pattern locked: skipping gate evaluation")
                break

            # Skip relationship gate if we're in spiral pattern
            if gate.glyph == '🜔' and input_state.get('pattern') == 'spiral':
                continue

            # Check symbolic context before evaluation
            if not self.should_activate_gate(gate.glyph, input_state):
                continue

            # Evaluate gate and get state changes
            mutation = self.evaluate_gate(gate.glyph, input_state, depth)
            if mutation:
                # Check for loops after evaluation
                if self.detect_loops(gate.glyph, input_state, mutation):
                    print(f"{'  ' * depth}⚠️ Loop detected for gate {gate.name} ({gate.glyph})")
                    continue

                # Only increment activation count after successful evaluation
                self.activation_counts[gate.glyph] += 1
                
                execution = GateExecution(
                    glyph=gate.glyph,
                    name=gate.name,
                    gate_type=gate.gate_type,
                    result=True,
                    function=gate.function,
                    depth=depth,
                    state_snapshot=input_state.copy()
                )
                self.execution_history.append(execution)
                activated.append(f"{gate.function}()")

                # Apply state modifications
                input_state.update(mutation)
                
                # Force persist pattern state
                if 'pattern' in mutation:
                    input_state['pattern'] = mutation['pattern']
                if 'active_gates' in mutation:
                    input_state['active_gates'] = mutation['active_gates'].copy()
                if 'pattern_history' in mutation:
                    input_state['pattern_history'] = mutation['pattern_history'].copy()
                
                # Save state snapshot after mutations
                self.state_history.append(input_state.copy())
                
                # Print debug info for state changes
                print(f"{'  ' * depth}🜂 State changes: {mutation}")
                
                # Check if spiral pattern is complete
                if mutation.get('spiral_complete', False):
                    print(f"{'  ' * depth}🜂 Spiral pattern complete, terminating recursion")
                    return activated
                
                # Recursive execution with modified state
                if depth < self.max_depth:
                    activated.extend(self.run(input_state.copy(), depth + 1))

        # Save trace if output path is specified
        if self.trace_output:
            self.save_trace()

        return activated

    def get_execution_trace(self) -> str:
        """Generate a formatted execution trace"""
        trace = []
        for execution in self.execution_history:
            indent = '  ' * execution.depth
            trace.append(f"{indent}🜂 Gate {execution.name} ({execution.glyph}) [{execution.gate_type}] => ✔")
            trace.append(f"{indent}  {execution.function}()")
            # Add state changes
            if execution.depth > 0:
                prev_state = self.state_history[execution.depth - 1]
                changes = {k: v for k, v in execution.state_snapshot.items() 
                          if k in prev_state and prev_state[k] != v}
                if changes:
                    trace.append(f"{indent}  State changes: {changes}")
        return '\n'.join(trace)

    def generate_mermaid_diagram(self) -> str:
        """Generate a Mermaid diagram of the execution flow"""
        diagram = ["graph TD"]
        node_style = "style {0} fill:#f9f,stroke:#333,stroke-width:2px"
        
        # Track node appearances for highlighting
        node_appearances = defaultdict(int)
        
        for i, execution in enumerate(self.execution_history):
            node_id = execution.glyph
            node_appearances[node_id] += 1
            
            # Create node with activation count
            label = f"{execution.glyph} {execution.name}"
            if node_appearances[node_id] > 1:
                label += f" ({node_appearances[node_id]})"
                diagram.append(f"    {node_id}[\"{label}\"]:::repeated")
            else:
                diagram.append(f"    {node_id}[\"{label}\"]")
            
            # Add edge from previous node
            if i > 0:
                prev_node = self.execution_history[i-1].glyph
                diagram.append(f"    {prev_node} --> {execution.glyph}")
        
        # Add styles
        diagram.append("\n    classDef repeated fill:#f96,stroke:#333,stroke-width:2px")
        
        return '\n'.join(diagram)

    def rollback_state(self, depth: int) -> Optional[Dict[str, bool]]:
        """Roll back to a previous state"""
        if 0 <= depth < len(self.state_history):
            return self.state_history[depth].copy()
        return None

    def debug_gate_state(self):
        """Print debug information about gate states"""
        print("\n=== GATE STATE DEBUG ===")
        for g in self.gates.values():
            print(f"{g.glyph}: {g.name} ({g.gate_type}) -> Trigger: {g.trigger} | Activations: {self.activation_counts[g.glyph]}")
        print("=======================\n")

    def load_external_patterns(self) -> None:
        """Load patterns from external sources"""
        print("🔄 Loading external patterns...")
        
        # Load from all sources
        for source, weight in self.pattern_echo.pattern_weights.items():
            patterns = self.pattern_echo.load_patterns_from_source(source)
            if patterns:
                self.external_patterns.extend(patterns)
                print(f"🔄 Loaded {len(patterns)} patterns from {source}")
        
        # Process patterns
        if self.external_patterns:
            self.pattern_context = self.pattern_echo.process_patterns(self.external_patterns)
            self.pattern_confidence = self.pattern_context.get("confidence", 0.0)
            print(f"🔄 Processed {len(self.external_patterns)} patterns with confidence {self.pattern_confidence:.2f}")

    def inject_external_pattern(self, pattern: str, source: str = "external") -> None:
        """Inject a pattern from an external source"""
        self.pattern_echo.inject_pattern(pattern, source)
        self.external_patterns.append(pattern)
        print(f"🔄 Injected pattern {pattern} from {source}")

    def get_expected_pattern(self) -> List[str]:
        """Get the expected pattern based on external sources"""
        if self.external_patterns:
            return self.pattern_echo.get_expected_pattern()
        return ['🜂', '🜄']  # Default pattern

if __name__ == "__main__":
    # Example symbolic input state
    input_state = {
        "breath": True,
        "memory": True,
        "signal": True,
        "echo": False
    }

    # Load symbol tags
    with open("symbol_tags.json", "r", encoding="utf-8") as f:
        tags = json.load(f)

    engine = SymbolicStackEngine(tags)
    result = engine.run(input_state)

    print("\n=== CATHEDRAL STACK TRACE ===")
    print(engine.get_execution_trace())
    
    print("\n=== EXECUTION FLOW ===")
    print(engine.generate_mermaid_diagram()) 