from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *
import matplotlib.pyplot as plt
import numpy as np

# Create the Two-Stage CMOS Op-Amp circuit
circuit = Circuit('Two-Stage CMOS Operational Amplifier - Improved')

# Supply voltages
VDD = 5  # Positive supply voltage
VSS = 0  # Negative supply (ground)

# Define power supplies
circuit.V('dd', 'vdd', circuit.gnd, VDD@u_V)

# Bias voltages for current sources
# These control the current through the transistors
VBIAS_P = 3.5  # Bias for PMOS current sources (lower voltage = more current)
VBIAS_N = 1.5  # Bias for NMOS tail current source

circuit.V('bias_p', 'vbias_p', circuit.gnd, VBIAS_P@u_V)
circuit.V('bias_n', 'vbias_n', circuit.gnd, VBIAS_N@u_V)

# Input signals (differential configuration)
# DC bias at mid-supply for maximum swing
VCM = 2.5  # Common-mode voltage
circuit.V('in_p', 'vin_p', circuit.gnd, f'{VCM} AC 0.5')  # Positive input with AC signal
circuit.V('in_n', 'vin_n', circuit.gnd, f'{VCM} AC 0')    # Negative input (reference)

# ============================================
# FIRST STAGE: Differential Amplifier
# ============================================

# M8: Tail current source for differential pair (NMOS)
# This sets the bias current for the differential pair
circuit.MOSFET('M8', 'n_tail', 'vbias_n', circuit.gnd, circuit.gnd, model='NMOS_BIG')

# M2, M3: Differential input pair (NMOS)
circuit.MOSFET('M2', 'n_d2', 'vin_p', 'n_tail', circuit.gnd, model='NMOS')
circuit.MOSFET('M3', 'n_d3', 'vin_n', 'n_tail', circuit.gnd, model='NMOS')

# M4, M5: Active load current mirror (PMOS)
# M4 is diode-connected (gate tied to drain)
circuit.MOSFET('M4', 'n_d2', 'n_d2', 'vdd', 'vdd', model='PMOS')
circuit.MOSFET('M5', 'n_d3', 'n_d2', 'vdd', 'vdd', model='PMOS')

# ============================================
# SECOND STAGE: Common-Source Amplifier
# ============================================

# M6: PMOS current source load for M7
circuit.MOSFET('M6', 'vout', 'vbias_p', 'vdd', 'vdd', model='PMOS')

# M7: Output stage driver (NMOS common-source)
# Gate driven by first stage output (n_d3)
circuit.MOSFET('M7', 'vout', 'n_d3', circuit.gnd, circuit.gnd, model='NMOS')

# M1: Additional PMOS for better matching/biasing (optional, can be removed)
# In many designs this helps with current mirroring
circuit.MOSFET('M1', 'n_m1', 'vbias_p', 'vdd', 'vdd', model='PMOS')
circuit.R('dummy', 'n_m1', circuit.gnd, 10@u_kOhm)  # Dummy load

# ============================================
# COMPENSATION AND LOAD CAPACITORS
# ============================================

# CA: Miller compensation capacitor (dominant pole compensation)
# Connected between output and gate of M7 for frequency compensation
circuit.C('A', 'n_d3', 'vout', 3@u_pF)

# CB: Additional compensation
circuit.C('B', 'vout', circuit.gnd, 0.5@u_pF)

# CL: Load capacitor (represents output load)
circuit.C('L', 'vout', circuit.gnd, 15@u_pF)

# ============================================
# TRANSISTOR MODELS
# ============================================

# NMOS model - standard input transistors
circuit.model('NMOS', 'nmos',
    level=1,
    kp=120e-6,      # Transconductance parameter
    vto=0.7,        # Threshold voltage
    lambda_=0.02,   # Channel length modulation
    gamma=0.4,      # Body effect parameter
    phi=0.65,       # Surface potential
    w=30e-6,        # Channel width for input pair
    l=2e-6          # Longer channel for better matching
)

# NMOS model - larger for tail current source
circuit.model('NMOS_BIG', 'nmos',
    level=1,
    kp=120e-6,
    vto=0.7,
    lambda_=0.02,
    gamma=0.4,
    phi=0.65,
    w=60e-6,        # Larger width for more current
    l=2e-6
)

# PMOS model - active loads and current sources
circuit.model('PMOS', 'pmos',
    level=1,
    kp=40e-6,       # Lower mobility than NMOS
    vto=-0.7,       # Negative threshold for PMOS
    lambda_=0.02,
    gamma=0.4,
    phi=0.65,
    w=60e-6,        # Wider to compensate for lower mobility
    l=2e-6
)

print("="*70)
print(" "*15 + "TWO-STAGE CMOS OPERATIONAL AMPLIFIER")
print("="*70)
print("\nCIRCUIT NETLIST:")
print("-"*70)
print(circuit)
print("="*70)

# Create simulator
simulator = circuit.simulator(temperature=25, nominal_temperature=25)
simulator.options(reltol=1e-3, abstol=1e-12, vntol=1e-6, itl1=300, itl2=100)

