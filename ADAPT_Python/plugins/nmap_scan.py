import asyncio
from models import Scan, Target
from knowledge_base import KnowledgeBase

class NmapScan(Scan):
    def __init__(self):
        # We define a basic network scan action
        super().__init__(name="Nmap_Fast_Scan", target_name="")
        # A simple guard precondition: execute only if the target's IP is known and port 80 is not confirmed open
        self.guard = lambda kb, t: t.get_property("ip") is not None and t.get_property("port_80") != "open"

    async def execute(self, kb: KnowledgeBase, target: Target):
        """
        Simulate an Nmap execution using the system.
        In a real application, you would use python-nmap or subprocess to run real nmap commands.
        """
        ip = target.get_property("ip")
        print(f"[Nmap Plugin] Scanning {ip} using nmap -F ...")
        await asyncio.sleep(2) # Simulating scan delay
        
        # Simulating findings updating the KnowledgeBase
        print(f"[Nmap Plugin] Found Port 80 open on {ip}!")
        target.set_property("port_80", "open")
        target.set_property("http_service", "Apache")
