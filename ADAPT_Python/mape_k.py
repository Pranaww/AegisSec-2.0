import asyncio
from knowledge_base import KnowledgeBase
from monitor import Monitor
from analyzer import Analyzer
from planner import Planner
from executor import Executor

class MAPEK:
    def __init__(self):
        self.kb = KnowledgeBase()
        self.monitor = Monitor(self.kb)
        self.analyzer = Analyzer(self.kb)
        self.planner = Planner(self.kb)
        self.executor = Executor(self.kb)
        self.loop_count = 0
        self.max_loops = 5

    async def run(self):
        print("====== [ADAPT initialized. Starting MAPE-K loop] ======")
        while self.loop_count < self.max_loops:
            self.loop_count += 1
            print(f"\n--- [MAPE-K] Loop {self.loop_count} ---")
            
            # Monitor Phase
            if self.monitor.has_active_probes():
                print("[Monitor] Probes are currently running. Waiting...")
                await asyncio.sleep(1)
                continue

            adaptation_needed = self.monitor.check_for_adaptation_need()
            if not adaptation_needed and self.loop_count > 1:
                print("All known targets are exploited or no adaptation is needed. Terminating.")
                break
                
            # Analyze Phase
            self.analyzer.analyze()

            # Plan Phase
            plan = self.planner.generate_plan()

            # Execute Phase
            if self.planner.has_plan():
                await self.executor.execute_plan(plan)
            else:
                print("No viable plan could be generated. Ending loop.")
                break

            await asyncio.sleep(1) # Pause to prevent tight looping

        print("====== [ADAPT Run Complete] ======")
