@echo off
REM Define paths for downloads and raw data
set "destination=..\data\raw"

REM Change the current directory to the script's location
cd /d %~dp0

REM Download files
echo Downloading files...
curl -O https://www.observatoires-des-loyers.org/datagouv/2024/Base_OP_2024_Nationale.csv
curl -O https://www.observatoires-des-loyers.org/datagouv/2023/Base_OP_2023_Nationale.csv
curl -O https://www.observatoires-des-loyers.org/datagouv/2022/Base_OP_2022_Nationale.csv
curl -O https://www.observatoires-des-loyers.org/datagouv/2021/Base_OP_2021_Nationale.csv
curl -O https://www.observatoires-des-loyers.org/datagouv/2020/Base_OP_2020_Nationale.csv
curl -O https://static.data.gouv.fr/resources/demandes-de-valeurs-foncieres/20241008-071049/valeursfoncieres-2024-s1.txt.zip
curl -O https://static.data.gouv.fr/resources/demandes-de-valeurs-foncieres/20241008-071041/valeursfoncieres-2023.txt.zip
curl -O https://static.data.gouv.fr/resources/demandes-de-valeurs-foncieres/20241008-071010/valeursfoncieres-2022.txt.zip
curl -O https://static.data.gouv.fr/resources/demandes-de-valeurs-foncieres/20241008-070955/valeursfoncieres-2021.txt.zip
curl -O https://static.data.gouv.fr/resources/demandes-de-valeurs-foncieres/20241008-070941/valeursfoncieres-2020.txt.zip

REM Extract ZIP files
echo Extracting ZIP files...
for %%f in (*.zip) do (
    echo Extracting %%f...
    powershell -Command "Expand-Archive -Path '%%f' -DestinationPath '%destination%' -Force"
)

REM Move CSV files to the raw data folder
echo Moving CSV files...
move Base_OP_*.csv "%destination%"

REM Delete ZIP files after extraction
echo Deleting ZIP files...
del *.zip

REM End of script
echo All files are ready in %destination%.
pause
