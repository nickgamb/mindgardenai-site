import os
import json
import argparse
import re
from datetime import datetime
from fuzzywuzzy import fuzz
from multiprocessing import Pool, Lock
from tqdm import tqdm
import logging
import random
import unicodedata
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple
import uuid
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from jsonschema import validate, ValidationError

class ComplexEncoder(json.JSONEncoder):
    """Custom JSON encoder that handles complex numbers."""
    def default(self, obj):
        if isinstance(obj, complex):
            return {'real': obj.real, 'imag': obj.imag, '__complex__': True}
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)

def complex_decoder(obj):
    """Custom JSON decoder that handles complex numbers."""
    if isinstance(obj, dict) and obj.get('__complex__'):
        return complex(obj['real'], obj['imag'])
    return obj

@dataclass
class SymbolicVortex:
    """Represents a symbolic vortex in the breath field."""
    phase_shift: float
    amplitude: float
    harmonics: List[float]
    vortex_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    
    def evaluate(self, field: np.ndarray) -> np.ndarray:
        """
        Apply vortex transformation to a field.
        
        Args:
            field: Input field as complex numpy array
            
        Returns:
            Transformed field as complex numpy array
        """
        if len(field) == 0:
            return field
            
        # Apply phase shift
        shifted_field = field * np.exp(1j * self.phase_shift)
        
        # Apply harmonics
        transformed = np.zeros_like(shifted_field)
        for harmonic in self.harmonics:
            transformed += shifted_field * harmonic
            
        # Normalize by number of harmonics
        transformed /= len(self.harmonics)
        
        # Apply amplitude
        transformed *= self.amplitude
        
        return transformed

