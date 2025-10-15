import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv, find_dotenv

from src.data_loader import charger_aeroports, charger_vols, charger_compagnies, charger_avions

def get_db_engine():
    load_dotenv(find_dotenv('.env.local'))
    
    db_url = os.getenv("DB_CONNECTION_STRING")
    print(f"DB_CONNECTION_STRING: {db_url}")
    
    if not db_url:
        raise ValueError("L'URL de connexion à la base de données n'est pas définie. Vérifiez votre fichier .env.local")
        
    try:
        engine = create_engine(db_url)
        print("Connexion à la base de données Supabase réussie.")
        return engine
    except Exception as e:
        print(f"Erreur de connexion à la base de données : {e}")
        return None

def populate_database():
    """
    Fonction principale pour charger, préparer et insérer toutes les données.
    """
    engine = get_db_engine()
    if engine is None:
        return

    # --- Étape 1 : Charger toutes les données depuis les fichiers ---
    print("\n--- Chargement des données depuis les fichiers source ---")
    df_aeroports = charger_aeroports()
    df_vols = charger_vols()
    df_compagnies = charger_compagnies()
    df_avions = charger_avions()
    
    # --- Étape 2 : Préparer et nettoyer les données (CRUCIAL) ---
    print("\n--- Préparation et nettoyage des données ---")

    # Problème 1: Ajouter les 4 aéroports manquants mentionnés dans l'énoncé
    aeroports_manquants = pd.DataFrame({
        'faa': ['BQN', 'PSE', 'SJU', 'STT'],
        'name': ['Rafael Hernandez Airport', 'Mercedita Airport', 'Luis Munoz Marin Intl', 'Cyril E. King Airport'],
        'lat': [18.4949, 18.0083, 18.4394, 18.3373],
        'lon': [-67.1294, -66.5633, -66.0018, -64.9734],
        'alt': [237, 29, 9, 24],
        'tz': [-4, -4, -4, -4],
        'dst': ['A', 'A', 'A', 'A'],
        'tzone': ['America/Puerto_Rico', 'America/Puerto_Rico', 'America/Puerto_Rico', 'America/St_Thomas']
    })
    df_aeroports = pd.concat([df_aeroports, aeroports_manquants], ignore_index=True)
    print("✅ 4 aéroports manquants ajoutés avec succès.")
    
    # Problème 2: Gérer les types de données avant insertion
    df_avions['year'] = df_avions['year'].astype('Int64')
    print("✅ Types de données corrigés.")

    # --- Étape 3 : Insérer les données dans Supabase (dans le bon ordre) ---
    print("\n--- Démarrage de l'insertion des données dans Supabase ---")
    try:
        # L'ordre est important à cause des clés étrangères !
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
        print(f"❌ Une erreur est survenue lors de l'insertion des données : {e}")