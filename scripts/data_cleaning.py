import os
import subprocess
import sys

# The .txt files used to generate the merged_occitanie.zip come from the following link:
# https://www.data.gouv.fr/fr/datasets/demandes-de-valeurs-foncieres/
# It includes data from early 2022 to mid-2024, but it is possible to extend the temporal and geographical coverage.

# Check and install pandas if necessary
try:
    import pandas as pd
except ImportError:
    print("The 'pandas' module is not installed. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas"])
    import pandas as pd

# Folder containing the TXT files
txt_folder = "C:/Users/leon/OneDrive/Documents/GitHub/Optimized-Rental-Yield-Visualization-for-Occitanie-Region/data/raw"
# Output file for merged data
output_file = "C:/Users/leon/OneDrive/Documents/GitHub/Optimized-Rental-Yield-Visualization-for-Occitanie-Region/data/processed/merged_occitanie.csv"

# List of columns to keep
useful_columns = [
    "Date mutation",
    "Nature mutation",
    "Valeur fonciere",
    "Code postal",
    "Commune",
    "Section",
    "Code departement",
    "Code commune",
    "No plan",
    "Type local",  # Already included in the list
    "Surface reelle bati",
    "Nombre pieces principales",
    "Surface terrain"
]

# List of department codes for the Occitanie region
occitanie_department_codes = ["09", "11", "12", "30", "31", "32", "34", "46", "48", "65", "66", "81", "82"]

# List to store filtered DataFrames
filtered_dataframes = []

# Iterate through TXT files in the folder
for file in os.listdir(txt_folder):
    if file.endswith(".txt"):
        file_path = os.path.join(txt_folder, file)
        print(f"Processing file: {file_path}")
        
        # Read the TXT file
        df = pd.read_csv(file_path, delimiter="|", low_memory=False)  # Check the delimiter if necessary
        
        # Check if the necessary columns are present
        existing_columns = [col for col in useful_columns if col in df.columns]
        
        # Filter the necessary columns
        filtered_df = df[existing_columns]
        
        # Remove rows where "Surface reelle bati" is empty
        filtered_df = filtered_df.dropna(subset=["Surface reelle bati"])
        
        # Filter by departments in the Occitanie region
        occitanie_df = filtered_df[filtered_df["Code departement"].astype(str).isin(occitanie_department_codes)]

        # Remove rows where "Type local" is "Dépendance"
        occitanie_df = occitanie_df[occitanie_df["Type local"] != "Dépendance"]

        # Remove rows where "Type local" is "Dépendance"
        occitanie_df = occitanie_df[occitanie_df["Type local"] != "Local industriel. commercial ou assimilé"]

        # Convert "Code postal" to integer (handle missing values)
        occitanie_df["Code postal"] = pd.to_numeric(occitanie_df["Code postal"], errors="coerce").fillna(0).astype(int)

        # Convert "Surface reelle bati" to integer (handle missing values)
        occitanie_df["Surface reelle bati"] = pd.to_numeric(occitanie_df["Surface reelle bati"], errors="coerce").fillna(0).astype(int)

        # Convert "Nombre pieces principales" to integer (handle missing values)
        occitanie_df["Nombre pieces principales"] = pd.to_numeric(occitanie_df["Nombre pieces principales"], errors="coerce").fillna(0).astype(int)

        # Convert "Surface terrain" to integer (handle missing values)
        occitanie_df["Surface terrain"] = pd.to_numeric(occitanie_df["Surface terrain"], errors="coerce").fillna(0).astype(int)
        
        # Add to the list of filtered DataFrames
        filtered_dataframes.append(occitanie_df)

# Merge all DataFrames into one
merged_df = pd.concat(filtered_dataframes, ignore_index=True)

# Save the result to a CSV file
merged_df.to_csv(output_file, index=False, sep=";")

print(f"Merged and filtered file created successfully: {output_file}")