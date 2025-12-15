@echo off
cd /d "%~dp0"
echo Starting ngspice with current mirror circuit...
"C:\Users\Mads2\miniconda3\Library\bin\ngspice.exe" current_mirror_bias.cir
