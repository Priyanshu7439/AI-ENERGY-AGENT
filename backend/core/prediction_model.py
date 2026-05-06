def predict_next_bill(current_units, current_bill, growth_rate=0.05):
    """
    Predict next month's bill based on usage growth.

    growth_rate = expected increase (default 5%)
    """

    predicted_units = current_units * (1 + growth_rate)

    # unit price approximation
    price_per_unit = current_bill / current_units if current_units != 0 else 0

    predicted_bill = predicted_units * price_per_unit

    return {
        "predicted_units": round(predicted_units, 2),
        "predicted_bill": round(predicted_bill, 2)
    }