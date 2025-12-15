# KiCad 9.0 SPICE Simulation Integration Guide

## Two-Stage CMOS Op-Amp Simulation in KiCad

This guide shows you how to simulate the two-stage CMOS operational amplifier in KiCad 9.0.

---

## Method 1: Direct SPICE Netlist Simulation (Easiest)

### Step 1: Open the SPICE File in KiCad

1. Open KiCad 9.0
2. Go to **File → Open → two_stage_opamp_kicad.cir**
3. Or use the command line:
   ```bash
   ngspice two_stage_opamp_kicad.cir
   ```

### Step 2: Run from KiCad Schematic Editor

1. Create a new KiCad project
2. Open the Schematic Editor
3. Go to **Inspect → Simulator**
4. In the simulator window: **File → Open Workbook → Browse** to `two_stage_opamp_kicad.cir`
5. Click **Run Simulation**

---

## Method 2: Build Schematic in KiCad (Recommended)

### Step 1: Create MOSFET Symbol Library

1. Open **Symbol Editor**
2. Create new library: `OpAmp_Custom.kicad_sym`
3. Add NMOS and PMOS symbols (or use built-in from `Simulation_SPICE` library)

### Step 2: Add SPICE Models to Components

For each MOSFET in your schematic:

1. Right-click component → **Properties**
2. Go to **Simulation Model** tab
3. Select **Model type: Raw SPICE Model**
4. Add model parameters:

**For NMOS:**
```
.model NMOS nmos (level=1 kp=120u vto=0.7 lambda=0.02 gamma=0.4 phi=0.65 w=30u l=2u)
```

**For PMOS:**
```
.model PMOS pmos (level=1 kp=40u vto=-0.7 lambda=0.02 gamma=0.4 phi=0.65 w=60u l=2u)
```

### Step 3: Draw the Circuit

Create your schematic with these components:

**Power Supplies:**
- Add `V` (Voltage Source) from `Simulation_SPICE` library
- VDD: 5V DC
- Vbias_p: 3.5V DC
- Vbias_n: 1.5V DC
- Vin_p: 2.5V DC + 0.5V AC
- Vin_n: 2.5V DC

**Transistors:**
- M1-M8: Add MOSFET symbols (NMOS/PMOS)
- Connect according to the circuit diagram

**Passives:**
- Add capacitors: CA (3pF), CB (0.5pF), CL (15pF)
- Add resistor: Rdummy (10kΩ)

### Step 4: Add Simulation Commands

1. Add a **Text** element to your schematic (Place → Text)
2. Add SPICE directives as text:

```spice
.ac dec 100 0.1 1G
.op
```

Or use the built-in simulation settings:

1. Go to **Inspect → Simulator**
2. Click **Settings** (gear icon)
3. Select simulation type:
   - **AC Analysis**: Start 0.1 Hz, Stop 1 GHz, Points/decade: 100
   - **Operating Point**: Check this box
   - **Transient**: Start 0, Stop 10µs, Step 1ns (optional)

### Step 5: Run Simulation

1. Open **Inspect → Simulator** (Ctrl+Shift+S)
2. Click **Run Simulation** button
3. View results in the plot window

### Step 6: Plot Results

In the simulator window:

**For Bode Plot (AC Analysis):**
1. Right-click in plot area → **Add Signal**
2. Select `V(vout)`
3. Click **Show Magnitude** and **Show Phase**

**For Operating Point:**
1. After simulation, check **SPICE log** tab
2. View node voltages

---

## Method 3: Using SPICE Netlist with KiCad Schematic

### Step 1: Create Hierarchical Sheet

1. Create your top-level schematic
2. Add **Hierarchical Sheet** (Place → Hierarchical Sheet)
3. Name it "OpAmp_Core"

### Step 2: Link SPICE Netlist

1. Right-click the hierarchical sheet → **Properties**
2. Go to **Simulation Model** tab
3. Select **SPICE subcircuit from file**
4. Browse to: `two_stage_opamp_kicad.cir`

### Step 3: Add Test Circuit

