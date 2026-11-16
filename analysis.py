
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
    "Nuclear", "Hydro", "Wind", "Solar", "Gas", "\nStorage"
]

    for column in columns:
        if column not in df.columns:
            raise ValueError(f"Missing column: {column}")

    annual_energy = df[columns].sum()
    total_energy = annual_energy.sum()

    if total_energy == 0:
        raise ValueError("Total energy supplied cannot be zero.")

    # Create a larger figure
    fig, ax = plt.subplots(figsize=(12, 9))

    # Create the pie chart
    wedges, texts, autotexts = ax.pie(
    annual_energy,
    labels=labels,
    autopct="%1.1f%%",
    startangle=90,
    radius=1.0,
    labeldistance=0.20,
    pctdistance=0.65,
    textprops={"fontsize": 16, "fontweight": "bold"},
    wedgeprops={"edgecolor": "white", "linewidth": 2}
)

    # Make technology names larger and bold
    for text in texts:
        text.set_fontsize(15)
        text.set_fontweight("bold")

    # Make percentages larger and bold
    for autotext in autotexts:
        autotext.set_fontsize(14)
        autotext.set_fontweight("bold")

    # Add a separate title above the chart
    fig.suptitle(
        "Annual Electricity Supply Mix",
        fontsize=22,
        fontweight="bold",
        y=0.97
    )

    # Reserve space between the title and the chart
    fig.subplots_adjust(
        top=0.82,
        bottom=0.08,
        left=0.12,
        right=0.88
    )
    ax.set_title("Electricity mix", pad=40)
    ax.axis("equal")

    plt.show()

