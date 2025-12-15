@echo off
echo ================================================
echo SPICEPilot Automated Setup Script
echo ================================================
echo.

:: Check if we're in the right directory
if not exist "requirements.txt" (
    echo ERROR: requirements.txt not found!
    echo Please run this script from the SPICEPilot directory.
    pause
    exit /b 1
)

echo [Step 1/5] Installing ngspice via conda...
echo.
call conda install -y -c conda-forge ngspice
if %errorlevel% neq 0 (
    echo ERROR: Failed to install ngspice
    echo Please install Miniconda/Anaconda first
    pause
    exit /b 1
)
echo ✓ ngspice installed successfully
echo.

echo [Step 2/5] Installing Python packages...
echo.
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install Python packages
    pause
    exit /b 1
)
echo ✓ Python packages installed successfully
echo.

echo [Step 3/5] Finding PySpice installation directory...
echo.
for /f "delims=" %%i in ('python -c "import PySpice; import os; print(os.path.dirname(PySpice.__file__))"') do set PYSPICE_DIR=%%i
echo PySpice directory: %PYSPICE_DIR%
echo.

echo [Step 4/5] Finding ngspice.dll...
echo.
:: Try common locations
set NGSPICE_DLL=
if exist "%CONDA_PREFIX%\Library\bin\ngspice.dll" (
    set NGSPICE_DLL=%CONDA_PREFIX%\Library\bin\ngspice.dll
) else if exist "%USERPROFILE%\miniconda3\Library\bin\ngspice.dll" (
    set NGSPICE_DLL=%USERPROFILE%\miniconda3\Library\bin\ngspice.dll
) else if exist "%USERPROFILE%\anaconda3\Library\bin\ngspice.dll" (
    set NGSPICE_DLL=%USERPROFILE%\anaconda3\Library\bin\ngspice.dll
) else (
    echo WARNING: Could not find ngspice.dll automatically
    echo Please manually copy ngspice.dll to the PySpice directory
    echo.
    echo Run these commands:
    echo   where ngspice.dll
    echo   copy [ngspice.dll path] "%PYSPICE_DIR%"
    echo.
    goto verify
)

echo Found ngspice.dll: %NGSPICE_DLL%
echo.

echo [Step 5/5] Copying ngspice.dll to PySpice directory...
echo.
copy /Y "%NGSPICE_DLL%" "%PYSPICE_DIR%\"
if %errorlevel% neq 0 (
    echo ERROR: Failed to copy ngspice.dll
    echo Please copy manually:
    echo   copy "%NGSPICE_DLL%" "%PYSPICE_DIR%"
    pause
    exit /b 1
)
echo ✓ ngspice.dll copied successfully
echo.

:verify
echo ================================================
echo Running verification...
echo ================================================
echo.

if exist "verify_setup.py" (
    python verify_setup.py
) else (
    echo Verification script not found, running basic test...
    python -c "import PySpice; print('PySpice version:', PySpice.__version__)"
    if %errorlevel% neq 0 (
        echo ERROR: PySpice test failed
        pause
        exit /b 1
    )
)

echo.
echo ================================================
echo Setup Complete!
echo ================================================
echo.
echo Next steps:
echo   1. Test with: cd examples\1_current_mirror
echo   2. Run: python current_mirror_bias.py
echo   3. Or run: ngspice current_mirror_bias.cir
echo.
echo For detailed documentation, see SETUP_INSTRUCTIONS.md
echo.
pause
