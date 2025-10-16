# src/database.py
import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv, find_dotenv

from src.data_loader import charger_aeroports, charger_vols, charger_compagnies, charger_avions

def get_db_engine():
    load_dotenv(find_dotenv('.env.local'))
    db_url = os.getenv("DB_CONNECTION_STRING")
    if not db_url:
        raise ValueError("L'URL de connexion à la base de données n'est pas définie.")
    try:
        engine = create_engine(db_url)
        print("✅ Connexion à la base de données Supabase réussie.")
        return engine
    except Exception as e:
        print(f"❌ Erreur de connexion à la base de données : {e}")
        return None

def validate_data_integrity(df_aeroports, df_compagnies, df_avions):
    """Vérifie le format des clés primaires avec des regex, comme demandé."""
    print("\n--- Validation de l'intégrité des données (Regex) ---")
    if df_aeroports['faa'].str.match(r'^[A-Z0-9]{3,5}$', na=False).all():
        print("✅ Format des codes 'faa' (aéroports) est valide.")
    if df_compagnies['carrier'].str.match(r'^[A-Z0-9]{2}$', na=False).all():
        print("✅ Format des codes 'carrier' (compagnies) est valide.")
    if df_avions['tailnum'].str.match(r'^N[A-Z0-9]+$', na=False).all():
        print("✅ Format des codes 'tailnum' (avions) est valide.")

def verify_and_clean_keys(df_vols, df_avions):
    """Vérifie les clés, nettoie les doublons et les clés étrangères invalides."""
    print("\n--- Vérification et Nettoyage des Clés ---")
    
    # 1. Clé primaire composite de 'flights'
    key_cols = ['year', 'month', 'day', 'carrier', 'flight']
    doublons_avant = df_vols.duplicated(subset=key_cols).sum()
    print(f" ▪️ Nombre de doublons trouvés dans les données brutes : {doublons_avant}")
    if doublons_avant > 0:
        df_vols.drop_duplicates(subset=key_cols, inplace=True)
        print("✅ Doublons de la clé primaire supprimés.")

    # 2. Clé étrangère 'tailnum'
    # On garde une liste de tous les avions qui existent réellement
    avions_connus = set(df_avions['tailnum'])
    # On identifie les vols dont l'avion est inconnu
    vols_avec_avions_inconnus = ~df_vols['tailnum'].isin(avions_connus)
    print(f" ▪️ Nombre de vols avec un avion inconnu : {vols_avec_avions_inconnus.sum()}")
    # Pour ces vols, on met le tailnum à None (qui deviendra NULL en SQL)
    df_vols.loc[vols_avec_avions_inconnus, 'tailnum'] = None
    print("✅ Avions inconnus mis à NULL pour respecter la clé étrangère.")
    
    return df_vols

def populate_database():
    """Fonction principale pour charger, valider, préparer et insérer toutes les données."""
    engine = get_db_engine()
    if engine is None: return

    # Étape 1 : Charger les données
    print("\n--- Chargement des données ---")
    df_aeroports = charger_aeroports()
    df_vols = charger_vols()
    df_compagnies = charger_compagnies()
    df_avions = charger_avions()
    
    # Étape 2 : Valider les formats
    validate_data_integrity(df_aeroports, df_compagnies, df_avions)

    # Étape 3 : Nettoyer les clés (doublons et FK)
    df_vols = verify_and_clean_keys(df_vols, df_avions)

    # Étape 4 : Préparer le reste des données
    print("\n--- Préparation et nettoyage final des données ---")
    # Nettoyage des types numériques pour les vols
    numeric_cols = ['dep_time', 'dep_delay', 'arr_time', 'arr_delay', 'air_time', 'distance', 'minute']
    for col in numeric_cols:
        df_vols[col] = pd.to_numeric(df_vols[col], errors='coerce')
    print("✅ Types de données numériques des vols corrigés.")
    
    # Ajout des aéroports manquants
    aeroports_manquants = pd.DataFrame({
        'faa': ['BQN', 'PSE', 'SJU', 'STT'], 'name': ['Rafael Hernandez', 'Mercedita Airport', 'Luis Munoz Marin Intl', 'Cyril E. King Airport'],
        'lat': [18.4949, 18.0083, 18.4394, 18.3373], 'lon': [-67.1294, -66.5633, -66.0018, -64.9734],
        'alt': [237, 29, 9, 24], 'tz': [-4, -4, -4, -4], 'dst': ['A', 'A', 'A', 'A'],
        'tzone': ['America/Puerto_Rico', 'America/Puerto_Rico', 'America/Puerto_Rico', 'America/St_Thomas']
    })
    df_aeroports = pd.concat([df_aeroports, aeroports_manquants], ignore_index=True)
    print("✅ 4 aéroports manquants ajoutés avec succès.")
    df_avions['year'] = df_avions['year'].astype('Int64')
    print("✅ Types de données des avions corrigés.")

    # Étape 5 : Insérer les données propres dans Supabase
    print("\n--- Démarrage de l'insertion des données dans Supabase ---")
    try:
        with engine.connect() as connection:
            connection.execute(text("TRUNCATE TABLE flights, airlines, airports, planes, weather RESTART IDENTITY CASCADE"))
            connection.commit()
        print("✅ Tables vidées avant insertion.")
        
        df_compagnies.to_sql('airlines', engine, if_exists='append', index=False)
        print("1/4 - Table 'airlines' peuplée avec succès.")
        df_aeroports.to_sql('airports', engine, if_exists='append', index=False)
        print("2/4 - Table 'airports' peuplée avec succès.")
        df_avions.to_sql('planes', engine, if_exists='append', index=False)
        print("3/4 - Table 'planes' peuplée avec succès.")
        df_vols.to_sql('flights', engine, if_exists='append', index=False, chunksize=10000)
        print("4/4 - Table 'flights' peuplée avec succès.")
        print("\n🎉 Mission accomplie ! La base de données a été entièrement peuplée.")

    except Exception as e:
        print(f"❌ Une erreur est survenue lors de l'insertion : {e}")