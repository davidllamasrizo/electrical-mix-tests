
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from analysis import (
    emissions_by_tech,
    co2_per_kwh,
    cc_stats,
    spared_pct,
    plot_week
)


# =====================================================
# 1. CREATE AN ARTIFICIAL DATASET (168 HOURS)
# =====================================================

print("\nCreating artificial dataset...")

np.random.seed(42)

hours = 168
time = np.arange(hours)

# Demand (kW): daily variation + random variation
demand = (
    180
    + 25 * np.sin(2 * np.pi * time / 24 - 1)
    + 10 * np.random.rand(hours)
)

# Nuclear generation (kW): constant
nuclear = np.full(hours, 100.0)

# Hydro generation (kW): relatively stable
hydro = 20 + 5 * np.random.rand(hours)

# Wind generation (kW): variable
wind = 30 + 20 * np.random.rand(hours)

# Solar generation (kW): zero at night, peaks during the day
solar = 50 * np.maximum(
    0,
    np.sin(2 * np.pi * (time % 24 - 6) / 24)
)

# Battery charge and discharge (kW)
battery_charge = np.zeros(hours)
battery_discharge = np.zeros(hours)

# Artificial battery parameters
C_storage = 200       # kWh
eta = 0.85
soc0 = 0.50
dt = 1

# Calculate battery operation
E_battery = C_storage * soc0

for t in range(hours):

    generation_without_gas = (
        nuclear[t] + hydro[t] + wind[t] + solar[t]
    )

    net_power = generation_without_gas - demand[t]

    if net_power > 0:
        # Surplus electricity: charge battery
        available_capacity = C_storage - E_battery

        charge = min(
            net_power,
            50,
            available_capacity / (eta * dt)
        )

        battery_charge[t] = charge
        E_battery += charge * eta * dt

    elif net_power < 0:
        # Electricity deficit: discharge battery
        deficit = abs(net_power)

        discharge = min(
            deficit,
            50,
            E_battery / dt
        )

        battery_discharge[t] = discharge
        E_battery -= discharge * dt


# Calculate state of charge (SOC)
E_battery = C_storage * soc0
soc = np.zeros(hours)

for t in range(hours):

    E_battery += battery_charge[t] * eta * dt
    E_battery -= battery_discharge[t] * dt

    E_battery = np.clip(E_battery, 0, C_storage)

    soc[t] = E_battery / C_storage


# Gas generation covers remaining deficit
total_generation_without_gas = (
    nuclear + hydro + wind + solar + battery_discharge
)

gas = np.maximum(
    0,
    demand + battery_charge - total_generation_without_gas
)

# Total generation
total_generation = (
    nuclear + hydro + wind + solar + gas + battery_discharge
)

# Curtailment: unused surplus after battery charging
curtailment = np.maximum(
    0,
    nuclear + hydro + wind + solar - demand - battery_charge
)


# Create DataFrame
df = pd.DataFrame({
    "demand": demand,
    "nuclear": nuclear,
    "hydro": hydro,
    "wind": wind,
    "solar": solar,
    "gas": gas,
    "battery_charge": battery_charge,
    "battery_discharge": battery_discharge,
    "curtailment": curtailment,
    "total_generation": total_generation,
    "soc": soc
})

# Store battery parameters in DataFrame attributes
df.attrs["C_storage"] = C_storage
df.attrs["eta"] = eta
df.attrs["soc0"] = soc0

print("Artificial dataset created successfully.")
print("Number of hours:", len(df))


# =====================================================
# 2. ARTIFICIAL EMISSION FACTORS
# =====================================================

emission_factors = {
    "nuclear": 0.012,
    "hydro": 0.024,
    "wind": 0.011,
    "solar": 0.040,
    "gas": 0.360
}


# =====================================================
# 3. TESTING ANALYSIS.PY
# =====================================================

print("\n" + "=" * 55)
print("TESTING ANALYSIS.PY")
print("=" * 55)


# 3.1 Test emissions_by_tech()

print("\n[1] Testing emissions_by_tech()")

emissions = emissions_by_tech(df, emission_factors)

print("Emissions by technology:")

for technology, value in emissions.items():
    print(f"  {technology}: {value:.2f} gCO2")

print("PASS: emissions_by_tech()")


# 3.2 Test co2_per_kwh()

print("\n[2] Testing co2_per_kwh()")

co2 = co2_per_kwh(df, emission_factors)

print(f"CO2 intensity: {co2:.2f} gCO2/kWh")

print("PASS: co2_per_kwh()")


# 3.3 Test cc_stats()

print("\n[3] Testing cc_stats()")

gas_results = cc_stats(df)

print("Gas statistics:")
print(gas_results)

print("PASS: cc_stats()")


# 3.4 Test spared_pct()

print("\n[4] Testing spared_pct()")

surplus = spared_pct(df)

print(f"Surplus percentage: {surplus:.2f}%")

print("PASS: spared_pct()")


# 3.5 Test plot_week()

print("\n[5] Testing plot_week()")

fig = plot_week(
    df,
    demand,
    start_hour=0
)

plt.show()

print("PASS: plot_week()")


# =====================================================
# 4. FINISH
# =====================================================

print("\nAll tests completed successfully!")


