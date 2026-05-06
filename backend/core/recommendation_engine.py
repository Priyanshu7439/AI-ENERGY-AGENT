def generate_recommendations(appliances, units, bill):
    insights = []
    recommendations = []

    # ---------- INSIGHTS ----------
    total_hours = sum(v.get("hours", 0) for v in appliances.values()) or 1

    # top contributors
    sorted_items = sorted(appliances.items(), key=lambda x: x[1].get("hours", 0), reverse=True)

    for name, data in sorted_items:
        hours = data.get("hours", 0)
        if hours <= 0:
            continue
        share = (hours / total_hours) * 100
        if share >= 20:
            insights.append(f"{name.upper()} contributes {round(share, 1)}% of total usage")

    # demand + bill based insights
    if units > 200:
        insights.append("High energy consumption detected this month")
    if bill > 1500:
        insights.append("Electricity bill is above average range")

    # 🔥 HARD FALLBACK (you were missing this)
    if not insights:
        insights = [
            "Usage is balanced across appliances",
            "No single appliance dominates your consumption"
        ]

    # ---------- RECOMMENDATIONS ----------
    if appliances.get("ac", {}).get("hours", 0) > 6:
        recommendations.append("Reduce AC usage to below 6 hours/day")
        recommendations.append("Set AC temperature to 24°C")

    if appliances.get("geyser", {}).get("hours", 0) > 2:
        recommendations.append("Limit geyser usage to reduce power spikes")

    if bill > 1500:
        recommendations.append("Shift heavy usage to off-peak hours")
        recommendations.append("Consider energy-efficient appliances")

    if not recommendations:
        recommendations = ["Your current usage pattern is efficient"]

    return {
        "insights": insights,
        "recommendations": recommendations
    }


# helper
def get_watt(device):
    watt_map = {
        "fan": 75,
        "ac": 1500,
        "fridge": 200,
        "light": 10,
        "geyser": 2000,
        "iron": 1000,
        "tv": 120,
        "mixer": 500
    }
    return watt_map.get(device, 100)