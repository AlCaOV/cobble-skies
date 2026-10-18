@echo off
rem One-time migration of an OLD Cobble Skies profile (1.5.x / 1.6.x) to the auto-updating version.
rem Old files are NOT deleted, only moved to *_old folders.
cd /d "%~dp0"
if not exist packwiz-installer-bootstrap.jar (
  echo packwiz-installer-bootstrap.jar not found next to this script. Unzip the whole archive into the profile folder.
  pause & exit /b 1
)
echo Moving old mods and datapacks aside...
if exist mods move /y mods mods_old >nul
mkdir mods
if exist config\openloader\packs move /y config\openloader\packs config\openloader\packs_old >nul
mkdir config\openloader\packs
echo Downloading the current Cobble Skies version (this takes a few minutes, ~600 MB)...
call update.bat
echo.
echo ---- update.log ----
type update.log
echo.
echo Done. Now set the Pre-launch hook in Modrinth App:  cmd /c update.bat
pause
