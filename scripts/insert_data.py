import mysql.connector
import pandas as pd

# Configuration de la connexion MySQL
db_config = {
    'host': 'localhost',       # Adresse de votre conteneur MySQL
    'user': 'root',            # Nom d'utilisateur MySQL
    'password': 'root_password', # Mot de passe MySQL
    'database': 'occitanie_yield_db' # Nom de la base de données
}

# Charger les données depuis un fichier CSV
data_file = '../data/processed/prixm2_loyer_rendement_communes.csv'  # Chemin vers votre fichier CSV

# Spécifiez les colonnes à lire comme chaînes (pour éviter la suppression des zéros initiaux)
data = pd.read_csv(
    data_file,
    sep=';',
    encoding='utf-8',
    dtype={'INSEE_COM': str, 'INSEE_DEP': str}  # Traite ces colonnes comme chaînes
)

# Connexion à la base de données
try:
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Préparer la requête d'insertion
    insert_query = """
    INSERT INTO communes_data (
        INSEE_COM, INSEE_DEP, NOM_COM_M, POPULATION,
        PrixMoyen_M2_2223, Prixm2Moyen_2022, Prixm2Moyen_2023,
        loyer_apparts, loyer_maisons, Rendement_locatif_apparts, Rendement_locatif_maisons
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    # Parcourir les données et insérer dans la table
    for index, row in data.iterrows():
        cursor.execute(insert_query, (
            row['INSEE_COM'],
            row['INSEE_DEP'],
            row['NOM_COM_M'],
            row['POPULATION'],
            row['PrixMoyen_M2_2223'],
            row['Prixm2Moyen_2022'],
            row['Prixm2Moyen_2023'],
            row['loyer_apparts'],
            row['loyer_maisons'],
            row['Rendement_locatif_apparts'],
            row['Rendement_locatif_maisons']
        ))

    # Valider les modifications
    connection.commit()
    print(f"Les données ont été insérées avec succès dans la table communes_data !")

except mysql.connector.Error as err:
    print(f"Erreur : {err}")
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("Connexion MySQL fermée.")
