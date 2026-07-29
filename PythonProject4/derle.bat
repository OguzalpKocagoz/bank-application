@echo off
REM Uygulamayi dagitima hazir hale getirir:
REM   dist_klasor\Banka Sistemi\          -> calisan uygulama klasoru
REM   dist_klasor\Banka-Sistemi-Windows.zip -> GitHub Releases'e yuklenecek dosya
REM
REM --onedir kullaniliyor (--onefile degil): daha hizli aciliyor ve
REM antivirus yanlis alarmlari belirgin sekilde daha az oluyor.
cd /d "%~dp0"

py -3 -m PyInstaller --noconfirm --onedir --windowed --clean ^
  --name "Banka Sistemi" ^
  --icon "%~dp0Main\banka.ico" ^
  --add-data "%~dp0Main\banka.ico;." ^
  --distpath "%~dp0dist_klasor" ^
  --workpath "%~dp0build" ^
  --specpath "%~dp0build" ^
  "%~dp0Main\main.py"

if errorlevel 1 goto hata

REM Test calistirmalarindan kalan veritabanini paketleme:
REM indirenlerin bos bir veritabaniyla baslamasi gerekir.
if exist "%~dp0dist_klasor\Banka Sistemi\banka.db" del "%~dp0dist_klasor\Banka Sistemi\banka.db"

copy /y "%~dp0OKU.txt" "%~dp0dist_klasor\Banka Sistemi\OKU.txt" >nul 2>&1

powershell -NoProfile -Command "Compress-Archive -Path '%~dp0dist_klasor\Banka Sistemi' -DestinationPath '%~dp0dist_klasor\Banka-Sistemi-Windows.zip' -Force"

echo.
echo Bitti.
echo   Uygulama : dist_klasor\Banka Sistemi\Banka Sistemi.exe
echo   Dagitim  : dist_klasor\Banka-Sistemi-Windows.zip
echo.
goto son

:hata
echo.
echo Derleme basarisiz. PyInstaller kurulu mu?  pip install pyinstaller
echo.

:son
pause
