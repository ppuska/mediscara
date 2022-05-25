@echo off

echo Converting the package to an executable with PyInstaller

pyinstaller -y .\main.spec
