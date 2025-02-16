import os
import pandas as pd
import mysql.connector

# Configuration générale
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root_password',
    'database': 'occitanie_yield_db'
}
base_path = "../data/raw/"
output_path = "../data/processed/prixm2_loyer_rendement_communes.csv"
chomage_file = '../data/raw/ECRT2023-F12.xlsx'
occitanie_departments = {
    "09": "Ariège", "11": "Aude", "12": "Aveyron", "30": "Gard",
    "31": "Haute-Garonne", "32": "Gers", "34": "Hérault", "46": "Lot",
    "48": "Lozère", "65": "Hautes-Pyrénées", "66": "Pyrénées-Orientales",
    "81": "Tarn", "82": "Tarn-et-Garonne"
}
occitanie_department_codes = list(occitanie_departments.keys())

# Changer de répertoire
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

def check_file_exists(file_path):
    if not os.path.exists(file_path):
        print(f"⚠️  Fichier introuvable : {file_path}")
        print("Fichiers disponibles :", os.listdir(os.path.dirname(file_path)))
        exit()

# Vérification des fichiers
files = {
    "DVF 2022": os.path.join(base_path, "dvf2022.csv"),
    "DVF 2023": os.path.join(base_path, "dvf2023.csv"),
    "Loyers Appartements": os.path.join(base_path, "Indicateurs_Appartement_2022.csv"),
    "Loyers Maisons": os.path.join(base_path, "Indicateurs_Maison_2022.csv"),
    "Données Communes": os.path.join(base_path, "donnees_communes.csv")
}

for path in files.values():
    check_file_exists(path)

# Chargement des données
dvf_2022 = pd.read_csv(files["DVF 2022"], sep=",", encoding="ISO-8859-1")
dvf_2023 = pd.read_csv(files["DVF 2023"], sep=",", encoding="ISO-8859-1")
loyers_appartements = pd.read_csv(files["Loyers Appartements"], sep=";", encoding="ISO-8859-1")
loyers_maisons = pd.read_csv(files["Loyers Maisons"], sep=";", encoding="ISO-8859-1")
donnees_communes = pd.read_csv(files["Données Communes"], sep=";", encoding="ISO-8859-1")

# Traitement des données DVF
dvf_2022 = dvf_2022[dvf_2022['INSEE_COM'].astype(str).str[:2].isin(occitanie_department_codes)]
dvf_2023 = dvf_2023[dvf_2023['INSEE_COM'].astype(str).str[:2].isin(occitanie_department_codes)]
dvf_combined = pd.merge(dvf_2022, dvf_2023, on='INSEE_COM', suffixes=('_2022', '_2023'))
dvf_combined['PrixMoyen_M2_2223'] = (
    (dvf_combined['Nb_mutations_2022'] * dvf_combined['Prixm2Moyen_2022']) +
    (dvf_combined['Nb_mutations_2023'] * dvf_combined['Prixm2Moyen_2023'])
) / (dvf_combined['Nb_mutations_2022'] + dvf_combined['Nb_mutations_2023'])

# Traitement des loyers
loyers_appartements.rename(columns={'loypredm2': 'loyer_apparts', 'R2_adj': 'R2appart'}, inplace=True)
loyers_maisons.rename(columns={'loypredm2': 'loyer_maisons', 'R2_adj': 'R2maison'}, inplace=True)
final_df = pd.merge(dvf_combined, loyers_appartements, left_on='INSEE_COM', right_on='INSEE_C', how='left')
final_df = pd.merge(final_df, loyers_maisons, left_on='INSEE_COM', right_on='INSEE_C', how='left')

# Intégration des données communes
donnees_communes.rename(columns={'COM': 'INSEE_COM', 'DEP': 'INSEE_DEP', 'Commune': 'NOM_COM_M', 'PTOT': 'POPULATION'}, inplace=True)
donnees_communes['NOM_COM_M'] = donnees_communes['NOM_COM_M'].apply(lambda x: x.encode('ISO-8859-1').decode('utf-8') if isinstance(x, str) else x)
final_df = pd.merge(final_df, donnees_communes[['INSEE_COM', 'INSEE_DEP', 'NOM_COM_M', 'POPULATION']], on='INSEE_COM', how='left')

