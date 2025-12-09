@echo off
echo ============================================
echo   BrowserStack - View Your iOS App
echo ============================================
echo.
echo Choose an option:
echo.
echo 1. View Test Dashboard (see recorded tests)
echo 2. Open App Live (manually test your app)
echo 3. Open Inspector (find element IDs)
echo 4. View Current Build Results
echo.
echo ============================================
echo.

set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    echo Opening BrowserStack App Automate Dashboard...
    start https://app-automate.browserstack.com/dashboard
)

if "%choice%"=="2" (
    echo Opening BrowserStack App Live for manual testing...
    start https://app-live.browserstack.com/
    echo.
    echo Steps to use App Live:
    echo 1. Select iOS device (e.g., iPhone 14 Pro)
    echo 2. Click "Upload App" or enter: bs://8ec7f6fdc019e0587d510e743584f2b376c652c4
    echo 3. Click "Start" to launch interactive session
    echo 4. You can now see and control your iOS app in the browser!
)

if "%choice%"=="3" (
    echo Opening BrowserStack App Live (Inspector)...
    start https://app-live.browserstack.com/
    echo.
    echo Steps to use Inspector:
    echo 1. Start an App Live session (see option 2)
    echo 2. Click the Inspector icon (magnifying glass)
    echo 3. Click any element to see its ID, XPath, etc.
)

if "%choice%"=="4" (
    echo Opening your latest build results...
    start https://automation.browserstack.com/builds/znx18m71dnc32zx14xgejww4i10le8domx4r9lp9
)

echo.
pause

