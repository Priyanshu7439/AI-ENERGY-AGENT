class UtilityAgent:
    def decide(self, state):
        demand = state["demand"]
        solar = state["solar"]
        wind = state["wind"]
        price = state["price"]

        renewable = solar + wind

        # Prefer renewable fully
        used_renewable = min(renewable, demand)

        # Decide grid usage smartly
        remaining = demand - used_renewable

        if price > 8:  # expensive → reduce usage slightly
            remaining *= 0.9

        allocation = {
            "solar": solar,
            "wind": wind,
            "grid": max(0, remaining)
        }

        return {
            "source_allocation": allocation,
            "reason": "Optimizing cost vs demand",
            "confidence": 0.85
        }