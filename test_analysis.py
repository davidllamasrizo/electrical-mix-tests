
import pandas as pd
import numpy as np

from analysis import co2_per_kwh, cc_stats, spared_pct, plot_pie


# 1. Create a fictional dataset for 7 days
df = pd.DataFrame({
    "demand": [200, 180, 190, 210, 195, 185, 205],
    "nuclear": [100, 100, 100, 100, 100, 100, 100],
    "hydro": [20, 25, 20, 15, 25, 20, 20],
    "wind": [30, 40, 30, 45, 35, 25, 40],
    "solar": [0, 10, 20, 30, 15, 5, 25],
    "gas": [50, 0, 20, 20, 20, 35, 20],
    "battery_discharge": [0, 10, 5, 0, 5, 10, 0],
    "battery_charge": [0, 0, 0, 0, 0, 0, 0],
    "curtailment": [0, 5, 0, 0, 0, 0, 0]
})

df["total_generation"] = (
    df["nuclear"] + df["hydro"] + df["wind"]
    + df["solar"] + df["gas"]
)


# 2. Define emission factors (kgCO2/kWh)
emission_factors = {
    "nuclear": 0.012,
    "hydro": 0.024,
    "wind": 0.011,
    "solar": 0.040,
    "gas": 0.360
}


# 3. Test CO2 intensity
co2 = co2_per_kwh(df, emission_factors)
print("CO2 intensity:", co2, "kgCO2/kWh")


# 4. Test gas capacity and load factor
gas_results = cc_stats(df)
print("Gas statistics:", gas_results)


# 5. Test surplus percentage
surplus = spared_pct(df)
print("Surplus percentage:", surplus, "%")


# 6. Test pie chart
plot_pie(df)

print("All tests completed successfully!")

