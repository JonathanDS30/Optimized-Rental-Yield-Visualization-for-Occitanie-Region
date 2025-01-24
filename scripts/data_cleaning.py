import os
import subprocess
import sys

# Check and install pandas if necessary
try:
    import pandas as pd
except ImportError:
    print("The 'pandas' module is not installed. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas"])
    import pandas as pd

# Define the base directory (relative to the script location)
base_dir = os.path.dirname(__file__)

# Define input and output folders (relative paths)
input_folder = os.path.join(base_dir,"..", "data", "raw")
output_folder = os.path.join(base_dir,"..", "data", "processed")

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Output files (in the 'processed' folder)
output_file_sales = os.path.join(output_folder, "cleaned_sales_data.csv")
output_file_rentals = os.path.join(output_folder, "cleaned_rentals_data.csv")

# List of columns to keep for TXT files
useful_columns_txt = [
    "Date mutation", "Nature mutation", "Valeur fonciere", "Code postal",
    "Commune", "Section", "Code departement", "Code commune", "No plan",
    "Type local", "Surface reelle bati", "Nombre pieces principales", "Surface terrain"
]

# List of department codes for the Occitanie region
occitanie_department_codes = ["09", "11", "12", "30", "31", "32", "34", "46", "48", "65", "66", "81", "82"]

# List of columns to keep for CSV files
useful_columns_csv = [
    "Data_year", "agglomeration", "Type_habitat", "nombre_pieces_homogene",
    "loyer_mensuel_1_decile", "loyer_mensuel_1_quartile", "loyer_mensuel_median",
    "loyer_mensuel_3_quartile", "loyer_mensuel_9_decile", "moyenne_loyer_mensuel",
    "surface_moyenne", "nombre_logements"
]

# Target agglomerations for CSV files
target_agglomerations = [
    "Agglomération d'Arles", "Agglomération de Montpellier", "Agglomération de Nîmes",
    "Agglomération de Sète", "Agglomération de Toulouse"
]

def process_txt_files(input_folder, output_file, useful_columns, department_codes):
    """
    Processes all TXT files in a folder, applies cleaning and filtering,
    and saves the merged result to a CSV file.
    """
    filtered_dataframes = []

    for file in os.listdir(input_folder):
        if file.endswith(".txt"):
            file_path = os.path.join(input_folder, file)
            print(f"Processing TXT file: {file_path}")
            
            df = pd.read_csv(file_path, delimiter="|", low_memory=False)
            existing_columns = [col for col in useful_columns if col in df.columns]
            filtered_df = df[existing_columns]

            # Remove rows with missing "Surface reelle bati"
            filtered_df = filtered_df.dropna(subset=["Surface reelle bati"])

            # Filter by departments in the Occitanie region
            filtered_df = filtered_df[filtered_df["Code departement"].astype(str).isin(department_codes)]

            # Remove rows with unwanted "Type local" values
            filtered_df = filtered_df[~filtered_df["Type local"].isin(["Dépendance", "Local industriel. commercial ou assimilé"])]

            # Convert numeric columns
            numeric_columns = ["Code postal", "Surface reelle bati", "Nombre pieces principales", "Surface terrain"]
            for col in numeric_columns:
                filtered_df[col] = pd.to_numeric(filtered_df[col], errors="coerce").fillna(0).astype(int)

            filtered_dataframes.append(filtered_df)

    # Merge all DataFrames and save to CSV
    merged_df = pd.concat(filtered_dataframes, ignore_index=True)
    merged_df.to_csv(output_file, index=False, sep=";")
    print(f"Cleaned TXT data saved to: {output_file}")

def clean_rental_data(df, useful_columns, target_agglomerations):
    """
    Cleans a DataFrame containing rental data.
    - Keeps only useful columns.
    - Removes rows with empty values in key columns.
    - Extracts the first number from "nombre_pieces_homogene".
    - Filters rows based on specific agglomerations.
    - Converts all numeric columns to integers.
    """
    df = df[useful_columns]
    df = df.dropna(subset=useful_columns)

    # Extract the first number from "nombre_pieces_homogene"
    df["nombre_pieces_homogene"] = df["nombre_pieces_homogene"].str.extract(r"(\d+)").astype(float).fillna(0).astype(int)

    # Filter rows based on specific agglomerations
    df = df[df["agglomeration"].isin(target_agglomerations)]

    # Convert numeric columns to integers
    numeric_columns = [
        "Data_year", "nombre_pieces_homogene", "loyer_mensuel_1_decile", "loyer_mensuel_1_quartile",
        "loyer_mensuel_median", "loyer_mensuel_3_quartile", "loyer_mensuel_9_decile",
        "moyenne_loyer_mensuel", "surface_moyenne", "nombre_logements"
    ]
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

    return df

def process_csv_files(input_folder, output_file, useful_columns, target_agglomerations):
    """
    Processes all CSV files in a folder, applies the cleaning function,
    and saves the results to a single CSV file.
    """
    cleaned_dataframes = []

    for file in os.listdir(input_folder):
        if file.endswith(".csv"):
            file_path = os.path.join(input_folder, file)
            print(f"Processing CSV file: {file_path}")
            
            df = pd.read_csv(file_path, delimiter=";", encoding="ISO-8859-1")
            cleaned_df = clean_rental_data(df, useful_columns, target_agglomerations)
            cleaned_dataframes.append(cleaned_df)

    # Merge all cleaned DataFrames and save to CSV
    merged_df = pd.concat(cleaned_dataframes, ignore_index=True)
    merged_df.to_csv(output_file, index=False, sep=";")
    print(f"Cleaned CSV data saved to: {output_file}")

# Process TXT files
process_txt_files(input_folder, output_file_sales, useful_columns_txt, occitanie_department_codes)

# Process CSV files
process_csv_files(input_folder, output_file_rentals, useful_columns_csv, target_agglomerations)
