@echo off
REM Clear Windows Icon Cache and Verify EXE Icon

echo ============================================================
echo  Clear Icon Cache and Verify EXE Icon
echo ============================================================
echo.

echo [1/3] Checking if icon is embedded in EXE...
python scripts\verify_icon.py
echo.

echo [2/3] Clearing Windows icon cache...
echo.

REM Stop Windows Explorer
taskkill /f /im explorer.exe >nul 2>&1

REM Delete icon cache files
echo Deleting icon cache...
del /f /q "%localappdata%\IconCache.db" >nul 2>&1
del /f /q "%localappdata%\Microsoft\Windows\Explorer\iconcache*.db" >nul 2>&1
del /f /q "%localappdata%\Microsoft\Windows\Explorer\thumbcache*.db" >nul 2>&1

echo Icon cache cleared.
echo.

REM Restart Windows Explorer
echo Restarting Windows Explorer...
start explorer.exe

timeout /t 2 >nul

echo.
echo [3/3] Done!
echo.
echo Please check the EXE icon in Windows Explorer now.
echo The icon should be visible after cache is cleared.
echo.
echo If still not showing:
echo 1. Try copying the EXE to a different folder
echo 2. Restart your computer
echo 3. Test on another computer
echo.
pause
