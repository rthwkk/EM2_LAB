import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Constants
Isc = 5.6  # Short circuit current
R02 = 1.594 # Resistance
Xo2 = 0.8049  # Reactance
v2 = 220  # Per-unit voltage
load_values = [i / 10 for i in range(1, 11)]  # Load values (x): 0.1 to 1.0
power_factors = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]  # Power factors (pf)

# Function to calculate phi from power factor
def calculate_phi(pf):
    return np.arccos(pf)  # Return phi in radians

# Function to calculate voltage regulation
def calculate_voltage_regulation(x, pf):
    phi = calculate_phi(pf)
    vr_lag = x * (Isc / v2) * (R02 * np.cos(phi) + Xo2 * np.sin(phi)) * 100
    vr_lead = x * (Isc / v2) * (R02 * np.cos(phi) - Xo2 * np.sin(phi)) * 100
    return vr_lag, vr_lead

# Store results
results = []
results_lag = {x: {"pf": [], "voltage_regulation": []} for x in load_values}
results_lead = {x: {"pf": [], "voltage_regulation": []} for x in load_values}

# Perform calculations for each combination of load and power factor
for pf in power_factors:
    for x in load_values:
        vr_lag, vr_lead = calculate_voltage_regulation(x, pf)
        results.append({
            "Load (x)": x,
            "Power Factor (pf)": pf,
            "Voltage Regulation (%) (lag)": round(vr_lag, 2),
            "Voltage Regulation (%) (lead)": round(vr_lead, 2)
        })
        results_lead[x]["pf"].append(pf)
        results_lead[x]["voltage_regulation"].append(vr_lead)
        results_lag[x]["pf"].append(pf)
        results_lag[x]["voltage_regulation"].append(vr_lag)

# Convert results to a DataFrame
df = pd.DataFrame(results)
df.to_csv("./EM/OC_SC_Load/predeterminationVoltageregulation.csv", index=False)
print("Results saved to './EM/OC_SC_Load/predeterminationVoltageregulation.csv'")

# --- Plot for Voltage Regulation vs Power Factor (Leading) ---
plt.figure(figsize=(10, 6))
for x in load_values:
    plt.plot(results_lead[x]["pf"], results_lead[x]["voltage_regulation"], label=f"Load {x*100:.0f}%")

plt.axhline(0, color='black', linewidth=1)
plt.xticks(results_lead[0.1]["pf"], labels=[f"{p:.1f}" for p in results_lead[0.1]["pf"]])
plt.title("Voltage Regulation vs Power Factor (Leading)", fontsize=16)
plt.xlabel("Power Factor (Leading)", fontsize=14)
plt.ylabel("Voltage Regulation (%)", fontsize=14)
plt.legend(title="Load Percentage", fontsize=10)
plt.grid(True)
plt.tight_layout()
plt.show()

# --- Plot for Voltage Regulation vs Power Factor (Lagging) ---
plt.figure(figsize=(10, 6))
for x in load_values:
    plt.plot(results_lag[x]["pf"], results_lag[x]["voltage_regulation"], label=f"Load {x*100:.0f}%")

plt.axhline(0, color='black', linewidth=1)
plt.xticks(results_lag[0.1]["pf"], labels=[f"{p:.1f}" for p in results_lag[0.1]["pf"]])
plt.title("Voltage Regulation vs Power Factor (Lagging)", fontsize=16)
plt.xlabel("Power Factor (Lagging)", fontsize=14)
plt.ylabel("Voltage Regulation (%)", fontsize=14)
plt.legend(title="Load Percentage", fontsize=10)
plt.grid(True)
plt.tight_layout()
plt.show()
