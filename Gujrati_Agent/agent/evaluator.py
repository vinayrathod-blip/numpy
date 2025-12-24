from .state_machine import State

class Evaluator:
    def evaluate_tools(self, memory, eligibility_outputs):
        missing = set()
        for item in eligibility_outputs or []:
            for f in item["result"].get("missing_fields", []):
                missing.add(f)
        if missing:
            return State.RESOLVE_GAPS, list(missing)
        return State.SELECT_SCHEME, []
