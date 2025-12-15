@echo off
cd /d "%~dp0"
echo ====================================================
echo   Current Mirror Bias Circuit - Interactive Simulation
echo ====================================================
echo.
echo Starting ngspice...
echo.
"C:\Users\Mads2\miniconda3\Library\bin\ngspice.exe" current_mirror_bias.cir
