@echo off
echo ====================================================
echo DEBUG: Testing batch file
echo ====================================================
echo.
echo Current directory BEFORE cd:
cd
echo.
echo Changing to batch file directory...
cd /d "%~dp0"
echo.
echo Current directory AFTER cd:
cd
echo.
echo Checking if circuit file exists:
dir current_mirror_bias.cir
echo.
echo Checking ngspice location:
where ngspice
echo.
echo Press any key to run ngspice...
pause
echo.
echo Running: ngspice current_mirror_bias.cir
echo.
"C:\Users\Mads2\miniconda3\Library\bin\ngspice.exe" current_mirror_bias.cir
echo.
echo ====================================================
echo Ngspice finished. Press any key to exit.
pause
