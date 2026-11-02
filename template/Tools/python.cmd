@echo off
rem Runs a Python script with the engine's own interpreter, in isolated mode. Commands call it by this fixed path
rem because Claude Code can't match a permission rule to a program named by a variable, such as $env:UE_ENGINE_DIR.
rem The engine is UE_ENGINE_DIR when it is set, else the one the .uproject's EngineAssociation names, looked up in the
rem registry as Unreal's own tools do: a registered source build, or a launcher install.
setlocal
if not defined UE_ENGINE_DIR call :find_engine
if not defined UE_ENGINE_DIR (
  echo No engine found: register it, or set UE_ENGINE_DIR in .claude/settings.local.json. 1>&2
  exit /b 2
)
"%UE_ENGINE_DIR%\Engine\Binaries\ThirdParty\Python3\Win64\python.exe" -I %*
exit /b %errorlevel%

:find_engine
rem The .uproject at the repository root, else in one folder below it.
set "uproject="
for %%f in ("%~dp0..\*.uproject") do set "uproject=%%~ff"
if not defined uproject for /d %%d in ("%~dp0..\*") do for %%f in ("%%~d\*.uproject") do set "uproject=%%~ff"
if not defined uproject exit /b
set "assoc="
for /f "tokens=2 delims=:" %%a in ('findstr /c:"EngineAssociation" "%uproject%"') do set "assoc=%%a"
if not defined assoc exit /b
set "assoc=%assoc:"=%"
set "assoc=%assoc:,=%"
set "assoc=%assoc: =%"
for /f "tokens=2,*" %%a in ('reg query "HKCU\Software\Epic Games\Unreal Engine\Builds" /v "%assoc%" 2^>nul ^| findstr /c:"REG_SZ"') do set "UE_ENGINE_DIR=%%b"
if defined UE_ENGINE_DIR exit /b
for /f "tokens=2,*" %%a in ('reg query "HKLM\SOFTWARE\EpicGames\Unreal Engine\%assoc%" /v InstalledDirectory 2^>nul ^| findstr /c:"REG_SZ"') do set "UE_ENGINE_DIR=%%b"
exit /b