# Calcul des indicateurs
final_df['PrixMoyen_M2_2223'] = final_df['PrixMoyen_M2_2223'].astype(float)
final_df['loyer_apparts'] = final_df['loyer_apparts'].str.replace(',', '.').astype(float)
final_df['loyer_maisons'] = final_df['loyer_maisons'].str.replace(',', '.').astype(float)
final_df['Loyer_annuel_apparts'] = final_df['loyer_apparts'] * 12
final_df['Loyer_annuel_maisons'] = final_df['loyer_maisons'] * 12
final_df['Rendement_locatif_apparts'] = (final_df['Loyer_annuel_apparts'] * 100) / final_df['PrixMoyen_M2_2223']
final_df['Rendement_locatif_maisons'] = (final_df['Loyer_annuel_maisons'] * 100) / final_df['PrixMoyen_M2_2223']
cols_to_round = ['PrixMoyen_M2_2223', 'Prixm2Moyen_2022', 'Prixm2Moyen_2023', 'loyer_apparts', 'loyer_maisons', 'Rendement_locatif_apparts', 'Rendement_locatif_maisons']
final_df[cols_to_round] = final_df[cols_to_round].round(2)

# Sélection explicite des colonnes finales
columns_to_keep = [
    'INSEE_COM', 'INSEE_DEP', 'NOM_COM_M', 'POPULATION', 'PrixMoyen_M2_2223',
    'Prixm2Moyen_2022', 'Prixm2Moyen_2023', 'loyer_apparts', 'loyer_maisons',
    'Rendement_locatif_apparts', 'Rendement_locatif_maisons'
]
final_df = final_df[columns_to_keep]

# Exportation en CSV
final_df.to_csv(output_path, index=False, sep=';', encoding='utf-8')

print(f"✅ Fichier CSV généré avec succès : {output_path}")

# Chargement des données de chômage
chomage_excel = pd.read_excel(chomage_file, sheet_name="Figure 2b", header=None)
header_row = chomage_excel[chomage_excel.isin(["Département"]).any(axis=1)].index[0]
chomage_data = chomage_excel.iloc[header_row + 1:header_row + 102, [0, 1]]
chomage_data.columns = ["NOM_DEP", "Taux_Chomage_2022"]
chomage_data["Taux_Chomage_2022"] = pd.to_numeric(chomage_data["Taux_Chomage_2022"], errors='coerce')
occ_dep_data = [
    (
        dep_code,
        dep_name,
        float(chomage_data.loc[chomage_data["NOM_DEP"] == dep_name, "Taux_Chomage_2022"].values[0])
    )
    for dep_code, dep_name in occitanie_departments.items()
    if dep_name in chomage_data["NOM_DEP"].values
]

# Insertion dans MySQL
try:
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    insert_departments_query = """
    INSERT INTO departements_data (INSEE_DEP, NOM_DEP, Taux_Chomage_2022)
    VALUES (%s, %s, %s)
    """
    for dep in occ_dep_data:
        cursor.execute(insert_departments_query, dep)

    insert_communes_query = """
    INSERT INTO communes_data (
        INSEE_COM, INSEE_DEP, NOM_COM_M, POPULATION,
        PrixMoyen_M2_2223, Prixm2Moyen_2022, Prixm2Moyen_2023,
        loyer_apparts, loyer_maisons, Rendement_locatif_apparts, Rendement_locatif_maisons
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    for _, row in final_df.iterrows():
        cursor.execute(insert_communes_query, (
            row['INSEE_COM'], row['INSEE_DEP'], row['NOM_COM_M'], row['POPULATION'],
            row['PrixMoyen_M2_2223'], row['Prixm2Moyen_2022'], row['Prixm2Moyen_2023'],
            row['loyer_apparts'], row['loyer_maisons'],
            row['Rendement_locatif_apparts'], row['Rendement_locatif_maisons']
        ))

    connection.commit()
    print("Insertion dans MySQL réussie.")
except mysql.connector.Error as err:
    print(f"Erreur MySQL : {err}")
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
