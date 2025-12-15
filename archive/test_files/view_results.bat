@echo off
cd /d "%~dp0"
echo ============================================================
echo   Current Mirror Circuit - View Results with Plots
echo ============================================================
echo.
echo This will open ngspice and automatically show you:
echo   1. Operating point results
echo   2. DC sweep plot (VDD from 0.5V to 1.2V)
echo.
echo Commands you can use in ngspice:
echo   - plot v(vd1) v(vs2) v(vd3)  : Plot all node voltages
echo   - print all                  : Print all values
echo   - quit                       : Exit
echo.
pause
echo.
"C:\Users\Mads2\miniconda3\Library\bin\ngspice.exe" current_mirror_bias.cir
