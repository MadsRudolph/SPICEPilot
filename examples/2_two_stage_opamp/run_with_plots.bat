@echo off
cd /d "%~dp0"
echo ================================================
echo   Two-Stage Op-Amp - Interactive Simulation
echo ================================================
echo.
echo This will open ngspice with interactive plotting
echo.
echo After it opens, type these commands:
echo   1. run
echo   2. plot vdb(vout)
echo   3. plot vp(vout)
echo.
pause
echo.
"C:\Users\Mads2\miniconda3\Library\bin\ngspice.exe" two_stage_opamp_kicad.cir
