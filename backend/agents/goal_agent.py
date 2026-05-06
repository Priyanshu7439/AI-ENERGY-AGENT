class GoalBasedAgent:
    def decide(self, state):
        demand = state["demand"]
        solar = state["solar"]
        wind = state["wind"]

        renewable = solar + wind
        grid_needed = max(0, demand - renewable)

        allocation = {
            "solar": solar,
            "wind": wind,
            "grid": grid_needed
        }

        return {
            "source_allocation": allocation,
            "reason": "Ensuring demand satisfaction",
            "confidence": 0.8
        }