from src.data_loader import charger_aeroports, charger_vols, charger_compagnies, charger_avions, charger_meteo
from src.analysis import (analyses_comptages_simples, analyses_classements, analyses_comptages_suite, 
                         analyse_par_compagnie, analyses_filtrage_et_tri, 
                         couverture_compagnies, destinations_exclusives, 
                         vols_principales_compagnies)
from src.database import populate_database

def run_analysis_mission():
    """
    Exécute la Mission 1 : charger les données depuis les fichiers et répondre à toutes les questions d'analyse.
    """
    print("--- Lancement de la Mission 1 : Analyse des Données ---\n")

    # Étape 1 : Chargement des données
    df_aeroports = charger_aeroports()
    df_vols = charger_vols()
    df_compagnies = charger_compagnies()
    df_avions = charger_avions()
    df_meteo = charger_meteo()

    print("\n--- Début de l'analyse ---")

    # Étape 2 : Analyses
    analyses_comptages_simples(df_aeroports, df_compagnies, df_avions, df_vols) #Q1
    analyses_comptages_suite(df_vols, df_aeroports) #Q1
    analyses_classements(df_vols, df_aeroports) #Q2
    analyse_par_compagnie(df_vols, df_compagnies) #Q3
    analyses_filtrage_et_tri(df_vols, df_aeroports, df_compagnies) #Q4 et Q5
    couverture_compagnies(df_vols, df_compagnies) #Q6
    destinations_exclusives(df_vols, df_compagnies) #Q7
    vols_principales_compagnies(df_vols, df_compagnies) #Q8
    
def run_database_mission():
    """
    Exécute la Mission 2 : peupler la base de données sur Supabase.
    """
    print("--- Lancement de la Mission 2 : Création et Peuplement de la DB ---")
    populate_database()
    

if __name__ == "__main__":
    run_database_mission()
    
    print("\n" + "="*50 + "\n")
    run_analysis_mission()