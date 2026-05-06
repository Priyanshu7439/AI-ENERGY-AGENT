🚀 ENERLYTICS — Intelligent Energy Optimization System

A hybrid AI-powered system that analyzes household electricity usage, predicts cost patterns, and autonomously optimizes consumption using adaptive decision logic and learning from historical behavior.

⚡ Why This Project Exists

Electricity consumption is increasing, but most users:

don’t understand where their bill comes from
can’t predict future costs
have no clear optimization strategy

Enerlytics solves this with intelligence, not just calculation.

🧠 Core Idea

This is not just a calculator.

It is a decision-making system that:

models appliance-level consumption
simulates optimization strategies
learns from user behavior over time
adapts recommendations dynamically

UI SCREENSHOT: 




🏗️ System Architecture

User Input → Backend Engine → Optimization Agent → Learning Layer → UI Visualization

Components:
Frontend (JS + Chart.js)
Real-time dashboard
Interactive simulation (What-if analysis)
Trend & breakdown visualization

Backend (FastAPI)
Unit calculation engine
Dynamic tariff system (state-based slabs)
Weather-aware adjustment
Multi-step optimization agent

AI Layer (Lightweight Learning System)
Stores user history
Learns usage vs cost patterns
Adapts recommendations over time

🔥 Key Features
1. ⚡ Appliance-Level Energy Modeling
Calculates units based on real-world power consumption
Provides granular breakdown per device
2. 🌦️ Weather-Aware Adjustment
AC usage dynamically adjusted using temperature API
Reflects real-world behavior patterns

3. 💸 Dynamic Tariff Engine
State-based slab pricing
Shows:
current rate
slab threshold
optimization target
4. 🤖 Optimization Agent (Core Intelligence)

Multi-step decision engine that:

identifies highest energy-consuming device
simulates reductions (iterative strategy search)
finds lowest-cost configuration

Example reasoning trace:

Step 1: baseline → ₹2450  
Step 2: reduce AC → ₹2100  
Step 3: reduce fridge → ₹1980  

5. 🔁 What-if Simulation Engine
Change any appliance usage
Instantly see cost impact
Compare before vs after

6. 🧠 Learning Layer (AI Component)

The system:

stores past usage patterns
computes:
average usage
cost per hour
adapts future recommendations

👉 This converts static logic into behavior-driven intelligence

7. 📈 Trend Analysis
Tracks historical bills
Visualizes usage trend
Enables pattern recognition

8. 🚀 One-Click Auto Optimization
Automatically identifies worst device
reduces usage intelligently
shows real savings instantly

9. 🧩 Explainable AI (Transparent Reasoning)

Unlike black-box models, this system shows:

decision steps
reasoning trace
cost impact of each action

| Layer         | Technology                         |
| ------------- | ---------------------------------- |
| Frontend      | HTML, CSS, JavaScript              |
| Visualization | Chart.js                           |
| Backend       | FastAPI (Python)                   |
| Data          | JSON (power + tariff models)       |
| AI Layer      | Custom lightweight learning system |
| API           | Weather API                        |

## ⚠️ Note on Weather Data

The current version uses a lightweight mock temperature model instead of a live API.

This decision was intentional to:
- avoid external dependency failures
- ensure consistent system behavior during testing
- keep the system fully runnable without API keys

The architecture is designed to easily integrate real-time weather APIs (e.g., OpenWeather) in production environments.

⚙️ How It Works (Flow)

1. User inputs appliance usage
2. Backend calculates units + cost
3. Weather adjusts AC usage
4. Tariff engine computes bill
5. Optimization agent simulates strategies
6. Best plan is selected
7. Learning layer updates patterns
8. UI displays:
9. insights
10. recommendations
11. reasoning
12. projections

🧠 What Makes This an AI Project

This system includes:

Decision-making agent (multi-step optimization)
Adaptive learning from history
Pattern-based prediction (cost/usage relationship)
Behavior-driven recommendations

👉 It is a hybrid AI system combining:

rule-based logic
search-based optimization
lightweight learning

⚖️ Design Philosophy

Not overengineered
Fully explainable
Real-world applicable
Fast and interactive

📌 Limitations (Honest Engineering)
No deep learning / large-scale dataset
Learning is statistical (not model-trained)
Limited to predefined appliances

👉 Designed intentionally for clarity + control + speed

🚀 Future Improvements
Train ML model (Linear Regression / XGBoost)
Real-time smart meter integration
IoT-based automation
Mobile app deployment
User profiles & cloud storage

💡 How to Run
Backend:

cd backend
uvicorn backend.main:app --reload

Frontend:

cd frontend
python -m http.server 5500

