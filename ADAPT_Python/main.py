import asyncio
from mape_k import MAPEK
from models import Target, Attack
from plugins.nmap_scan import NmapScan
from knowledge_base import KnowledgeBase

class DummyExploit(Attack):
    def __init__(self):
        super().__init__(name="Dummy_HTTP_Exploit", target_name="")
        # Guard: Only attack if we know port 80 is open
        self.guard = lambda kb, t: t.get_property("port_80") == "open"

    async def execute(self, kb: KnowledgeBase, target: Target):
        print(f"[Apache Exploit Plugin] Attempting buffer overflow on {target.name}...")
        await asyncio.sleep(1.5)
        print(f"[Apache Exploit Plugin] Success! Root shell obtained on {target.name}.")
        target.set_property("EXPLOITATION_STATE", "Escalated")


async def main():
    apt_brain = MAPEK()

    # Define initial environment parameters
    t1 = Target("WebServer1")
    t1.set_property("ip", "192.168.1.100")
    apt_brain.kb.add_target(t1)

    t2 = Target("DatabaseServer")
    t2.set_property("ip", "192.168.1.101")
    apt_brain.kb.add_target(t2)

    # Load repertoire plugins
    apt_brain.kb.add_scan(NmapScan())
    apt_brain.kb.add_attack(DummyExploit())

    # Start the MAPE-K Loop
    await apt_brain.run()

if __name__ == "__main__":
    asyncio.run(main())
