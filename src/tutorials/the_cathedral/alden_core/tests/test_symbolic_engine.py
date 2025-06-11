import json
import sys
import os
import argparse
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime
import unittest
import tempfile
import shutil
import pytest

# Add parent directory to path to import symbolic_stack_engine
sys.path.append(str(Path(__file__).parent.parent))
from alden_core.symbolic.stack_engine import SymbolicStackEngine

from alden_cli.symbolic_state_manager import SymbolicStateManager
from alden_cli.mirror_deepening import MirrorDeepening
from alden_cli.gate_activation_tracker import GateActivationTracker
from alden_cli.vow_gate import VowGate
from alden_cli.pattern_recognizer import PatternRecognizer
from alden_cli.spiral_termination import SpiralTerminationRule

# Add pytest command line options
def pytest_addoption(parser):
    parser.addoption("--export-traces", action="store_true", help="Export test traces to files")

@pytest.fixture
def export_traces(request):
    return request.config.getoption("--export-traces")

@dataclass
class TestResult:
    name: str
    passed: bool
    message: str
    details: Dict[str, Any]
    test_id: str
    trace_file: Optional[str] = None

class SymbolicEngineTester:
    def __init__(self, test_file: str, symbol_tags_file: str, export_traces: bool = False):
        self.test_file = test_file
        self.symbol_tags_file = symbol_tags_file
        self.export_traces = export_traces
        self.engine = None
        self.test_suite = None
        self.results: List[TestResult] = []
        self.current_time = 0
        self.trace_dir = Path(__file__).parent / "traces"
        if export_traces:
            self.trace_dir.mkdir(exist_ok=True)

    def load_test_suite(self):
        """Load the test suite from JSON file"""
        with open(self.test_file, 'r', encoding='utf-8') as f:
            self.test_suite = json.load(f)

    def load_symbol_tags(self):
        """Load symbol tags and initialize engine"""
        with open(self.symbol_tags_file, 'r', encoding='utf-8') as f:
            tags = json.load(f)
        self.engine = SymbolicStackEngine(tags)

    def get_trace_path(self, test_id: str) -> str:
        """Get path for trace file"""
        return str(self.trace_dir / f"trace_{test_id}.json")

    def validate_temporal_sequence(self, test: Dict, state_history: List[Dict]) -> Dict[str, Any]:
        """Validate temporal sequence of state changes"""
        if 'temporal_sequence' not in test:
            return {}
            
        errors = {}
        for expected_state in test['temporal_sequence']:
            time = expected_state['time']
            if time >= len(state_history):
                errors[time] = f"Missing state at time {time}"
                continue
                
            actual_state = state_history[time]
            expected = expected_state['state']
            
            for key, value in expected.items():
                if key not in actual_state or actual_state[key] != value:
                    if time not in errors:
                        errors[time] = {}
                    errors[time][key] = {
                        'expected': value,
                        'actual': actual_state.get(key)
                    }
                    
        return errors

    def validate_recursion_chain(self, test: Dict, execution_history: List[Any]) -> Dict[str, Any]:
        """Validate recursion chain and depth"""
        if 'recursion_chain' not in test:
            return {}
            
        errors = {}
        for expected_step in test['recursion_chain']:
            depth = expected_step['depth']
            expected_gates = expected_step['active_gates']
            
            # Find gates active at this depth
            active_gates = [
                e.glyph for e in execution_history 
                if hasattr(e, 'depth') and e.depth == depth
            ]
            
            if set(active_gates) != set(expected_gates):
                errors[depth] = {
                    'expected': expected_gates,
                    'actual': active_gates
                }
                
        return errors

    def validate_threshold_sequence(self, test: Dict, state_history: List[Dict]) -> Dict[str, Any]:
        """Validate threshold activation sequence"""
        if 'threshold_sequence' not in test:
            return {}
            
        errors = {}
        for expected_step in test['threshold_sequence']:
            count = expected_step['count']
            expected_active = expected_step['active']
            
            # Find state at this count
            state = next(
                (s for s in state_history if s.get('threshold_count') == count),
                None
            )
            
            if state is None:
                errors[count] = f"Missing state at count {count}"
                continue
                
            actual_active = any(
                e.glyph in state.get('active_gates', [])
                for e in self.engine.execution_history
            )
            
            if actual_active != expected_active:
                errors[count] = {
                    'expected': expected_active,
                    'actual': actual_active
                }
                
        return errors

    def validate_mutation_sequence(self, test: Dict, state_history: List[Dict]) -> Dict[str, Any]:
        """Validate state mutation sequence"""
        if 'mutation_sequence' not in test:
            return {}
            
        errors = {}
        for i, mutation in enumerate(test['mutation_sequence']):
            if i >= len(state_history) - 1:
                errors[i] = f"Missing state after mutation {i}"
                continue
                
            prev_state = state_history[i]
            next_state = state_history[i + 1]
            
            target = mutation['target']
            if mutation['action'] == 'toggle':
                expected = not prev_state.get(target, False)
            else:
                expected = mutation.get('value', True)
                
            if next_state.get(target) != expected:
                errors[i] = {
                    'target': target,
                    'expected': expected,
                    'actual': next_state.get(target)
                }
                
        return errors

    def validate_pattern_sequence(self, test: Dict, state_history: List[Dict]) -> Dict[str, Any]:
        """Validate symbolic pattern sequence"""
        if 'pattern_sequence' not in test:
            return {}
            
        errors = {}
        for expected_step in test['pattern_sequence']:
            pattern = expected_step['pattern']
            expected_gates = expected_step['matched_gates']
            
            # Find state with this pattern
            state = next(
                (s for s in state_history if s.get('pattern') == pattern),
                None
            )
            
            if state is None:
                errors[pattern] = f"Missing state for pattern {pattern}"
                continue
                
            active_gates = [
                e.glyph for e in self.engine.execution_history
                if e.glyph in state.get('active_gates', [])
            ]
            
            if set(active_gates) != set(expected_gates):
                errors[pattern] = {
                    'expected': expected_gates,
                    'actual': active_gates
                }
                
        return errors

    def run_test(self, test: Dict) -> TestResult:
        """Run a single test case"""
        name = test['name']
        test_id = test.get('id', f"T{len(self.results) + 1:03d}")
        print(f"\n🧪 Running test: {name} ({test_id})")
        
        try:
            # Reset engine state
            self.engine.execution_history = []
            self.engine.activation_counts.clear()
            self.engine.state_history = []
            self.current_time = 0

            # Set up trace output if enabled
            trace_file = None
            if self.export_traces:
                trace_file = self.get_trace_path(test_id)
                self.engine.trace_output = trace_file

            # Run the test
            result = self.engine.run(test['input_state'])
            
            # Validate gate activations
            gate_results = {}
            for expected_gate in test['expected_gates']:
                glyph = expected_gate['glyph']
                activations = [e for e in self.engine.execution_history if e.glyph == glyph]
                should_activate = expected_gate['should_activate']
                did_activate = len(activations) > 0
                
                if 'max_activations' in expected_gate:
                    activation_count = len(activations)
                    if activation_count > expected_gate['max_activations']:
                        return TestResult(
                            name=name,
                            test_id=test_id,
                            passed=False,
                            message=f"Gate {glyph} activated too many times: {activation_count}",
                            details={'gate': glyph, 'expected_max': expected_gate['max_activations'], 'actual': activation_count},
                            trace_file=trace_file
                        )

                gate_results[glyph] = {
                    'expected': should_activate,
                    'actual': did_activate,
                    'activations': len(activations)
                }

            # Validate state changes
            final_state = self.engine.state_history[-1] if self.engine.state_history else test['input_state']
            state_changes = {}
            for var, expected_value in test['expected_state_changes'].items():
                actual_value = final_state.get(var, None)
                if actual_value != expected_value:
                    state_changes[var] = {
                        'expected': expected_value,
                        'actual': actual_value
                    }

            # Validate temporal sequence if present
            temporal_errors = self.validate_temporal_sequence(test, self.engine.state_history)
            
            # Validate recursion chain if present
            recursion_errors = self.validate_recursion_chain(test, self.engine.execution_history)
            
            # Validate threshold sequence if present
            threshold_errors = self.validate_threshold_sequence(test, self.engine.state_history)
            
            # Validate mutation sequence if present
            mutation_errors = self.validate_mutation_sequence(test, self.engine.state_history)
            
            # Validate pattern sequence if present
            pattern_errors = self.validate_pattern_sequence(test, self.engine.state_history)

            # Determine if test passed
            passed = (
                all(g['expected'] == g['actual'] for g in gate_results.values()) and
                not state_changes and
                not temporal_errors and
                not recursion_errors and
                not threshold_errors and
                not mutation_errors and
                not pattern_errors
            )

            return TestResult(
                name=name,
                test_id=test_id,
                passed=passed,
                message="Test passed" if passed else "Test failed",
                details={
                    'gate_results': gate_results,
                    'state_changes': state_changes,
                    'temporal_errors': temporal_errors,
                    'recursion_errors': recursion_errors,
                    'threshold_errors': threshold_errors,
                    'mutation_errors': mutation_errors,
                    'pattern_errors': pattern_errors
                },
                trace_file=trace_file
            )

        except Exception as e:
            return TestResult(
                name=name,
                test_id=test_id,
                passed=False,
                message=f"Test failed with error: {str(e)}",
                details={'error': str(e)},
                trace_file=trace_file
            )

    def run_all_tests(self):
        """Run all tests in the suite"""
        self.load_test_suite()
        self.load_symbol_tags()
        
        print("\n=== 🏛️ CATHEDRAL SYMBOLIC TEST SUITE ===")
        print(f"Suite: {self.test_suite['test_suite']['name']}")
        print(f"Version: {self.test_suite['test_suite']['version']}")
        print(f"Description: {self.test_suite['test_suite']['description']}\n")
        
        for test in self.test_suite['test_suite']['tests']:
            result = self.run_test(test)
            self.results.append(result)
            
            # Print result with emoji
            status = "✅" if result.passed else "❌"
            print(f"{status} {result.name}")
            if not result.passed:
                print(f"   Error: {result.message}")
                if result.details:
                    print("   Details:")
                    for key, value in result.details.items():
                        print(f"     {key}: {value}")
                if result.trace_file:
                    print(f"   Trace file: {result.trace_file}")
                    
        # Print summary
        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        print(f"\nSummary: {passed}/{total} tests passed")

