@echo off
rem Run open_mobiles.py using its absolute path
where py >nul 2>&1
if %ERRORLEVEL%==0 (
    py -3 "C:\__tz_pers\CCS\Misca_Mouse\open_mobiles.py"
) else (
    python "C:\__tz_pers\CCS\Misca_Mouse\open_mobiles.py"
)
pause
