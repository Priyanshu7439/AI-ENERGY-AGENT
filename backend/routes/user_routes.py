from fastapi import APIRouter
from backend.real_user.tariff_engine import calculate_bill
from backend.services.weather_service import get_temperature
import json
import os
import copy

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POWER_PATH = os.path.join(BASE_DIR, "data", "appliance_power.json")
TARIFF_PATH = os.path.join(BASE_DIR, "data", "tariff_data.json")

with open(POWER_PATH) as f:
    POWER = json.load(f)

with open(TARIFF_PATH) as f:
    TARIFF = json.load(f)


# ================= UNITS =================
def calculate_units(appliances):
    total_units = 0
    breakdown = {}

    for name, data in appliances.items():
        hours = data.get("hours", 0)
        power = POWER.get(name, 0)

        units = power * hours
        breakdown[name] = round(units, 2)
        total_units += units

    return round(total_units, 2), breakdown


# ================= SLAB =================
def get_slab_info(units, state):
    slabs = TARIFF.get(state.lower(), [])
    prev_limit = 0

    for slab in slabs:
        if units <= slab["limit"]:
            return {
                "current_rate": slab["rate"],
                "current_limit": slab["limit"],
                "previous_limit": prev_limit
            }
        prev_limit = slab["limit"]

    return {"current_rate": None}


# ================= INTELLIGENT AGENT =================
def agent_optimize(appliances, state):
    trace = []

    # baseline
    units, breakdown = calculate_units(appliances)
    base_bill = calculate_bill(units, state)

    best_bill = base_bill
    best_plan = copy.deepcopy(appliances)

    trace.append({
        "step": 1,
        "action": "baseline",
        "bill": round(base_bill, 2)
    })

    # sort devices by usage
    devices = sorted(breakdown.items(), key=lambda x: x[1], reverse=True)

    strategies = []

    # Strategy 1: reduce top device
    if len(devices) >= 1:
        d1 = devices[0][0]
        s1 = copy.deepcopy(appliances)
        s1[d1]["hours"] *= 0.8
        strategies.append(("reduce_top_device", s1))

    # Strategy 2: reduce top 2
    if len(devices) >= 2:
        d1, d2 = devices[0][0], devices[1][0]
        s2 = copy.deepcopy(appliances)
        s2[d1]["hours"] *= 0.8
        s2[d2]["hours"] *= 0.8
        strategies.append(("reduce_top_2_devices", s2))

    # Strategy 3: reduce all heavy (>1 unit)
    s3 = copy.deepcopy(appliances)
    for k, v in breakdown.items():
        if v > 1:
            s3[k]["hours"] *= 0.85
    strategies.append(("reduce_all_heavy", s3))

    # evaluate all
    step = 2
    for name, config in strategies:
        units, _ = calculate_units(config)
        new_bill = calculate_bill(units, state)

        trace.append({
            "step": step,
            "action": name,
            "bill": round(new_bill, 2)
        })

        if new_bill < best_bill:
            best_bill = new_bill
            best_plan = config

        step += 1

    return {
        "best_bill": round(best_bill, 2),
        "best_plan": best_plan,
        "trace": trace
    }


# ================= ANALYZE =================
@router.post("/analyze")
def analyze(data: dict):
    state = data.get("state", "kolkata")
    appliances = data.get("appliances", {})

    # WEATHER
    temp = get_temperature(state)

    if temp and "ac" in appliances:
        if temp > 35:
            appliances["ac"]["hours"] *= 1.3
        elif temp > 30:
            appliances["ac"]["hours"] *= 1.15
        elif temp < 25:
            appliances["ac"]["hours"] *= 0.8

    units, breakdown = calculate_units(appliances)
    bill = calculate_bill(units, state)

    
    agent_result = agent_optimize(copy.deepcopy(appliances), state)

    # COST BREAKDOWN
    cost_breakdown = {}
    total_units = sum(breakdown.values())

    for name, unit in breakdown.items():
        cost = (unit / total_units) * bill if total_units else 0
        cost_breakdown[name] = round(cost, 2)

    slab_info = get_slab_info(units, state)

    return {
        "units": units,
        "bill": bill,
        "prediction": round(bill * 1.1, 2),
        "temperature": temp,

        "cost_breakdown": cost_breakdown,
        "daily_bill": bill,
        "monthly_bill": round(bill * 30, 2),
        "yearly_bill": round(bill * 365, 2),

        "breakdown": breakdown,

        "current_rate": slab_info.get("current_rate"),
        "current_limit": slab_info.get("current_limit"),
        "previous_limit": slab_info.get("previous_limit"),

        
        "agent_trace": agent_result["trace"],
        "optimized_bill": agent_result["best_bill"],
        "optimized_plan": agent_result["best_plan"]
    }


# ================= WHAT IF =================
@router.post("/what-if")
def what_if(data: dict):
    state = data.get("state", "kolkata")
    appliances = data.get("appliances", {})
    changes = data.get("changes", {})

    old_units, _ = calculate_units(appliances)
    old_bill = calculate_bill(old_units, state)

    for key, value in changes.items():
        if key in appliances:
            appliances[key]["hours"] = value["hours"]

    new_units, _ = calculate_units(appliances)
    new_bill = calculate_bill(new_units, state)

    return {
        "old_bill": old_bill,
        "new_bill": new_bill,
        "monthly_savings": round(old_bill - new_bill, 2),
        "yearly_savings": round((old_bill - new_bill) * 12, 2)
    }