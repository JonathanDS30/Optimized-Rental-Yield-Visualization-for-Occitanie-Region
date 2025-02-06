import pandas as pd

# Définition des codes des départements de l'Occitanie
occitanie_department_codes = ["09", "11", "12", "30", "31", "32", "34", "46", "48", "65", "66", "81", "82"]

# Chargement des fichiers DVF (2022 et 2023)
dvf_2022 = pd.read_csv('../data/raw/dvf2022.csv', sep=',', encoding='ISO-8859-1')
dvf_2023 = pd.read_csv('../data/raw/dvf2023.csv', sep=',', encoding='ISO-8859-1')

# Filtrer uniquement les communes d'Occitanie
dvf_2022 = dvf_2022[dvf_2022['INSEE_COM'].astype(str).str[:2].isin(occitanie_department_codes)]
dvf_2023 = dvf_2023[dvf_2023['INSEE_COM'].astype(str).str[:2].isin(occitanie_department_codes)]

# Fusionner les deux fichiers et calculer la moyenne pondérée du prix au m2
dvf_combined = pd.merge(dvf_2022, dvf_2023, on='INSEE_COM', suffixes=('_2022', '_2023'))
dvf_combined['PrixMoyen_M2_2223'] = (
    (dvf_combined['Nb_mutations_2022'] * dvf_combined['Prixm2Moyen_2022']) + 
    (dvf_combined['Nb_mutations_2023'] * dvf_combined['Prixm2Moyen_2023'])
) / (dvf_combined['Nb_mutations_2022'] + dvf_combined['Nb_mutations_2023'])

# Charger les fichiers des loyers (2022 pour maisons & appartements)
loyers_appartements = pd.read_csv('../data/raw/Indicateurs_Appartement_2022.csv', sep=';', encoding='ISO-8859-1')
loyers_maisons = pd.read_csv('../data/raw/Indicateurs_Maison_2022.csv', sep=';', encoding='ISO-8859-1')

# Filtrer uniquement les communes d'Occitanie
loyers_appartements = loyers_appartements[loyers_appartements['INSEE_C'].astype(str).str[:2].isin(occitanie_department_codes)]
loyers_maisons = loyers_maisons[loyers_maisons['INSEE_C'].astype(str).str[:2].isin(occitanie_department_codes)]

# Sélectionner les colonnes nécessaires
loyers_appartements = loyers_appartements[['INSEE_C', 'LIBGEO', 'loypredm2', 'R2_adj']]
loyers_maisons = loyers_maisons[['INSEE_C', 'LIBGEO', 'loypredm2', 'R2_adj']]

# Renommer les colonnes pour éviter les conflits
loyers_appartements.rename(columns={'loypredm2': 'loyer_apparts', 'R2_adj': 'R2appart'}, inplace=True)
loyers_maisons.rename(columns={'loypredm2': 'loyer_maisons', 'R2_adj': 'R2maison'}, inplace=True)

# Fusionner avec les données de ventes
final_df = pd.merge(dvf_combined, loyers_appartements, left_on='INSEE_COM', right_on='INSEE_C', how='left')
final_df = pd.merge(final_df, loyers_maisons, left_on='INSEE_COM', right_on='INSEE_C', how='left')

# Convertir les valeurs des loyers en float (remplacer la virgule par un point si nécessaire)
final_df['loyer_apparts'] = final_df['loyer_apparts'].astype(str).str.replace(',', '.').astype(float)
final_df['loyer_maisons'] = final_df['loyer_maisons'].astype(str).str.replace(',', '.').astype(float)
final_df['PrixMoyen_M2_2223'] = final_df['PrixMoyen_M2_2223'].astype(float)

# Calcul du loyer annuel estimé
final_df['Loyer_annuel_apparts'] = final_df['loyer_apparts'] * 12
final_df['Loyer_annuel_maisons'] = final_df['loyer_maisons'] * 12

# Calcul du rendement locatif
final_df['Rendement_locatif_apparts'] = (final_df['Loyer_annuel_apparts'] * 100) / final_df['PrixMoyen_M2_2223']
final_df['Rendement_locatif_maisons'] = (final_df['Loyer_annuel_maisons'] * 100) / final_df['PrixMoyen_M2_2223']

# Arrondir toutes les colonnes numériques à 2 décimales
final_df = final_df.round(2)

# Sélectionner les colonnes finales
columns_to_keep = [
    'INSEE_COM', 'PrixMoyen_M2_2223', 'Prixm2Moyen_2022', 'Prixm2Moyen_2023',
    'loyer_apparts', 'loyer_maisons', 'Rendement_locatif_apparts', 'Rendement_locatif_maisons'
]
final_df = final_df[columns_to_keep]

# Exporter le fichier final avec rendement locatif
final_df.to_csv('../data/processed/prixm2_loyer_rendement_communes.csv', index=False, sep=';', encoding='utf-8')

print("Fichier prixm2_loyer_rendement_communes.csv généré avec succès !")