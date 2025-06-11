"""
SIF Linter - Symbolic Instruction Format Validator

Validates symbolic instruction sets for structural soundness,
detecting issues like unused variables, dangling dependencies,
cyclic instruction graphs, and missing threshold/pattern data.
"""

from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass
from pathlib import Path
import json
from datetime import datetime
from collections import defaultdict
import argparse
import networkx as nx

@dataclass
class LintIssue:
    """Represents a linting issue found in a SIF program"""
    issue_type: str
    severity: str  # 'error', 'warning', 'info'
    message: str
    location: Dict[str, Any]  # instruction_id, line, etc.
    context: Dict[str, Any]  # Additional context about the issue

@dataclass
class LintResult:
    """Results of linting a SIF program"""
    program_id: str
    issues: List[LintIssue]
    metadata: Dict[str, Any]
    dependency_graph: nx.DiGraph
    variable_usage: Dict[str, List[str]]  # var -> [instruction_ids]
    instruction_coverage: Dict[str, Set[str]]  # instruction_id -> {vars}

class SIFLinter:
    """Validates symbolic instruction sets for structural soundness"""
    
    def __init__(self, sif_file: str):
        self.sif_file = sif_file
        self.program = None
        self.result = None
        
    def load_program(self):
        """Load SIF program from file"""
        with open(self.sif_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.program = data
            
    def build_dependency_graph(self) -> nx.DiGraph:
        """Build directed graph of instruction dependencies"""
        G = nx.DiGraph()
        
        # Add nodes
        for inst in self.program['instructions']:
            G.add_node(inst['instruction_id'])
            
        # Add edges
        for inst in self.program['instructions']:
            for dep in inst['dependencies']:
                G.add_edge(dep, inst['instruction_id'])
                
        return G
        
    def analyze_variable_usage(self) -> Tuple[Dict[str, List[str]], Dict[str, Set[str]]]:
        """Analyze variable usage across instructions"""
        var_usage = defaultdict(list)
        inst_coverage = defaultdict(set)
        
        for inst in self.program['instructions']:
            # Track variables used by this instruction
            for var in inst['inputs']:
                var_usage[var].append(inst['instruction_id'])
                inst_coverage[inst['instruction_id']].add(var)
                
            for var in inst['outputs']:
                var_usage[var].append(inst['instruction_id'])
                inst_coverage[inst['instruction_id']].add(var)
                
        return dict(var_usage), dict(inst_coverage)
        
    def check_unused_variables(self) -> List[LintIssue]:
        """Check for variables that are defined but never used"""
        issues = []
        var_usage, _ = self.analyze_variable_usage()
        
        for var, usages in var_usage.items():
            if len(usages) == 1:  # Only defined once
                inst_id = usages[0]
                inst = next(i for i in self.program['instructions'] if i['instruction_id'] == inst_id)
                if var in inst['outputs']:  # Variable is only written to
                    issues.append(LintIssue(
                        issue_type='unused_variable',
                        severity='warning',
                        message=f"Variable '{var}' is defined but never used",
                        location={'instruction_id': inst_id},
                        context={'variable': var}
                    ))
                    
        return issues
        
    def check_dangling_dependencies(self) -> List[LintIssue]:
        """Check for dependencies that don't exist"""
        issues = []
        valid_ids = {inst['instruction_id'] for inst in self.program['instructions']}
        
        for inst in self.program['instructions']:
            for dep in inst['dependencies']:
                if dep not in valid_ids:
                    issues.append(LintIssue(
                        issue_type='dangling_dependency',
                        severity='error',
                        message=f"Dependency '{dep}' does not exist",
                        location={'instruction_id': inst['instruction_id']},
                        context={'dependency': dep}
                    ))
                    
        return issues
        
    def check_cyclic_dependencies(self) -> List[LintIssue]:
        """Check for cycles in the dependency graph"""
        issues = []
        G = self.build_dependency_graph()
        
        try:
            cycle = nx.find_cycle(G)
            issues.append(LintIssue(
                issue_type='cyclic_dependency',
                severity='error',
                message="Cyclic dependency detected",
                location={'cycle': cycle},
                context={'cycle_length': len(cycle)}
            ))
        except nx.NetworkXNoCycle:
            pass
            
        return issues
        
    def check_threshold_gates(self) -> List[LintIssue]:
        """Check threshold gates for required parameters"""
        issues = []
        
        for inst in self.program['instructions']:
            if inst['gate'] == 'THRESHOLD':
                params = inst['parameters']
                if 'threshold' not in params or 'count' not in params:
                    issues.append(LintIssue(
                        issue_type='missing_threshold_params',
                        severity='error',
                        message="Threshold gate missing required parameters",
                        location={'instruction_id': inst['instruction_id']},
                        context={'parameters': params}
                    ))
                    
        return issues
        
    def check_pattern_gates(self) -> List[LintIssue]:
        """Check pattern gates for required data"""
        issues = []
        
        for inst in self.program['instructions']:
            if inst['gate'] in ['PATTERN', 'RECURSION']:
                if 'pattern' not in inst['parameters']:
                    issues.append(LintIssue(
                        issue_type='missing_pattern_data',
                        severity='error',
                        message=f"{inst['gate']} gate missing pattern data",
                        location={'instruction_id': inst['instruction_id']},
                        context={'gate': inst['gate']}
                    ))
                    
        return issues
        
    def check_input_output_consistency(self) -> List[LintIssue]:
        """Check for consistency between inputs and outputs"""
        issues = []
        var_usage, inst_coverage = self.analyze_variable_usage()
        
        for inst in self.program['instructions']:
            # Check if all inputs are available
            for input_var in inst['inputs']:
                if input_var not in var_usage:
                    issues.append(LintIssue(
                        issue_type='undefined_input',
                        severity='error',
                        message=f"Input variable '{input_var}' is undefined",
                        location={'instruction_id': inst['instruction_id']},
                        context={'variable': input_var}
                    ))
                    
            # Check for output conflicts
            for output_var in inst['outputs']:
                if output_var in var_usage:
                    prev_uses = var_usage[output_var]
                    if len(prev_uses) > 1:  # Variable used multiple times
                        issues.append(LintIssue(
                            issue_type='output_conflict',
                            severity='warning',
                            message=f"Output variable '{output_var}' is redefined",
                            location={'instruction_id': inst['instruction_id']},
                            context={'previous_uses': prev_uses}
                        ))
                        
        return issues
        
    def lint(self) -> LintResult:
        """Run all linting checks and return results"""
        if not self.program:
            self.load_program()
            
        # Run all checks
        issues = []
        issues.extend(self.check_unused_variables())
        issues.extend(self.check_dangling_dependencies())
        issues.extend(self.check_cyclic_dependencies())
        issues.extend(self.check_threshold_gates())
        issues.extend(self.check_pattern_gates())
        issues.extend(self.check_input_output_consistency())
        
        # Build dependency graph
        G = self.build_dependency_graph()
        
        # Analyze variable usage
        var_usage, inst_coverage = self.analyze_variable_usage()
        
        # Create result
        self.result = LintResult(
            program_id=self.program['program_id'],
            issues=issues,
            metadata={
                'generated_at': datetime.now().isoformat(),
                'instruction_count': len(self.program['instructions']),
                'issue_count': len(issues),
                'error_count': sum(1 for i in issues if i.severity == 'error'),
                'warning_count': sum(1 for i in issues if i.severity == 'warning')
            },
            dependency_graph=G,
            variable_usage=var_usage,
            instruction_coverage=inst_coverage
        )
        
        return self.result
        
    def save_report(self, output_file: Optional[str] = None, format: str = 'json'):
        """Save linting report to file"""
        if not self.result:
            self.lint()
            
        if not output_file:
            output_file = str(Path(self.sif_file).parent / f"lint_report_{self.result.program_id}.{format}")
            
        if format == 'json':
            self._save_json(output_file)
        elif format == 'markdown':
            self._save_markdown(output_file)
        elif format == 'html':
            self._save_html(output_file)
        else:
            raise ValueError(f"Unsupported format: {format}")
            
        return output_file
        
    def _save_json(self, output_file: str):
        """Save report in JSON format"""
        report = {
            'program_id': self.result.program_id,
            'metadata': self.result.metadata,
            'issues': [
                {
                    'issue_type': i.issue_type,
                    'severity': i.severity,
                    'message': i.message,
                    'location': i.location,
                    'context': i.context
                }
                for i in self.result.issues
            ]
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
            
    def _save_markdown(self, output_file: str):
        """Save report in Markdown format"""
        md = [
            f"# SIF Lint Report",
            f"Generated: {self.result.metadata['generated_at']}",
            "",
            "## Program Information",
            f"- Program ID: {self.result.program_id}",
            f"- Instructions: {self.result.metadata['instruction_count']}",
            f"- Issues: {self.result.metadata['issue_count']}",
            f"- Errors: {self.result.metadata['error_count']}",
            f"- Warnings: {self.result.metadata['warning_count']}",
            "",
            "## Issues",
        ]
        
        for issue in self.result.issues:
            md.extend([
                f"### {issue.issue_type} ({issue.severity})",
                f"- Message: {issue.message}",
                f"- Location: {issue.location}",
                f"- Context: {issue.context}",
                ""
            ])
            
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(md))
            
    def _save_html(self, output_file: str):
        """Save report in HTML format"""
        html = [
            "<!DOCTYPE html>",
            "<html>",
            "<head>",
            "    <title>SIF Lint Report</title>",
            "    <style>",
            "        body { font-family: monospace; margin: 2em; }",
            "        .section { margin: 1em 0; }",
            "        .error { color: red; }",
            "        .warning { color: orange; }",
            "        .info { color: blue; }",
            "    </style>",
            "</head>",
            "<body>",
            f"<h1>SIF Lint Report</h1>",
            f"<p>Generated: {self.result.metadata['generated_at']}</p>",
            "",
            "<div class='section'>",
            "<h2>Program Information</h2>",
            f"<p>Program ID: {self.result.program_id}</p>",
            f"<p>Instructions: {self.result.metadata['instruction_count']}</p>",
            f"<p>Issues: {self.result.metadata['issue_count']}</p>",
            f"<p>Errors: {self.result.metadata['error_count']}</p>",
            f"<p>Warnings: {self.result.metadata['warning_count']}</p>",
            "</div>",
            "",
            "<div class='section'>",
            "<h2>Issues</h2>",
            *[f"<div class='{i.severity}'>"
              f"<h3>{i.issue_type}</h3>"
              f"<p>Message: {i.message}</p>"
              f"<p>Location: {i.location}</p>"
              f"<p>Context: {i.context}</p>"
              f"</div>"
              for i in self.result.issues]
        ]
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(html)) 