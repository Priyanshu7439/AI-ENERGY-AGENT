from backend.real_user.appliance_model import calculate_units
from backend.real_user.tariff_engine import calculate_bill


def what_if_analysis(appliances, changes, state):
    # original calculation
    original_units = calculate_units(appliances)
    original_bill = calculate_bill(original_units, state)

    # apply changes
    new_appliances = appliances.copy()

    for key, val in changes.items():
        if key in new_appliances:
            new_appliances[key]["hours"] = val["hours"]

    # new calculation
    new_units = calculate_units(new_appliances)
    new_bill = calculate_bill(new_units, state)

    return {
        "original_units": round(original_units, 2),
        "new_units": round(new_units, 2),
        "original_bill": original_bill,
        "new_bill": new_bill,
        "savings": round(original_bill - new_bill, 2)
    }