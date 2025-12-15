@echo off
cd /d "%~dp0"
echo ====================================================
echo   Two-Stage CMOS Op-Amp - Simulation
echo ====================================================
echo.
echo Starting ngspice...
echo.
"C:\Users\Mads2\miniconda3\Library\bin\ngspice.exe" two_stage_opamp_kicad.cir