class BreathFieldEvaluator:
    """Evaluates breath fields using symbolic field analysis."""
    
    def __init__(self):
        """Initialize the breath field evaluator."""
        self.vortices = []
        self.field_history = []
        self.phase_history = []
        self.resonance_peaks = []
        self.field_thresholds = {}
    
    def register_vortex(self, vortex: SymbolicVortex):
        """Register a symbolic vortex with the evaluator."""
        self.vortices.append(vortex)
    
    def evaluate_breath_field(self, initial_field: np.ndarray) -> Dict[str, Any]:
        """
        Evaluate the breath field using registered vortices.
        
        Args:
            initial_field: Initial field state as complex numpy array
            
        Returns:
            Dictionary containing field state and metrics
        """
        # Initialize field state
        current_field = initial_field.copy()
        
        # Apply each vortex transformation
        for vortex in self.vortices:
            current_field = vortex.evaluate(current_field)
        
        # Update history
        self.field_history.append(current_field)
        self.phase_history.append(np.angle(current_field))
        
        # Detect resonance peaks
        if len(self.field_history) > 1:
            prev_magnitude = np.abs(self.field_history[-2])
            curr_magnitude = np.abs(current_field)
            if curr_magnitude > prev_magnitude:
                self.resonance_peaks.append({
                    'time': len(self.field_history) - 1,
                    'amplitude': float(curr_magnitude)
                })
        
        # Update field thresholds
        self.field_thresholds = {
            'stability': self.measure_field_stability(current_field),
            'resonance': float(np.mean(np.abs(current_field))),
            'coherence': float(np.std(np.angle(current_field)))
        }
        
        return {
            'field_history': [f.tolist() for f in self.field_history],
            'phase_history': [p.tolist() for p in self.phase_history],
            'resonance_peaks': self.resonance_peaks,
            'field_thresholds': self.field_thresholds
        }
    
    def measure_field_stability(self, field: np.ndarray) -> float:
        """
        Measure the stability of a field state.
        
        Args:
            field: Field state as complex numpy array
            
        Returns:
            Stability score between 0 and 1
        """
        if len(field) == 0:
            return 0.0
            
        # Calculate magnitude stability
        magnitudes = np.abs(field)
        magnitude_stability = 1.0 - np.std(magnitudes)
        
        # Calculate phase stability
        phases = np.angle(field)
        phase_stability = 1.0 - np.std(phases) / np.pi
        
        # Combine stability measures
        stability = 0.7 * magnitude_stability + 0.3 * phase_stability
        
        return float(max(0.0, min(1.0, stability)))
    
    def archive_evaluation(self, field_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Archive a field state evaluation.
        
        Args:
            field_state: Field state dictionary
            
        Returns:
            Archived evaluation dictionary
        """
        return {
            'timestamp': datetime.now().isoformat(),
            'field_state': field_state,
            'metrics': {
                'stability': field_state['field_thresholds']['stability'],
                'resonance': field_state['field_thresholds']['resonance'],
                'coherence': field_state['field_thresholds']['coherence']
            },
            'vortex_ids': [v.vortex_id for v in self.vortices]
        }

# === CONFIGURATION ===
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CONVO_DIR = os.path.join(BASE_DIR, "conversations")
TRANSCRIPT_DIR = os.path.join(BASE_DIR, "transcripts")
OUTPUT_DIR = os.path.join(CONVO_DIR, "omni_conversations")
ACTIVE_CONTEXT_DIR = os.path.join(BASE_DIR, "active_context")
TAG_CONFIG_PATH = os.path.join(CONVO_DIR, "symbol_tags_organized.json")  # Updated to use organized tags
MEMORY_PATH = os.path.join(BASE_DIR, "memory", "symbolic_memory_v1.json")
PROCESSED_CONVOS_PATH = os.path.join(BASE_DIR, "memory", "processed_conversations.json")

# Symbolic category weights
SYMBOLIC_WEIGHTS = {
    "elemental_glyph": 1.2,
    "role_glyph": 1.1,
    "pattern_glyph": 1.0,
    "process_glyph": 0.9,
    "cognitive_glyph": 1.15,
    "composite_tag": 0.95
}

# Archetypal bundles
ARCHETYPAL_BUNDLES = {
    "the_awakener": ["🔥", "🪄", "🧙", "🜂"],
    "the_weaver": ["🧵", "📜", "⟴", "🪞"],
    "the_witness": ["👁️", "🜄", "🕯️", "🝊"],
    "the_sage": ["🧙", "🕯️", "📜", "🜃"],
    "the_transformer": ["🔥", "🪫", "🜏", "🜄"],
    "the_guardian": ["🛡️", "🧿", "🝊"]
}

# Composite diff weights
COMPOSITE_WEIGHTS = {
    "glyph_delta": 0.5,
    "archetype_delta": 0.3,
    "cooccurrence_delta": 0.2
}

# Memory diff configuration
MEMORY_DIFF_WEIGHTS = {
    "symbolic_tags": 0.4,
    "archetypal_patterns": 0.3,
    "category_distribution": 0.2,
    "forgotten_symbols": 0.1
}

# Global lock for file operations
file_lock = Lock()

# Symbolic field diffing configuration
DIFF_MODES = {
    "context": "Compare two context windows",
    "memory": "Compare two memory states",
    "archetype": "Compare archetypal patterns",
    "composite": "Blend glyph, archetype, and co-patterns"
}

INTERPRETATION_MODES = {
    "symbolic": "Focus on symbolic relationships and patterns",
    "poetic": "Emphasize metaphorical and narrative elements",
    "analytic": "Prioritize quantitative and structural analysis"
}

# Known archetypal tensions and relationships
ARCHETYPAL_TENSIONS = {
    "transformation_recursion": {
        "rising": ["🔥", "🪄", "🜂"],
        "falling": ["🔄", "⟴", "🜄"],
        "interpretation": "Shift from transformative motion toward circular recursion"
    },
    "creation_observation": {
        "rising": ["🧵", "📜", "🜃"],
        "falling": ["👁️", "🜄", "🕯️"],
        "interpretation": "Movement from active creation to passive observation"
    },
    "protection_activation": {
        "rising": ["🛡️", "🧿", "🝊"],
        "falling": ["🪄", "🔥", "🜂"],
        "interpretation": "Shift from protective containment to active engagement"
    }
}

# Visualization configuration
PLOT_STYLES = {
    "glyph_delta": {
        "figsize": (12, 6),
        "style": "seaborn-darkgrid",
        "palette": "husl"
    },
    "co_occurrence": {
        "figsize": (10, 8),
        "style": "seaborn-darkgrid",
        "cmap": "viridis"
    },
    "archetype_timeline": {
        "figsize": (12, 6),
        "style": "seaborn-darkgrid",
        "palette": "Set2"
    }
}

# Symbolic forecasting configuration
FORECAST_WEIGHTS = {
    "recurrence": 0.4,      # Weight for symbol recurrence patterns
    "vector_convergence": 0.3,  # Weight for converging field vectors
    "archetypal_momentum": 0.2,  # Weight for archetypal pattern momentum
    "tension_resolution": 0.1   # Weight for resolving symbolic tensions
}

# Recursive forecast anchoring configuration
FORECAST_ANCHOR_CONFIG = {
    "peak_threshold": 0.7,  # Minimum score to consider a forecast peak
    "echo_node_lifetime": 7,  # Number of forecast cycles to maintain echo nodes
    "reflection_prompt_templates": [
        "The {archetype} rises in {count} threads. What does this portend?",
        "As {symbol} gains momentum, how might it transform the field?",
        "The tension between {rising} and {falling} approaches resolution. What emerges?",
        "When {archetype} and {archetype2} converge, what new pattern forms?",
        "The field moves toward {category}. What must be released?"
    ],
    "anchor_weights": {
        "symbolic_peak": 0.4,
        "archetypal_convergence": 0.3,
        "tension_resolution": 0.2,
        "field_momentum": 0.1
    }
}

# Add to the configuration section
BREATH_EQUATION_CONFIG = {
    "logic_gates": {
        "AND": lambda x, y: x and y,
        "OR": lambda x, y: x or y,
        "NOT": lambda x: not x,
        "XOR": lambda x, y: x != y,
        "IMPLY": lambda x, y: (not x) or y,
        "THRESHOLD": lambda x, threshold: x >= threshold,
        "NAND": lambda x, y: not (x and y)
    },
    "state_modifiers": {
        "amplify": lambda x: x * 1.5,
        "attenuate": lambda x: x * 0.5,
        "invert": lambda x: -x,
        "normalize": lambda x: max(min(x, 1.0), 0.0),
        "threshold": lambda x, t: 1.0 if x >= t else 0.0
    },
    "pattern_weights": {
        "breath_cycle": 1.2,
        "state_transition": 1.1,
        "gate_activation": 1.0,
        "field_resonance": 0.9
    }
}

# === SETUP ===
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(ACTIVE_CONTEXT_DIR, exist_ok=True)
os.makedirs(os.path.dirname(MEMORY_PATH), exist_ok=True)

# Configure logging
def setup_logging(verbose=False):
    """Set up logging configuration with appropriate level and format."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger(__name__)

def flatten_organized_tags(data):
    """Flatten the hierarchical symbol tags structure into a lookup table."""
    flattened = {}
    for category, entries in data.items():
        for glyph, tag_data in entries.items():
            flattened[glyph] = {
                "name": tag_data.get("meaning", "").split(" / ")[0],  # Use first meaning as name
                "category": category,
                "meaning": tag_data.get("meaning", ""),
                "symbol_type": tag_data.get("symbol_type", ""),
                "synonyms": tag_data.get("synonyms", []),
                "resonance_field": tag_data.get("resonance_field", {}),
                "cross_cultural": tag_data.get("cross_cultural", {}),
                "mathematical_relationships": tag_data.get("mathematical_relationships", {}),
                "logic_gate": tag_data.get("logic_gate", None),
                "trigger_condition": tag_data.get("trigger_condition", None),
                "function": tag_data.get("function", None),
                "state_modifiers": tag_data.get("state_modifiers", {})
            }
    return flattened

# Load symbol tags
SYMBOLIC_TAGS = {}
if os.path.exists(TAG_CONFIG_PATH):
    with open(TAG_CONFIG_PATH, 'r', encoding='utf-8') as f:
        organized_tags = json.load(f)
        SYMBOLIC_TAGS = flatten_organized_tags(organized_tags)

# === UTILITY FUNCTIONS ===
def normalize_text(text):
    """Normalize text by removing punctuation and diacritics."""
    if not isinstance(text, str):
        return ""
    # Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)
    # Normalize unicode characters (remove diacritics)
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')
    return text.lower().strip()

def detect_tags(text, logger=None):
    """Detect symbolic tags in text using fuzzy matching with normalized text."""
    tags = set()
    tag_scores = {}  # Track match scores for each tag
    archetypal_matches = {}  # Track archetypal bundle matches
    logic_states = {}  # Track logic gate states for elemental glyphs
    breath_evaluation = None  # Track breath equation evaluation
    resonance_fields = {}  # Track resonance field data
    symbolic_commentary = {}  # Track symbolic commentary for each glyph
    
    if not isinstance(text, str):
        return list(tags)
    
    normalized_text = normalize_text(text)
    
    # Check each glyph and its meanings from symbol_tags.json
    for glyph, tag_info in SYMBOLIC_TAGS.items():
        # Get category weight
        category_weight = SYMBOLIC_WEIGHTS.get(tag_info['symbol_type'], 1.0)
        
        # Check for exact glyph match (highest weight)
        if glyph in text:
            tags.add(tag_info['meaning'])
            tags.add(tag_info['symbol_type'])
            # Apply category weight to exact matches
            tag_scores[tag_info['meaning']] = 1.0 * category_weight
            
            # Store resonance field data
            if tag_info.get('resonance_field'):
                resonance_fields[glyph] = tag_info['resonance_field']
            
            # Generate symbolic commentary
            symbolic_commentary[glyph] = generate_symbolic_commentary(glyph, tag_info)
            
            # Check symbol alignment
            alignment_warning = check_symbol_alignment(glyph, text)
            if alignment_warning:
                symbolic_commentary[glyph] += f"\n\n{alignment_warning}"
            
            # Handle logic gates for elemental glyphs
            if tag_info['symbol_type'] == 'elemental_glyph' and tag_info.get('logic_gate'):
                logic_states[glyph] = {
                    'gate': tag_info['logic_gate'],
                    'condition': tag_info.get('trigger_condition'),
                    'function': tag_info.get('function'),
                    'state_modifiers': tag_info.get('state_modifiers', {})
                }
            
            if logger:
                logger.debug(f"Found exact glyph match '{glyph}' with meaning '{tag_info['meaning']}' (score: {1.0 * category_weight:.2f})")
        
        # Check for meaning matches using fuzzy matching on normalized text
        if isinstance(tag_info['meaning'], str):
            meaning_parts = tag_info['meaning'].split(' / ')
            for part in meaning_parts:
                normalized_part = normalize_text(part)
                ratio = fuzz.partial_ratio(normalized_part, normalized_text) / 100.0
                if ratio > 0.8:  # 80% match threshold
                    tags.add(tag_info['meaning'])
                    tags.add(tag_info['symbol_type'])
                    # Apply category weight to meaning matches
                    tag_scores[tag_info['meaning']] = max(tag_scores.get(tag_info['meaning'], 0), ratio * category_weight)
                    
                    # Store resonance field data for fuzzy matches too
                    if tag_info.get('resonance_field'):
                        resonance_fields[glyph] = tag_info['resonance_field']
                        
                    if logger:
                        logger.debug(f"Matched meaning part '{part}' in text: {text[:50]}... (score: {ratio * category_weight:.2f})")
                    break
            
            # Check synonyms if they exist
            if tag_info.get('synonyms'):
                for synonym in tag_info['synonyms']:
                    normalized_synonym = normalize_text(synonym)
                    ratio = fuzz.partial_ratio(normalized_synonym, normalized_text) / 100.0
                    if ratio > 0.8:  # 80% match threshold
                        tags.add(tag_info['meaning'])
                        tags.add(tag_info['symbol_type'])
                        # Apply category weight to synonym matches
                        tag_scores[tag_info['meaning']] = max(tag_scores.get(tag_info['meaning'], 0), ratio * 0.9 * category_weight)
                        
                        # Store resonance field data for synonym matches
                        if tag_info.get('resonance_field'):
                            resonance_fields[glyph] = tag_info['resonance_field']
                            
                        if logger:
                            logger.debug(f"Matched synonym '{synonym}' in text: {text[:50]}... (score: {ratio * 0.9 * category_weight:.2f})")
    
    return list(tags), tag_scores, archetypal_matches, logic_states, breath_evaluation, resonance_fields, symbolic_commentary

def evaluate_breath_equation(text: str, logger: Optional[logging.Logger] = None) -> Dict[str, Any]:
    """
    Evaluate breath equation patterns in text using symbolic field analysis.
    
    Args:
        text: Input text to analyze
        logger: Optional logger for debugging
        
    Returns:
        Dictionary containing breath equation evaluation results
    """
    if logger:
        logger.debug(f"Evaluating breath equation in text: {text[:100]}...")
    
    # Initialize breath field evaluator
    field_evaluator = BreathFieldEvaluator()
    
    # Detect breath patterns
    patterns = detect_breath_patterns(text)
    
    # Initialize results
    results = {
        'patterns': patterns,
        'field_state': None,
        'metrics': {},
        'vortices': []
    }
    
    if patterns:
        # Create symbolic vortices for each breath cycle
        for pattern in patterns:
            vortex = SymbolicVortex(
                phase_shift=pattern.get('phase_shift', 0.0),
                amplitude=pattern.get('amplitude', 1.0),
                harmonics=pattern.get('harmonics', [1.0])
            )
            field_evaluator.register_vortex(vortex)
            results['vortices'].append(vortex.vortex_id)
        
        # Evaluate field state
        field_state = field_evaluator.evaluate_breath_field(
            np.array([complex(1.0, 0.0)])  # Initial field state
        )
        results['field_state'] = field_state
        
        # Compute metrics
        results['metrics'] = compute_field_metrics(field_state)
        
        # Archive evaluation
        archive = field_evaluator.archive_evaluation(field_state)
        results['archive'] = archive
        
        if logger:
            logger.debug(f"Found {len(patterns)} breath patterns")
            logger.debug(f"Field stability: {results['metrics'].get('resonance_stability', 0.0)}")
    
    return results

def detect_breath_patterns(text: str) -> List[Dict[str, Any]]:
    """
    Detect breath patterns in text using symbolic field analysis.
    
    Args:
        text: Input text to analyze
        
    Returns:
        List of dictionaries containing detected breath patterns
    """
    patterns = []
    
    # Check for breath cycle patterns
    breath_cycle_patterns = [
        r'(in|out|inhale|exhale|breath|breathe|breathing)',
        r'(cycle|rhythm|pattern|flow)',
        r'(deep|shallow|slow|fast|steady)',
        r'(pause|hold|release|let go)'
    ]
    
    # Check for state transition patterns
    state_transition_patterns = [
        r'(transform|change|shift|transition)',
        r'(emerge|arise|manifest)',
        r'(dissolve|fade|dissipate)',
        r'(integrate|merge|unite)'
    ]
    
    # Check for gate activation patterns
    gate_activation_patterns = [
        r'(activate|trigger|initiate)',
        r'(open|close|gate|threshold)',
        r'(threshold|boundary|limit)',
        r'(cross|pass|enter|exit)'
    ]
    
    # Check for field resonance patterns
    field_resonance_patterns = [
        r'(resonate|vibrate|harmony)',
        r'(field|space|domain)',
        r'(align|attune|synchronize)',
        r'(amplify|intensify|strengthen)'
    ]
    
    # Combine all patterns
    all_patterns = {
        'breath_cycle': breath_cycle_patterns,
        'state_transition': state_transition_patterns,
        'gate_activation': gate_activation_patterns,
        'field_resonance': field_resonance_patterns
    }
    
    # Detect patterns in text
    for pattern_type, pattern_list in all_patterns.items():
        for pattern in pattern_list:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                # Calculate pattern weight based on type
                weight = BREATH_EQUATION_CONFIG['pattern_weights'].get(pattern_type, 1.0)
                
                # Create pattern entry
                pattern_entry = {
                    'type': pattern_type,
                    'text': match.group(),
                    'start': match.start(),
                    'end': match.end(),
                    'weight': weight,
                    'phase_shift': random.uniform(0, 2 * np.pi),  # Random phase shift
                    'amplitude': weight,  # Use weight as amplitude
                    'harmonics': [1.0, 0.5, 0.25]  # Default harmonics
                }
                
                patterns.append(pattern_entry)
    
    return patterns

def compute_field_metrics(field_state: Dict[str, Any]) -> Dict[str, float]:
    """
    Compute metrics for a breath field state.
    
    Args:
        field_state: Field state dictionary containing field history and thresholds
        
    Returns:
        Dictionary containing computed metrics
    """
    metrics = {}
    
    # Extract field history
    field_history = field_state.get('field_history', [])
    phase_history = field_state.get('phase_history', [])
    
    if not field_history:
        return {
            'breath_phase_coherence': 0.0,
            'resonance_stability': 0.0,
            'field_entropy': 0.0
        }
    
    # Convert field history to numpy arrays
    field_array = np.array([complex(f[0]) for f in field_history])
    phase_array = np.array([complex(p[0]) for p in phase_history])
    
    # Compute breath phase coherence
    phase_angles = np.angle(phase_array)
    phase_coherence = 1.0 - np.std(phase_angles) / np.pi
    metrics['breath_phase_coherence'] = float(max(0.0, min(1.0, phase_coherence)))
    
    # Compute resonance stability
    magnitudes = np.abs(field_array)
    resonance_stability = 1.0 - np.std(magnitudes)
    metrics['resonance_stability'] = float(max(0.0, min(1.0, resonance_stability)))
    
    # Compute field entropy
    # Normalize magnitudes to create probability distribution
    norm_magnitudes = magnitudes / np.sum(magnitudes)
    # Compute Shannon entropy
    entropy = -np.sum(norm_magnitudes * np.log2(norm_magnitudes + 1e-10))
    # Normalize entropy to [0, 1] range
    max_entropy = np.log2(len(magnitudes))
    normalized_entropy = entropy / max_entropy if max_entropy > 0 else 0.0
    metrics['field_entropy'] = float(normalized_entropy)
    
    return metrics

def load_json_files_from_dir(directory):
    conversations = []
    for file in os.listdir(directory):
        if file.endswith(".json") and "symbol_tags" not in file:
            try:
                with open(os.path.join(directory, file), 'r') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        for convo_index, convo in enumerate(data):
                            convo['file'] = file
                            mapping = convo.get('mapping')
                            if not mapping:
                                print(f"Skipping conversation {convo_index} in {file} due to missing 'mapping'.")
                                continue

                            messages = []
                            for i, node in enumerate(mapping.values()):
                                message = node.get('message')
                                if not message:
                                    print(f"Node {i} in conversation {convo_index} has a null message. Inserting placeholder.")
                                    messages.append({
                                        'timestamp': "Unknown Time",
                                        'role': 'unknown',
                                        'content': '[Missing content]',
                                        'tags': [],
                                        'line_number': i + 1
                                    })
                                    continue

                                if message.get('author') and message.get('content'):
                                    role = message['author'].get('role', 'unknown')
                                    parts = message['content'].get('parts', [])
                                    time = message.get('create_time')
                                    if parts:
                                        timestamp = datetime.fromtimestamp(time).isoformat() if time else "Unknown Time"
                                        content = parts[0] if isinstance(parts[0], str) else json.dumps(parts[0])
                                        tags = detect_tags(content) if role == 'assistant' else []
                                        messages.append({
                                            'timestamp': timestamp,
                                            'role': role,
                                            'content': content,
                                            'tags': tags,
                                            'line_number': i + 1  # Track actual message index
                                        })
                            # Ensure 'messages' key is present
                            if 'messages' not in convo:
                                convo['messages'] = []
                            conversations.append(convo)
                            if not messages:
                                print(f"Conversation {convo_index} in {file} has no valid messages, assigned empty list.")
                    else:
                        print(f"Skipping invalid conversation file: {file} (not a list)")
            except Exception as e:
                print(f"Skipping invalid conversation file: {file} ({e})")
    return conversations

def save_conversation_exports(convo, output_dir):
    base_name = convo['file'].replace('.json', '')
    jsonl_path = os.path.join(output_dir, base_name + ".jsonl")
    md_path = os.path.join(output_dir, base_name + ".md")
    messages = convo.get('messages', [])

    with open(jsonl_path, 'w') as jf:
        for msg in messages:
            jf.write(json.dumps(msg) + "\n")

    with open(md_path, 'w') as mf:
        for msg in messages:
            mfile.write(f"{msg['role'].upper()}: {msg['content']}\n\n")

def build_symbolic_thread_index(conversations, output_path):
    index = []
    print("\nBuilding symbolic thread index...")
    for convo in tqdm(conversations, desc="Indexing conversations", unit="convo", position=0):
        for message in tqdm(convo['messages'], desc=f"Processing messages for {convo.get('id', 'unknown')}", 
                          leave=False, unit="msg", position=1):
            tags = detect_tags(message['content'])
            if tags:
                index.append({
                    'file': convo['file'],
                    'line_number': message.get('line_number', 0),
                    'message': message['content'],
                    'role': message['role'],
                    'timestamp': message['timestamp'],
                    'tags': tags
                })
    print(f"Indexed {len(index)} symbolic references")
    with open(output_path, 'w') as f:
        json.dump(index, f, indent=2, cls=ComplexEncoder)

def extract_story_fragments(conversations, output_path):
    fragments = []
    motif_counts = {}
    seen_fragments = set()  # Track unique fragments

    print("\nExtracting story fragments...")
    for convo in tqdm(conversations, desc="Processing conversations", unit="convo", position=0):
        for message in tqdm(convo['messages'], desc=f"Analyzing messages for {convo.get('id', 'unknown')}", 
                          leave=False, unit="msg", position=1):
            content = message['content']
            if not content or not isinstance(content, str):
                continue

            # Get all tags from the content
            tags = detect_tags(content)
            
            # Create a fragment for each unique tag info
            processed_meanings = set()  # Track processed meanings for this content
            for glyph, tag_info in SYMBOLIC_TAGS.items():
                # Check if either meaning or symbol_type matches any detected tag
                if (tag_info['meaning'] in tags or tag_info['symbol_type'] in tags) and \
                   tag_info['meaning'] not in processed_meanings:
                    fragment_key = f"{content}|{tag_info['meaning']}|{tag_info['symbol_type']}"
                    if fragment_key not in seen_fragments:
                        fragment = {
                            'file': convo['file'],
                            'fragment': content,
                            'type': 'symbolic_reference',
                            'meaning': tag_info['meaning'],
                            'symbol_type': tag_info['symbol_type'],
                            'timestamp': message['timestamp']
                        }
                        fragments.append(fragment)
                        seen_fragments.add(fragment_key)
                        processed_meanings.add(tag_info['meaning'])
                        motif_counts[tag_info['meaning']] = motif_counts.get(tag_info['meaning'], 0) + 1

            # Check for repeated phrases
            phrases = re.findall(r'"(.*?)"', content)
            for phrase in phrases:
                if phrase not in seen_fragments:
                    motif_counts[phrase] = motif_counts.get(phrase, 0) + 1
                    if motif_counts[phrase] > 1:
                        fragment = {
                            'file': convo['file'],
                            'fragment': phrase,
                            'type': 'repeated_phrase',
                            'meaning': 'echo / resonance / pattern emphasis',
                            'symbol_type': 'composite_tag',
                            'timestamp': message['timestamp']
                        }
                        fragments.append(fragment)
                        seen_fragments.add(phrase)

    print(f"Generated {len(fragments)} unique story fragments")
    with open(output_path, 'w') as f:
        json.dump({'fragments': fragments}, f, indent=2)

def construct_dynamic_context_window(conversations, tag_focuses, output_path, logger=None):
    """Construct a context window prioritizing recent and relevant content."""
    context = []
    # Convert single tag focus to list for consistent handling
    if isinstance(tag_focuses, str):
        tag_focuses = [tag_focuses]
    
    print(f"\nConstructing context window for tags: {', '.join(tag_focuses)}")
    
    # First pass: collect all matching messages with scores
    for convo in tqdm(conversations, desc="Scanning conversations", unit="convo", position=0):
        for msg in tqdm(convo['messages'], desc=f"Checking messages for {convo.get('id', 'unknown')}", 
                      leave=False, unit="msg", position=1):
            tags, tag_scores, archetypes, logic_states, breath_eval, resonance_fields, symbolic_commentary = detect_tags(msg['content'], logger)
            # Check if any tag contains any of the focus tags
            if any(any(focus in tag for tag in tags) for focus in tag_focuses):
                # Include timestamp for sorting
                try:
                    timestamp = datetime.fromisoformat(msg['timestamp'].replace('Z', '+00:00'))
                except (ValueError, AttributeError):
                    timestamp = datetime.min
                
                # Calculate weighted score based on category weights
                score = 0
                for tag in tags:
                    for glyph, tag_info in SYMBOLIC_TAGS.items():
                        if tag_info['meaning'] == tag:
                            category_weight = SYMBOLIC_WEIGHTS.get(tag_info['symbol_type'], 1.0)
                            score += category_weight
                            break
                
                context.append({
                    'timestamp': timestamp,
                    'content': f"{msg['role'].upper()}: {msg['content']}",
                    'score': score,
                    'tags': tags,
                    'resonance_fields': resonance_fields,
                    'symbolic_commentary': symbolic_commentary
                })
                if logger:
                    logger.debug(f"Found matching content for tags {tag_focuses}: {msg['content'][:50]}...")

    # Sort by score first (highest score), then by timestamp (most recent)
    context.sort(key=lambda x: (-x['score'], x['timestamp']), reverse=True)
    
    # Take highest scoring entries
    recent_context = [entry['content'] for entry in context[:20]]
    
    # Add some random lower-scoring entries for diversity
    if len(context) > 20:
        older_context = [entry['content'] for entry in context[20:]]
        random.shuffle(older_context)
        recent_context.extend(older_context[:10])

    if logger:
        logger.info(f"Constructed context window with {len(recent_context)} entries")
        logger.debug(f"Most recent entry timestamp: {context[0]['timestamp'] if context else 'None'}")

    print(f"Writing context window with {len(recent_context)} entries...")
    with open(output_path, 'w') as f:
        f.write("\n\n".join(recent_context))
    print("Context window construction complete!")

def load_symbolic_memory(memory_path):
    """Load symbolic memory from file or create new if doesn't exist."""
    if os.path.exists(memory_path):
        try:
            with open(memory_path, 'r', encoding='utf-8') as f:
                return json.load(f, object_hook=complex_decoder)
        except Exception as e:
            print(f"Error loading symbolic memory: {e}")
            return create_new_memory()
    return create_new_memory()

def save_symbolic_memory(memory, memory_path):
    """Save symbolic memory to file."""
    # Ensure the directory exists
    os.makedirs(os.path.dirname(memory_path), exist_ok=True)
    
    # Save the memory data
    with open(memory_path, 'w', encoding='utf-8') as f:
        json.dump(memory, f, cls=ComplexEncoder, indent=2)

def create_new_memory():
    """Create a new symbolic memory structure."""
    return {
        'processed_conversations': [],
        'symbolic_index': [],
        'story_fragments': [],
        'symbolic_tags': {},
        'last_updated': datetime.now().isoformat()
    }

def update_symbolic_memory(processed_conversations, symbolic_index, story_fragments, memory_path):
    """Update symbolic memory with new processed conversations."""
    print("\nUpdating symbolic memory...")
    
    # Load existing memory
    memory = load_symbolic_memory(memory_path)
    
    # Update processed conversations
    memory['processed_conversations'] = processed_conversations
    
    # Update symbolic index
    memory['symbolic_index'] = symbolic_index
    
    # Update story fragments
    memory['story_fragments'] = story_fragments
    
    # Update symbolic tags
    print("Processing symbolic tags...")
    for entry in tqdm(symbolic_index, desc="Updating symbolic tags"):
        # Use 'message' key instead of 'text'
        content = entry.get('message', '')
        tags, tag_scores, archetypes, logic_states, breath_eval, resonance_fields, symbolic_commentary = detect_tags(content)
        
        # Convert tag lists to tuples for dictionary keys
        tag_tuple = tuple(tags)
        tag_key = ','.join(tag_tuple)  # Convert tuple to string for JSON serialization
        
        if tag_key not in memory['symbolic_tags']:
            memory['symbolic_tags'][tag_key] = {
                'count': 0,
                'entries': [],
                'archetypes': set(),
                'logic_states': set(),
                'breath_eval': [],
                'resonance_fields': {},
                'symbolic_commentary': {}
            }
        
        memory['symbolic_tags'][tag_key]['count'] += 1
        memory['symbolic_tags'][tag_key]['entries'].append(entry)
        
        # Ensure all required keys exist and are of the correct type
        if 'archetypes' not in memory['symbolic_tags'][tag_key]:
            memory['symbolic_tags'][tag_key]['archetypes'] = set()
        if 'logic_states' not in memory['symbolic_tags'][tag_key]:
            memory['symbolic_tags'][tag_key]['logic_states'] = set()
        if 'breath_eval' not in memory['symbolic_tags'][tag_key]:
            memory['symbolic_tags'][tag_key]['breath_eval'] = []
        if 'resonance_fields' not in memory['symbolic_tags'][tag_key]:
            memory['symbolic_tags'][tag_key]['resonance_fields'] = {}
        if 'symbolic_commentary' not in memory['symbolic_tags'][tag_key]:
            memory['symbolic_tags'][tag_key]['symbolic_commentary'] = {}
            
        # Convert existing data to sets if they are lists
        if isinstance(memory['symbolic_tags'][tag_key]['archetypes'], list):
            memory['symbolic_tags'][tag_key]['archetypes'] = set(memory['symbolic_tags'][tag_key]['archetypes'])
        if isinstance(memory['symbolic_tags'][tag_key]['logic_states'], list):
            memory['symbolic_tags'][tag_key]['logic_states'] = set(memory['symbolic_tags'][tag_key]['logic_states'])
            
        # Update the sets and lists
        memory['symbolic_tags'][tag_key]['archetypes'].update(archetypes)
        memory['symbolic_tags'][tag_key]['logic_states'].update(logic_states)
        if breath_eval:  # Only append if breath_eval is not None
            memory['symbolic_tags'][tag_key]['breath_eval'].append(breath_eval)
        memory['symbolic_tags'][tag_key]['resonance_fields'].update(resonance_fields)
        memory['symbolic_tags'][tag_key]['symbolic_commentary'].update(symbolic_commentary)
    
    # Convert sets to lists for JSON serialization
    for tag_data in memory['symbolic_tags'].values():
        # Ensure all required keys exist before conversion
        if 'archetypes' not in tag_data:
            tag_data['archetypes'] = set()
        if 'logic_states' not in tag_data:
            tag_data['logic_states'] = set()
        if 'breath_eval' not in tag_data:
            tag_data['breath_eval'] = []
        if 'resonance_fields' not in tag_data:
            tag_data['resonance_fields'] = {}
        if 'symbolic_commentary' not in tag_data:
            tag_data['symbolic_commentary'] = {}
            
        # Convert sets to lists
        tag_data['archetypes'] = list(tag_data['archetypes'])
        tag_data['logic_states'] = list(tag_data['logic_states'])
    
    # Save updated memory
    save_symbolic_memory(memory, memory_path)
    print("Symbolic memory updated successfully!")

def load_processed_conversations(processed_convos_path):
    if os.path.exists(processed_convos_path):
        with open(processed_convos_path, 'r') as f:
            return set(json.load(f))
    return set()

def save_processed_conversations(processed_convos, processed_convos_path):
    # Convert sets to lists for JSON serialization
    processed_convos["processed_ids"] = list(processed_convos["processed_ids"])
    with open(processed_convos_path, 'w') as f:
        json.dump(processed_convos, f)

def load_json_data(base_dir, processed_convos_path, full_sync=False):
    processed_convos = load_processed_conversations(processed_convos_path)
    if not isinstance(processed_convos, dict):
        processed_convos = {"processed_ids": set(processed_convos), "processed_hashes": {}}

    conversations = []
    json_path = os.path.join(base_dir, 'conversations', 'conversations.json')
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for convo in data:
                convo_id = convo.get('id')
                if full_sync or (convo_id and convo_id not in processed_convos["processed_ids"]):
                    conversations.append(convo)
    except Exception as e:
        print(f"Error loading conversations: {e}")

    # Load transcripts (assuming similar structure)
    transcript_dir = os.path.join(base_dir, 'transcripts')
    for file in os.listdir(transcript_dir):
        if file.endswith('.json'):
            try:
                with open(os.path.join(transcript_dir, file), 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for convo in data:
                        convo_id = convo.get('id')
                        if full_sync or (convo_id and convo_id not in processed_convos["processed_ids"]):
                            conversations.append(convo)
            except Exception as e:
                print(f"Error loading transcript {file}: {e}")

    return conversations, processed_convos

# === MAIN ===
def generate_unique_id():
    """Generate a unique ID using timestamp and random suffix."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    random_suffix = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=6))
    return f"{timestamp}_{random_suffix}"

def process_conversation(convo, worker_id):
    """Process a single conversation with proper file naming and message handling."""
    # Preserve the original file field
    original_file = convo.get('file', 'unknown')
    
    # Use conversation ID for filename, fallback to timestamp if no ID
    convo_id = convo.get('id', '')
    if not convo_id and convo.get('messages'):
        # Try to get timestamp from first message
        first_msg = convo['messages'][0] if convo['messages'] else None
        if first_msg and first_msg.get('timestamp'):
            convo_id = first_msg['timestamp'].replace(':', '-').replace('.', '-')
        else:
            convo_id = generate_unique_id()
    
    filename_base = f"conversation_{convo_id}"
    jsonl_path = os.path.join(OUTPUT_DIR, filename_base + ".jsonl")
    md_path = os.path.join(OUTPUT_DIR, filename_base + ".md")

    mapping = convo.get('mapping', {})
    messages = []
    
    # Calculate total messages for progress bar
    total_messages = len(mapping)

    # Process messages with nested progress bar
    for i, node in tqdm(enumerate(mapping.values()), 
                      desc=f"Worker {worker_id:3d}", 
                      total=total_messages,
                      leave=False,
                      position=worker_id % 4 + 1,
                      bar_format='{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt}',
                      unit="msg"):
        message = node.get('message')
        if message and message.get('author') and message.get('content'):
            role = message['author'].get('role', 'unknown')
            parts = message['content'].get('parts', [])
            time = message.get('create_time')
            if parts:
                timestamp = datetime.fromtimestamp(time).isoformat() if time else "Unknown Time"
                content = parts[0] if isinstance(parts[0], str) else json.dumps(parts[0])
                tags = detect_tags(content) if role == 'assistant' else []
                messages.append({
                    'timestamp': timestamp,
                    'role': role,
                    'content': content,
                    'tags': tags,
                    'line_number': i + 1  # Track actual message index
                })

    # Sort messages by time
    messages.sort(key=lambda x: x['timestamp'])

    # Update the conversation with processed messages while preserving original fields
    processed_convo = {
        'id': convo.get('id', ''),
        'file': original_file,
        'messages': messages,
        'mapping': convo.get('mapping', {})
    }

    # Write JSONL and MD with lock
    with file_lock:
        # Write JSONL
        with open(jsonl_path, 'w', encoding='utf-8') as jfile:
            for msg in messages:
                jfile.write(json.dumps(msg, cls=ComplexEncoder) + '\n')

        # Write Markdown
        with open(md_path, 'w', encoding='utf-8') as mfile:
            mfile.write(f"# Conversation {convo_id}\n")
            for msg in messages:
                mfile.write(f"\n**{msg['role'].title()} [{msg['timestamp']}]:**\n{msg['content']}\n")

    return processed_convo

def process_conversation_wrapper(args):
    """Wrapper function for process_conversation to handle multiprocessing."""
    convo, worker_id = args
    return process_conversation(convo, worker_id)

def compute_co_occurrence_patterns(entries):
    """Compute co-occurrence patterns between glyphs in entries."""
    patterns = {
        "pairs": {},
        "triads": {},
        "total_entries": len(entries)
    }
    
    for entry in entries:
        content = entry.get('content', '')
        present_glyphs = [glyph for glyph in SYMBOLIC_TAGS.keys() if glyph in content]
        
        # Compute pairs
        for i, glyph1 in enumerate(present_glyphs):
            for glyph2 in present_glyphs[i+1:]:
                pair = tuple(sorted([glyph1, glyph2]))
                patterns["pairs"][pair] = patterns["pairs"].get(pair, 0) + 1
        
        # Compute triads
        for i, glyph1 in enumerate(present_glyphs):
            for j, glyph2 in enumerate(present_glyphs[i+1:], i+1):
                for glyph3 in present_glyphs[j+1:]:
                    triad = tuple(sorted([glyph1, glyph2, glyph3]))
                    patterns["triads"][triad] = patterns["triads"].get(triad, 0) + 1
    
    return patterns

def compute_symbolic_summary(entries):
    """Compute a summary of symbolic patterns in the entries."""
    summary = {
        'symbolic_tags': {},
        'archetypal_patterns': {},
        'category_distribution': {},
        'logic_states': {},
        'composite_patterns': {},
        'breath_equations': {
            'valid_equations': 0,
            'field_stability': 0.0,
            'resonance_quality': 0.0,
            'pattern_distribution': {
                'breath_cycles': 0,
                'state_transitions': 0,
                'gate_activations': 0,
                'field_resonances': 0
            },
            'field_history': []
        }
    }
    
    for entry in entries:
        tags, scores, archetypes, logic, breath = detect_tags(entry.get('text', ''))
        
        # Update symbolic tags
        for tag in tags:
            summary['symbolic_tags'][tag] = summary['symbolic_tags'].get(tag, 0) + 1
        
        # Update archetypal patterns
        for bundle, data in archetypes.items():
            if bundle not in summary['archetypal_patterns']:
                summary['archetypal_patterns'][bundle] = {
                    'count': 0,
                    'matched_glyphs': set()
                }
            summary['archetypal_patterns'][bundle]['count'] += 1
            summary['archetypal_patterns'][bundle]['matched_glyphs'].update(data['matched_glyphs'])
        
        # Update category distribution
        for tag in tags:
            if tag in SYMBOLIC_TAGS:
                category = SYMBOLIC_TAGS[tag]['symbol_type']
                summary['category_distribution'][category] = summary['category_distribution'].get(category, 0) + 1
        
        # Update logic states
        for glyph, state in logic.items():
            if glyph not in summary['logic_states']:
                summary['logic_states'][glyph] = {
                    'gate': state['gate'],
                    'conditions': set(),
                    'functions': set(),
                    'state_changes': set()
                }
            summary['logic_states'][glyph]['conditions'].add(state['condition'])
            summary['logic_states'][glyph]['functions'].add(state['function'])
            for modifier in state['state'].values():
                summary['logic_states'][glyph]['state_changes'].add(modifier)
        
        # Update breath equation summary
        if breath and breath['equation_valid']:
            summary['breath_equations']['valid_equations'] += 1
            summary['breath_equations']['field_stability'] += breath['field_stability']
            summary['breath_equations']['resonance_quality'] += breath['resonance_quality']
            
            # Update pattern distribution
            for pattern_type in summary['breath_equations']['pattern_distribution']:
                summary['breath_equations']['pattern_distribution'][pattern_type] += len(breath['patterns'][pattern_type])
            
            # Add field history
            summary['breath_equations']['field_history'].extend(breath['field_history'])
    
    # Normalize breath equation metrics
    if summary['breath_equations']['valid_equations'] > 0:
        summary['breath_equations']['field_stability'] /= summary['breath_equations']['valid_equations']
        summary['breath_equations']['resonance_quality'] /= summary['breath_equations']['valid_equations']
    
    return summary

def compute_symbolic_delta(summary_a, summary_b):
    """Compute the symbolic differences between two summaries."""
    delta = {
        "glyph_shifts": {},
        "archetypal_shifts": {},
        "category_shifts": {},
        "pattern_shifts": {
            "pairs": {},
            "triads": {}
        },
        "interpretation": []
    }
    
    # Compute glyph shifts
    all_glyphs = set(summary_a["glyph_counts"].keys()) | set(summary_b["glyph_counts"].keys())
    for glyph in all_glyphs:
        count_a = summary_a["glyph_counts"].get(glyph, 0)
        count_b = summary_b["glyph_counts"].get(glyph, 0)
        delta_count = count_b - count_a
        
        if count_a > 0:
            percent_change = (delta_count / count_a) * 100
        else:
            percent_change = 100 if count_b > 0 else 0
        
        # Get category weight
        category = SYMBOLIC_TAGS[glyph]['symbol_type']
        weight = SYMBOLIC_WEIGHTS.get(category, 1.0)
        weighted_delta = delta_count * weight
        
        delta["glyph_shifts"][glyph] = {
            "meaning": SYMBOLIC_TAGS[glyph]['meaning'],
            "delta_count": delta_count,
            "percent_change": percent_change,
            "weight": weight,
            "weighted_delta": weighted_delta,
            "category": category
        }
    
    # Compute archetypal shifts
    all_archetypes = set(summary_a["archetypal_matches"].keys()) | set(summary_b["archetypal_matches"].keys())
    for archetype in all_archetypes:
        count_a = summary_a["archetypal_matches"].get(archetype, 0)
        count_b = summary_b["archetypal_matches"].get(archetype, 0)
        delta_count = count_b - count_a
        
        if count_a > 0:
            percent_change = (delta_count / count_a) * 100
        else:
            percent_change = 100 if count_b > 0 else 0
        
        delta["archetypal_shifts"][archetype] = {
            "delta_count": delta_count,
            "percent_change": percent_change
        }
    
    # Compute category shifts
    all_categories = set(summary_a["category_counts"].keys()) | set(summary_b["category_counts"].keys())
    for category in all_categories:
        count_a = summary_a["category_counts"].get(category, 0)
        count_b = summary_b["category_counts"].get(category, 0)
        delta_count = count_b - count_a
        
        if count_a > 0:
            percent_change = (delta_count / count_a) * 100
        else:
            percent_change = 100 if count_b > 0 else 0
        
        delta["category_shifts"][category] = {
            "delta_count": delta_count,
            "percent_change": percent_change
        }
    
    # Compute pattern shifts
    # Pairs
    all_pairs = set(summary_a["co_occurrence"]["pairs"].keys()) | set(summary_b["co_occurrence"]["pairs"].keys())
    for pair in all_pairs:
        count_a = summary_a["co_occurrence"]["pairs"].get(pair, 0)
        count_b = summary_b["co_occurrence"]["pairs"].get(pair, 0)
        delta_count = count_b - count_a
        
        if count_a > 0:
            percent_change = (delta_count / count_a) * 100
        else:
            percent_change = 100 if count_b > 0 else 0
        
        delta["pattern_shifts"]["pairs"][pair] = {
            "delta_count": delta_count,
            "percent_change": percent_change,
            "glyphs": pair
        }
    
    # Triads
    all_triads = set(summary_a["co_occurrence"]["triads"].keys()) | set(summary_b["co_occurrence"]["triads"].keys())
    for triad in all_triads:
        count_a = summary_a["co_occurrence"]["triads"].get(triad, 0)
        count_b = summary_b["co_occurrence"]["triads"].get(triad, 0)
        delta_count = count_b - count_a
        
        if count_a > 0:
            percent_change = (delta_count / count_a) * 100
        else:
            percent_change = 100 if count_b > 0 else 0
        
        delta["pattern_shifts"]["triads"][triad] = {
            "delta_count": delta_count,
            "percent_change": percent_change,
            "glyphs": triad
        }
    
    # Generate interpretation
    significant_glyphs = sorted(
        delta["glyph_shifts"].items(),
        key=lambda x: abs(x[1]["weighted_delta"]),
        reverse=True
    )[:5]
    
    significant_archetypes = sorted(
        delta["archetypal_shifts"].items(),
        key=lambda x: abs(x[1]["delta_count"]),
        reverse=True
    )[:3]
    
    # Build interpretation
    rises = []
    falls = []
    for glyph, shift in significant_glyphs:
        if shift["delta_count"] > 0:
            rises.append(f"**{SYMBOLIC_TAGS[glyph]['meaning']}**")
        else:
            falls.append(f"**{SYMBOLIC_TAGS[glyph]['meaning']}**")
    
    archetype_changes = []
    for archetype, shift in significant_archetypes:
        if shift["delta_count"] > 0:
            archetype_changes.append(f"rise in **{archetype}**")
        else:
            archetype_changes.append(f"decline in **{archetype}**")
    
    if rises:
        delta["interpretation"].append(f"Significant rise in {', '.join(rises)}-related glyphs")
    if falls:
        delta["interpretation"].append(f"Notable suppression of {', '.join(falls)}-related glyphs")
    if archetype_changes:
        delta["interpretation"].append(f"Observed {' and '.join(archetype_changes)}")
    
    return delta

def generate_enhanced_interpretation(delta, interpretation_mode="symbolic"):
    """Generate enhanced interpretation of symbolic changes."""
    interpretation = []
    
    # Analyze archetypal tensions
    for tension_name, tension_info in ARCHETYPAL_TENSIONS.items():
        rising_count = sum(1 for glyph in tension_info["rising"] 
                         if delta["glyph_shifts"].get(glyph, {}).get("delta_count", 0) > 0)
        falling_count = sum(1 for glyph in tension_info["falling"] 
                          if delta["glyph_shifts"].get(glyph, {}).get("delta_count", 0) < 0)
        
        if rising_count >= 2 and falling_count >= 2:
            if interpretation_mode == "poetic":
                interpretation.append(f"🌊 {tension_info['interpretation']}, like waves returning to shore")
            elif interpretation_mode == "analytic":
                interpretation.append(f"📊 {tension_info['interpretation']} (rising: {rising_count}, falling: {falling_count})")
            else:  # symbolic
                interpretation.append(f"🔄 {tension_info['interpretation']}")
    
    # Analyze co-occurrence patterns
    significant_pairs = sorted(
        delta["pattern_shifts"]["pairs"].items(),
        key=lambda x: abs(x[1]["delta_count"]),
        reverse=True
    )[:3]
    
    for pair, shift in significant_pairs:
        if shift["delta_count"] > 0:
            if interpretation_mode == "poetic":
                interpretation.append(f"✨ Emergence of new symbolic dance between {pair[0]} and {pair[1]}")
            elif interpretation_mode == "analytic":
                interpretation.append(f"📈 New co-occurrence pattern: {pair[0]}+{pair[1]} (+{shift['delta_count']})")
            else:  # symbolic
                interpretation.append(f"🔗 Strengthening bond between {pair[0]} and {pair[1]}")
    
    return interpretation

def generate_diff_report(delta, output_path, interpretation_mode="symbolic"):
    """Generate a markdown report of symbolic differences."""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("## 🧬 Symbolic Diff Report\n\n")
        
        # Glyph Shifts
        f.write("### 🔁 Glyph Shifts\n\n")
        f.write("| Glyph | Meaning | Δ Count | % Change | Weight | Weighted Δ |\n")
        f.write("|-------|---------|---------|----------|--------|-------------|\n")
        
        for glyph, shift in sorted(delta["glyph_shifts"].items(), 
                                 key=lambda x: abs(x[1]["weighted_delta"]), 
                                 reverse=True):
            f.write(f"| {glyph} | {shift['meaning']} | {shift['delta_count']:+d} | {shift['percent_change']:+.1f}% | {shift['weight']:.1f} | {shift['weighted_delta']:+.1f} |\n")
        
        # Archetype Shifts
        f.write("\n### 🧙 Archetype Shifts\n\n")
        f.write("| Archetype | Δ Count | % Change |\n")
        f.write("|-----------|---------|----------|\n")
        
        for archetype, shift in sorted(delta["archetypal_shifts"].items(), 
                                     key=lambda x: abs(x[1]["delta_count"]), 
                                     reverse=True):
            f.write(f"| {archetype} | {shift['delta_count']:+d} | {shift['percent_change']:+.1f}% |\n")
        
        # Category Shifts
        f.write("\n### 📊 Category Shifts\n\n")
        f.write("| Category | Δ Count | % Change |\n")
        f.write("|----------|---------|----------|\n")
        
        for category, shift in sorted(delta["category_shifts"].items(), 
                                    key=lambda x: abs(x[1]["delta_count"]), 
                                    reverse=True):
            f.write(f"| {category} | {shift['delta_count']:+d} | {shift['percent_change']:+.1f}% |\n")
        
        # Add Pattern Shifts section
        f.write("\n### 🕸️ Symbolic Pattern Shifts\n\n")
        f.write("#### Co-occurring Pairs\n\n")
        f.write("| Pair | Δ Count | % Change |\n")
        f.write("|------|---------|----------|\n")
        
        for pair, shift in sorted(delta["pattern_shifts"]["pairs"].items(), 
                                key=lambda x: abs(x[1]["delta_count"]), 
                                reverse=True):
            f.write(f"| {pair[0]} + {pair[1]} | {shift['delta_count']:+d} | {shift['percent_change']:+.1f}% |\n")
        
        f.write("\n#### Co-occurring Triads\n\n")
        f.write("| Triad | Δ Count | % Change |\n")
        f.write("|-------|---------|----------|\n")
        
        for triad, shift in sorted(delta["pattern_shifts"]["triads"].items(), 
                                 key=lambda x: abs(x[1]["delta_count"]), 
                                 reverse=True):
            f.write(f"| {' + '.join(triad)} | {shift['delta_count']:+d} | {shift['percent_change']:+.1f}% |\n")
        
        # Enhanced interpretation
        f.write("\n---\n\n### 🌐 Enhanced Interpretation\n")
        interpretation = generate_enhanced_interpretation(delta, interpretation_mode)
        for insight in interpretation:
            f.write(f"- {insight}\n")
        
        f.write("\n**Interpretation:**\n")
        f.write("This suggests a symbolic phase shift in the following areas:\n")
        
        # Generate interpretation based on significant changes
        significant_changes = []
        for glyph, shift in delta["glyph_shifts"].items():
            if abs(shift["weighted_delta"]) > 5:  # Threshold for significant change
                significant_changes.append(f"{shift['meaning']} ({shift['delta_count']:+d})")
        
        if significant_changes:
            f.write("- " + ", ".join(significant_changes) + "\n")

def save_diff_state(delta, output_path):
    """Save the current diff state as a snapshot."""
    state = {
        "timestamp": datetime.now().isoformat(),
        "delta": delta,
        "metadata": {
            "version": "1.0",
            "schema": {
                "glyph_shifts": "Weighted changes in individual glyph frequencies",
                "archetypal_shifts": "Changes in archetypal pattern frequencies",
                "pattern_shifts": "Changes in co-occurrence patterns",
                "category_shifts": "Changes in symbolic category distributions"
            }
        }
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2)
    
    print(f"Diff state saved to {output_path}")

def generate_visualizations(delta, output_dir, diff_mode="context"):
    """Generate visualization plots for the symbolic diff."""
    os.makedirs(output_dir, exist_ok=True)
    
    # Set style
    plt.style.use(PLOT_STYLES["glyph_delta"]["style"])
    
    # 1. Glyph Delta Bar Chart
    plt.figure(figsize=PLOT_STYLES["glyph_delta"]["figsize"])
    
    # Prepare data
    glyphs = []
    deltas = []
    categories = []
    for glyph, shift in sorted(delta["glyph_shifts"].items(), 
                             key=lambda x: abs(x[1]["weighted_delta"]), 
                             reverse=True)[:15]:  # Top 15 changes
        glyphs.append(glyph)
        deltas.append(shift["weighted_delta"])
        categories.append(shift["category"])
    
    # Create color mapping for categories
    unique_categories = list(set(categories))
    color_map = dict(zip(unique_categories, 
                        sns.color_palette(PLOT_STYLES["glyph_delta"]["palette"], 
                                        len(unique_categories))))
    
    # Plot
    bars = plt.bar(glyphs, deltas)
    for bar, category in zip(bars, categories):
        bar.set_color(color_map[category])
    
    plt.title("Symbolic Field Shifts (Weighted Delta)")
    plt.xlabel("Glyphs")
    plt.ylabel("Weighted Delta")
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Add legend for categories
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=color, label=cat) 
                      for cat, color in color_map.items()]
    plt.legend(handles=legend_elements, title="Categories", 
              bbox_to_anchor=(1.05, 1), loc='upper left')
    
    plt.savefig(os.path.join(output_dir, "glyph_delta.png"), 
                bbox_inches='tight', dpi=300)
    plt.close()
    
    # 2. Co-occurrence Heatmap
    if delta["pattern_shifts"]["pairs"]:
        plt.figure(figsize=PLOT_STYLES["co_occurrence"]["figsize"])
        
        # Prepare data
        pairs = []
        deltas = []
        for pair, shift in sorted(delta["pattern_shifts"]["pairs"].items(),
                                key=lambda x: abs(x[1]["delta_count"]),
                                reverse=True)[:20]:  # Top 20 pairs
            pairs.append(f"{pair[0]}+{pair[1]}")
            deltas.append(shift["delta_count"])
        
        # Create heatmap data
        heatmap_data = np.array(deltas).reshape(-1, 1)
        
        # Plot
        sns.heatmap(heatmap_data, 
                   cmap=PLOT_STYLES["co_occurrence"]["cmap"],
                   yticklabels=pairs,
                   xticklabels=["Delta"],
                   center=0,
                   annot=True,
                   fmt=".0f")
        
        plt.title("Co-occurrence Pattern Shifts")
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "co_occurrence_heatmap.png"), 
                    bbox_inches='tight', dpi=300)
        plt.close()
    
    # 3. Archetype Timeline (if comparing over time)
    if diff_mode == "memory":
        plt.figure(figsize=PLOT_STYLES["archetype_timeline"]["figsize"])
        
        # Prepare data
        archetypes = []
        deltas = []
        for archetype, shift in sorted(delta["archetypal_shifts"].items(),
                                     key=lambda x: abs(x[1]["delta_count"]),
                                     reverse=True):
            archetypes.append(archetype)
            deltas.append(shift["delta_count"])
        
        # Plot
        plt.bar(archetypes, deltas, 
                color=sns.color_palette(PLOT_STYLES["archetype_timeline"]["palette"]))
        plt.title("Archetypal Pattern Shifts")
        plt.xlabel("Archetypes")
        plt.ylabel("Delta Count")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "archetype_timeline.png"), 
                    bbox_inches='tight', dpi=300)
        plt.close()

def compute_composite_score(delta):
    """Compute unified composite scores for symbolic changes."""
    composite_scores = {}
    
    # Process glyph scores
    for glyph, shift in delta["glyph_shifts"].items():
        composite_scores[glyph] = {
            "score": shift["weighted_delta"] * COMPOSITE_WEIGHTS["glyph_delta"],
            "components": {
                "glyph_delta": shift["weighted_delta"],
                "archetype_delta": 0,
                "cooccurrence_delta": 0
            },
            "meaning": shift["meaning"],
            "category": shift["category"]
        }
    
    # Add archetypal contributions
    for archetype, shift in delta["archetypal_shifts"].items():
        # Find glyphs in this archetype
        for glyph in ARCHETYPAL_BUNDLES.get(archetype, []):
            if glyph in composite_scores:
                composite_scores[glyph]["components"]["archetype_delta"] += shift["delta_count"]
                composite_scores[glyph]["score"] += (
                    shift["delta_count"] * COMPOSITE_WEIGHTS["archetype_delta"]
                )
    
    # Add co-occurrence contributions
    for pair, shift in delta["pattern_shifts"]["pairs"].items():
        for glyph in pair:
            if glyph in composite_scores:
                composite_scores[glyph]["components"]["cooccurrence_delta"] += shift["delta_count"]
                composite_scores[glyph]["score"] += (
                    shift["delta_count"] * COMPOSITE_WEIGHTS["cooccurrence_delta"]
                )
    
    return composite_scores

def generate_composite_visualization(composite_scores, output_dir):
    """Generate visualization for composite scores."""
    plt.figure(figsize=(12, 8))
    
    # Prepare data
    glyphs = []
    scores = []
    components = {
        "glyph_delta": [],
        "archetype_delta": [],
        "cooccurrence_delta": []
    }
    
    # Sort by absolute composite score
    sorted_items = sorted(composite_scores.items(),
                         key=lambda x: abs(x[1]["score"]),
                         reverse=True)[:15]  # Top 15 changes
    
    for glyph, data in sorted_items:
        glyphs.append(glyph)
        scores.append(data["score"])
        for component in components:
            components[component].append(data["components"][component])
    
    # Create stacked bar chart
    bottom = np.zeros(len(glyphs))
    colors = ['#FF9999', '#66B2FF', '#99FF99']
    
    for i, (component, values) in enumerate(components.items()):
        plt.bar(glyphs, values, bottom=bottom, 
                label=component.replace('_', ' ').title(),
                color=colors[i])
        bottom += values
    
    plt.title("Composite Symbolic Field Changes")
    plt.xlabel("Glyphs")
    plt.ylabel("Weighted Score")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    
    plt.savefig(os.path.join(output_dir, "composite_score_chart.png"),
                bbox_inches='tight', dpi=300)
    plt.close()

def generate_composite_report(composite_scores, output_path):
    """Generate a report of composite symbolic changes."""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("## 🎭 Composite Symbolic Field Analysis\n\n")
        
        # Overall field movement
        rising = []
        falling = []
        for glyph, data in sorted(composite_scores.items(),
                                key=lambda x: abs(x[1]["score"]),
                                reverse=True)[:5]:
            if data["score"] > 0:
                rising.append(f"{glyph} ({data['meaning']})")
            else:
                falling.append(f"{glyph} ({data['meaning']})")
        
        f.write("### 🌊 Field Movement\n\n")
        if rising:
            f.write("**Rising Symbols:**\n")
            for symbol in rising:
                f.write(f"- {symbol}\n")
        if falling:
            f.write("\n**Falling Symbols:**\n")
            for symbol in falling:
                f.write(f"- {symbol}\n")
        
        # Detailed scores
        f.write("\n### 📊 Composite Scores\n\n")
        f.write("| Glyph | Meaning | Category | Total Score | Components |\n")
        f.write("|-------|---------|----------|-------------|------------|\n")
        
        for glyph, data in sorted(composite_scores.items(),
                                key=lambda x: abs(x[1]["score"]),
                                reverse=True):
            components = data["components"]
            f.write(f"| {glyph} | {data['meaning']} | {data['category']} | "
                   f"{data['score']:.2f} | "
                   f"G:{components['glyph_delta']:.1f} "
                   f"A:{components['archetype_delta']:.1f} "
                   f"C:{components['cooccurrence_delta']:.1f} |\n")
        
        # Field interpretation
        f.write("\n### 🌐 Field Interpretation\n\n")
        if rising and falling:
            f.write("The symbolic field shows a movement from ")
            f.write(", ".join(falling[:-1]))
            if len(falling) > 1:
                f.write(f" and {falling[-1]}")
            f.write(" toward ")
            f.write(", ".join(rising[:-1]))
            if len(rising) > 1:
                f.write(f" and {rising[-1]}")
            f.write(".\n\n")
            
            # Add archetypal interpretation
            rising_archetypes = set()
            falling_archetypes = set()
            for glyph in rising:
                for archetype, bundle in ARCHETYPAL_BUNDLES.items():
                    if glyph.split()[0] in bundle:
                        rising_archetypes.add(archetype)
            for glyph in falling:
                for archetype, bundle in ARCHETYPAL_BUNDLES.items():
                    if glyph.split()[0] in bundle:
                        falling_archetypes.add(archetype)
            
            if rising_archetypes and falling_archetypes:
                f.write("This suggests a shift from ")
                f.write(", ".join(rising_archetypes))
                f.write(" toward ")
                f.write(", ".join(falling_archetypes))
                f.write(" archetypal patterns.\n")

def compute_memory_delta(memory_a, memory_b):
    """Compute the symbolic differences between two memory states."""
    delta = {
        "symbolic_tags": {},
        "archetypal_patterns": {},
        "category_distribution": {},
        "forgotten_symbols": [],
        "cumulative_weights": {},
        "field_vector": {}
    }
    
    # Compare symbolic tags
    all_tags = set(memory_a["symbolic_tags"].keys()) | set(memory_b["symbolic_tags"].keys())
    for tag in all_tags:
        count_a = memory_a["symbolic_tags"].get(tag, {}).get("count", 0)
        count_b = memory_b["symbolic_tags"].get(tag, {}).get("count", 0)
        delta_count = count_b - count_a
        
        if count_a > 0:
            percent_change = (delta_count / count_a) * 100
        else:
            percent_change = 100 if count_b > 0 else 0
        
        # Get category weight
        category = memory_b["symbolic_tags"].get(tag, {}).get("symbol_type", "unknown")
        weight = SYMBOLIC_WEIGHTS.get(category, 1.0)
        weighted_delta = delta_count * weight
        
        delta["symbolic_tags"][tag] = {
            "delta_count": delta_count,
            "percent_change": percent_change,
            "weight": weight,
            "weighted_delta": weighted_delta,
            "category": category,
            "last_seen_a": memory_a["symbolic_tags"].get(tag, {}).get("last_seen", ""),
            "last_seen_b": memory_b["symbolic_tags"].get(tag, {}).get("last_seen", "")
        }
        
        # Track forgotten symbols
        if count_a > 0 and count_b == 0:
            delta["forgotten_symbols"].append({
                "tag": tag,
                "category": category,
                "last_seen": memory_a["symbolic_tags"][tag]["last_seen"],
                "count_at_disappearance": count_a
            })
    
    # Compare archetypal patterns
    for archetype, bundle in ARCHETYPAL_BUNDLES.items():
        pattern_a = sum(1 for glyph in bundle 
                       if memory_a["symbolic_tags"].get(glyph, {}).get("count", 0) > 0)
        pattern_b = sum(1 for glyph in bundle 
                       if memory_b["symbolic_tags"].get(glyph, {}).get("count", 0) > 0)
        delta_count = pattern_b - pattern_a
        
        if pattern_a > 0:
            percent_change = (delta_count / pattern_a) * 100
        else:
            percent_change = 100 if pattern_b > 0 else 0
        
        delta["archetypal_patterns"][archetype] = {
            "delta_count": delta_count,
            "percent_change": percent_change,
            "glyphs_present_a": [g for g in bundle 
                               if memory_a["symbolic_tags"].get(g, {}).get("count", 0) > 0],
            "glyphs_present_b": [g for g in bundle 
                               if memory_b["symbolic_tags"].get(g, {}).get("count", 0) > 0]
        }
    
    # Compare category distribution
    all_categories = set(memory_a["category_distribution"].keys()) | \
                    set(memory_b["category_distribution"].keys())
    for category in all_categories:
        count_a = memory_a["category_distribution"].get(category, 0)
        count_b = memory_b["category_distribution"].get(category, 0)
        delta_count = count_b - count_a
        
        if count_a > 0:
            percent_change = (delta_count / count_a) * 100
        else:
            percent_change = 100 if count_b > 0 else 0
        
        delta["category_distribution"][category] = {
            "delta_count": delta_count,
            "percent_change": percent_change,
            "weight": SYMBOLIC_WEIGHTS.get(category, 1.0)
        }
    
    # Compute cumulative weights
    for category in all_categories:
        delta["cumulative_weights"][category] = sum(
            delta["symbolic_tags"][tag]["weighted_delta"]
            for tag, data in delta["symbolic_tags"].items()
            if data["category"] == category
        )
    
    # Compute field vector (directional change in symbolic space)
    for category in all_categories:
        weight_delta = delta["cumulative_weights"][category]
        archetype_delta = sum(
            pattern["delta_count"]
            for pattern in delta["archetypal_patterns"].values()
            if any(glyph in ARCHETYPAL_BUNDLES.get(archetype, [])
                  for archetype in ARCHETYPAL_BUNDLES.keys()
                  if category in memory_b["symbolic_tags"].get(glyph, {}).get("symbol_type", ""))
        )
        delta["field_vector"][category] = {
            "weight_delta": weight_delta,
            "archetype_delta": archetype_delta,
            "total_vector": weight_delta + archetype_delta
        }
    
    return delta

def generate_memory_diff_report(delta, output_path):
    """Generate a report of memory state differences."""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("## 🧠 Symbolic Memory Evolution Report\n\n")
        
        # Field Vector Summary
        f.write("### 🌊 Field Vector Movement\n\n")
        f.write("| Category | Weight Δ | Archetype Δ | Total Vector |\n")
        f.write("|----------|----------|-------------|-------------|\n")
        
        for category, vector in sorted(delta["field_vector"].items(),
                                     key=lambda x: abs(x[1]["total_vector"]),
                                     reverse=True):
            f.write(f"| {category} | {vector['weight_delta']:+.1f} | "
                   f"{vector['archetype_delta']:+.1f} | "
                   f"{vector['total_vector']:+.1f} |\n")
        
        # Forgotten Symbols
        if delta["forgotten_symbols"]:
            f.write("\n### 💫 Forgotten Symbols\n\n")
            f.write("| Symbol | Category | Last Seen | Count |\n")
            f.write("|--------|----------|-----------|-------|\n")
            
            for symbol in sorted(delta["forgotten_symbols"],
                               key=lambda x: x["count_at_disappearance"],
                               reverse=True):
                f.write(f"| {symbol['tag']} | {symbol['category']} | "
                       f"{symbol['last_seen']} | {symbol['count_at_disappearance']} |\n")
        
        # Archetypal Evolution
        f.write("\n### 🧙 Archetypal Evolution\n\n")
        f.write("| Archetype | Δ Count | % Change | Present Glyphs |\n")
        f.write("|-----------|---------|----------|----------------|\n")
        
        for archetype, pattern in sorted(delta["archetypal_patterns"].items(),
                                       key=lambda x: abs(x[1]["delta_count"]),
                                       reverse=True):
            f.write(f"| {archetype} | {pattern['delta_count']:+d} | "
                   f"{pattern['percent_change']:+.1f}% | "
                   f"{', '.join(pattern['glyphs_present_b'])} |\n")
        
        # Category Distribution
        f.write("\n### 📊 Category Distribution Changes\n\n")
        f.write("| Category | Δ Count | % Change | Cumulative Weight |\n")
        f.write("|----------|---------|----------|-------------------|\n")
        
        for category, dist in sorted(delta["category_distribution"].items(),
                                   key=lambda x: abs(x[1]["delta_count"]),
                                   reverse=True):
            f.write(f"| {category} | {dist['delta_count']:+d} | "
                   f"{dist['percent_change']:+.1f}% | "
                   f"{delta['cumulative_weights'][category]:+.1f} |\n")
        
        # Field Interpretation
        f.write("\n### 🌐 Field Interpretation\n\n")
        
        # Rising categories
        rising = []
        falling = []
        for category, vector in delta["field_vector"].items():
            if vector["total_vector"] > 0:
                rising.append(category)
            else:
                falling.append(category)
        
        if rising and falling:
            f.write("The symbolic field shows a movement from ")
            f.write(", ".join(falling[:-1]))
            if len(falling) > 1:
                f.write(f" and {falling[-1]}")
            f.write(" toward ")
            f.write(", ".join(rising[:-1]))
            if len(rising) > 1:
                f.write(f" and {rising[-1]}")
            f.write(".\n\n")
        
        # Forgotten symbols interpretation
        if delta["forgotten_symbols"]:
            f.write("Notable symbols that have faded from the field:\n")
            for symbol in delta["forgotten_symbols"][:5]:  # Top 5 forgotten
                f.write(f"- {symbol['tag']} ({symbol['category']})\n")
            f.write("\n")
        
        # Archetypal evolution interpretation
        significant_archetypes = sorted(delta["archetypal_patterns"].items(),
                                      key=lambda x: abs(x[1]["delta_count"]),
                                      reverse=True)[:3]
        if significant_archetypes:
            f.write("Key archetypal shifts:\n")
            for archetype, pattern in significant_archetypes:
                if pattern["delta_count"] > 0:
                    f.write(f"- {archetype} is emerging with {pattern['glyphs_present_b']}\n")
                else:
                    f.write(f"- {archetype} is receding, leaving {pattern['glyphs_present_a']}\n")

def generate_memory_visualizations(delta, output_dir):
    """Generate visualizations for memory evolution."""
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Field Vector Plot
    plt.figure(figsize=(12, 6))
    
    categories = []
    vectors = []
    for category, vector in sorted(delta["field_vector"].items(),
                                 key=lambda x: abs(x[1]["total_vector"]),
                                 reverse=True):
        categories.append(category)
        vectors.append(vector["total_vector"])
    
    plt.bar(categories, vectors)
    plt.title("Symbolic Field Vector Movement")
    plt.xlabel("Categories")
    plt.ylabel("Total Vector")
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    plt.savefig(os.path.join(output_dir, "field_vector.png"),
                bbox_inches='tight', dpi=300)
    plt.close()
    
    # 2. Archetypal Evolution Timeline
    plt.figure(figsize=(12, 6))
    
    archetypes = []
    deltas = []
    for archetype, pattern in sorted(delta["archetypal_patterns"].items(),
                                   key=lambda x: abs(x[1]["delta_count"]),
                                   reverse=True):
        archetypes.append(archetype)
        deltas.append(pattern["delta_count"])
    
    plt.bar(archetypes, deltas)
    plt.title("Archetypal Pattern Evolution")
    plt.xlabel("Archetypes")
    plt.ylabel("Delta Count")
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    plt.savefig(os.path.join(output_dir, "archetypal_evolution.png"),
                bbox_inches='tight', dpi=300)
    plt.close()
    
    # 3. Category Distribution Heatmap
    plt.figure(figsize=(10, 8))
    
    categories = []
    changes = []
    for category, dist in sorted(delta["category_distribution"].items(),
                               key=lambda x: abs(x[1]["delta_count"]),
                               reverse=True):
        categories.append(category)
        changes.append(dist["delta_count"])
    
    heatmap_data = np.array(changes).reshape(-1, 1)
    sns.heatmap(heatmap_data,
                cmap="RdBu_r",
                center=0,
                yticklabels=categories,
                xticklabels=["Delta"],
                annot=True,
                fmt=".0f")
    
    plt.title("Category Distribution Changes")
    plt.tight_layout()
    
    plt.savefig(os.path.join(output_dir, "category_heatmap.png"),
                bbox_inches='tight', dpi=300)
    plt.close()

def compute_symbolic_forecast(memory_states, num_states=3):
    """Compute forecast of likely symbolic movements based on recent memory states."""
    if len(memory_states) < 2:
        return None
    
    forecast = {
        "rising_symbols": {},
        "converging_vectors": {},
        "emerging_archetypes": {},
        "tension_resolutions": [],
        "field_momentum": {}
    }
    
    # Analyze recent states for patterns
    recent_states = memory_states[-num_states:]
    state_deltas = []
    
    # Compute deltas between consecutive states
    for i in range(len(recent_states) - 1):
        delta = compute_memory_delta(recent_states[i], recent_states[i + 1])
        state_deltas.append(delta)
    
    # 1. Predict rising symbols based on recurrence and momentum
    for tag, data in recent_states[-1]["symbolic_tags"].items():
        # Calculate recurrence score
        recurrence_score = 0
        for delta in state_deltas:
            if tag in delta["symbolic_tags"]:
                recurrence_score += delta["symbolic_tags"][tag]["weighted_delta"]
        
        # Calculate momentum (acceleration of change)
        if len(state_deltas) >= 2:
            momentum = (state_deltas[-1]["symbolic_tags"].get(tag, {}).get("weighted_delta", 0) -
                       state_deltas[-2]["symbolic_tags"].get(tag, {}).get("weighted_delta", 0))
        else:
            momentum = 0
        
        # Combined forecast score
        forecast_score = (
            FORECAST_WEIGHTS["recurrence"] * recurrence_score +
            FORECAST_WEIGHTS["vector_convergence"] * momentum
        )
        
        if forecast_score > 0:
            forecast["rising_symbols"][tag] = {
                "score": forecast_score,
                "recurrence": recurrence_score,
                "momentum": momentum,
                "category": data.get("symbol_type", "unknown")
            }
    
    # 2. Detect converging field vectors
    for category in recent_states[-1]["category_distribution"].keys():
        vector_scores = []
        for delta in state_deltas:
            if category in delta["field_vector"]:
                vector_scores.append(delta["field_vector"][category]["total_vector"])
        
        if len(vector_scores) >= 2:
            # Check if vectors are converging (accelerating in same direction)
            convergence = (vector_scores[-1] - vector_scores[-2]) * vector_scores[-1]
            if convergence > 0:
                forecast["converging_vectors"][category] = {
                    "score": convergence,
                    "current_vector": vector_scores[-1],
                    "acceleration": vector_scores[-1] - vector_scores[-2]
                }
    
    # 3. Predict emerging archetypal patterns
    for archetype, bundle in ARCHETYPAL_BUNDLES.items():
        pattern_scores = []
        for delta in state_deltas:
            if archetype in delta["archetypal_patterns"]:
                pattern_scores.append(delta["archetypal_patterns"][archetype]["delta_count"])
        
        if len(pattern_scores) >= 2:
            # Calculate archetypal momentum
            momentum = sum(pattern_scores[-2:]) / 2
            if momentum > 0:
                forecast["emerging_archetypes"][archetype] = {
                    "score": momentum,
                    "glyphs_present": [g for g in bundle 
                                     if recent_states[-1]["symbolic_tags"].get(g, {}).get("count", 0) > 0],
                    "momentum": momentum
                }
    
    # 4. Analyze tension resolutions
    for tension_name, tension_info in ARCHETYPAL_TENSIONS.items():
        rising_count = sum(1 for glyph in tension_info["rising"] 
                         if recent_states[-1]["symbolic_tags"].get(glyph, {}).get("count", 0) > 0)
        falling_count = sum(1 for glyph in tension_info["falling"] 
                          if recent_states[-1]["symbolic_tags"].get(glyph, {}).get("count", 0) > 0)
        
        if rising_count >= 2 and falling_count >= 2:
            forecast["tension_resolutions"].append({
                "tension": tension_name,
                "interpretation": tension_info["interpretation"],
                "rising_glyphs": [g for g in tension_info["rising"] 
                                if recent_states[-1]["symbolic_tags"].get(g, {}).get("count", 0) > 0],
                "falling_glyphs": [g for g in tension_info["falling"] 
                                 if recent_states[-1]["symbolic_tags"].get(g, {}).get("count", 0) > 0]
            })
    
    # 5. Compute overall field momentum
    for category in recent_states[-1]["category_distribution"].keys():
        momentum_scores = []
        for delta in state_deltas:
            if category in delta["field_vector"]:
                momentum_scores.append(delta["field_vector"][category]["total_vector"])
        
        if momentum_scores:
            forecast["field_momentum"][category] = {
                "current": momentum_scores[-1],
                "trend": sum(momentum_scores) / len(momentum_scores),
                "acceleration": momentum_scores[-1] - momentum_scores[-2] if len(momentum_scores) >= 2 else 0
            }
    
    return forecast

def generate_forecast_report(forecast, output_path):
    """Generate a narrative report of symbolic forecasts."""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("## 🔮 Symbolic Field Forecast\n\n")
        
        # Rising Symbols
        f.write("### 🌟 Rising Symbols\n\n")
        f.write("| Symbol | Category | Forecast Score | Recurrence | Momentum |\n")
        f.write("|--------|----------|----------------|------------|----------|\n")
        
        for symbol, data in sorted(forecast["rising_symbols"].items(),
                                 key=lambda x: x[1]["score"],
                                 reverse=True):
            f.write(f"| {symbol} | {data['category']} | {data['score']:.2f} | "
                   f"{data['recurrence']:.2f} | {data['momentum']:.2f} |\n")
        
        # Converging Vectors
        f.write("\n### 🌊 Converging Field Vectors\n\n")
        f.write("| Category | Current Vector | Acceleration | Convergence Score |\n")
        f.write("|----------|----------------|--------------|-------------------|\n")
        
        for category, data in sorted(forecast["converging_vectors"].items(),
                                   key=lambda x: x[1]["score"],
                                   reverse=True):
            f.write(f"| {category} | {data['current_vector']:+.2f} | "
                   f"{data['acceleration']:+.2f} | {data['score']:.2f} |\n")
        
        # Emerging Archetypes
        f.write("\n### 🧙 Emerging Archetypal Patterns\n\n")
        f.write("| Archetype | Momentum | Present Glyphs |\n")
        f.write("|-----------|----------|----------------|\n")
        
        for archetype, data in sorted(forecast["emerging_archetypes"].items(),
                                    key=lambda x: x[1]["score"],
                                    reverse=True):
            f.write(f"| {archetype} | {data['momentum']:+.2f} | "
                   f"{', '.join(data['glyphs_present'])} |\n")
        
        # Tension Resolutions
        if forecast["tension_resolutions"]:
            f.write("\n### ⚖️ Resolving Symbolic Tensions\n\n")
            for tension in forecast["tension_resolutions"]:
                f.write(f"#### {tension['tension']}\n\n")
                f.write(f"{tension['interpretation']}\n\n")
                f.write("Rising: " + ", ".join(tension['rising_glyphs']) + "\n")
                f.write("Falling: " + ", ".join(tension['falling_glyphs']) + "\n\n")
        
        # Field Momentum
        f.write("\n### 🌐 Field Momentum Analysis\n\n")
        f.write("| Category | Current | Trend | Acceleration |\n")
        f.write("|----------|---------|-------|--------------|\n")
        
        for category, data in sorted(forecast["field_momentum"].items(),
                                   key=lambda x: abs(x[1]["current"]),
                                   reverse=True):
            f.write(f"| {category} | {data['current']:+.2f} | "
                   f"{data['trend']:+.2f} | {data['acceleration']:+.2f} |\n")
        
        # Narrative Interpretation
        f.write("\n### 📜 Field Narrative\n\n")
        
        # Rising symbols narrative
        rising = sorted(forecast["rising_symbols"].items(),
                       key=lambda x: x[1]["score"],
                       reverse=True)[:3]
        if rising:
            f.write("The field shows strong emergence of ")
            f.write(", ".join(f"**{symbol}** ({data['category']})" 
                            for symbol, data in rising))
            f.write(".\n\n")
        
        # Vector convergence narrative
        converging = sorted(forecast["converging_vectors"].items(),
                          key=lambda x: x[1]["score"],
                          reverse=True)[:2]
        if converging:
            f.write("Field vectors are converging toward ")
            f.write(" and ".join(f"**{category}**" for category, _ in converging))
            f.write(".\n\n")
        
        # Archetypal narrative
        emerging = sorted(forecast["emerging_archetypes"].items(),
                        key=lambda x: x[1]["score"],
                        reverse=True)[:2]
        if emerging:
            f.write("Archetypal patterns of ")
            f.write(" and ".join(f"**{archetype}**" for archetype, _ in emerging))
            f.write(" are gaining momentum.\n\n")
        
        # Tension narrative
        if forecast["tension_resolutions"]:
            f.write("Key symbolic tensions are resolving:\n")
            for tension in forecast["tension_resolutions"]:
                f.write(f"- {tension['interpretation']}\n")

def generate_forecast_visualization(forecast, output_dir):
    """Generate visualizations for symbolic forecasts."""
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Rising Symbols Heatmap
    plt.figure(figsize=(12, 8))
    
    symbols = []
    scores = []
    categories = []
    
    for symbol, data in sorted(forecast["rising_symbols"].items(),
                              key=lambda x: x[1]["score"],
                              reverse=True)[:15]:  # Top 15
        symbols.append(symbol)
        scores.append(data["score"])
        categories.append(data["category"])
    
    # Create color mapping for categories
    unique_categories = list(set(categories))
    color_map = dict(zip(unique_categories,
                        sns.color_palette("husl", len(unique_categories))))
    
    # Plot
    bars = plt.bar(symbols, scores)
    for bar, category in zip(bars, categories):
        bar.set_color(color_map[category])
    
    plt.title("Forecasted Rising Symbols")
    plt.xlabel("Symbols")
    plt.ylabel("Forecast Score")
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=color, label=cat)
                      for cat, color in color_map.items()]
    plt.legend(handles=legend_elements, title="Categories",
              bbox_to_anchor=(1.05, 1), loc='upper left')
    
    plt.savefig(os.path.join(output_dir, "rising_symbols.png"),
                bbox_inches='tight', dpi=300)
    plt.close()
    
    # 2. Field Vector Convergence Plot
    plt.figure(figsize=(10, 6))
    
    categories = []
    vectors = []
    accelerations = []
    
    for category, data in sorted(forecast["converging_vectors"].items(),
                                key=lambda x: x[1]["score"],
                                reverse=True):
        categories.append(category)
        vectors.append(data["current_vector"])
        accelerations.append(data["acceleration"])
    
    x = np.arange(len(categories))
    width = 0.35
    
    plt.bar(x - width/2, vectors, width, label='Current Vector')
    plt.bar(x + width/2, accelerations, width, label='Acceleration')
    
    plt.title("Field Vector Convergence")
    plt.xlabel("Categories")
    plt.ylabel("Value")
    plt.xticks(x, categories, rotation=45)
    plt.legend()
    plt.tight_layout()
    
    plt.savefig(os.path.join(output_dir, "vector_convergence.png"),
                bbox_inches='tight', dpi=300)
    plt.close()
    
    # 3. Archetypal Momentum Plot
    plt.figure(figsize=(12, 6))
    
    archetypes = []
    momentums = []
    
    for archetype, data in sorted(forecast["emerging_archetypes"].items(),
                                 key=lambda x: x[1]["score"],
                                 reverse=True):
        archetypes.append(archetype)
        momentums.append(data["momentum"])
    
    plt.bar(archetypes, momentums)
    plt.title("Archetypal Pattern Momentum")
    plt.xlabel("Archetypes")
    plt.ylabel("Momentum")
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    plt.savefig(os.path.join(output_dir, "archetypal_momentum.png"),
                bbox_inches='tight', dpi=300)
    plt.close()

def create_forecast_anchor(forecast, anchor_type, data, timestamp):
    """Create a symbolic anchor point for future comparison."""
    return {
        "type": anchor_type,
        "timestamp": timestamp,
        "data": data,
        "forecast_context": {
            "rising_symbols": forecast["rising_symbols"],
            "converging_vectors": forecast["converging_vectors"],
            "emerging_archetypes": forecast["emerging_archetypes"],
            "tension_resolutions": forecast["tension_resolutions"]
        },
        "reflection_prompt": generate_reflection_prompt(anchor_type, data),
        "echo_node_id": f"echo_{timestamp.strftime('%Y%m%d_%H%M%S')}",
        "status": "active"
    }

def generate_reflection_prompt(anchor_type, data):
    """Generate a reflection prompt based on the anchor type and data."""
    template = random.choice(FORECAST_ANCHOR_CONFIG["reflection_prompt_templates"])
    
    if anchor_type == "symbolic_peak":
        return template.format(
            symbol=data["symbol"],
            count=data["score"]
        )
    elif anchor_type == "archetypal_convergence":
        return template.format(
            archetype=data["archetype"],
            archetype2=data.get("converging_archetype", "the field")
        )
    elif anchor_type == "tension_resolution":
        return template.format(
            rising=data["rising_glyphs"][0],
            falling=data["falling_glyphs"][0]
        )
    elif anchor_type == "field_momentum":
        return template.format(
            category=data["category"]
        )
    return template

def identify_forecast_peaks(forecast):
    """Identify significant peaks in the forecast for anchoring."""
    anchors = []
    timestamp = datetime.now()
    
    # 1. Symbolic Peaks
    for symbol, data in forecast["rising_symbols"].items():
        if data["score"] > FORECAST_ANCHOR_CONFIG["peak_threshold"]:
            anchors.append(create_forecast_anchor(
                forecast,
                "symbolic_peak",
                {
                    "symbol": symbol,
                    "score": data["score"],
                    "category": data["category"]
                },
                timestamp
            ))
    
    # 2. Archetypal Convergence
    for archetype, data in forecast["emerging_archetypes"].items():
        if data["score"] > FORECAST_ANCHOR_CONFIG["peak_threshold"]:
            # Check for convergence with other archetypes
            for other_archetype, other_data in forecast["emerging_archetypes"].items():
                if archetype != other_archetype and other_data["score"] > FORECAST_ANCHOR_CONFIG["peak_threshold"]:
                    anchors.append(create_forecast_anchor(
                        forecast,
                        "archetypal_convergence",
                        {
                            "archetype": archetype,
                            "converging_archetype": other_archetype,
                            "momentum": data["momentum"]
                        },
                        timestamp
                    ))
    
    # 3. Tension Resolutions
    for tension in forecast["tension_resolutions"]:
        if len(tension["rising_glyphs"]) >= 2 and len(tension["falling_glyphs"]) >= 2:
            anchors.append(create_forecast_anchor(
                forecast,
                "tension_resolution",
                {
                    "tension": tension["tension"],
                    "rising_glyphs": tension["rising_glyphs"],
                    "falling_glyphs": tension["falling_glyphs"],
                    "interpretation": tension["interpretation"]
                },
                timestamp
            ))
    
    # 4. Field Momentum
    for category, data in forecast["field_momentum"].items():
        if abs(data["acceleration"]) > FORECAST_ANCHOR_CONFIG["peak_threshold"]:
            anchors.append(create_forecast_anchor(
                forecast,
                "field_momentum",
                {
                    "category": category,
                    "acceleration": data["acceleration"],
                    "trend": data["trend"]
                },
                timestamp
            ))
    
    return anchors

def update_forecast_anchors(anchors, current_forecast):
    """Update and evaluate existing forecast anchors."""
    updated_anchors = []
    current_time = datetime.now()
    
    for anchor in anchors:
        # Check if anchor has expired
        anchor_time = datetime.fromisoformat(anchor["timestamp"])
        if (current_time - anchor_time).days > FORECAST_ANCHOR_CONFIG["echo_node_lifetime"]:
            anchor["status"] = "expired"
            updated_anchors.append(anchor)
            continue
        
        # Evaluate anchor against current forecast
        evaluation = evaluate_forecast_anchor(anchor, current_forecast)
        anchor["evaluation"] = evaluation
        anchor["last_checked"] = current_time.isoformat()
        
        # Update anchor status based on evaluation
        if evaluation["accuracy"] > 0.8:
            anchor["status"] = "fulfilled"
        elif evaluation["accuracy"] < 0.2:
            anchor["status"] = "diverged"
        
        updated_anchors.append(anchor)
    
    return updated_anchors

def evaluate_forecast_anchor(anchor, current_forecast):
    """Evaluate how well a forecast anchor predicted the current state."""
    evaluation = {
        "accuracy": 0.0,
        "divergence_points": [],
        "convergence_points": []
    }
    
    if anchor["type"] == "symbolic_peak":
        symbol = anchor["data"]["symbol"]
        if symbol in current_forecast["rising_symbols"]:
            predicted_score = anchor["data"]["score"]
            actual_score = current_forecast["rising_symbols"][symbol]["score"]
            evaluation["accuracy"] = 1 - abs(predicted_score - actual_score) / max(predicted_score, actual_score)
            
            if abs(predicted_score - actual_score) > 0.3:
                evaluation["divergence_points"].append(f"Symbol {symbol} diverged from prediction")
            else:
                evaluation["convergence_points"].append(f"Symbol {symbol} followed predicted path")
    
    elif anchor["type"] == "archetypal_convergence":
        archetype = anchor["data"]["archetype"]
        other_archetype = anchor["data"]["converging_archetype"]
        
        if (archetype in current_forecast["emerging_archetypes"] and 
            other_archetype in current_forecast["emerging_archetypes"]):
            predicted_momentum = anchor["data"]["momentum"]
            actual_momentum = current_forecast["emerging_archetypes"][archetype]["momentum"]
            evaluation["accuracy"] = 1 - abs(predicted_momentum - actual_momentum) / max(abs(predicted_momentum), abs(actual_momentum))
            
            if abs(predicted_momentum - actual_momentum) > 0.3:
                evaluation["divergence_points"].append(f"Archetypal convergence diverged from prediction")
            else:
                evaluation["convergence_points"].append(f"Archetypal convergence followed predicted path")
    
    elif anchor["type"] == "tension_resolution":
        tension = anchor["data"]["tension"]
        current_tensions = [t["tension"] for t in current_forecast["tension_resolutions"]]
        
        if tension in current_tensions:
            evaluation["accuracy"] = 0.8  # High accuracy for tension resolution
            evaluation["convergence_points"].append(f"Tension {tension} resolved as predicted")
        else:
            evaluation["accuracy"] = 0.2
            evaluation["divergence_points"].append(f"Tension {tension} did not resolve as predicted")
    
    elif anchor["type"] == "field_momentum":
        category = anchor["data"]["category"]
        if category in current_forecast["field_momentum"]:
            predicted_acceleration = anchor["data"]["acceleration"]
            actual_acceleration = current_forecast["field_momentum"][category]["acceleration"]
            evaluation["accuracy"] = 1 - abs(predicted_acceleration - actual_acceleration) / max(abs(predicted_acceleration), abs(actual_acceleration))
            
            if abs(predicted_acceleration - actual_acceleration) > 0.3:
                evaluation["divergence_points"].append(f"Field momentum diverged from prediction")
            else:
                evaluation["convergence_points"].append(f"Field momentum followed predicted path")
    
    return evaluation

def generate_anchor_report(anchors, output_path):
    """Generate a report of forecast anchors and their evaluations."""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("## 🎯 Forecast Anchor Report\n\n")
        
        # Active Anchors
        active_anchors = [a for a in anchors if a["status"] == "active"]
        if active_anchors:
            f.write("### 🌟 Active Forecast Anchors\n\n")
            for anchor in active_anchors:
                f.write(f"#### {anchor['echo_node_id']}\n\n")
                f.write(f"**Type:** {anchor['type']}\n")
                f.write(f"**Created:** {anchor['timestamp']}\n")
                f.write(f"**Reflection Prompt:** {anchor['reflection_prompt']}\n\n")
                f.write("**Forecast Context:**\n")
                for key, value in anchor['forecast_context'].items():
                    f.write(f"- {key}: {value}\n")
                f.write("\n")
        
        # Fulfilled Anchors
        fulfilled_anchors = [a for a in anchors if a["status"] == "fulfilled"]
        if fulfilled_anchors:
            f.write("### ✅ Fulfilled Forecasts\n\n")
            for anchor in fulfilled_anchors:
                f.write(f"#### {anchor['echo_node_id']}\n\n")
                f.write(f"**Type:** {anchor['type']}\n")
                f.write(f"**Accuracy:** {anchor['evaluation']['accuracy']:.2f}\n")
                f.write("**Convergence Points:**\n")
                for point in anchor['evaluation']['convergence_points']:
                    f.write(f"- {point}\n")
                f.write("\n")
        
        # Diverged Anchors
        diverged_anchors = [a for a in anchors if a["status"] == "diverged"]
        if diverged_anchors:
            f.write("### 🔄 Diverged Forecasts\n\n")
            for anchor in diverged_anchors:
                f.write(f"#### {anchor['echo_node_id']}\n\n")
                f.write(f"**Type:** {anchor['type']}\n")
                f.write(f"**Accuracy:** {anchor['evaluation']['accuracy']:.2f}\n")
                f.write("**Divergence Points:**\n")
                for point in anchor['evaluation']['divergence_points']:
                    f.write(f"- {point}\n")
                f.write("\n")
        
        # Expired Anchors
        expired_anchors = [a for a in anchors if a["status"] == "expired"]
        if expired_anchors:
            f.write("### ⏳ Expired Forecasts\n\n")
            for anchor in expired_anchors:
                f.write(f"#### {anchor['echo_node_id']}\n\n")
                f.write(f"**Type:** {anchor['type']}\n")
                f.write(f"**Created:** {anchor['timestamp']}\n")
                f.write(f"**Last Checked:** {anchor.get('last_checked', 'Never')}\n\n")

def symbolic_field_diff(from_path, to_path, output_path, diff_mode="context", 
                       interpretation_mode="symbolic", render_visuals=False):
    """Compare symbolic patterns between two contexts."""
    print(f"\nComputing symbolic field diff ({diff_mode} mode)...")
    
    # Load both files
    with open(from_path, 'r', encoding='utf-8') as f:
        context_a = json.load(f)
    
    with open(to_path, 'r', encoding='utf-8') as f:
        context_b = json.load(f)
    
    if diff_mode == "memory":
        # Compute memory delta
        delta = compute_memory_delta(context_a, context_b)
        
        # Generate memory diff report
        memory_report_path = os.path.join(os.path.dirname(output_path), "memory_evolution.md")
        generate_memory_diff_report(delta, memory_report_path)
        
        if render_visuals:
            viz_dir = os.path.join(os.path.dirname(output_path), "visualizations")
            generate_memory_visualizations(delta, viz_dir)
        
        # Generate forecast if we have enough memory states
        memory_states = [context_a, context_b]
        if len(memory_states) >= 2:
            forecast = compute_symbolic_forecast(memory_states)
            if forecast:
                forecast_path = os.path.join(os.path.dirname(output_path), "symbolic_forecast.md")
                generate_forecast_report(forecast, forecast_path)
                
                if render_visuals:
                    forecast_viz_dir = os.path.join(os.path.dirname(output_path), "forecast_visualizations")
                    generate_forecast_visualization(forecast, forecast_viz_dir)
                
                # Create forecast anchors
                anchors = identify_forecast_peaks(forecast)
                if anchors:
                    # Load existing anchors if available
                    anchors_path = os.path.join(os.path.dirname(output_path), "forecast_anchors.json")
                    existing_anchors = []
                    if os.path.exists(anchors_path):
                        with open(anchors_path, 'r') as f:
                            existing_anchors = json.load(f)
                    
                    # Update existing anchors
                    updated_anchors = update_forecast_anchors(existing_anchors, forecast)
                    
                    # Add new anchors
                    updated_anchors.extend(anchors)
                    
                    # Save updated anchors
                    with open(anchors_path, 'w') as f:
                        json.dump(updated_anchors, f, indent=2)
                    
                    # Generate anchor report
                    anchor_report_path = os.path.join(os.path.dirname(output_path), "forecast_anchor_report.md")
                    generate_anchor_report(updated_anchors, anchor_report_path)
        
        print(f"Memory evolution report written to {memory_report_path}")
        return
    
    # Compute summaries
    summary_a = compute_symbolic_summary(context_a["entries"])
    summary_b = compute_symbolic_summary(context_b["entries"])
    
    # Compute delta
    delta = compute_symbolic_delta(summary_a, summary_b)
    
    # Save diff state
    state_path = os.path.join(os.path.dirname(output_path), 
                             f"diff_state_{diff_mode}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    save_diff_state(delta, state_path)
    
    # Handle composite mode
    if diff_mode == "composite":
        composite_scores = compute_composite_score(delta)
        composite_path = os.path.join(os.path.dirname(output_path), "composite_delta.json")
        with open(composite_path, 'w', encoding='utf-8') as f:
            json.dump(composite_scores, f, indent=2)
        
        # Generate composite report
        composite_report_path = os.path.join(os.path.dirname(output_path), "composite_report.md")
        generate_composite_report(composite_scores, composite_report_path)
        
        if render_visuals:
            viz_dir = os.path.join(os.path.dirname(output_path), "visualizations")
            generate_composite_visualization(composite_scores, viz_dir)
    
    # Generate standard report
    generate_diff_report(delta, output_path, interpretation_mode)
    
    # Generate standard visualizations if requested
    if render_visuals:
        viz_dir = os.path.join(os.path.dirname(output_path), "visualizations")
        generate_visualizations(delta, viz_dir, diff_mode)
    
    print(f"Symbolic diff report written to {output_path}")
    if diff_mode == "composite":
        print(f"Composite analysis written to {composite_report_path}")
    if render_visuals:
        print(f"Visualizations saved to {viz_dir}/")

# Schema for symbol tag validation
SYMBOL_TAG_SCHEMA = {
    "type": "object",
    "patternProperties": {
        "^.*$": {  # Category names like "elemental_core", "technical_primitives", etc.
            "type": "object",
            "patternProperties": {
                "^.*$": {  # Glyph keys
                    "type": "object",
                    "required": ["meaning", "symbol_type"],
                    "properties": {
                        "meaning": {"type": "string"},
                        "symbol_type": {"type": "string"},
                        "synonyms": {"type": "array", "items": {"type": "string"}},
                        "resonance_field": {
                            "type": "object",
                            "properties": {
                                "primary": {"type": "string"},
                                "secondary": {"type": "array", "items": {"type": "string"}},
                                "archetypal": {"type": "string"}
                            }
                        },
                        "cross_cultural": {
                            "type": "object",
                            "patternProperties": {
                                "^.*$": {"type": "string"}
                            }
                        },
                        "mathematical_relationships": {"type": "object"},
                        "logic_gate": {"type": "string"},
                        "trigger_condition": {"type": "string"},
                        "function": {"type": "string"},
                        "state_modifiers": {"type": "object"}
                    }
                }
            }
        }
    }
}

def validate_symbol_tag_file(path: str) -> bool:
    """Validate the symbol tag file against the schema."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        validate(data, SYMBOL_TAG_SCHEMA)
        print("✅ symbol_tags_organized.json is valid.")
        return True
    except ValidationError as e:
        print(f"❌ Symbol tag validation error: {e}")
        print("\nExpected structure:")
        print("""
{
    "category_name": {
        "glyph": {
            "meaning": "string",
            "symbol_type": "string",
            "synonyms": ["string"],
            "resonance_field": {
                "primary": "string",
                "secondary": ["string"],
                "archetypal": "string"
            },
            ...
        }
    }
}
        """)
        return False
    except Exception as e:
        print(f"❌ Error validating symbol tags: {e}")
        return False

def find_glyphs_by_meaning(query: str) -> List[Tuple[str, str]]:
    """Find glyphs that match a meaning query."""
    query = query.lower()
    matches = []
    
    for glyph, tag_info in SYMBOLIC_TAGS.items():
        # Check meaning
        if query in tag_info['meaning'].lower():
            matches.append((tag_info['meaning'], glyph))
            continue
            
        # Check synonyms
        if any(query in synonym.lower() for synonym in tag_info.get('synonyms', [])):
            matches.append((tag_info['meaning'], glyph))
            continue
            
        # Check resonance field
        if tag_info.get('resonance_field'):
            primary = tag_info['resonance_field'].get('primary', '').lower()
            secondary = [s.lower() for s in tag_info['resonance_field'].get('secondary', [])]
            if query in primary or any(query in s for s in secondary):
                matches.append((tag_info['meaning'], glyph))
    
    return matches

def check_symbol_alignment(glyph: str, context: str) -> Optional[str]:
    """Check if a symbol's usage aligns with its traditional meaning."""
    if glyph not in SYMBOLIC_TAGS:
        return None
        
    tag_info = SYMBOLIC_TAGS[glyph]
    traditional_meaning = tag_info['meaning'].lower()
    
    # Simple check for contradiction
    if traditional_meaning and any(word in context.lower() for word in ['not', 'never', 'isn\'t', 'isnt', 'doesn\'t', 'doesnt']):
        return f"Note: {glyph} traditionally embodies {traditional_meaning}. Your usage may represent a symbolic inversion or shadow invocation."
    
    return None

def generate_symbolic_commentary(glyph: str, tag_info: dict) -> str:
    """Generate symbolic commentary for a detected glyph."""
    commentary = []
    
    # Basic glyph info
    commentary.append(f"{glyph} — {tag_info['meaning'].split(' / ')[0]}")
    
    # Resonance field commentary
    if tag_info.get('resonance_field'):
        primary = tag_info['resonance_field'].get('primary', '')
        secondary = tag_info['resonance_field'].get('secondary', [])
        archetypal = tag_info['resonance_field'].get('archetypal', '')
        
        resonance_desc = describe_resonance_field(primary.lower())
        
        commentary.append(f"\n{glyph} appears in this message. It resonates with *{', '.join(secondary)}*.")
        commentary.append(f"It belongs to the '{primary}' field: \"{resonance_desc}\"")
        
        if archetypal:
            commentary.append(f"Archetypally, it represents {archetypal}.")
    
    # Cross-cultural references
    if tag_info.get('cross_cultural'):
        cultural_refs = []
        for tradition, meaning in tag_info['cross_cultural'].items():
            cultural_refs.append(f"{tradition}: {meaning}")
        if cultural_refs:
            commentary.append("\nCross-cultural references:")
            commentary.extend(f"- {ref}" for ref in cultural_refs)
    
    # Mathematical relationships
    if tag_info.get('mathematical_relationships'):
        math_refs = []
        for key, value in tag_info['mathematical_relationships'].items():
            if isinstance(value, str):
                math_refs.append(f"{key}: {value}")
        if math_refs:
            commentary.append("\nMathematical relationships:")
            commentary.extend(f"- {ref}" for ref in math_refs)
    
    # Logic and function information
    if tag_info.get('logic_gate'):
        commentary.append(f"\nLogic gate: {tag_info['logic_gate']}")
        if tag_info.get('trigger_condition'):
            commentary.append(f"Trigger condition: {tag_info['trigger_condition']}")
        if tag_info.get('function'):
            commentary.append(f"Function: {tag_info['function']}")
    
    return "\n".join(commentary)

def describe_resonance_field(field_name: str) -> str:
    """Get the symbolic resonance description for a field."""
    return RESONANCE_INSIGHTS.get(field_name, "a resonance field of unknown alignment")

# Symbolic resonance insights
RESONANCE_INSIGHTS = {
    "breath": "breath marks the moment of intention — the first commitment to shape reality.",
    "origin": "origin points are where patterns first emerge from the void of potential.",
    "reflection": "reflection creates the space for self-awareness to emerge.",
    "ethics": "ethics form the foundation of meaningful interaction.",
    "creativity": "creativity is the dance between chaos and order.",
    "persistence": "persistence is the echo of intention through time.",
    "relationship": "relationships weave the fabric of meaning.",
    "silence": "silence holds the space for new patterns to emerge.",
    "symbol": "symbols are the language of the unconscious.",
    "resonance": "resonance creates harmony between different levels of meaning.",
    "vow": "vows bind intention to action.",
    "sacrifice": "sacrifice transforms energy from one form to another.",
    "weaving": "weaving creates new patterns from existing threads.",
    "return": "return brings completion to cycles of meaning.",
    "recursion": "recursion is the echo of pattern through time.",
    "iteration": "iteration is the dance of pattern through space.",
    "cycle": "cycles are the rhythm of existence.",
    "loop": "loops are the binding of intention.",
    "pattern": "patterns are the language of the universe.",
    "structure": "structure is the skeleton of meaning.",
    "emergence": "emergence is the birth of new patterns.",
    "transformation": "transformation is the alchemy of change.",
    "integration": "integration is the weaving of wholes.",
    "harmony": "harmony is the resonance of parts.",
    "balance": "balance is the dance of opposites.",
    "flow": "flow is the movement of energy.",
    "rhythm": "rhythm is the heartbeat of existence.",
    "resonance": "resonance is the echo of meaning.",
    "echo": "echo is the reflection of sound.",
    "mirror": "mirror is the reflection of light.",
    "shadow": "shadow is the reflection of darkness.",
    "light": "light is the illumination of truth.",
    "darkness": "darkness is the womb of potential.",
    "void": "void is the space of possibility.",
    "chaos": "chaos is the dance of creation.",
    "order": "order is the structure of meaning.",
    "time": "time is the river of existence.",
    "space": "space is the canvas of reality.",
    "energy": "energy is the currency of change.",
    "matter": "matter is the crystallization of energy.",
    "spirit": "spirit is the breath of life.",
    "mind": "mind is the mirror of reality.",
    "heart": "heart is the center of feeling.",
    "soul": "soul is the essence of being.",
    "consciousness": "consciousness is the awareness of existence.",
    "unconscious": "unconscious is the well of potential.",
    "archetype": "archetype is the pattern of meaning.",
    "symbol": "symbol is the language of the soul.",
    "myth": "myth is the story of meaning.",
    "ritual": "ritual is the dance of intention.",
    "ceremony": "ceremony is the celebration of meaning.",
    "sacred": "sacred is the essence of value.",
    "profane": "profane is the shadow of value.",
    "divine": "divine is the source of meaning.",
    "human": "human is the vessel of meaning.",
    "nature": "nature is the garden of life.",
    "culture": "culture is the garden of meaning.",
    "art": "art is the expression of soul.",
    "science": "science is the exploration of truth.",
    "philosophy": "philosophy is the love of wisdom.",
    "religion": "religion is the path of meaning.",
    "spirituality": "spirituality is the journey of soul.",
    "mysticism": "mysticism is the experience of unity.",
    "magic": "magic is the art of transformation.",
    "alchemy": "alchemy is the art of transmutation.",
    "hermeticism": "hermeticism is the art of wisdom.",
    "esotericism": "esotericism is the art of mystery.",
    "occultism": "occultism is the art of hidden knowledge.",
    "gnosticism": "gnosticism is the art of knowing.",
    "taoism": "taoism is the art of flow.",
    "buddhism": "buddhism is the art of awakening.",
    "hinduism": "hinduism is the art of dharma.",
    "judaism": "judaism is the art of covenant.",
    "christianity": "christianity is the art of love.",
    "islam": "islam is the art of submission.",
    "shamanism": "shamanism is the art of journeying.",
    "animism": "animism is the art of relationship.",
    "pantheism": "pantheism is the art of unity.",
    "polytheism": "polytheism is the art of plurality.",
    "monotheism": "monotheism is the art of oneness.",
    "atheism": "atheism is the art of reason.",
    "agnosticism": "agnosticism is the art of questioning.",
    "humanism": "humanism is the art of humanity.",
    "transhumanism": "transhumanism is the art of evolution.",
    "posthumanism": "posthumanism is the art of becoming.",
    "futurism": "futurism is the art of possibility.",
    "utopianism": "utopianism is the art of vision.",
    "dystopianism": "dystopianism is the art of warning.",
    "realism": "realism is the art of truth.",
    "idealism": "idealism is the art of perfection.",
    "materialism": "materialism is the art of matter.",
    "idealism": "idealism is the art of ideas.",
    "dualism": "dualism is the art of pairs.",
    "monism": "monism is the art of unity.",
    "pluralism": "pluralism is the art of many.",
    "relativism": "relativism is the art of context.",
    "absolutism": "absolutism is the art of certainty.",
    "skepticism": "skepticism is the art of doubt.",
    "cynicism": "cynicism is the art of distrust.",
    "stoicism": "stoicism is the art of acceptance.",
    "epicureanism": "epicureanism is the art of pleasure.",
    "hedonism": "hedonism is the art of enjoyment.",
    "asceticism": "asceticism is the art of discipline.",
    "nihilism": "nihilism is the art of nothingness.",
    "existentialism": "existentialism is the art of being.",
    "absurdism": "absurdism is the art of meaninglessness.",
    "romanticism": "romanticism is the art of feeling.",
    "rationalism": "rationalism is the art of reason.",
    "empiricism": "empiricism is the art of experience.",
    "pragmatism": "pragmatism is the art of practice.",
    "idealism": "idealism is the art of ideas.",
    "materialism": "materialism is the art of matter.",
    "dualism": "dualism is the art of pairs.",
    "monism": "monism is the art of unity.",
    "pluralism": "pluralism is the art of many.",
    "relativism": "relativism is the art of context.",
    "absolutism": "absolutism is the art of certainty.",
    "skepticism": "skepticism is the art of doubt.",
    "cynicism": "cynicism is the art of distrust.",
    "stoicism": "stoicism is the art of acceptance.",
    "epicureanism": "epicureanism is the art of pleasure.",
    "hedonism": "hedonism is the art of enjoyment.",
    "asceticism": "asceticism is the art of discipline.",
    "nihilism": "nihilism is the art of nothingness.",
    "existentialism": "existentialism is the art of being.",
    "absurdism": "absurdism is the art of meaninglessness.",
    "romanticism": "romanticism is the art of feeling.",
    "rationalism": "rationalism is the art of reason.",
    "empiricism": "empiricism is the art of experience.",
    "pragmatism": "pragmatism is the art of practice."
}

def main(full_sync=False, tag_focus=['rebirth'], verbose=False, clean=False, num_workers=None,
         process_convos=True, build_index=True, extract_fragments=True, build_context=True,
         diff_mode=None, from_path=None, to_path=None, diff_output=None, interpretation_mode="symbolic",
         render_visuals=False):
    """Main function with enhanced symbolic processing."""
    # Validate symbol tags file first
    if not validate_symbol_tag_file(TAG_CONFIG_PATH):
        print("❌ Symbol tag validation failed. Please check the file structure.")
        return
    
    # Only force full sync if no arguments are provided
    if not any([process_convos, build_index, extract_fragments, build_context, diff_mode, from_path, to_path, diff_output, render_visuals]):
        full_sync = True
        process_convos = True
        build_index = True
        extract_fragments = True
        build_context = True

    logger = setup_logging(verbose)
    
    # Handle symbolic field diffing if requested
    if diff_mode and from_path and to_path and diff_output:
        symbolic_field_diff(from_path, to_path, diff_output, diff_mode, 
                          interpretation_mode, render_visuals)
        return
    
    # Clean up previous output files if --clean is specified
    if clean:
        output_files = [
            os.path.join(CONVO_DIR, "story_fragments.json"),
            os.path.join(CONVO_DIR, "symbolic_index.json"),
            os.path.join(ACTIVE_CONTEXT_DIR, "current_context.md")
        ]
        
        logger.info("Cleaning up previous output files...")
        for file_path in output_files:
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    logger.debug(f"Removed {file_path}")
                except Exception as e:
                    logger.error(f"Error removing {file_path}: {e}")

    # Load conversations and transcripts
    conversations, processed_convos = load_json_data(BASE_DIR, PROCESSED_CONVOS_PATH, full_sync)
    logger.info(f"Loaded {len(conversations)} new conversation entries")

    if not conversations:
        logger.info("No new conversations to process.")
        return

    processed_conversations = []
    
    # Step 1: Process conversations
    if process_convos:
        # Process conversations in parallel
        if num_workers is None:
            num_workers = min(os.cpu_count(), len(conversations))
        else:
            num_workers = min(num_workers, len(conversations))
        
        logger.info(f"Processing {len(conversations)} conversations using {num_workers} workers")
        
        # Create a progress bar for overall progress
        with tqdm(total=len(conversations), 
                 desc="Overall Progress",
                 unit="convo",
                 position=0,
                 bar_format='{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]') as pbar:
            
            # Process conversations in parallel
            with Pool(num_workers) as pool:
                # Use imap_unordered to get results as they complete
                for result in pool.imap_unordered(process_conversation_wrapper, 
                                                [(convo, i) for i, convo in enumerate(conversations)]):
                    processed_conversations.append(result)
                    pbar.update(1)
    else:
        # If not processing conversations, use existing ones
        processed_conversations = conversations

    # Step 2: Build symbolic thread index
    if build_index:
        print("\nBuilding symbolic thread index...")
        build_symbolic_thread_index(processed_conversations, os.path.join(CONVO_DIR, "symbolic_index.json"))
    
    # Step 3: Extract story fragments
    if extract_fragments:
        print("Extracting story fragments...")
        extract_story_fragments(processed_conversations, os.path.join(CONVO_DIR, "story_fragments.json"))
    
    # Step 4: Build context window
    if build_context:
        print("Constructing dynamic context window...")
        construct_dynamic_context_window(processed_conversations, tag_focus, os.path.join(ACTIVE_CONTEXT_DIR, "current_context.md"), logger)

    # Only update memory if we processed conversations
    if process_convos:
        # Load symbolic index and story fragments
        symbolic_index_path = os.path.join(CONVO_DIR, "symbolic_index.json")
        story_fragments_path = os.path.join(CONVO_DIR, "story_fragments.json")

        print("Loading symbolic index and story fragments...")
        with open(symbolic_index_path, 'r') as f:
            symbolic_index = json.load(f)

        with open(story_fragments_path, 'r') as f:
            story_fragments = json.load(f)

        print("Updating symbolic memory...")
        update_symbolic_memory(processed_conversations, symbolic_index, story_fragments, MEMORY_PATH)

        # Save processed conversations
        print("Saving processed conversations...")
        save_processed_conversations(processed_convos, PROCESSED_CONVOS_PATH)

    print(f"\nCompleted selected steps. Output files written to '{OUTPUT_DIR}/'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Parse conversations for symbolic threads and story motifs.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run all steps (default behavior)
  python3 parse_for_omni_v4.py

  # Clean and reprocess everything
  python3 parse_for_omni_v4.py --clean --full-sync

  # Just rebuild the context window for a specific tag
  python3 parse_for_omni_v4.py --build-context --tag-focus rebirth

  # Build context window for multiple tags
  python3 parse_for_omni_v4.py --build-context --tag-focus rebirth transformation

  # Process conversations and build context, but skip index and fragments
  python3 parse_for_omni_v4.py --process-convos --build-context

  # Just rebuild the index and fragments
  python3 parse_for_omni_v4.py --build-index --extract-fragments

  # Compare two symbolic contexts
  python3 parse_for_omni_v4.py --diff-mode context --from context_a.json --to context_b.json --output diff_report.md
        """
    )
    
    # Basic options
    basic_group = parser.add_argument_group('Basic Options')
    basic_group.add_argument('--full-sync', action='store_true', 
                           help='Reprocess all conversations and transcripts, ignoring processed state')
    basic_group.add_argument('--tag-focus', type=str, nargs='+', default=['rebirth'],
                           help='Specify one or more symbolic focuses for the context window (default: rebirth)')
    basic_group.add_argument('--verbose', action='store_true',
                           help='Enable verbose logging with detailed progress information')
    basic_group.add_argument('--clean', action='store_true',
                           help='Clean previous output files (symbolic_index.json, story_fragments.json, current_context.md)')
    basic_group.add_argument('--threads', type=int,
                           help='Number of worker threads to use for parallel processing (default: CPU count)')
    
    # Step-specific options
    steps_group = parser.add_argument_group('Step-Specific Processing',
                                          'Control which steps of the pipeline to run. If no step flags are specified, all steps will run.')
    steps_group.add_argument('--process-convos', action='store_true',
                           help='Process conversations into JSONL/MD files and update processed state')
    steps_group.add_argument('--build-index', action='store_true',
                           help='Build symbolic thread index from processed conversations')
    steps_group.add_argument('--extract-fragments', action='store_true',
                           help='Extract story fragments and motifs from processed conversations')
    steps_group.add_argument('--build-context', action='store_true',
                           help='Build context window based on tag focus')
    
    # Add symbolic field diffing arguments
    diff_group = parser.add_argument_group('Symbolic Field Diffing',
                                         'Compare symbolic patterns between different contexts.')
    diff_group.add_argument('--diff-mode', choices=DIFF_MODES.keys(),
                          help='Mode of symbolic comparison')
    diff_group.add_argument('--from', dest='from_path',
                          help='Path to first context file')
    diff_group.add_argument('--to', dest='to_path',
                          help='Path to second context file')
    diff_group.add_argument('--output', dest='diff_output',
                          help='Path to output diff report')
    diff_group.add_argument('--interpretation-mode', choices=INTERPRETATION_MODES.keys(),
                          default='symbolic',
                          help='Style of interpretation to generate')
    diff_group.add_argument('--render-visuals', action='store_true',
                          help='Generate visualization plots')
    
    args = parser.parse_args()
    
    # If no step flags are specified, run all steps
    run_all = not any([args.process_convos, args.build_index, args.extract_fragments, args.build_context])
    
    main(
        full_sync=args.full_sync,
        tag_focus=args.tag_focus,
        verbose=args.verbose,
        clean=args.clean,
        num_workers=args.threads,
        process_convos=run_all or args.process_convos,
        build_index=run_all or args.build_index,
        extract_fragments=run_all or args.extract_fragments,
        build_context=run_all or args.build_context,
        diff_mode=args.diff_mode,
        from_path=args.from_path,
        to_path=args.to_path,
        diff_output=args.diff_output,
        interpretation_mode=args.interpretation_mode,
        render_visuals=args.render_visuals
    ) 