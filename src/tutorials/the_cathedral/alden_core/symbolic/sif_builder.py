"""
SIF Builder - Symbolic Instruction Format Builder

Builds and validates symbolic instruction sets for the Alden system,
ensuring proper structure and dependencies between instructions.
"""

from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass
from pathlib import Path
import json
from datetime import datetime
import uuid
import networkx as nx

@dataclass
class SIFInstruction:
    """Represents a single instruction in a SIF program"""
    instruction_id: str
    gate: str
    inputs: List[str]
    outputs: List[str]
    dependencies: List[str]
    parameters: Dict[str, Any]
    metadata: Dict[str, Any]

class SIFBuilder:
    """Builds and validates symbolic instruction sets"""
    
    def __init__(self, program_id: Optional[str] = None):
        self.program_id = program_id or str(uuid.uuid4())
        self.instructions: List[SIFInstruction] = []
        self.variables: Set[str] = set()
        self.dependency_graph = nx.DiGraph()
        
    def add_instruction(self, 
                       gate: str,
                       inputs: List[str],
                       outputs: List[str],
                       dependencies: List[str],
                       parameters: Dict[str, Any],
                       metadata: Optional[Dict[str, Any]] = None) -> str:
        """Add a new instruction to the program"""
        # Generate unique ID
        instruction_id = str(uuid.uuid4())
        
        # Create instruction
        instruction = SIFInstruction(
            instruction_id=instruction_id,
            gate=gate,
            inputs=inputs,
            outputs=outputs,
            dependencies=dependencies,
            parameters=parameters,
            metadata=metadata or {}
        )
        
        # Add to program
        self.instructions.append(instruction)
        
        # Update variables
        self.variables.update(inputs)
        self.variables.update(outputs)
        
        # Update dependency graph
        self.dependency_graph.add_node(instruction_id)
        for dep in dependencies:
            self.dependency_graph.add_edge(dep, instruction_id)
            
        return instruction_id
        
    def remove_instruction(self, instruction_id: str) -> bool:
        """Remove an instruction from the program"""
        # Find instruction
        instruction = next((i for i in self.instructions if i.instruction_id == instruction_id), None)
        if not instruction:
            return False
            
        # Remove from program
        self.instructions.remove(instruction)
        
        # Update variables
        self.variables.difference_update(instruction.inputs)
        self.variables.difference_update(instruction.outputs)
        
        # Update dependency graph
        self.dependency_graph.remove_node(instruction_id)
        
        return True
        
    def get_instruction(self, instruction_id: str) -> Optional[SIFInstruction]:
        """Get an instruction by ID"""
        return next((i for i in self.instructions if i.instruction_id == instruction_id), None)
        
    def get_dependent_instructions(self, instruction_id: str) -> List[str]:
        """Get IDs of instructions that depend on the given instruction"""
        return list(self.dependency_graph.successors(instruction_id))
        
    def get_dependency_chain(self, instruction_id: str) -> List[str]:
        """Get the full dependency chain for an instruction"""
        chain = []
        visited = set()
        
        def visit(node):
            if node in visited:
                return
            visited.add(node)
            for pred in self.dependency_graph.predecessors(node):
                visit(pred)
            chain.append(node)
            
        visit(instruction_id)
        return chain
        
    def validate(self) -> List[str]:
        """Validate the program structure"""
        errors = []
        
        # Check for cycles
        try:
            cycle = nx.find_cycle(self.dependency_graph)
            errors.append(f"Cyclic dependency detected: {' -> '.join(cycle)}")
        except nx.NetworkXNoCycle:
            pass
            
        # Check for undefined variables
        for inst in self.instructions:
            for var in inst.inputs:
                if var not in self.variables:
                    errors.append(f"Undefined input variable '{var}' in instruction {inst.instruction_id}")
                    
        # Check for missing dependencies
        for inst in self.instructions:
            for dep in inst.dependencies:
                if not any(i.instruction_id == dep for i in self.instructions):
                    errors.append(f"Missing dependency '{dep}' in instruction {inst.instruction_id}")
                    
        return errors
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert program to dictionary format"""
        return {
            'program_id': self.program_id,
            'generated_at': datetime.now().isoformat(),
            'instructions': [
                {
                    'instruction_id': i.instruction_id,
                    'gate': i.gate,
                    'inputs': i.inputs,
                    'outputs': i.outputs,
                    'dependencies': i.dependencies,
                    'parameters': i.parameters,
                    'metadata': i.metadata
                }
                for i in self.instructions
            ]
        }
        
    def save(self, output_file: str):
        """Save program to file"""
        data = self.to_dict()
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
            
    @classmethod
    def load(cls, input_file: str) -> 'SIFBuilder':
        """Load program from file"""
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        builder = cls(program_id=data['program_id'])
        
        for inst in data['instructions']:
            builder.add_instruction(
                gate=inst['gate'],
                inputs=inst['inputs'],
                outputs=inst['outputs'],
                dependencies=inst['dependencies'],
                parameters=inst['parameters'],
                metadata=inst.get('metadata', {})
            )
            
        return builder 