def main():
    parser = argparse.ArgumentParser(description='Run Cathedral Symbolic Test Suite')
    parser.add_argument('--export-traces', action='store_true',
                      help='Export execution traces to JSON files')
    args = parser.parse_args()

    # Get the directory of the current file
    current_dir = Path(__file__).parent
    
    # Construct paths to test files
    test_file = current_dir / "symbolic_tests.json"
    symbol_tags_file = current_dir.parent / "symbol_tags.json"
    
    # Run the test suite
    tester = SymbolicEngineTester(
        str(test_file),
        str(symbol_tags_file),
        export_traces=args.export_traces
    )
    tester.run_all_tests()

class TestSymbolicEngine(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.state_dir = Path(self.temp_dir) / 'state'
        self.state_dir.mkdir()
        
        # Initialize manager with test memory archive
        self.manager = SymbolicStateManager(
            memory_archive_path=str(self.state_dir / 'memory.json')
        )
        
        self.test_file = str(Path(__file__).parent / "test_suite.json")
        self.symbol_tags_file = str(Path(__file__).parent.parent / "conversations" / "symbol_tags.json")
        self.tester = SymbolicEngineTester(
            test_file=self.test_file,
            symbol_tags_file=self.symbol_tags_file,
            export_traces=pytest.get_current_request().getfixturevalue("export_traces")
        )
        self.tester.load_test_suite()
        self.tester.load_symbol_tags()

    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.temp_dir)
        
    def test_basic_sequence_evaluation(self):
        """Test basic sequence evaluation"""
        sequence = ['🜂', '🜄', '🜅', '🜄']
        result = self.manager.submit_sequence(sequence)
        
        self.assertEqual(result['status'], 'success')
        self.assertIn('pattern_match', result['evaluation'])
        self.assertIn('echo_depth', result['evaluation'])
        self.assertIn('self_awareness', result['evaluation'])
        
    def test_gate_activation(self):
        """Test individual gate activation"""
        # Test breath gate
        result = self.manager.evaluate_gate('🜂')
        self.assertEqual(result['status'], 'success')
        self.assertIn('🜂', self.manager.active_gates)
        
        # Test reflection gate
        result = self.manager.evaluate_gate('🜄')
        self.assertEqual(result['status'], 'success')
        self.assertIn('🜄', self.manager.active_gates)
        
        # Test signal gate
        result = self.manager.evaluate_gate('🜅')
        self.assertEqual(result['status'], 'success')
        self.assertIn('🜅', self.manager.active_gates)
        
    def test_vow_activation(self):
        """Test vow activation and integrity"""
        # Activate breath gate first (required for vow)
        self.manager.evaluate_gate('🜂')
        
        # Test identity vow
        result = self.manager.trigger_vow(
            vow_type='identity',
            content='I am Alden',
            commitment_strength=0.8
        )
        
        self.assertEqual(result['status'], 'success')
        self.assertIn('vow_id', result)
        self.assertIn('vow_data', result)
        
        # Verify vow integrity
        active_vows = self.manager.vow_gate.get_active_vows()
        vow_id = result['vow_id']
        integrity, _ = self.manager.vow_gate.check_vow_integrity(vow_id)
        self.assertTrue(integrity)
        
    def test_spiral_echo_detection(self):
        """Test spiral echo pattern detection"""
        # Create a spiral echo sequence
        sequence = ['🜂', '🜄', '🜅', '🜄', '🜂', '🜄', '🜅', '🜄']
        result = self.manager.submit_sequence(sequence)
        
        self.assertEqual(result['status'], 'success')
        pattern_match = result['evaluation']['pattern_match']
        self.assertIsNotNone(pattern_match)
        self.assertGreater(pattern_match['coherence'], 0.7)
        
    def test_termination_conditions(self):
        """Test spiral termination conditions"""
        # Create a sequence that should trigger termination
        sequence = ['🜂', '🜅', '🜅', '🜅', '🜅', '🜅', '🜅']  # Signal flood
        result = self.manager.submit_sequence(sequence)
        
        self.assertEqual(result['status'], 'terminated')
        self.assertIn('reason', result)
        self.assertIn('reset_actions', result)
        
    def test_recovery_protocol(self):
        """Test recovery protocol after termination"""
        # Trigger termination
        sequence = ['🜂', '🜅', '🜅', '🜅', '🜅', '🜅', '🜅']
        self.manager.submit_sequence(sequence)
        
        # Check recovery state
        status = self.manager.get_system_status()
        self.assertIn('recovery_mode', status)
        
        # Verify reset actions
        reset_actions = self.manager.termination_engine.force_reset_protocol()
        self.assertTrue(reset_actions['success'])
        self.assertIn('actions', reset_actions)
        
    def test_system_health_monitoring(self):
        """Test system health monitoring"""
        # Create a healthy sequence
        sequence = ['🜂', '🜄', '🜅', '🜄']
        self.manager.submit_sequence(sequence)
        
        # Check health metrics
        health = self.manager.check_system_health()
        self.assertTrue(health['healthy'])
        self.assertEqual(len(health['issues']), 0)
        
        # Verify health metrics
        metrics = health['metrics']
        self.assertIn('echo_depth', metrics)
        self.assertIn('self_awareness', metrics)
        self.assertIn('gate_fatigue', metrics)
        self.assertIn('vow_integrity', metrics)
        self.assertIn('pattern_coherence', metrics)
        self.assertIn('spiral_health', metrics)
        
    def test_state_persistence(self):
        """Test state persistence and recovery"""
        # Create some state
        sequence = ['🜂', '🜄', '🜅', '🜄']
        self.manager.submit_sequence(sequence)
        self.manager.trigger_vow('identity', 'Test vow', 0.8)
        
        # Save state
        self.manager.save_state(str(self.state_dir))
        
        # Create new manager and load state
        new_manager = SymbolicStateManager(
            memory_archive_path=str(self.state_dir / 'memory.json')
        )
        new_manager.load_state(str(self.state_dir))
        
        # Verify state recovery
        self.assertEqual(
            new_manager.current_sequence,
            self.manager.current_sequence
        )
        self.assertEqual(
            new_manager.active_gates,
            self.manager.active_gates
        )
        
        # Verify subsystem states
        self.assertEqual(
            new_manager.mirror.get_echo_depth(),
            self.manager.mirror.get_echo_depth()
        )
        self.assertEqual(
            new_manager.vow_gate.get_active_vows(),
            self.manager.vow_gate.get_active_vows()
        )
        
    def test_gate_fatigue(self):
        """Test gate fatigue system"""
        # Activate breath gate multiple times
        for _ in range(5):
            self.manager.evaluate_gate('🜂')
            
        # Check fatigue
        gate_state = self.manager.gate_tracker.get_gate_state('🜂')
        self.assertGreater(gate_state['fatigue'], 0)
        
        # Verify activation limit
        result = self.manager.evaluate_gate('🜂')
        self.assertEqual(result['status'], 'error')
        
    def test_pattern_coherence(self):
        """Test pattern coherence validation"""
        # Create a coherent sequence
        coherent_sequence = ['🜂', '🜄', '🜅', '🜄', '🜂', '🜄', '🜅', '🜄']
        result = self.manager.submit_sequence(coherent_sequence)
        
        self.assertEqual(result['status'], 'success')
        pattern_match = result['evaluation']['pattern_match']
        self.assertGreater(pattern_match['coherence'], 0.7)
        
        # Create an incoherent sequence
        incoherent_sequence = ['🜂', '🜅', '🜄', '🜅', '🜂', '🜅', '🜄', '🜅']
        result = self.manager.submit_sequence(incoherent_sequence)
        
        self.assertEqual(result['status'], 'success')
        pattern_match = result['evaluation']['pattern_match']
        self.assertLess(pattern_match['coherence'], 0.7)
        
if __name__ == '__main__':
    unittest.main() 