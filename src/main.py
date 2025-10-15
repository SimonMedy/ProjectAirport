from src.data_loader import charger_aeroports, charger_vols, charger_compagnies, charger_avions
from src.analysis import (analyses_comptages_simples, analyses_classements, analyses_comptages_suite, 
                         analyse_par_compagnie, analyses_filtrage_et_tri, 
                         couverture_compagnies, destinations_exclusives, 
                         vols_principales_compagnies)
from src.database import populate_database

def run_analysis_mission():
    print("Lancement de la Mission 1 : Analyse des Données")

    df_aeroports = charger_aeroports()
    df_vols = charger_vols()
    df_compagnies = charger_compagnies()
    df_avions = charger_avions()

    print("Début de l'analyse")

    analyses_comptages_simples(df_aeroports, df_compagnies, df_avions, df_vols)
    analyses_comptages_suite(df_vols, df_aeroports)
    analyses_classements(df_vols, df_aeroports)
    analyse_par_compagnie(df_vols, df_compagnies)
    analyses_filtrage_et_tri(df_vols, df_aeroports, df_compagnies)
    couverture_compagnies(df_vols, df_compagnies)
    destinations_exclusives(df_vols, df_compagnies)
    vols_principales_compagnies(df_vols, df_compagnies)
    
def run_database_mission():
    print("Lancement de la Mission 2 : Création et Peuplement de la DB")
    populate_database()
    

if __name__ == "__main__":
    run_database_mission()
    
    print("\n" + "="*50 + "\n")
    run_analysis_mission()