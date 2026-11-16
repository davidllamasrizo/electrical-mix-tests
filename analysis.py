
import matplotlib.pyplot as plt


def co2_per_kwh(df, emission_factors) -> float:
    """Calculate annual CO2 emissions per kWh generated."""

    technologies = ["nuclear", "hydro", "wind", "solar", "gas"]

    for technology in technologies:
        if technology not in df.columns:
            raise ValueError(f"Missing column: {technology}")

        if technology not in emission_factors:
            raise ValueError(f"Missing emission factor: {technology}")

    annual_energy = df[technologies].sum()

    total_emissions = sum(
        annual_energy[technology] * emission_factors[technology]
        for technology in technologies
    )

    total_generation = annual_energy.sum()

    if total_generation == 0:
        raise ValueError("Total electricity generation cannot be zero.")

    co2_intensity = total_emissions / total_generation

    return float(co2_intensity)


def cc_stats(df) -> dict:
    """Calculate installed gas capacity and its load factor."""

    if "gas" not in df.columns:
        raise ValueError("Missing column: gas")

    installed_capacity = df["gas"].max() / 1000
    average_generation = df["gas"].mean()

    if installed_capacity > 0:
        load_factor = average_generation / (installed_capacity * 1000)
    else:
        load_factor = 0.0

    return {
        "installed_gas_capacity_MW": float(installed_capacity),
        "gas_load_factor": float(load_factor)
    }


def spared_pct(df) -> float:
    """Calculate surplus electricity as a percentage of total production."""

    required_columns = ["curtailment", "total_generation"]

    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f"Missing column: {column}")

    total_surplus = df["curtailment"].sum()
    total_generation = df["total_generation"].sum()

    if total_generation == 0:
        raise ValueError("Total generation cannot be zero.")

    surplus_percentage = (total_surplus / total_generation) * 100

    return float(surplus_percentage)


def plot_pie(df):
    """Plot the annual contribution of each technology and storage."""

    columns = [
        "nuclear", "hydro", "wind", "solar", "gas",
        "battery_discharge"
    ]

    labels = [
        "Nuclear", "Hydro", "Wind", "Solar", "Gas", "Storage"
    ]

    for column in columns:
        if column not in df.columns:
            raise ValueError(f"Missing column: {column}")

    annual_energy = df[columns].sum()
    total_energy = annual_energy.sum()

    if total_energy == 0:
        raise ValueError("Total energy supplied cannot be zero.")

    plt.figure(figsize=(9, 7))
    plt.pie(
        annual_energy,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90
    )
    plt.title("Annual Electricity Supply Mix")
    plt.axis("equal")
    plt.tight_layout()
    plt.show()

