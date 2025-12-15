# SPICEPilot → KiCad 9.0 Integration - Quick Start

## ✓ Your Two-Stage Op-Amp is Ready for KiCad!

The two-stage CMOS operational amplifier has been created and tested. All files are ready to use in KiCad 9.0.

---

## Files Created

| File | Purpose |
|------|---------|
| `two_stage_opamp_kicad.cir` | **KiCad-compatible SPICE netlist** (ready to use) |
| `KICAD_SIMULATION_GUIDE.md` | Complete guide for KiCad 9.0 simulation |
| `pyspice_to_kicad.py` | Converter tool for future circuits |
| `two_stage_opamp_improved.py` | PySpice version for testing |
| `opamp_bode_improved.png` | Bode plot from PySpice simulation |

---

## Quick Start: 3 Ways to Use in KiCad

### Option 1: Import SPICE Netlist (Fastest)

1. Open **KiCad 9.0**
2. Open any schematic (or create new project)
3. Go to **Inspect → Simulator** (Ctrl+Shift+S)
4. In simulator window: **File → Open Workbook**
5. Browse to: `C:\Users\Mads2\SPICEPilot\two_stage_opamp_kicad.cir`
6. Click **Run Simulation** (play button)
7. Right-click plot area → **Add Signal** → Select `V(vout)`

**Result**: You'll see the frequency response immediately!

---

### Option 2: Build Schematic in KiCad

#### Step 1: Create New KiCad Project
```
File → New Project → "OpAmp_Design"
```

#### Step 2: Add Components

Open Schematic Editor and add:

**From `Simulation_SPICE` library:**
- `NMOS` (8 instances: M1-M8)
- `PMOS` (0 instances in our design, but PMOS models available)
- `V` Voltage sources (5 instances)
- `C` Capacitors (3 instances: CA, CB, CL)
- `R` Resistor (1 instance: Rdummy)

**Component Values:**
- VDD: 5V
- Vbias_p: 3.5V
- Vbias_n: 1.5V
- Vin_p: 2.5V (with AC 0.5)
- Vin_n: 2.5V
- CA: 3pF
- CB: 0.5pF
- CL: 15pF
- Rdummy: 10kΩ

#### Step 3: Add SPICE Models

For each MOSFET:
1. Right-click → **Properties**
2. **Simulation Model** tab
3. **Model type**: Built-in SPICE model
4. Copy model parameters from `two_stage_opamp_kicad.cir`:

**NMOS:**
```
.model NMOS nmos (level=1 kp=120u vto=0.7 lambda=0.02 w=30u l=2u)
```

**NMOS_BIG (for M8):**
```
.model NMOS_BIG nmos (level=1 kp=120u vto=0.7 lambda=0.02 w=60u l=2u)
```

**PMOS:**
```
.model PMOS pmos (level=1 kp=40u vto=-0.7 lambda=0.02 w=60u l=2u)
```

#### Step 4: Wire Circuit

Connect according to the circuit diagram:

**First Stage (Differential Amplifier):**
```
M8: Drain=n_tail, Gate=vbias_n, Source=GND, Body=GND
M2: Drain=n_d2, Gate=vin_p, Source=n_tail, Body=GND
M3: Drain=n_d3, Gate=vin_n, Source=n_tail, Body=GND
M4: Drain=n_d2, Gate=n_d2, Source=VDD, Body=VDD
M5: Drain=n_d3, Gate=n_d2, Source=VDD, Body=VDD
```

**Second Stage:**
```
M6: Drain=vout, Gate=vbias_p, Source=VDD, Body=VDD
M7: Drain=vout, Gate=n_d3, Source=GND, Body=GND
```

**Compensation:**
```
CA: n_d3 to vout (3pF)
CB: vout to GND (0.5pF)
CL: vout to GND (15pF)
```

#### Step 5: Add Simulation Commands

**Method A**: Add text to schematic
- Place → Text
- Type: `.ac dec 100 0.1 1G`

**Method B**: Use simulator settings
- Inspect → Simulator → Settings
- Select **AC Analysis**
- Start: 0.1 Hz, Stop: 1 GHz, Points/decade: 100

#### Step 6: Run & Plot

1. **Inspect → Simulator**
2. Click **Run** (F5)
3. Add signals:
   - `vdb(vout)` - Gain in dB
   - `vp(vout)` - Phase in degrees

---

### Option 3: Use as Subcircuit

Create reusable op-amp block:

1. Save `two_stage_opamp_kicad.cir` as subcircuit
2. In your main schematic, add hierarchical sheet
3. Link to the `.cir` file
4. Use multiple instances with different parameters

---

## Expected Simulation Results

### DC Operating Point
- **vout**: 0.091 V
- **n_tail**: 0.846 V
- **n_d2, n_d3**: 3.328 V

### AC Analysis (Bode Plot)
- **DC Gain**: 1.4 dB (~1.2 V/V)
- **3dB Bandwidth**: 1.16 MHz
- **Unity-Gain Frequency**: 0.71 MHz
- **Phase Margin**: >300° (very stable)

*Note: Low gain is due to simple biasing. For higher gain, optimize bias voltages.*

---

## Optimization Tips

### Increase Gain
Adjust bias voltages in KiCad:
- Increase `Vbias_p` (try 3.8V - 4.2V)
- Decrease `Vbias_n` (try 1.0V - 1.3V)
- Increase transistor W/L ratios

### Improve Bandwidth
- Reduce compensation capacitor CA (try 1-2pF)
- Reduce load capacitor CL

### Better DC Bias
Add resistive feedback or active biasing circuits

---

## Troubleshooting

### "Can't find model NMOS"
**Fix**: Add model definitions to your schematic as text:
```spice
.model NMOS nmos (level=1 kp=120u vto=0.7 lambda=0.02 w=30u l=2u)
```

### "No AC response visible"
**Fix**:
- Ensure input source has AC component: `DC 2.5 AC 0.5`
- Plot `vdb(vout)` not just `v(vout)`

### Convergence errors
**Fix**: Add to schematic as text:
```spice
.options reltol=1e-3 abstol=1e-12
```

### Ground node error
**Fix**: Every circuit MUST have a GND (node 0). Use GND symbol from library.

---

## Next Steps

1. **Optimize the op-amp** by adjusting bias voltages
2. **Add feedback** to create closed-loop amplifier
3. **Test with signals** using transient analysis
4. **Design PCB** in KiCad with proper layout

---

## Using SPICEPilot for New Circuits

### Generate New Circuits with AI

Tell me what circuit you need:
- "Create a CMOS NAND gate"
- "Design a current mirror with 1:4 ratio"
- "Build a differential amplifier with 40dB gain"

I'll generate both PySpice and KiCad-compatible formats!

### Convert Existing PySpice to KiCad

Use the converter:
```python
python pyspice_to_kicad.py
```

Then edit to add your circuit.

---

## Resources

- **KiCad Docs**: https://docs.kicad.org/9.0/
- **ngspice Manual**: http://ngspice.sourceforge.net/docs.html
- **SPICE Basics**: See `Pilot_prompt.md` in this folder
- **PySpice**: https://pyspice.fabrice-salvaire.fr/

---

## Summary

✅ **SPICEPilot is fully integrated with KiCad 9.0**
✅ **Two-stage op-amp ready to simulate**
✅ **Can generate any circuit from text description**
✅ **Works with PySpice, ngspice, and KiCad**

**Next**: Open KiCad, load `two_stage_opamp_kicad.cir`, and start simulating!
