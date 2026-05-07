from backend.simulation.simulator import Simulator
from backend.agents.reflex_agent import ReflexAgent
from backend.agents.goal_agent import GoalBasedAgent
from backend.agents.utility_agent import UtilityAgent
from backend.agents.learning_agent import LearningAgent
from backend.core.resolver import DecisionEngine


class SimulationService:
    def __init__(self, hours=24):
        self.simulator = Simulator(hours=hours)

        # Agents
        self.reflex = ReflexAgent()
        self.goal = GoalBasedAgent()
        self.utility = UtilityAgent()
        self.learning = LearningAgent()

        # Decision Engine
        self.decision_engine = DecisionEngine()

    def run(self):
        df = self.simulator.run()

        results = []

        for _, row in df.iterrows():
            state = {
                "demand": row["demand"],
                "solar": row["solar"],
                "wind": row["wind"],
                "price": row["price"]
            }

            # 🔹 Collect agent outputs
            agent_outputs = {
                "reflex": self.reflex.decide(state),
                "goal": self.goal.decide(state),
                "utility": self.utility.decide(state),
                "learning": self.learning.decide(state)
            }

            # 🔹 Resolve using Decision Engine
            decision = self.decision_engine.resolve(state, agent_outputs)

            # 🔹 Store result (IMPORTANT: structured output)
            results.append({
                "time": row["time"],
                "hour": row["hour"],
                "demand": state["demand"],
                "solar": state["solar"],
                "wind": state["wind"],
                "price": state["price"],

                "selected_agent": decision["selected_agent"],
                "final_allocation": decision["final_allocation"],

                # Advanced insight 
                "agent_scores": decision["all_results"]
            })

        return results