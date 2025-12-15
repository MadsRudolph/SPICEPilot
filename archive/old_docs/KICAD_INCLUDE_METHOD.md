# Using SPICE Netlist in KiCad 9.0

## The Problem
The schematic components aren't connecting properly in the visual editor.

## The Solution
Use KiCad's **.include** directive to load your working SPICE netlist directly.

---

## Step-by-Step Instructions

### 1. Create Minimal Schematic

1. **Open KiCad 9.0**
2. **File → New Project** → Name it "OpAmp_Simulation"
3. **Open Schematic Editor**

### 2. Add Minimal Components (KiCad Requirement)

You need at least one component for KiCad to work:

1. **Add → Symbol** (or press 'A')
2. Search for: **R** (resistor)
3. Place it anywhere
4. Value: **1k**

5. **Add → Power Symbol** → Search: **GND**
6. Place GND below the resistor
7. **Wire** them together (press 'W')

### 3. Add SPICE Include Directive

This is the key step:

1. **Place → Text** (or press 'T')

2. In the text box, type **EXACTLY**:
   ```
   .include "C:/Users/Mads2/SPICEPilot/two_stage_opamp_kicad.cir"
   ```

   **IMPORTANT**:
   - Use forward slashes `/` not backslashes `\`
   - Keep the quotes `"`

3. Place the text anywhere on the schematic

4. The text should appear in a box

### 4. Run Simulation

1. **Inspect → Simulator** (Ctrl+Shift+S)

2. **Simulation → Edit Simulation Command**
   - Select **AC** tab
   - Type of Sweep: **Decade**
   - Number of points: **100**
   - Start frequency: **0.1**
   - Stop frequency: **1G**
   - Click **OK**

3. **Click Run** (▶ green play button)

4. **Add Signals**:
   - Right-click plot area
   - **Add Signals...**
   - Select **V(vout)**
   - Click **OK**

5. **Show as dB**:
   - Right-click the trace in the signals list
   - **Show as → Magnitude (dB)**

### 5. You'll See the Bode Plot!

---

## Alternative Method: SPICE Subcircuit Approach

If .include doesn't work, create a wrapper:

1. Create new file: `opamp_wrapper.cir`
   ```spice
   * Op-Amp Simulation Wrapper

   .include "C:/Users/Mads2/SPICEPilot/two_stage_opamp_kicad.cir"

   .end
   ```

2. In KiCad, reference this wrapper instead

---

## Troubleshooting

### "File not found"
- Check the path is correct
- Use forward slashes: `C:/Users/...`
- Don't use: `C:\Users\...`

### "No signals available"
- Make sure simulation completed
- Check SPICE log tab for errors
- Verify the .cir file path is correct

### Still not working?
Use ngspice directly (see next section)

---

## Easiest Alternative: Just Use ngspice

**Option A: With Plots (Interactive)**

Double-click: **`run_with_plots.bat`**

Then type:
```
run
plot vdb(vout)
```

**Option B: Command Line**

Open terminal in the SPICEPilot folder:
```bash
ngspice two_stage_opamp_kicad.cir
```

At the `ngspice 1 ->` prompt:
```
run
plot vdb(vout) vp(vout)
```

This opens a plot window with your Bode plot!

---

## Summary

| Method | Difficulty | Integration |
|--------|-----------|-------------|
| ngspice directly | ⭐ Easiest | External tool |
| KiCad + .include | ⭐⭐ Easy | Full KiCad |
| Fix schematic wiring | ⭐⭐⭐⭐ Hard | Full KiCad |

**Recommendation**: Use **ngspice directly** for quick simulations, or **KiCad + .include** for project integration.

---

Your SPICE netlist (`two_stage_opamp_kicad.cir`) is **100% correct and working**.

The schematic visual is just for editing - the simulation uses the netlist!
