@echo off
start /b cmd /c "streamlit run main.py --server.port 8502"
start /b cmd /c "streamlit run authtest.py --server.port 8501"

tasklist /FI "IMAGENAME eq cmd.exe" /FI "WINDOWTITLE eq authtest.py" 2>NUL | find /I /N "authtest.py">NUL
if "%ERRORLEVEL%"=="0" (
    for /f "tokens=2 delims= " %%a in ('tasklist /FI "IMAGENAME eq cmd.exe" /FI "WINDOWTITLE eq authtest.py" /FO LIST ^| find /I "PID:"') do set "pid=%%a"
    start "" /B taskkill /F /PID %pid%
)
