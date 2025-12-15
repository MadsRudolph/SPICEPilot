#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SPICEPilot Setup Verification Script

Checks that all required packages and dependencies are correctly installed.
"""

import sys
import os

# Configure encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def check_module(module_name, package_name=None):
    """Check if a Python module can be imported."""
    if package_name is None:
        package_name = module_name

    try:
        mod = __import__(module_name)
        version = getattr(mod, '__version__', 'unknown')
        print(f"✅ {package_name:15s} {version}")
        return True
    except ImportError:
        print(f"❌ {package_name:15s} NOT INSTALLED")
        return False

def check_ngspice():
    """Check if ngspice is accessible."""
    import subprocess
    try:
        result = subprocess.run(['ngspice', '--version'],
                              capture_output=True,
                              text=True,
                              timeout=5)
        if result.returncode == 0:
            # Extract version from output
            version_line = result.stdout.split('\n')[0] if result.stdout else 'unknown'
            print(f"✅ ngspice         {version_line.strip()}")
            return True
        else:
            print(f"❌ ngspice         NOT ACCESSIBLE")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print(f"❌ ngspice         NOT FOUND IN PATH")
        return False

def check_ngspice_dll():
    """Check if PySpice can load ngspice.dll."""
    try:
        from PySpice.Spice.NgSpice.Shared import NgSpiceShared
        print(f"✅ ngspice.dll     Loadable by PySpice")
        return True
    except Exception as e:
        print(f"❌ ngspice.dll     Cannot load: {str(e)}")
        print(f"   Hint: Copy ngspice.dll to PySpice directory")
        return False

def check_pyspice_location():
    """Show PySpice installation location."""
    try:
        import PySpice
        pyspice_dir = os.path.dirname(PySpice.__file__)
        print(f"\nℹ️  PySpice location: {pyspice_dir}")
        return pyspice_dir
    except ImportError:
        return None

def check_examples():
    """Check if example files exist."""
    examples = [
        'examples/1_current_mirror/current_mirror_bias.py',
        'examples/1_current_mirror/current_mirror_bias.cir',
        'examples/2_two_stage_opamp/two_stage_opamp_improved.py',
    ]

    print("\nExample files:")
    all_exist = True
    for example in examples:
        if os.path.exists(example):
            print(f"✅ {example}")
        else:
            print(f"❌ {example} NOT FOUND")
            all_exist = False

    return all_exist

def main():
    print("=" * 60)
    print("SPICEPilot Setup Verification")
    print("=" * 60)
    print("\nChecking Python packages:")
    print("-" * 60)

    all_ok = True

    # Check required packages
    all_ok &= check_module('PySpice')
    all_ok &= check_module('matplotlib')
    all_ok &= check_module('numpy')
    all_ok &= check_module('scipy')

    # Optional but useful packages
    check_module('pandas')

    print("\nChecking external tools:")
    print("-" * 60)

    # Check ngspice (command line is optional if DLL works)
    ngspice_cli = check_ngspice()
    ngspice_dll = check_ngspice_dll()

    # DLL is essential, CLI is nice to have
    all_ok &= ngspice_dll
    if not ngspice_cli and ngspice_dll:
        print("   ℹ️  Note: ngspice CLI not in PATH, but DLL works (sufficient for PySpice)")

    # Show PySpice location
    pyspice_dir = check_pyspice_location()

    # Check examples
    print()
    print("-" * 60)
    examples_ok = check_examples()

    # Final summary
    print("\n" + "=" * 60)
    if all_ok and examples_ok:
        print("✅ All checks passed!")
        print("\nYou're ready to use SPICEPilot!")
        print("\nQuick start:")
        print("  cd examples/1_current_mirror")
        print("  python current_mirror_bias.py")
    else:
        print("❌ Some checks failed")
        print("\nPlease review the errors above and:")
        print("  1. Install missing packages: pip install -r requirements.txt")
        print("  2. Install ngspice: conda install -c conda-forge ngspice")
        if pyspice_dir:
            print(f"  3. Copy ngspice.dll to: {pyspice_dir}")
        print("\nSee SETUP_INSTRUCTIONS.md for detailed help")
        sys.exit(1)

    print("=" * 60)

if __name__ == '__main__':
    main()
