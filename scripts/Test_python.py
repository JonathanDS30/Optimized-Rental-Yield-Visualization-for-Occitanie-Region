import pandas as pd
import os

# Vérifier le répertoire de travail
print("Répertoire de travail AVANT :", os.getcwd())

# Définir les chemins absolus
base_path = "D:/Thomas/Documents/GitHub/Optimized-Rental-Yield-Visualization-for-Occitanie-Region/data/raw/"

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

# Vérifier le répertoire de travail après chargement
print("Répertoire de travail APRÈS :", os.getcwd())

# Afficher les 10 premières lignes de chaque fichier chargé
print("\n📌 DVF 2022 - 10 premières lignes :")
print(dvf_2022.head(10))

print("\n📌 DVF 2023 - 10 premières lignes :")
print(dvf_2023.head(10))

print("\n📌 Loyers Appartements - 10 premières lignes :")
print(loyers_appartements.head(10))

print("\n📌 Loyers Maisons - 10 premières lignes :")
print(loyers_maisons.head(10))

print("\n📌 Données Communes - 10 premières lignes :")
print(donnees_communes.head(10))

print("✅ Tous les fichiers ont été chargés avec succès !")
