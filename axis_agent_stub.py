# axis_agent_stub.py
class AxisAgentStub:
    def __init__(self):
        print("AXIS stub initialized.")
    def analyze(self, payload: dict) -> dict:
        """
        Simulated AXIS analysis of incoming signals.
        Expected payload format:
        {
        "user_id": str,
        "hrv_data": list,        # HRV time-series or summarized metrics
        "text_context": str,     # raw or preprocessed chat input
        "timestamp": str         # ISO timestamp
        }
        """
        
        # Simulated processing based on input
        score = 0.82
        if "pointless" in payload.get("text_context", "").lower():
            score -= 0.3
        return {
        "axis_score": 0.82,
        "recursion_flags": ["slight_conflict", "hesitation"],
        "notes": "Mock output: detected mixed emotional recursion."
        }