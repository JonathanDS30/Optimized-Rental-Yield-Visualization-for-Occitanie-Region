# Optimized Rental Yield Visualization for Occitanie Region

## Project Context
This project aims to help a real estate investor identify areas with high rental yield in the Occitanie region. It uses opendata (DVF, INSEE, etc.) to calculate rental yield and present the results in tables and charts using Jasper.

## Repository Structure
- **data/**: Contains raw and processed data.
- **jasper_project/**: Contains Jasper project files.
- **scripts/**: Python scripts for data cleaning and analysis.
- **docs/**: Documentation and final report.

## Installation and Usage
1. Clone the repository:
   ```bash
   git clone https://github.com/JonathanDS30/Optimized-Rental-Yield-Visualization-for-Occitanie-Region.git

2. go to the link : https://www.data.gouv.fr/fr/datasets/demandes-de-valeurs-foncieres/
3. Download 6 files : Valeurs foncieres 2019-2024
4. Put this files in the directory ./data/raw/
5. Open pyton file "./scripts/data_cleaning.py"
6. Change with your absolute path variables "txt_folder" and "output_file"
7. Run script data_cleaning.py 