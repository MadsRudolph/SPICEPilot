"""
PySpice to KiCad SPICE Converter
Converts PySpice Circuit objects to KiCad-compatible .cir files
"""

from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *
import re

def pyspice_to_kicad(circuit, output_file, include_controls=True):
    """
    Convert a PySpice Circuit to KiCad-compatible SPICE netlist

    Args:
        circuit: PySpice Circuit object
        output_file: Path to output .cir file
        include_controls: Include .control block for ngspice
    """

    # Get the SPICE netlist from PySpice
    netlist_str = str(circuit)

    # Clean up the netlist for KiCad compatibility
    lines = netlist_str.split('\n')
    kicad_lines = []

    # Add header
    kicad_lines.append(f"* {circuit.title}")
    kicad_lines.append("* KiCad 9.0 Compatible Netlist")
    kicad_lines.append("* Converted from PySpice")
    kicad_lines.append("")
    kicad_lines.append(f".title {circuit.title}")
    kicad_lines.append("")

    # Process each line
    in_model = False
    model_lines = []
    component_lines = []

    for line in lines:
        line = line.strip()

        if not line or line.startswith('.title'):
            continue

        # Handle .model statements - format them nicely for KiCad
        if line.startswith('.model'):
            in_model = True
            model_lines.append("")
            model_lines.append(line)
            continue

        # Regular component or source
        if not line.startswith('.'):
            component_lines.append(line)
        elif in_model:
            model_lines.append(line)

    # Write components section
    if component_lines:
        kicad_lines.append("* ============================================")
        kicad_lines.append("* CIRCUIT COMPONENTS")
        kicad_lines.append("* ============================================")
        kicad_lines.append("")
        kicad_lines.extend(component_lines)
        kicad_lines.append("")

    # Write models section
    if model_lines:
        kicad_lines.append("* ============================================")
        kicad_lines.append("* TRANSISTOR MODELS")
        kicad_lines.append("* ============================================")
        kicad_lines.extend(model_lines)
        kicad_lines.append("")

    # Add simulation commands
    kicad_lines.append("* ============================================")
    kicad_lines.append("* SIMULATION COMMANDS")
    kicad_lines.append("* ============================================")
    kicad_lines.append("")
    kicad_lines.append("* Operating Point Analysis")
    kicad_lines.append(".op")
    kicad_lines.append("")
    kicad_lines.append("* AC Analysis (Bode Plot)")
    kicad_lines.append("* Uncomment to run:")
    kicad_lines.append("*.ac dec 100 0.1 1G")
    kicad_lines.append("")
    kicad_lines.append("* Transient Analysis")
    kicad_lines.append("* Uncomment to run:")
    kicad_lines.append("*.tran 1n 10u")
    kicad_lines.append("")

    # Add control block for ngspice
    if include_controls:
        kicad_lines.append("* ngspice control commands")
        kicad_lines.append(".control")
        kicad_lines.append("op")
        kicad_lines.append("print all")
        kicad_lines.append("")
        kicad_lines.append("* Uncomment for AC analysis:")
        kicad_lines.append("*ac dec 100 0.1 1G")
        kicad_lines.append("*plot vdb(vout)")
        kicad_lines.append("*plot vp(vout)")
        kicad_lines.append(".endc")
        kicad_lines.append("")

    kicad_lines.append(".end")

    # Write to file
    with open(output_file, 'w') as f:
        f.write('\n'.join(kicad_lines))

    print(f"✓ KiCad SPICE netlist created: {output_file}")
    print(f"  Total lines: {len(kicad_lines)}")
    print(f"  Components: {len(component_lines)}")
    print(f"\nTo use in KiCad 9.0:")
    print(f"  1. Open KiCad Schematic Editor")
    print(f"  2. Inspect → Simulator")
    print(f"  3. File → Open Workbook → {output_file}")
    print(f"  4. Run Simulation")


def add_kicad_simulation_commands(cir_file, sim_type='ac'):
    """
    Add specific simulation commands to a .cir file

    Args:
        cir_file: Path to .cir file
        sim_type: 'ac', 'tran', 'dc', or 'all'
    """

    sim_commands = {
        'ac': [
            "* AC Analysis (Frequency Response)",
            ".ac dec 100 0.1 1G",
            "",
            ".control",
            "ac dec 100 0.1 1G",
            "plot vdb(vout) title 'Frequency Response (Gain)'",
            "plot vp(vout) title 'Frequency Response (Phase)'",
            ".endc"
        ],
        'tran': [
            "* Transient Analysis (Time Domain)",
            ".tran 1n 10u",
            "",
            ".control",
            "tran 1n 10u",
            "plot v(vout) v(vin_p) title 'Transient Response'",
            ".endc"
        ],
        'dc': [
            "* DC Sweep Analysis",
            ".dc Vin_p 0 5 0.01",
            "",
            ".control",
            "dc Vin_p 0 5 0.01",
            "plot v(vout) title 'DC Transfer Characteristic'",
            ".endc"
        ],
        'all': [
            "* Operating Point",
            ".op",
            "",
            "* AC Analysis",
            ".ac dec 100 0.1 1G",
            "",
            "* Transient Analysis",
            ".tran 1n 10u",
            "",
            ".control",
            "op",
            "print all",
            "ac dec 100 0.1 1G",
            "plot vdb(vout)",
            "plot vp(vout)",
            "tran 1n 10u",
            "plot v(vout)",
            ".endc"
        ]
    }

    commands = sim_commands.get(sim_type, sim_commands['all'])

    # Read existing file
    with open(cir_file, 'r') as f:
        content = f.read()

    # Find .end and insert before it
    if '.end' in content:
        content = content.replace('.end', '\n'.join(commands) + '\n\n.end')
    else:
        content += '\n\n' + '\n'.join(commands) + '\n\n.end'

    # Write back
    with open(cir_file, 'w') as f:
        f.write(content)

    print(f"✓ Added {sim_type} simulation commands to {cir_file}")


# Example usage
if __name__ == "__main__":
    print("="*60)
    print("PySpice to KiCad SPICE Converter")
    print("="*60)

    # Example: Create a simple test circuit
    circuit = Circuit('Voltage Divider Example')
    circuit.V('input', 'vin', circuit.gnd, 10@u_V)
    circuit.R(1, 'vin', 'vout', 1@u_kOhm)
    circuit.R(2, 'vout', circuit.gnd, 1@u_kOhm)

    # Convert to KiCad format
    pyspice_to_kicad(circuit, 'voltage_divider_kicad.cir')

    print("\n" + "="*60)
    print("Conversion complete!")
    print("="*60)
