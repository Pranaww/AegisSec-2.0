from knowledge_base import KnowledgeBase
from typing import List, Tuple
from models import Action

class Planner:
    def __init__(self, kb: KnowledgeBase, max_scans: int = 5, max_attacks: int = 2):
        self.kb = kb
        self.max_scans = max_scans
        self.max_attacks = max_attacks
        self.plan: List[Tuple[Action, str]] = [] # A list of (Action, TargetName)

    def generate_plan(self):
        """
        Select highest utility targets and highest utility actions that have their guards satisfied.
        """
        print("[Planner] Generating attack/scan plan...")
        self.plan.clear()
        
        active_actions_count = len(self.kb.active_actions)
        
        # Determine available capacity (very simplified)
        slots_available = self.max_scans + self.max_attacks - active_actions_count
        
        for tu in self.kb.target_utility:
            if slots_available <= 0:
                break
                
            target = self.kb.targets.get(tu.option_name)
            if not target:
                continue
                
            # Try scheduling an attack first (preference over scan)
            for au in self.kb.attack_utility:
                if slots_available <= 0: break
                attack = self.kb.attacks.get(au.option_name)
                action_id = f"{attack.name}_{target.name}"
                
                # If not active, not complete, and guard passes, add to plan
                if not self.kb.is_action_active(action_id) and not self.kb.is_action_completed(action_id):
                    if attack.guard(self.kb, target):
                        print(f"[Planner] Adding ATTACK {attack.name} against {target.name}")
                        self.plan.append((attack, target.name))
                        slots_available -= 1

            # Try scheduling a scan if attack couldn't consume all slots
            for su in self.kb.scan_utility:
                if slots_available <= 0: break
                scan = self.kb.scans.get(su.option_name)
                action_id = f"{scan.name}_{target.name}"
                
                if not self.kb.is_action_active(action_id) and not self.kb.is_action_completed(action_id):
                    if scan.guard(self.kb, target):
                        print(f"[Planner] Adding SCAN {scan.name} against {target.name}")
                        self.plan.append((scan, target.name))
                        slots_available -= 1
        return self.plan

    def has_plan(self) -> bool:
        return len(self.plan) > 0

    def get_plan(self) -> List[Tuple[Action, str]]:
        return self.plan
