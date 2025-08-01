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

        #I am adding simple score logic rather than a static response
        """It will check for negative keywords and adjusts the score, making simulation more dynamic. In real application, this would be much more complex in terms of the scoring engine!"""

        #Simulated processing based on input
        text_context = payload.get("text_context", "").lower()
        score = 0.82 

        #Simple logic to make a little less static

        if "pointless" in text_context or "anymore" in text_context:
            score -= 0.4
        if "fine" in text_context and "guess" in text_context:
            score -= 0.2

        return {
        "axis_score": round(score, 2),
        "recursion_flags": ["slight_conflict", "hesitation"],
        "notes": "Mock output: detected mixed emotional recursion."
        }