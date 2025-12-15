from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

# Create a simple voltage divider circuit
circuit = Circuit('Voltage Divider Test')

# Power supply
circuit.V('input', 'in', circuit.gnd, 10@u_V)

# Resistors
circuit.R(1, 'in', 'out', 1@u_kOhm)
circuit.R(2, 'out', circuit.gnd, 1@u_kOhm)

print("Circuit created successfully!")
print(circuit)

# Create simulator
simulator = circuit.simulator(temperature=25, nominal_temperature=25)

# Run operating point analysis
print("\nRunning DC operating point analysis...")
analysis = simulator.operating_point()

# Print results
print("\nResults:")
for node in analysis.nodes.values():
    print(f"  {str(node)}: {float(node):.3f} V")

print("\nSPICEPilot setup is working correctly!")
