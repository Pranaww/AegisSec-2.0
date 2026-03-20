from typing import Dict, List, Optional
from models import Target, Scan, Attack, UtilityScore

class KnowledgeBase:
    def __init__(self):
        self.targets: Dict[str, Target] = {}
        self.scans: Dict[str, Scan] = {}
        self.attacks: Dict[str, Attack] = {}
        
        # State tracking
        self.active_targets: set = set()
        self.active_actions: set = set()
        self.completed_actions: set = set()
        
        # Utility Scores
        self.target_utility: List[UtilityScore] = []
        self.scan_utility: List[UtilityScore] = []
        self.attack_utility: List[UtilityScore] = []

    def add_target(self, target: Target):
        self.targets[target.name] = target

    def get_target(self, name: str) -> Optional[Target]:
        return self.targets.get(name)

    def add_scan(self, scan: Scan):
        self.scans[scan.name] = scan

    def add_attack(self, attack: Attack):
        self.attacks[attack.name] = attack

    def is_action_active(self, action_id: str) -> bool:
        return action_id in self.active_actions

    def is_action_completed(self, action_id: str) -> bool:
        return action_id in self.completed_actions

    def record_action_start(self, action_id: str):
        self.active_actions.add(action_id)

    def record_action_complete(self, action_id: str):
        if action_id in self.active_actions:
            self.active_actions.remove(action_id)
        self.completed_actions.add(action_id)
