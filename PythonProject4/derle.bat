@echo off
REM Uygulamayi tek dosyalik bir .exe haline getirir -> dist\Banka Sistemi.exe
cd /d "%~dp0"

py -3 -m PyInstaller --noconfirm --onefile --windowed --clean ^
  --name "Banka Sistemi" ^
  --icon "%~dp0Main\banka.ico" ^
  --add-data "%~dp0Main\banka.ico;." ^
  --distpath "%~dp0dist" ^
  --workpath "%~dp0build" ^
  --specpath "%~dp0" ^
  "%~dp0Main\main.py"

echo.
echo Derleme bitti: dist\Banka Sistemi.exe
echo Mevcut kayitlari tasimak icin Main\banka.db dosyasini dist klasorune kopyalayin.
pause
