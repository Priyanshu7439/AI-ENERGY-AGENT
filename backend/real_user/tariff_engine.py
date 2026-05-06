import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "tariff_data.json")

with open(DATA_PATH) as f:
    TARIFF = json.load(f)


def calculate_bill(units, state="kolkata"):
    slabs = TARIFF.get(state.lower())

    if not slabs:
        raise ValueError("Invalid state")

    remaining_units = units
    total_cost = 0
    prev_limit = 0

    for slab in slabs:
        limit = slab["limit"]
        rate = slab["rate"]

        if remaining_units <= 0:
            break

        slab_units = min(remaining_units, limit - prev_limit)

        total_cost += slab_units * rate

        remaining_units -= slab_units
        prev_limit = limit

    return round(total_cost, 2)