@echo off
echo ================================================
echo   Two-Stage CMOS Op-Amp - SPICE Simulation
echo ================================================
echo.

cd /d "%~dp0"

echo Running ngspice simulation...
echo.

"C:\Users\Mads2\miniconda3\Library\bin\ngspice.exe" two_stage_opamp_kicad.cir

echo.
echo ================================================
echo Simulation complete. Press any key to exit.
pause > nul
