# SPICE Circuit Examples

Complete working circuit examples with simulations.

## Quick Start

Each circuit folder has a **RUN.bat** file - just double-click it to simulate!

## Available Circuits

### 1. Current Mirror Bias Circuit
**Folder:** `1_current_mirror/`

**Circuit:** NMOS current mirror with bias network
- VDD = 0.9V
- Three NMOS transistors (Kp=180µ, Vto=0.4V)
- 45µA current sources
- Validated: 99.7% theoretical accuracy

**Files:**
- `current_mirror_bias.cir` - SPICE netlist
- `current_mirror_bias.py` - PySpice implementation
- `RUN.bat` - Double-click to simulate

**Expected Results:**
- VD1 = 0.648V
- VS2 ≈ 0V (current mirror output)
- VD3 = 0.649V

---

### 2. Two-Stage CMOS Op-Amp
**Folder:** `2_two_stage_opamp/`

**Circuit:** Two-stage operational amplifier
- VDD = 5V
- Differential input stage with PMOS current mirror load
- Common-source output stage
- Miller compensation

**Files:**
- `two_stage_opamp_kicad.cir` - SPICE netlist
- `two_stage_opamp_improved.py` - PySpice implementation
- `two_stage_opamp.kicad_pro` - KiCad project
- `two_stage_opamp.kicad_sch` - KiCad schematic
- `RUN.bat` - Double-click to simulate

**Expected Results:**
- DC Gain: 1.4 dB (needs optimization)
- 3dB Bandwidth: 1.16 MHz
- Unity-Gain Frequency: 0.71 MHz
- Phase Margin: >300°

---

## How to Simulate

### Method 1: Double-Click RUN.bat (Easiest)
1. Navigate to circuit folder
2. Double-click `RUN.bat`
3. View results in ngspice window

### Method 2: Command Line
```bash
cd examples/1_current_mirror
ngspice current_mirror_bias.cir
```

### Method 3: Python/PySpice
```bash
cd examples/1_current_mirror
python current_mirror_bias.py
```

## Documentation

Complete documentation available in:
`C:\Users\Mads2\DTU\Obsidian\Courses\Integrated Analog Electronics\LTspice & Kicad\`

**Key guides:**
- [[README - Start Here]] - Documentation index
- [[06 - Current Mirror Circuit Example]] - Circuit 1 details
- [[02 - Two-Stage CMOS Op-Amp]] - Circuit 2 details
- [[04 - Simulation Workflows]] - How to run simulations
- [[Quick Reference - SPICE Commands]] - Command cheatsheet

## Results Location

Simulation outputs are saved to:
- `../../results/plots/` - Plot images
- `../../results/logs/` - Simulation logs

---

**Need help?** See the Obsidian documentation or run `ngspice` from command line with `cd` to the circuit directory.
