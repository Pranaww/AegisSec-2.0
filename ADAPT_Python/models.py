from dataclasses import dataclass, field
from typing import List, Dict, Callable, Any, Optional

@dataclass
class Property:
    name: str
    value: Any

@dataclass
class Target:
    name: str
    properties: Dict[str, Any] = field(default_factory=dict)
    
    def set_property(self, key: str, value: Any):
        self.properties[key] = value

    def get_property(self, key: str, default=None):
        return self.properties.get(key, default)

    def is_exploited(self) -> bool:
        state = self.get_property("EXPLOITATION_STATE", "Unexploited")
        return state in ["Escalated", "Compromised", "CnC"]

@dataclass
class Action:
    name: str
    target_name: str
    guard: Callable[['KnowledgeBase', 'Target'], bool] = lambda kb, target: True

@dataclass
class Scan(Action):
    scan_type: str = "Network"

@dataclass
class Attack(Action):
    steps: List[str] = field(default_factory=list)

@dataclass
class UtilityScore:
    option_name: str
    score: float
