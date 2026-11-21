import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# =====================================================
# ARTIFICIAL BATTERY STORAGE
# =====================================================

print("\nCreating artificial battery storage...")

# Battery parameters
C_storage = 200       # Capacity in kWh
eta = 0.85             # Battery efficiency
soc0 = 0.50            # Initial SOC: 50%
dt = 1                 # Time step: 1 hour

# Initial stored energy
E_battery = C_storage * soc0

# Create SOC array
soc = np.zeros(len(df))

# Calculate SOC hour by hour
for t in range(len(df)):

    charge = df["battery_charge"].iloc[t]
    discharge = df["battery_discharge"].iloc[t]

    # Update stored energy
    E_battery += charge * eta * dt
    E_battery -= discharge * dt

    # Keep energy within battery capacity
    E_battery = np.clip(E_battery, 0, C_storage)

    # Calculate SOC
    soc[t] = E_battery / C_storage

# Add SOC to DataFrame
df["soc"] = soc

# Store battery parameters
df.attrs["C_storage"] = C_storage
df.attrs["eta"] = eta
df.attrs["soc0"] = soc0

print("Artificial battery storage created successfully.")
print("Battery capacity:", C_storage, "kWh")
print("Initial SOC:", soc0 * 100, "%")
print("Final SOC:", round(soc[-1] * 100, 2), "%")
print("Minimum SOC:", round(soc.min() * 100, 2), "%")
print("Maximum SOC:", round(soc.max() * 100, 2), "%")


# =====================================================
# TESTING ANALYSIS.PY
# =====================================================

print("\n" + "=" * 55)
print("TESTING ANALYSIS.PY")
print("=" * 55)

# 1. Test emissions_by_tech()

print("\n[1] Testing emissions_by_tech()")

emissions = emissions_by_tech(df, emission_factors)

print("Emissions by technology:")
for technology, value in emissions.items():
    print(f"  {technology}: {value:.2f} gCO2")

print("PASS: emissions_by_tech()")


# 2. Test co2_per_kwh()

print("\n[2] Testing co2_per_kwh()")

co2 = co2_per_kwh(df, emission_factors)

print(f"CO2 intensity: {co2:.2f} gCO2/kWh")

print("PASS: co2_per_kwh()")


# 3. Test cc_stats()

print("\n[3] Testing cc_stats()")

gas_results = cc_stats(df)

print("Gas statistics:")
print(gas_results)

print("PASS: cc_stats()")


# 4. Test spared_pct()

print("\n[4] Testing spared_pct()")

surplus = spared_pct(df)

print(f"Surplus percentage: {surplus:.2f}%")

print("PASS: spared_pct()")


# 5. Test plot_week()

print("\n[5] Testing plot_week()")

fig = plot_week(
    df,
    demand,
    start_hour=0
)

plt.show()

print("PASS: plot_week()")

print("\nAll tests completed successfully!")

