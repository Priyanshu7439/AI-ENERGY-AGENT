import numpy as np
import pandas as pd


class Simulator:
    def __init__(self, hours=48, seed=42):
        self.hours = hours
        np.random.seed(seed)

        # Configurable parameters
        self.base_demand = 50
        self.solar_capacity = 40
        self.wind_capacity = 30
        self.base_price = 5

    def generate_time_index(self):
        return np.arange(self.hours)

    def demand_curve(self, t):
        hour = t % 24

        # Morning peak (around 8 AM)
        morning_peak = 30 * np.exp(-0.5 * ((hour - 8) / 2) ** 2)

        # Evening peak (around 7 PM)
        evening_peak = 40 * np.exp(-0.5 * ((hour - 19) / 3) ** 2)

        # Base + peaks + noise
        noise = np.random.normal(0, 3)
        demand = self.base_demand + morning_peak + evening_peak + noise

        return max(demand, 0)

    def solar_generation(self, t):
        hour = t % 24

        # Sinusoidal solar curve (6 AM to 6 PM)
        solar = np.sin(np.pi * (hour - 6) / 12)

        solar = max(solar, 0)

        # Weather factor (cloudiness)
        weather_factor = np.random.uniform(0.6, 1.0)

        return solar * self.solar_capacity * weather_factor

    def wind_generation(self, prev_wind):
        change = np.random.normal(0, 2)
        wind = prev_wind + change

        return np.clip(wind, 0, self.wind_capacity)

    def price_function(self, demand, hour):
        # Demand-based pricing
        price = self.base_price + 0.05 * demand

        # Peak hour surcharge (evening)
        if 18 <= hour <= 22:
            price *= 1.2

        # Random fluctuation
        price += np.random.normal(0, 0.5)

        return max(price, 0)

    def run(self):
        data = []

        prev_wind = np.random.uniform(5, 15)

        for t in self.generate_time_index():
            hour = t % 24

            demand = self.demand_curve(t)
            solar = self.solar_generation(t)
            wind = self.wind_generation(prev_wind)
            price = self.price_function(demand, hour)

            prev_wind = wind

            data.append({
                "time": t,
                "hour": hour,
                "demand": round(demand, 2),
                "solar": round(solar, 2),
                "wind": round(wind, 2),
                "price": round(price, 2)
            })

        return pd.DataFrame(data)