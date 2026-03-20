from knowledge_base import KnowledgeBase
from models import Target

class Monitor:
    def __init__(self, kb: KnowledgeBase):
        self.kb = kb
        self.probes_running = 0

    def start_probe(self):
        self.probes_running += 1

    def end_probe(self):
        self.probes_running -= 1

    def has_active_probes(self) -> bool:
        return self.probes_running > 0

    def check_for_adaptation_need(self) -> bool:
        """
        Evaluate if adaptation (Analysis + Planning) is needed.
        For example, if we discovered a new target or a state changed.
        """
        # Simplistic logic: If we have targets and they aren't all exploited, we need adaptation
        unexploited = [t for t in self.kb.targets.values() if not t.is_exploited()]
        return len(unexploited) > 0

    def get_unexploited_targets(self):
        return [t for t in self.kb.targets.values() if not t.is_exploited()]
