
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from analysis import (
    emissions_by_tech,
    co2_per_kwh,
    cc_stats,
    spared_pct,
    plot_week,
    plot_pie,
    plot_co2_pie
)


# =====================================================
# 1. CREATE A FICTIONAL DATASET FOR ONE WEEK (168 HOURS)
# =====================================================

hours = np.arange(168)

# Electricity demand (kW)
demand = 200 + 20 * np.sin(2 * np.pi * hours / 24)

# Generation from each technology (kW)
nuclear = np.full(168, 100.0)

hydro = 20 + 5 * np.sin(2 * np.pi * hours / 168)

wind = 35 + 10 * np.sin(2 * np.pi * hours / 48)

# Solar generation: zero at night, maximum during the day
solar = 40 * np.maximum(
    0,
    np.sin(2 * np.pi * (hours % 24 - 6) / 24)
)

# Battery discharge (kW)
battery_discharge = np.full(168, 5.0)

# Battery charging (kW)
battery_charge = np.zeros(168)

# Calculate the generation before gas
generation_without_gas = (
    nuclear + hydro + wind + solar
)

# Gas covers any remaining demand
gas = np.maximum(
    demand - generation_without_gas - battery_discharge,
    0
)

# Curtailment: generation exceeding demand
curtailment = np.maximum(
    generation_without_gas - demand,
    0
)

# Create DataFrame
df = pd.DataFrame({
    "demand": demand,
    "nuclear": nuclear,
    "hydro": hydro,
    "wind": wind,
    "solar": solar,
    "gas": gas,
    "battery_discharge": battery_discharge,
    "battery_charge": battery_charge,
    "curtailment": curtailment
})

# Total generation from the five generation technologies
df["total_generation"] = (
    df["nuclear"]
    + df["hydro"]
    + df["wind"]
    + df["solar"]
    + df["gas"]
)


print("=" * 55)
print("TESTING ANALYSIS.PY")
print("=" * 55)

print("\nDataset created successfully.")
print("Number of hours:", len(df))


# =====================================================
# 2. DEFINE EMISSION FACTORS
# =====================================================

# Units: gCO2/kWh
# These are the equivalent of the earlier kgCO2/kWh
# factors multiplied by 1000.

emission_factors = {
    "nuclear": 12,
    "hydro": 24,
    "wind": 11,
    "solar": 40,
    "gas": 360
}


# =====================================================
# 3. TEST emissions_by_tech()
# =====================================================

print("\n[1] Testing emissions_by_tech()")

emissions = emissions_by_tech(df, emission_factors)

print("Emissions by technology:")

for technology, value in emissions.items():
    print(f"  {technology}: {value:.2f} gCO2")

assert isinstance(emissions, dict)
assert len(emissions) == 5
assert all(value >= 0 for value in emissions.values())

print("PASS: emissions_by_tech()")


# =====================================================
# 4. TEST co2_per_kwh()
# =====================================================

print("\n[2] Testing co2_per_kwh()")

co2 = co2_per_kwh(df, emission_factors)

print(f"CO2 intensity: {co2:.2f} gCO2/kWh")

assert isinstance(co2, float)
assert 0 <= co2 <= max(emission_factors.values())

print("PASS: co2_per_kwh()")


# =====================================================
# 5. TEST cc_stats()
# =====================================================

print("\n[3] Testing cc_stats()")

gas_results = cc_stats(df)

print("Gas statistics:")
print(
    "  Installed gas capacity:",
    f"{gas_results['installed_gas_capacity_MW']:.4f} MW"
)
print(
    "  Gas load factor:",
    f"{gas_results['gas_load_factor'] * 100:.2f}%"
)

assert gas_results["installed_gas_capacity_MW"] >= 0
assert 0 <= gas_results["gas_load_factor"] <= 1

print("PASS: cc_stats()")


# =====================================================
# 6. TEST spared_pct()
# =====================================================

print("\n[4] Testing spared_pct()")

surplus = spared_pct(df)

print(f"Surplus percentage: {surplus:.2f}%")

assert isinstance(surplus, float)
assert 0 <= surplus <= 100

print("PASS: spared_pct()")


# =====================================================
# 7. TEST plot_week()
# =====================================================

print("\n[5] Testing plot_week()")

fig = plot_week(
    df,
    demand,
    start_hour=0
)

assert fig is not None

print("PASS: plot_week()")

plt.show()


# =====================================================
# 8. TEST plot_pie()
# =====================================================

print("\n[6] Testing plot_pie()")

plot_pie(df)

print("PASS: plot_pie()")


# =====================================================
# 9. TEST plot_co2_pie()
# =====================================================

print("\n[7] Testing plot_co2_pie()")

plot_co2_pie(df, emission_factors)

print("PASS: plot_co2_pie()")


# =====================================================
# 10. FINAL RESULT
# =====================================================

print("\n" + "=" * 55)
print("ALL ANALYSIS TESTS COMPLETED SUCCESSFULLY!")
print("=" * 55)

plt.show()

