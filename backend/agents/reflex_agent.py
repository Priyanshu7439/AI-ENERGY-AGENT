class ReflexAgent:
    def decide(self, state):
        demand = state["demand"]
        solar = state["solar"]
        wind = state["wind"]

        renewable = solar + wind

        if renewable >= demand:
            allocation = {
                "solar": solar,
                "wind": wind,
                "grid": 0
            }
        else:
            allocation = {
                "solar": solar,
                "wind": wind,
                "grid": demand - renewable
            }

        return {
            "source_allocation": allocation,
            "reason": "Immediate response using available resources",
            "confidence": 0.6
        }