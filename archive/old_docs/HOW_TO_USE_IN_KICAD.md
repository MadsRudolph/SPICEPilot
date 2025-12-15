# How to Use Two-Stage Op-Amp in KiCad 9.0

## Method 1: Using Simulator with Raw SPICE Netlist (Recommended)

### Step-by-Step Instructions:

1. **Open KiCad 9.0**
   - Start KiCad or open any existing project

2. **Open the Schematic Editor**
   - Click on "Schematic Editor" from KiCad main window
   - Or open any existing schematic

3. **Open the Simulator**
   - In Schematic Editor: **Inspect → Simulator** (or Ctrl+Shift+S)
   - A new window will open: "SPICE Simulator"

4. **Load the SPICE Netlist**
   - In the Simulator window: **File → New Analysis Tab**
   - Or click the **Settings** icon (gear icon)
   - In the dialog that opens:
     - **Netlist**: Click "..." browse button
     - Navigate to: `C:\Users\Mads2\SPICEPilot\two_stage_opamp_kicad.cir`
     - Select the file and click Open

5. **Configure Simulation Type**
   - Still in Settings dialog:
   - Select **AC** tab
   - Set:
     - Scale: **Decade**
     - Number of points per decade: **100**
     - Start frequency: **0.1**
     - Stop frequency: **1G** (1 GHz)
   - Click **OK**

6. **Run the Simulation**
   - Click the **Run Simulation** button (Play icon ▶)
   - Wait a few seconds for simulation to complete

7. **Add Signals to Plot**
   - After simulation completes, right-click in the plot area
   - Select **Add Signals...**
   - From the list, select `V(vout)`
   - Click **OK**
   - The frequency response will appear!

8. **View Gain in dB**
   - Right-click on the `V(vout)` trace in the signals list (left side)
   - Select **Show Magnitude in dB**
   - The Y-axis will now show gain in decibels

9. **Add Phase Plot**
   - Right-click in plot area → **Add Signals**
   - Select `V(vout)` again
   - Right-click the new trace → **Show Phase**
   - You now have both magnitude and phase!

---

## Method 2: Using Workbook File

1. **Open KiCad Schematic Editor**

2. **Open Simulator** (Inspect → Simulator)

3. **Load Workbook**
   - In Simulator: **File → Open Workbook**
   - Browse to: `C:\Users\Mads2\SPICEPilot\two_stage_opamp.wbk`
   - Click Open

4. **Set Netlist Path**
   - If prompted for netlist location
   - Browse to: `two_stage_opamp_kicad.cir`

5. **Run Simulation**
   - Click **Run** (▶ button)
   - The workbook includes 3 pre-configured tabs:
     - **AC Analysis** (Bode plot)
     - **Operating Point** (DC voltages)
     - **Transient** (time response)

---

## Method 3: Command Line (For Testing)

If KiCad gives issues, test with ngspice directly:

```bash
cd C:\Users\Mads2\SPICEPilot
ngspice two_stage_opamp_kicad.cir
```

Once in ngspice prompt:
```
ngspice> run
ngspice> plot vdb(vout)
ngspice> plot vp(vout)
```

---

## Troubleshooting

### "Cannot find netlist file"
**Solution**:
- Make sure you're pointing to the full path: `C:\Users\Mads2\SPICEPilot\two_stage_opamp_kicad.cir`
- Or copy the .cir file to your KiCad project folder

### "No signals available"
**Solution**:
- Make sure simulation ran successfully (check for error messages)
- Look in the **SPICE log** tab for errors
- Try running Operating Point analysis first (.op)

### "Simulation failed to converge"
**Solution**:
- The netlist already includes convergence options
- If still failing, edit the .cir file and add:
  ```
  .options reltol=1e-2 abstol=1e-10
  ```

### Workbook doesn't load
**Solution**:
- Use Method 1 (raw SPICE netlist) instead
- KiCad workbooks are tied to schematic files
- For standalone SPICE files, direct netlist loading works better

---

## What You Should See

### AC Analysis (Bode Plot)
- **Gain**: Starting around 1-2 dB, rolling off at higher frequencies
- **3dB Bandwidth**: ~1.16 MHz
- **Phase**: Starting near 0°, rolling to negative values

### Operating Point (.op)
Key voltages:
- `vout` = 0.091 V
- `vdd` = 5.0 V
- `vin_p`, `vin_n` = 2.5 V
- `n_d2`, `n_d3` ≈ 3.3 V

### Transient Analysis
- Step response of the amplifier
- Shows settling time and behavior

---

## Tips for Best Results

1. **Start with AC analysis** - easiest to see if circuit works
2. **Check SPICE log** - contains detailed simulation info
3. **Use cursors** - Right-click plot → Show Cursors (measure frequencies/gain)
4. **Save workbook** - After setting up plots: File → Save Workbook
5. **Export data** - File → Export as CSV for external analysis

---

## Next Steps

Once you have the simulation running:

1. **Modify bias voltages** to optimize gain
2. **Sweep parameters** to see effects
3. **Add feedback** to create closed-loop amplifier
4. **Build the schematic** in KiCad for PCB layout

---

## Quick Reference

| Action | How To |
|--------|--------|
| Open Simulator | Inspect → Simulator (Ctrl+Shift+S) |
| Load netlist | Settings → Browse to .cir file |
| Run simulation | Click ▶ Play button |
| Add signal | Right-click plot → Add Signals |
| Show dB | Right-click trace → Show Magnitude in dB |
| Show phase | Right-click trace → Show Phase |
| Cursors | Right-click plot → Show Cursors |
| Export | File → Export as CSV |

---

If you still have issues, let me know what error message you're seeing!
