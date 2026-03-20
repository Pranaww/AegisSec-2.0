import asyncio
from knowledge_base import KnowledgeBase
from typing import List, Tuple
from models import Action

class Executor:
    def __init__(self, kb: KnowledgeBase):
        self.kb = kb

    async def _run_action(self, action: Action, target_name: str, executor_callback):
        action_id = f"{action.name}_{target_name}"
        self.kb.record_action_start(action_id)
        
        target = self.kb.get_target(target_name)
        print(f"[Executor] -> Starting {action.name} on {target_name}...")
        
        try:
            # Here we would actually run a subprocess or an external tool plugin.
            # For demonstration, we use the executor_callback if it is provided by the action (via a plugin wrapper)
            # or simulate execution delay.
            if hasattr(action, 'execute'):
                await getattr(action, 'execute')(self.kb, target)
            else:
                await asyncio.sleep(1) # Simulate tool run
                print(f"[Executor] <- Finished empty action {action.name}")
        except Exception as e:
            print(f"[Executor] Action {action_id} failed with error: {str(e)}")
        finally:
            self.kb.record_action_complete(action_id)
            print(f"[Executor] <- Completed {action.name} on {target_name}")

    async def execute_plan(self, plan: List[Tuple[Action, str]]):
        if not plan:
            return

        print(f"[Executor] Executing plan with {len(plan)} actions...")
        tasks = []
        for action, target_name in plan:
            tasks.append(self._run_action(action, target_name, None))
        
        await asyncio.gather(*tasks)
        print("[Executor] Execution phase complete.")
