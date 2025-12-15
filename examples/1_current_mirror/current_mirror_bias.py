"""
Current Mirror Bias Circuit - Problem 1
Based on Figure 1: LT Spice schematic

Circuit description:
- NMOS current mirror with bias network
- Model: NMOS_SH (Kp=180u, Vto=0.4)
- Supply: VDD=0.9V
"""

from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *
import matplotlib.pyplot as plt
import numpy as np

# Create circuit
circuit = Circuit('Current Mirror Bias Circuit')

# Power supplies
VDD = 0.9
circuit.V('dd', 'vdd', circuit.gnd, VDD@u_V)

# Current sources
circuit.I('1', 'vdd', 'vd1', 45@u_uA)  # I1: 45µA from VDD to VD1
circuit.I('2', 'vs2', circuit.gnd, 45@u_uA)  # I2: 45µA from VS2 to ground

# Resistor
circuit.R('1', 'vdd', 'vd3', 5.56@u_kOhm)  # R1: 5.56k

# MOSFETs - all NMOS_SH
# M1: Diode-connected, drain and gate to VD1, source to VSS
circuit.MOSFET('1', 'vd1', 'vd1', circuit.gnd, circuit.gnd, model='NMOS_SH')

# M2: Gate to VD1 (current mirror), drain to VDD, source to VS2
circuit.MOSFET('2', 'vdd', 'vd1', 'vs2', circuit.gnd, model='NMOS_SH')

# M3: Diode-connected, drain and gate to VD3, source to VSS
circuit.MOSFET('3', 'vd3', 'vd3', circuit.gnd, circuit.gnd, model='NMOS_SH')

# NMOS model
circuit.model('NMOS_SH', 'nmos',
              level=1,
              kp=180e-6,      # Process transconductance parameter
              vto=0.4,        # Threshold voltage
              lambda_=0.02,   # Channel-length modulation (typical)
              w=8e-6,         # Width = 8µm
              l=1e-6)         # Length = 1µm

print("=" * 60)
print("Current Mirror Bias Circuit - Operating Point Analysis")
print("=" * 60)
print("\nCircuit Parameters:")
print(f"  VDD = {VDD} V")
print(f"  I1 = I2 = 45 uA")
print(f"  R1 = 5.56 kOhm")
print(f"  NMOS: Kp=180u, Vto=0.4V, W=8um, L=1um")
print("=" * 60)

# Create simulator
simulator = circuit.simulator(temperature=25, nominal_temperature=25)

# Operating point analysis
print("\nRunning DC operating point analysis...")
try:
    analysis = simulator.operating_point()

    print("\n" + "=" * 60)
    print("DC Operating Point Results:")
    print("=" * 60)

    # Extract node voltages
    vd1 = float(analysis['vd1'])
    vs2 = float(analysis['vs2'])
    vd3 = float(analysis['vd3'])

    print(f"\nNode Voltages:")
    print(f"  VD1 (M1 drain/gate) = {vd1:.6f} V")
    print(f"  VS2 (M2 gate/source) = {vs2:.6f} V")
    print(f"  VD3 (M3 drain/gate) = {vd3:.6f} V")

    # Calculate currents through resistor
    i_r1 = (VDD - vd3) / 5.56e3
    print(f"\nCalculated Currents:")
    print(f"  I(R1) = {i_r1*1e6:.3f} uA")
    print(f"  I1 = 45.0 uA (current source)")
    print(f"  I2 = 45.0 uA (current source)")

    # Calculate MOSFET parameters
    print(f"\nMOSFET Operating Points:")
    print(f"  M1: VGS = {vd1:.6f} V, VDS = {vd1:.6f} V (diode-connected)")
    print(f"  M2: VGS = {vs2:.6f} V, VDS = {VDD-vs2:.6f} V")
    print(f"  M3: VGS = {vd3:.6f} V, VDS = {vd3:.6f} V (diode-connected)")

    # Check saturation
    print(f"\nSaturation Check (VDS > VGS - Vto):")
    print(f"  M1: {vd1:.3f} > {vd1-0.4:.3f} ? {vd1 > vd1-0.4}")
    print(f"  M2: {VDD-vs2:.3f} > {vs2-0.4:.3f} ? {VDD-vs2 > vs2-0.4}")
    print(f"  M3: {vd3:.3f} > {vd3-0.4:.3f} ? {vd3 > vd3-0.4}")

    print("=" * 60)
    print("[OK] Operating point analysis completed successfully!")
    print("=" * 60)

except Exception as e:
    print(f"\n[ERROR] Error during simulation: {e}")
    print("=" * 60)

# VDD sweep analysis
print("\nRunning VDD sweep analysis (0.5V to 1.2V)...")
try:
    vdd_values = np.linspace(0.5, 1.2, 50)
    vd1_values = []
    vs2_values = []
    vd3_values = []

    for vdd_val in vdd_values:
        # Update VDD
        circuit.V('dd', 'vdd', circuit.gnd, vdd_val@u_V)
        simulator = circuit.simulator(temperature=25, nominal_temperature=25)
        analysis = simulator.operating_point()

        vd1_values.append(float(analysis['vd1']))
        vs2_values.append(float(analysis['vs2']))
        vd3_values.append(float(analysis['vd3']))

    # Plot results
    plt.figure(figsize=(12, 8))

    # Voltage vs VDD
    plt.subplot(2, 1, 1)
    plt.plot(vdd_values, vd1_values, 'b-', linewidth=2, label='VD1 (M1 diode)')
    plt.plot(vdd_values, vs2_values, 'r-', linewidth=2, label='VS2 (M2 gate/source)')
    plt.plot(vdd_values, vd3_values, 'g-', linewidth=2, label='VD3 (M3 diode)')
    plt.plot(vdd_values, vdd_values, 'k--', linewidth=1, alpha=0.5, label='VDD')
    plt.axvline(x=0.9, color='gray', linestyle=':', alpha=0.7, label='Nominal VDD=0.9V')
    plt.grid(True, alpha=0.3)
    plt.xlabel('VDD (V)', fontsize=12)
    plt.ylabel('Node Voltage (V)', fontsize=12)
    plt.title('Current Mirror Bias Circuit - VDD Sweep', fontsize=14, fontweight='bold')
    plt.legend(loc='best')

    # Current through R1 vs VDD
    plt.subplot(2, 1, 2)
    i_r1_values = [(vdd - vd3)/5.56e3*1e6 for vdd, vd3 in zip(vdd_values, vd3_values)]
    plt.plot(vdd_values, i_r1_values, 'g-', linewidth=2, label='I(R1)')
    plt.axhline(y=45, color='orange', linestyle='--', linewidth=2, label='I1=I2=45uA')
    plt.axvline(x=0.9, color='gray', linestyle=':', alpha=0.7, label='Nominal VDD=0.9V')
    plt.grid(True, alpha=0.3)
    plt.xlabel('VDD (V)', fontsize=12)
    plt.ylabel('Current (uA)', fontsize=12)
    plt.title('Current through R1', fontsize=14, fontweight='bold')
    plt.legend(loc='best')

    plt.tight_layout()
    plt.savefig('current_mirror_bias_sweep.png', dpi=300, bbox_inches='tight')
    print("[OK] Plot saved as 'current_mirror_bias_sweep.png'")
    plt.show()

except Exception as e:
    print(f"[ERROR] Error during VDD sweep: {e}")

print("\n" + "=" * 60)
print("Simulation Complete!")
print("=" * 60)
