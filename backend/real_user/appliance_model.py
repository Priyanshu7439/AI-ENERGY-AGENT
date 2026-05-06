APPLIANCE_WATT = {
    "fan": 75,
    "ac": 1500,
    "fridge": 200,
    "light": 10,
    "geyser": 2000,
    "iron": 1000,
    "tv": 120,
    "mixer": 500,
    "blender": 100,
    "charging_application": 300
}


def calculate_units(appliances, days=30):
    total_units = 0

    for name, data in appliances.items():
        watt = APPLIANCE_WATT.get(name, 100)
        hours = data["hours"]
        count = data.get("count", 1)

        units = (watt * hours * count * days) / 1000
        total_units += units

    return total_units