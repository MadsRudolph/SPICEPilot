# SPICEPilot Setup Instructions

Complete guide for setting up SPICEPilot on a new PC.

## Prerequisites

- Miniconda or Anaconda installed
- Git (for cloning the repository)
- Windows OS (adjust paths for Linux/Mac)

## Quick Setup (Automated)

1. **Pull the repository:**
   ```bash
   cd C:\Users\YourUsername\DTU
   git pull
   git submodule update --init --recursive
   ```

2. **Run the setup script:**
   ```bash
   cd SPICEPilot
   setup.bat
   ```

   This will automatically:
   - Install ngspice via conda
   - Install Python packages (PySpice, matplotlib, numpy, etc.)
   - Copy ngspice.dll to PySpice folder
   - Verify the installation

## Manual Setup (Step by Step)

If the automated script doesn't work, follow these steps:

### 1. Install ngspice

```bash
conda install -c conda-forge ngspice
```

Verify installation:
```bash
ngspice --version
```

### 2. Install Python Packages

```bash
pip install -r requirements.txt
```

This installs:
- PySpice 1.5
- matplotlib 3.10.8
- numpy 2.3.5
- scipy 1.16.3

### 3. Copy ngspice.dll to PySpice

**Find PySpice location:**
```bash
python -c "import PySpice; import os; print(os.path.dirname(PySpice.__file__))"
```

**Find ngspice.dll location:**
```bash
where ngspice.dll
```
(Usually: `C:\Users\YourUsername\miniconda3\Library\bin\ngspice.dll`)

**Copy the DLL:**
```bash
# Example (adjust paths for your system):
copy C:\Users\YourUsername\miniconda3\Library\bin\ngspice.dll C:\Users\YourUsername\miniconda3\Lib\site-packages\PySpice\
```

### 4. Verify Installation

```bash
python verify_setup.py
```

If you see "✅ All checks passed!" you're ready to go!

## Testing Your Setup

### Test 1: Run Current Mirror Example

```bash
cd examples\1_current_mirror
python current_mirror_bias.py
```

Expected: Console output showing voltages and currents.

### Test 2: Run ngspice

```bash
cd examples\1_current_mirror
ngspice current_mirror_bias.cir
```

In ngspice prompt:
```
run
print all
quit
```

Expected: Node voltages displayed.

### Test 3: Run Op-Amp Simulation

```bash
cd examples\2_two_stage_opamp
python two_stage_opamp_improved.py
```

Expected: Bode plot window appears.

## Troubleshooting

### Error: "cannot load library ngspice.dll"

**Problem:** PySpice can't find ngspice.dll

**Solution:**
1. Find ngspice.dll: `where ngspice.dll`
2. Find PySpice folder: `python -c "import PySpice; import os; print(os.path.dirname(PySpice.__file__))"`
3. Copy DLL to PySpice folder

### Error: "ModuleNotFoundError: No module named 'PySpice'"

**Problem:** PySpice not installed

**Solution:**
```bash
pip install PySpice
```

### Error: "ngspice: command not found"

**Problem:** ngspice not in PATH or not installed

**Solution:**
```bash
conda install -c conda-forge ngspice
```

### Warning: "Unsupported ngspice version"

**Problem:** Harmless warning, can be ignored

**Solution:** No action needed, everything will work.

## File Locations

After setup, your directory structure should be:

```
C:\Users\YourUsername\DTU\
├── SPICEPilot\                          # Git submodule
│   ├── examples\
│   │   ├── 1_current_mirror\
│   │   └── 2_two_stage_opamp\
│   ├── results\
│   ├── requirements.txt                 # Python packages
│   ├── setup.bat                        # Automated setup
│   ├── verify_setup.py                  # Verification script
│   └── SETUP_INSTRUCTIONS.md            # This file
│
└── Obsidian\
    └── Courses\Integrated Analog Electronics\LTspice & Kicad\
        └── [Documentation files]
```

## Package Versions

This setup was tested with:
- Python 3.13
- PySpice 1.5
- ngspice 41
- matplotlib 3.10.8
- numpy 2.3.5
- scipy 1.16.3

## Next Steps

After successful setup:
1. Review the documentation in `Obsidian/Courses/Integrated Analog Electronics/LTspice & Kicad/`
2. Start with `README - Start Here.md`
3. Try the current mirror example
4. Explore the two-stage op-amp design

## Need Help?

Check the troubleshooting guides:
- `Obsidian/.../05 - Troubleshooting Guide.md`
- GitHub issues on the SPICEPilot repository

---

**Last Updated:** 2025-12-15
**Tested On:** Windows 11, Python 3.13, Miniconda
