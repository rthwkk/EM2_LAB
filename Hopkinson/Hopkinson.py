import pandas as pd
import matplotlib.pyplot as plt

def calculate_values(I1, I2, I3, I4, rm, rg, V):
    # Calculate Wc
    Wc = 0.5 * (V * I1 - ((I1 + I2) ** 2) * rm - (I2 ** 2) * rg)

    # Calculate ipm
    ipm = V * (I1 + I2 + I3)

    # Calculate opm
    opm = ipm - Wc - V * I3 - ((I1 + I2) ** 2) * rm

    # Calculate nm
    nm = (opm / ipm) * 100

    # Calculate opg
    opg = V * (I2)

    # Calculate ipg
    ipg = opg + Wc + V * I4 + ((I2) ** 2) * rg

    # Calculate ng
    ng = (opg / ipg) * 100

    return Wc, ipm, opm, nm, opg, ipg, ng

def read_inputs_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file if line.strip()]  # Strip whitespace and ignore blank lines
        if len(lines) % 4 != 0:
            raise ValueError("Input file must have a number of lines that is a multiple of 4.")
        # Group lines into chunks of 4
        input_sets = [lines[i:i+4] for i in range(0, len(lines), 4)]
    # Convert to floats and return as tuples
    input_values = [tuple(map(float, group)) for group in input_sets]
    return input_values

def main(file_path):
    # Constants
    rm = 1.1
    rg = 0.961
    V = 220

    # Read inputs
    input_values = read_inputs_from_file(file_path)

    # Results storage
    results = []

    for I1, I2, I3, I4 in input_values:
        Wc, ipm, opm, nm, opg, ipg, ng = calculate_values(I1, I2, I3, I4, rm, rg, V)
        results.append([I1, I2, I3, I4, Wc, ipm, opm, nm, opg, ipg, ng])

    # Create a DataFrame for tabular display
    columns = ["I1", "I2", "I3", "I4", "Wc", "ipm", "opm", "nm (%)", "opg", "ipg", "ng (%)"]
    df = pd.DataFrame(results, columns=columns)

    # Print the table
    print(df)

    # Plot the graph
    plt.figure(figsize=(10, 6))
    plt.plot(df["opg"], df["ng (%)"], marker='o', label="ng vs opg")
    plt.plot(df["opm"], df["nm (%)"], marker='x', label="nm vs opm")
    plt.xlabel("Output")
    plt.ylabel("Efficiency (%)")
    plt.title("Efficiency vs Output")
    plt.legend()
    plt.grid(True)
    plt.show()

# File path for input
file_path = "/home/rithwik/lab/EM/hop_data.txt" # Replace with the actual path to your text file

# Execute the program
main(file_path)