Around your op-amp block, add:
- Input signal sources
- Load resistor/capacitor
- Power supplies

### Step 4: Simulate

1. **Inspect → Simulator**
2. Configure and run simulation

---

## Simulation Types Available

### 1. Operating Point (.op)
Shows DC voltages at all nodes

**Expected Results:**
- vout ≈ 0.1V (needs bias optimization)
- vin_p, vin_n = 2.5V
- vdd = 5V

### 2. AC Analysis (.ac)
Frequency response (Bode plot)

**Expected Results:**
- DC Gain: ~1.4 dB
- 3dB BW: ~1.16 MHz
- Unity-gain freq: ~0.71 MHz
- Phase margin: Good stability

**To plot in KiCad:**
- Add signal: `vdb(vout)` for gain in dB
- Add signal: `vp(vout)` for phase in degrees

### 3. Transient Analysis (.tran)
Time-domain step response

**Example command:**
```spice
.tran 1n 10u
```

---

## Tips for KiCad 9.0 SPICE Simulation

### Using Built-in SPICE Models

KiCad has built-in models in:
- **Symbol Library**: `Simulation_SPICE`
- **SPICE Models**: Includes basic BJT, MOSFET, diode models

### Viewing Currents

To measure current through a component:
1. In simulator, add probe: `I(Vdd)` for current through VDD
2. Or add `I(M1)` for transistor drain current

### Optimization

To optimize bias voltages:
1. Use **Parametric sweep** in KiCad simulator
2. **Settings → Custom** → Add:
   ```spice
   .step param Vbias 1 4 0.1
   ```

### Saving Plots

1. In simulator window: **File → Export current plot as CSV**
2. Or screenshot: Right-click plot → **Export as image**

---

## Common Issues & Solutions

### Issue: "Model not found"
**Solution**: Make sure `.model` statements are in your netlist or added to component properties

### Issue: "Convergence failed"
**Solution**:
- Add `.options reltol=1e-3 abstol=1e-12` to netlist
- Adjust initial conditions
- Check for floating nodes

### Issue: Can't see AC response
**Solution**:
- Make sure input has AC component: `DC 2.5 AC 0.5`
- Use `vdb(vout)` for dB scale
- Check frequency range is correct

### Issue: No ground node
**Solution**: KiCad requires node `0` as ground. Use GND symbol from library.

---

## Exporting Results

### To Python/Matplotlib
1. Export CSV from KiCad simulator
2. Use Python script:

```python
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('kicad_ac_analysis.csv')
plt.semilogx(data['frequency'], data['vout_db'])
plt.show()
```

### To LTspice
The `.cir` file is compatible with LTspice:
1. Open LTspice
2. **File → Open → two_stage_opamp_kicad.cir**
3. Run simulation

---

## Advanced: Creating Reusable Op-Amp Subcircuit

Create a `.subckt` definition for reuse:

```spice
.subckt OPAMP_2STAGE vin_p vin_n vout vdd vss
* (paste transistor definitions here)
* with updated node names
.ends
```

Then use in KiCad:
```spice
X1 in+ in- out VDD VSS OPAMP_2STAGE
```

---

## Quick Reference: KiCad Simulator Shortcuts

| Action | Shortcut |
|--------|----------|
| Open Simulator | Ctrl+Shift+S |
| Run Simulation | F5 |
| Add Signal | Ctrl+A |
| Zoom In | Ctrl++ |
| Zoom Out | Ctrl+- |
| Measure cursor | M |
| Show grid | G |

---

## Next Steps

1. **Optimize bias voltages** for higher gain
2. **Add feedback network** to create closed-loop amplifier
3. **Test with real signals** using transient analysis
4. **Layout in KiCad PCB** with parasitic extraction

For questions, refer to:
- KiCad Documentation: https://docs.kicad.org/
- ngspice Manual: http://ngspice.sourceforge.net/docs.html
- SPICEPilot: Pilot_prompt.md

---

**Note**: The SPICE netlist in `two_stage_opamp_kicad.cir` is ready to use in KiCad 9.0 without modifications.