try:
    print("\n[1] DC OPERATING POINT ANALYSIS")
    print("-"*70)

    dc_analysis = simulator.operating_point()

    print("\nKey Node Voltages:")
    print(f"  Output (vout):           {float(dc_analysis['vout']):.3f} V")
    print(f"  Tail node (n_tail):      {float(dc_analysis['n_tail']):.3f} V")
    print(f"  M2 drain (n_d2):         {float(dc_analysis['n_d2']):.3f} V")
    print(f"  M3 drain (n_d3):         {float(dc_analysis['n_d3']):.3f} V")
    print(f"  Input common-mode:       {VCM:.3f} V")

    vout_dc = float(dc_analysis['vout'])
    print(f"\nDC Output: {vout_dc:.3f} V (should be near {VDD/2:.1f}V for good swing)")

    print("\n[2] AC FREQUENCY RESPONSE ANALYSIS")
    print("-"*70)

    ac_analysis = simulator.ac(
        start_frequency=0.1@u_Hz,
        stop_frequency=1@u_GHz,
        number_of_points=200,
        variation='dec'
    )

    # Extract data
    frequency = np.array(ac_analysis.frequency)
    vout_ac = np.array(ac_analysis['vout'])

    # Calculate gain and phase
    gain_linear = np.abs(vout_ac)
    gain_db = 20 * np.log10(gain_linear + 1e-20)  # Add small value to avoid log(0)
    phase_deg = np.angle(vout_ac, deg=True)

    # Find performance metrics
    dc_gain_db = gain_db[0]

    # Find 3dB bandwidth
    gain_3db = dc_gain_db - 3
    bw_3db_idx = np.where(gain_db <= gain_3db)[0]
    if len(bw_3db_idx) > 0:
        bw_3db = frequency[bw_3db_idx[0]]
        print(f"\nDC Gain:              {dc_gain_db:.1f} dB ({10**(dc_gain_db/20):.1f} V/V)")
        print(f"3dB Bandwidth:        {bw_3db:.2e} Hz ({bw_3db/1e3:.2f} kHz)")
    else:
        print(f"\nDC Gain:              {dc_gain_db:.1f} dB ({10**(dc_gain_db/20):.1f} V/V)")
        print("3dB Bandwidth:        >1 GHz")

    # Find unity-gain frequency and phase margin
    ugf_idx = np.where(gain_db <= 0)[0]
    if len(ugf_idx) > 0:
        ugf = frequency[ugf_idx[0]]
        phase_margin = 180 + phase_deg[ugf_idx[0]]
        print(f"Unity-Gain Frequency: {ugf/1e6:.2f} MHz")
        print(f"Phase Margin:         {phase_margin:.1f} degrees")

        if phase_margin > 45:
            print("  -> Stability: GOOD (PM > 45 degrees)")
        else:
            print("  -> Stability: WARNING (PM < 45 degrees)")
    else:
        print("Unity-Gain Frequency: Not reached")

    # Create comprehensive Bode plot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 9))

    # Magnitude plot
    ax1.semilogx(frequency, gain_db, 'b-', linewidth=2.5, label='Gain')
    ax1.grid(True, which='both', alpha=0.3, linestyle='-', linewidth=0.5)
    ax1.grid(True, which='minor', alpha=0.15, linestyle=':', linewidth=0.5)
    ax1.set_ylabel('Gain (dB)', fontsize=12, fontweight='bold')
    ax1.set_title('Two-Stage CMOS Op-Amp: Bode Plot',
                  fontsize=14, fontweight='bold', pad=15)
    ax1.axhline(y=0, color='r', linestyle='--', alpha=0.6, linewidth=1.5, label='0 dB')
    ax1.axhline(y=dc_gain_db-3, color='g', linestyle=':', alpha=0.6, label='-3 dB')
    ax1.legend(loc='upper right', fontsize=10)
    ax1.set_ylim([min(gain_db)-10, max(gain_db)+10])

    # Phase plot
    ax2.semilogx(frequency, phase_deg, 'r-', linewidth=2.5, label='Phase')
    ax2.grid(True, which='both', alpha=0.3, linestyle='-', linewidth=0.5)
    ax2.grid(True, which='minor', alpha=0.15, linestyle=':', linewidth=0.5)
    ax2.set_xlabel('Frequency (Hz)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Phase (degrees)', fontsize=12, fontweight='bold')
    ax2.axhline(y=-180, color='r', linestyle='--', alpha=0.6, linewidth=1.5, label='-180°')
    ax2.axhline(y=0, color='k', linestyle='-', alpha=0.3, linewidth=1)
    ax2.legend(loc='lower left', fontsize=10)
    ax2.set_ylim([-200, 50])

    plt.tight_layout()
    plt.savefig('opamp_bode_improved.png', dpi=300, bbox_inches='tight')
    print(f"\nBode plot saved: opamp_bode_improved.png")
    plt.show()

    print("\n" + "="*70)
    print(" "*20 + "SIMULATION COMPLETED SUCCESSFULLY")
    print("="*70)

except Exception as e:
    print(f"\nERROR: {str(e)}")
    print("\nTroubleshooting tips:")
    print("  - Adjust bias voltages (VBIAS_P, VBIAS_N)")
    print("  - Check transistor sizing (W/L ratios)")
    print("  - Verify power supply connections")
    import traceback
    traceback.print_exc()
