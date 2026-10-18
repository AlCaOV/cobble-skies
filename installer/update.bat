@echo off
rem Cobble Skies auto-updater (packwiz). Runs as a Modrinth App pre-launch hook.
cd /d "%~dp0"
set "PACK_URL=https://raw.githubusercontent.com/AlCaOV/cobble-skies/main/pack.toml"
set "JAVA="
where java >nul 2>&1 && set "JAVA=java"
if not defined JAVA for /d %%D in ("%APPDATA%\ModrinthApp\meta\java_versions\*jre21*") do set "JAVA=%%D\bin\java.exe"
if not defined JAVA for /d %%D in ("%APPDATA%\ModrinthApp\meta\java_versions\zulu21*") do set "JAVA=%%D\bin\java.exe"
if not defined JAVA for /d %%D in ("%APPDATA%\ModrinthApp\meta\java_versions\*") do set "JAVA=%%D\bin\java.exe"
if not defined JAVA (
  echo [Cobble Skies] Java not found, skipping update.>> update.log
  exit /b 0
)
echo [%date% %time%] updating from %PACK_URL% using %JAVA%> update.log
"%JAVA%" -jar packwiz-installer-bootstrap.jar -g -s client "%PACK_URL%" >> update.log 2>&1
echo [%date% %time%] done (exit %errorlevel%)>> update.log
exit /b 0
