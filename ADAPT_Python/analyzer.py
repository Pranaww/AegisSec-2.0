from knowledge_base import KnowledgeBase
from models import UtilityScore
import random

class Analyzer:
    def __init__(self, kb: KnowledgeBase):
        self.kb = kb

    def analyze(self):
        """
        Rank the targets, scans, and attacks. 
        In a real scenario, this involves analyzing properties, probabilities of success, etc.
        For simplicity, we randomly rank them if they are valid.
        """
        print("[Analyzer] Running utility analysis...")
        
        # Rank targets
        target_scores = []
        for target_name, target in self.kb.targets.items():
            if not target.is_exploited():
                # Prefer targets with more properties discovered (just an example heuristic)
                score = len(target.properties) * 10.0 + random.uniform(0, 5)
                target_scores.append(UtilityScore(target_name, score))
        
        target_scores.sort(key=lambda x: x.score, reverse=True)
        self.kb.target_utility = target_scores

        # Rank Scans
        scan_scores = []
        for scan_name, scan in self.kb.scans.items():
            score = 50.0 + random.uniform(0, 10)
            scan_scores.append(UtilityScore(scan_name, score))
        scan_scores.sort(key=lambda x: x.score, reverse=True)
        self.kb.scan_utility = scan_scores

        # Rank Attacks
        attack_scores = []
        for attack_name, attack in self.kb.attacks.items():
            score = 80.0 + random.uniform(0, 20)
            attack_scores.append(UtilityScore(attack_name, score))
        attack_scores.sort(key=lambda x: x.score, reverse=True)
        self.kb.attack_utility = attack_scores

        print(f"[Analyzer] Computed utilities - Targets: {len(target_scores)}, Scans: {len(scan_scores)}, Attacks: {len(attack_scores)}")
