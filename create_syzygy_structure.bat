@echo off
title Create SYZYGY Folder Structure
echo.
echo === Creating core SYZYGY directories ===
echo.

set "BASE=D:\SYZYGY"

mkdir "%BASE%"
mkdir "%BASE%\INGEST"
mkdir "%BASE%\INGEST\RAW"
mkdir "%BASE%\LOGS"
mkdir "%BASE%\OUTPUT"
mkdir "%BASE%\SCRIPTS"
mkdir "%BASE%\TEMP"
mkdir "%BASE%\BACKUP"

echo.
echo === Folder structure created successfully under D:\SYZYGY ===
echo Press CTRL + C to stop or close this window when ready.
pause >nul
