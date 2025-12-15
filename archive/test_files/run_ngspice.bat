@echo off
cd /d "%~dp0"
echo Starting ngspice simulator...
echo.
"C:\Users\Mads2\miniconda3\Library\bin\ngspice.exe" -b two_stage_opamp_kicad.cir -o results.txt
echo.
echo Simulation complete! Check results.txt
echo.
echo To run interactively with plots, type: ngspice two_stage_opamp_kicad.cir
pause
