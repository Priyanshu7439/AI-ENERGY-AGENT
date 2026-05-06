import numpy as np

class LearningAgent:
    def __init__(self):
        self.history = []

    def predict_demand(self):
        if len(self.history) < 3:
            return self.history[-1] if self.history else 50
        return np.mean(self.history[-3:])

    def decide(self, state):
        current_demand = state["demand"]
        solar = state["solar"]
        wind = state["wind"]

        self.history.append(current_demand)

        predicted = self.predict_demand()

        # 🔥 Smarter prediction blending
        adjusted_demand = 0.7 * current_demand + 0.3 * predicted

        renewable = solar + wind
        grid_needed = max(0, adjusted_demand - renewable)

        return {
            "source_allocation": {
                "solar": solar,
                "wind": wind,
                "grid": grid_needed
            },
            "reason": "Adaptive demand prediction",
            "confidence": 0.9
        }