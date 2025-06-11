"""
Memory shard management system for storing and tracking significant interpretations
"""

import os
import json
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Union
from enum import Enum
from pathlib import Path

class ShardStatus(Enum):
    """Status of a memory shard"""
    ACTIVE = "active"
    FULFILLED = "fulfilled"
    DIVERGED = "diverged"
    UNRESOLVED = "unresolved"

@dataclass
class MemoryShard:
    """A memory shard storing a significant interpretation"""
    origin_context_id: str
    interpretation_summary: str
    forecast_path: Optional[str]
    result: ShardStatus
    associated_symbols: Dict[str, float]  # symbol -> weight
    voice: str
    depth: str
    timestamp: str
    resonance_score: float = 0.0
    echo_count: int = 0
    linked_shards: List[str] = None  # IDs of related shards
    
    def __post_init__(self):
        if self.linked_shards is None:
            self.linked_shards = []
    
    def to_dict(self) -> Dict:
        """Convert shard to dictionary format"""
        data = asdict(self)
        data['result'] = self.result.value
        return data
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'MemoryShard':
        """Create shard from dictionary format"""
        data['result'] = ShardStatus(data['result'])
        return cls(**data)

class MemoryShardManager:
    """Manages the creation, storage, and retrieval of memory shards"""
    
    def __init__(self, shard_dir: str):
        """Initialize the memory shard manager"""
        self.shard_dir = Path(shard_dir)
        self.shard_dir.mkdir(parents=True, exist_ok=True)
        self.index_path = self.shard_dir / "shard_index.jsonl"
        self._ensure_index_exists()
    
    def _ensure_index_exists(self):
        """Ensure the shard index file exists"""
        if not self.index_path.exists():
            self.index_path.touch()
    
    def _generate_shard_id(self) -> str:
        """Generate a unique shard ID"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"memory_shard_{timestamp}"
    
    def create_shard(self,
                    context_id: str,
                    interpretation: str,
                    symbols: Dict[str, float],
                    voice: str,
                    depth: str,
                    forecast_path: Optional[str] = None,
                    status: ShardStatus = ShardStatus.ACTIVE) -> str:
        """Create a new memory shard"""
        shard_id = self._generate_shard_id()
        shard = MemoryShard(
            origin_context_id=context_id,
            interpretation_summary=interpretation,
            forecast_path=forecast_path,
            result=status,
            associated_symbols=symbols,
            voice=voice,
            depth=depth,
            timestamp=datetime.now().isoformat()
        )
        
        # Save shard to file
        shard_path = self.shard_dir / f"{shard_id}.json"
        with open(shard_path, 'w', encoding='utf-8') as f:
            json.dump(shard.to_dict(), f, indent=2)
        
        # Add to index
        self._add_to_index(shard_id, shard)
        
        return shard_id
    
    def _add_to_index(self, shard_id: str, shard: MemoryShard):
        """Add a shard to the index"""
        index_entry = {
            "shard_id": shard_id,
            "timestamp": shard.timestamp,
            "mode": shard.voice,
            "depth": shard.depth,
            "summary": shard.interpretation_summary,
            "symbols": list(shard.associated_symbols.keys()),
            "result": shard.result.value,
            "linked_memory": None  # Will be updated if linked
        }
        
        with open(self.index_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(index_entry) + '\n')
    
    def get_shard(self, shard_id: str) -> Optional[MemoryShard]:
        """Retrieve a memory shard by ID"""
        shard_path = self.shard_dir / f"{shard_id}.json"
        if not shard_path.exists():
            return None
        
        with open(shard_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return MemoryShard.from_dict(data)
    
    def update_shard_status(self, shard_id: str, new_status: ShardStatus):
        """Update the status of a memory shard"""
        shard = self.get_shard(shard_id)
        if not shard:
            return
        
        shard.result = new_status
        shard_path = self.shard_dir / f"{shard_id}.json"
        with open(shard_path, 'w', encoding='utf-8') as f:
            json.dump(shard.to_dict(), f, indent=2)
        
        # Update index entry
        self._update_index_entry(shard_id, {"result": new_status.value})
    
    def _update_index_entry(self, shard_id: str, updates: Dict):
        """Update an entry in the index file"""
        # Read all entries
        entries = []
        with open(self.index_path, 'r', encoding='utf-8') as f:
            for line in f:
                entry = json.loads(line)
                if entry["shard_id"] == shard_id:
                    entry.update(updates)
                entries.append(entry)
        
        # Write back all entries
        with open(self.index_path, 'w', encoding='utf-8') as f:
            for entry in entries:
                f.write(json.dumps(entry) + '\n')
    
    def link_shards(self, shard_id1: str, shard_id2: str):
        """Link two memory shards together"""
        shard1 = self.get_shard(shard_id1)
        shard2 = self.get_shard(shard_id2)
        if not (shard1 and shard2):
            return
        
        # Update shard1
        if shard_id2 not in shard1.linked_shards:
            shard1.linked_shards.append(shard_id2)
            shard1_path = self.shard_dir / f"{shard_id1}.json"
            with open(shard1_path, 'w', encoding='utf-8') as f:
                json.dump(shard1.to_dict(), f, indent=2)
        
        # Update shard2
        if shard_id1 not in shard2.linked_shards:
            shard2.linked_shards.append(shard_id1)
            shard2_path = self.shard_dir / f"{shard_id2}.json"
            with open(shard2_path, 'w', encoding='utf-8') as f:
                json.dump(shard2.to_dict(), f, indent=2)
        
        # Update index entries
        self._update_index_entry(shard_id1, {"linked_memory": shard_id2})
        self._update_index_entry(shard_id2, {"linked_memory": shard_id1})
    
    def search_shards(self,
                     symbol: Optional[str] = None,
                     mode: Optional[str] = None,
                     status: Optional[ShardStatus] = None,
                     min_resonance: float = 0.0) -> List[Dict]:
        """Search for memory shards matching criteria"""
        results = []
        with open(self.index_path, 'r', encoding='utf-8') as f:
            for line in f:
                entry = json.loads(line)
                
                # Apply filters
                if symbol and symbol not in entry["symbols"]:
                    continue
                if mode and mode != entry["mode"]:
                    continue
                if status and status.value != entry["result"]:
                    continue
                
                # Get full shard data
                shard = self.get_shard(entry["shard_id"])
                if shard and shard.resonance_score >= min_resonance:
                    results.append(shard.to_dict())
        
        return results
    
    def compute_shard_resonance(self, shard_id: str, current_symbols: Dict[str, float]) -> float:
        """Compute resonance score between a shard and current symbols"""
        shard = self.get_shard(shard_id)
        if not shard:
            return 0.0
        
        # Compute weighted symbol overlap
        overlap_score = 0.0
        total_weight = 0.0
        
        for symbol, weight in shard.associated_symbols.items():
            if symbol in current_symbols:
                overlap_score += weight * current_symbols[symbol]
            total_weight += weight
        
        if total_weight == 0:
            return 0.0
        
        return overlap_score / total_weight
    
    def update_shard_resonance(self, shard_id: str, current_symbols: Dict[str, float]):
        """Update a shard's resonance score based on current symbols"""
        shard = self.get_shard(shard_id)
        if not shard:
            return
        
        shard.resonance_score = self.compute_shard_resonance(shard_id, current_symbols)
        shard_path = self.shard_dir / f"{shard_id}.json"
        with open(shard_path, 'w', encoding='utf-8') as f:
            json.dump(shard.to_dict(), f, indent=2)
    
    def get_echo_candidates(self, current_symbols: Dict[str, float], 
                          min_resonance: float = 0.7) -> List[Dict]:
        """Get shards that might echo in the current context"""
        candidates = []
        
        # Get all shards
        with open(self.index_path, 'r', encoding='utf-8') as f:
            for line in f:
                entry = json.loads(line)
                shard = self.get_shard(entry["shard_id"])
                if not shard:
                    continue
                
                # Compute resonance
                resonance = self.compute_shard_resonance(entry["shard_id"], current_symbols)
                if resonance >= min_resonance:
                    candidates.append({
                        "shard": shard.to_dict(),
                        "resonance": resonance
                    })
        
        # Sort by resonance
        candidates.sort(key=lambda x: x["resonance"], reverse=True)
        return candidates 