class DecisionEngine:
    def evaluate(self, allocation, state):
        demand = state["demand"]
        price = state["price"]

        solar = allocation["solar"]
        wind = allocation["wind"]
        grid = allocation["grid"]

        total_supply = solar + wind + grid

        satisfaction = min(total_supply / demand, 1)
        cost = grid * price
        renewable_ratio = (solar + wind) / total_supply if total_supply > 0 else 0

        return {
            "satisfaction": satisfaction,
            "cost": cost,
            "renewable_ratio": renewable_ratio
        }

    def score(self, metrics, state):
        demand = state["demand"]

        # 🔥 Dynamic scoring (THIS IS THE UPGRADE)
        if demand > 80:
            return (
                0.7 * metrics["satisfaction"] +
                0.2 * metrics["renewable_ratio"] -
                0.1 * metrics["cost"] / 100
            )
        else:
            return (
                0.4 * metrics["satisfaction"] +
                0.3 * metrics["renewable_ratio"] -
                0.3 * metrics["cost"] / 100
            )

    def resolve(self, state, agent_outputs):
        best_agent = None
        best_score = float("-inf")
        best_result = None

        all_results = {}

        for name, output in agent_outputs.items():
            allocation = output["source_allocation"]

            metrics = self.evaluate(allocation, state)
            score = self.score(metrics, state)

            all_results[name] = {
                "metrics": metrics,
                "score": score
            }

            if score > best_score:
                best_score = score
                best_agent = name
                best_result = allocation

        return {
            "selected_agent": best_agent,
            "final_allocation": best_result,
            "all_results": all_results
        }