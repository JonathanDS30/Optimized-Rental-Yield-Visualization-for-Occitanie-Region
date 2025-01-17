import os
import subprocess
import sys
# Les fichiers .txt utilisées pour générer le fichier_fusionne_occitanie.zip viennent du lien suivant : 
# https://www.data.gouv.fr/fr/datasets/demandes-de-valeurs-foncieres/ et il regroupe les données depuis début 2020 jusqu'à mi-2024 mais il est tout à fait possible d'étendre la couverture temporelle et géographique 
# Vérification et installation de pandas si nécessaire
try:
    import pandas as pd
except ImportError:
    print("Le module 'pandas' n'est pas installé. Installation en cours...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas"])
    import pandas as pd

# Dossier contenant les fichiers TXT
dossier_txt = "path"
# Fichier de sortie pour les données fusionnées
fichier_sortie = "path/fichier_fusionne_occitanie.csv"

# Liste des colonnes à conserver
colonnes_utiles = [
    "Date mutation",
    "Nature mutation",
    "Valeur fonciere",
    "Code postal",
    "Commune",
    "Section",
    "Code departement",
    "Code commune",
    "No plan",
    "Type local",
    "Surface reelle bati",
    "Nombre pieces principales",
    "Surface terrain"
]

# Liste des codes départements de la région Occitanie
codes_departements_occitanie = ["09", "11", "12", "30", "31", "32", "34", "46", "48", "65", "66", "81", "82"]

# Liste pour stocker les DataFrames filtrés
fichiers_dataframes = []

# Parcours des fichiers TXT dans le dossier
for fichier in os.listdir(dossier_txt):
    if fichier.endswith(".txt"):
        chemin_fichier = os.path.join(dossier_txt, fichier)
        print(f"Traitement du fichier : {chemin_fichier}")
        
        # Lecture du fichier TXT
        df = pd.read_csv(chemin_fichier, delimiter="|", low_memory=False)  # Vérifiez le délimiteur si nécessaire
        
        # Vérifiez si les colonnes nécessaires sont présentes
        colonnes_existantes = [col for col in colonnes_utiles if col in df.columns]
        
        # Filtrage des colonnes nécessaires
        df_filtre = df[colonnes_existantes]
        
        # Suppression des lignes où "Surface reelle bati" est vide
        df_filtre = df_filtre.dropna(subset=["Surface reelle bati"])
        
        # Filtrage par les départements de la région Occitanie
        df_occitanie = df_filtre[df_filtre["Code departement"].astype(str).isin(codes_departements_occitanie)]

        # Supprimer les décimales dans "Code departement"
        df_filtre["Code departement"] = df_filtre["Code departement"].astype(str).str.split(".").str[0].astype(int)
        
        # Ajouter au tableau des DataFrames filtrés
        fichiers_dataframes.append(df_occitanie)

# Fusionner tous les DataFrames en un seul
df_fusionne = pd.concat(fichiers_dataframes, ignore_index=True)

# Sauvegarder le résultat dans un fichier CSV
df_fusionne.to_csv(fichier_sortie, index=False, sep=";")

print(f"Fichier fusionné et filtré créé avec succès : {fichier_sortie}")
