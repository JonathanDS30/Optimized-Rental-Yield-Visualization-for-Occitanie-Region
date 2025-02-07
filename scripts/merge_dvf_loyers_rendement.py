import pandas as pd
import os

# S'assurer que le répertoire de travail est correct
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
print("Répertoire de travail ajusté :", os.getcwd())


# Vérifier le répertoire de travail
print("Répertoire de travail AVANT :", os.getcwd())

# Définir les chemins relatifs
base_path = "../data/raw/"

def check_file_exists(file_path):
    """Vérifie si le fichier existe et liste les fichiers disponibles en cas d'erreur."""
    if not os.path.exists(file_path):
        print(f"⚠️  Le fichier {file_path} est introuvable !")
        print("Dossier actuel :", os.getcwd())
        print("Fichiers disponibles dans data/raw/ :", os.listdir(base_path))
    else:
        print(f"✅ Le fichier {file_path} est bien présent.")

# Vérifier les fichiers avant chargement
files = {
    "DVF 2022": os.path.join(base_path, "dvf2022.csv"),
    "DVF 2023": os.path.join(base_path, "dvf2023.csv"),
    "Loyers Appartements": os.path.join(base_path, "Indicateurs_Appartement_2022.csv"),
    "Loyers Maisons": os.path.join(base_path, "Indicateurs_Maison_2022.csv"),
    "Données Communes": os.path.join(base_path, "donnees_communes.csv")
}

for name, path in files.items():
    check_file_exists(path)

# Charger les fichiers
try:
    dvf_2022 = pd.read_csv(files["DVF 2022"], sep=",", encoding="ISO-8859-1")
    dvf_2023 = pd.read_csv(files["DVF 2023"], sep=",", encoding="ISO-8859-1")
    loyers_appartements = pd.read_csv(files["Loyers Appartements"], sep=";", encoding="ISO-8859-1")
    loyers_maisons = pd.read_csv(files["Loyers Maisons"], sep=";", encoding="ISO-8859-1")
    donnees_communes = pd.read_csv(files["Données Communes"], sep=";", encoding="ISO-8859-1")
except FileNotFoundError as e:
    print(f"❌ Erreur : {e}")
    exit()

# Filtrer uniquement les communes d'Occitanie
occitanie_department_codes = ["09", "11", "12", "30", "31", "32", "34", "46", "48", "65", "66", "81", "82"]
dvf_2022 = dvf_2022[dvf_2022['INSEE_COM'].astype(str).str[:2].isin(occitanie_department_codes)]
dvf_2023 = dvf_2023[dvf_2023['INSEE_COM'].astype(str).str[:2].isin(occitanie_department_codes)]

# Fusionner les deux fichiers et calculer la moyenne pondérée du prix au m2
dvf_combined = pd.merge(dvf_2022, dvf_2023, on='INSEE_COM', suffixes=('_2022', '_2023'))
dvf_combined['PrixMoyen_M2_2223'] = (
    (dvf_combined['Nb_mutations_2022'] * dvf_combined['Prixm2Moyen_2022']) + 
    (dvf_combined['Nb_mutations_2023'] * dvf_combined['Prixm2Moyen_2023'])
) / (dvf_combined['Nb_mutations_2022'] + dvf_combined['Nb_mutations_2023'])

# Filtrer les loyers des communes d'Occitanie
loyers_appartements = loyers_appartements[loyers_appartements['INSEE_C'].astype(str).str[:2].isin(occitanie_department_codes)]
loyers_maisons = loyers_maisons[loyers_maisons['INSEE_C'].astype(str).str[:2].isin(occitanie_department_codes)]

# Renommer et fusionner les données des loyers
loyers_appartements.rename(columns={'loypredm2': 'loyer_apparts', 'R2_adj': 'R2appart'}, inplace=True)
loyers_maisons.rename(columns={'loypredm2': 'loyer_maisons', 'R2_adj': 'R2maison'}, inplace=True)
final_df = pd.merge(dvf_combined, loyers_appartements, left_on='INSEE_COM', right_on='INSEE_C', how='left')
final_df = pd.merge(final_df, loyers_maisons, left_on='INSEE_COM', right_on='INSEE_C', how='left')

# Ajouter les données communes avec DEP, Commune et PTOT
donnees_communes = donnees_communes.rename(columns={'COM': 'INSEE_COM', 'DEP': 'INSEE_DEP', 'Commune': 'NOM_COM_M', 'PTOT': 'POPULATION'})
donnees_communes = donnees_communes[['INSEE_COM', 'INSEE_DEP', 'NOM_COM_M', 'POPULATION']]
donnees_communes['NOM_COM_M'] = donnees_communes['NOM_COM_M'].apply(lambda x: x.encode('ISO-8859-1').decode('utf-8') if isinstance(x, str) else x)
final_df = pd.merge(final_df, donnees_communes, on='INSEE_COM', how='left')

# Convertir les valeurs en float si nécessaire
final_df['PrixMoyen_M2_2223'] = final_df['PrixMoyen_M2_2223'].astype(float)
final_df['loyer_apparts'] = final_df['loyer_apparts'].astype(str).str.replace(',', '.').astype(float)
final_df['loyer_maisons'] = final_df['loyer_maisons'].astype(str).str.replace(',', '.').astype(float)

# Calcul du rendement locatif
final_df['Loyer_annuel_apparts'] = final_df['loyer_apparts'] * 12
final_df['Loyer_annuel_maisons'] = final_df['loyer_maisons'] * 12
final_df['Rendement_locatif_apparts'] = (final_df['Loyer_annuel_apparts'] * 100) / final_df['PrixMoyen_M2_2223']
final_df['Rendement_locatif_maisons'] = (final_df['Loyer_annuel_maisons'] * 100) / final_df['PrixMoyen_M2_2223']

# Arrondir les colonnes numériques à deux chiffres après la virgule
cols_to_round = ['PrixMoyen_M2_2223', 'Prixm2Moyen_2022', 'Prixm2Moyen_2023', 'loyer_apparts', 'loyer_maisons', 'Rendement_locatif_apparts', 'Rendement_locatif_maisons']
final_df[cols_to_round] = final_df[cols_to_round].round(2)

# Sélectionner les colonnes finales
columns_to_keep = [
    'INSEE_COM', 'INSEE_DEP', 'NOM_COM_M', 'POPULATION', 'PrixMoyen_M2_2223', 'Prixm2Moyen_2022', 'Prixm2Moyen_2023',
    'loyer_apparts', 'loyer_maisons', 'Rendement_locatif_apparts', 'Rendement_locatif_maisons'
]
final_df = final_df[columns_to_keep]

# Exporter le fichier final
output_path = "../data/processed/prixm2_loyer_rendement_communes.csv"
final_df.to_csv(output_path, index=False, sep=';', encoding='utf-8')

print(f"✅ Fichier généré avec succès : {output_path}")
