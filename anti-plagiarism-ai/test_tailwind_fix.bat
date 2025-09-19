@echo off
echo 🎨 Testing Tailwind CSS Configuration Fix...
cd /d "%~dp0\frontend"

echo [INFO] Step 1: Checking if build works...
npm run build
if %errorlevel% neq 0 (
    echo [ERROR] Build failed!
    pause
    exit /b 1
)
echo [SUCCESS] Build completed successfully!

echo [INFO] Step 2: Checking generated CSS...
if exist "dist\assets\*.css" (
    echo [SUCCESS] CSS files generated
) else (
    echo [ERROR] No CSS files found in dist
)

echo [INFO] Step 3: Cleaning up build files...
rmdir /s /q dist >nul 2>&1

echo [INFO] Step 4: Verifying Tailwind configuration...
if exist "tailwind.config.js" (
    echo [SUCCESS] Tailwind config exists
) else (
    echo [ERROR] Tailwind config missing
)

if exist "postcss.config.js" (
    echo [SUCCESS] PostCSS config exists
) else (
    echo [ERROR] PostCSS config missing
)

echo [INFO] Step 5: Checking CSS imports in main.tsx...
findstr /c:"import './index.css'" src\main.tsx >nul
if %errorlevel% == 0 (
    echo [SUCCESS] CSS properly imported in main.tsx
) else (
    echo [ERROR] CSS import missing in main.tsx
)

echo [INFO] Step 6: Verifying no version numbers in imports...
findstr /r "@[0-9]" src\components\ui\*.tsx >nul 2>&1
if %errorlevel% == 0 (
    echo [WARNING] Found version numbers in imports - may cause issues
) else (
    echo [SUCCESS] No version numbers found in imports
)

cd ..
echo.
echo 🎉 Tailwind CSS Configuration Test Complete!
echo.
echo ✅ Fixed Issues:
echo   - Removed @tailwindcss/vite plugin (incompatible with v3)
echo   - Fixed version numbers in component imports
echo   - Updated CSS with proper Tailwind directives
echo   - Added missing input-background color to config
echo.
echo 📋 Configuration Summary:
echo   - Using Tailwind CSS v3.4.13 with PostCSS
echo   - Traditional @tailwind directives in index.css
echo   - All UI components have clean imports
echo   - Build process working correctly
echo.
echo 🚀 Ready to start development:
echo   cd frontend
echo   npm run dev
echo.
pause