from src.data_loader import charger_aeroports, charger_vols, charger_compagnies, charger_avions
from src.analysis import analyses_comptages_simples, analyses_classements, analyses_comptages_suite, analyse_par_compagnie, analyses_filtrage_et_tri

def main():
    """Fonction principale du programme."""
    print("--- Lancement de la Mission 1 : Analyse des Données ---\n")

    # Étape 1 : Chargement des données
    df_aeroports = charger_aeroports()
    df_vols = charger_vols()
    df_compagnies = charger_compagnies()
    df_avions = charger_avions()

    print("\n--- Début de l'analyse ---")

    # Étape 2 : Analyses
    #analyses_comptages_simples(df_aeroports, df_compagnies, df_avions, df_vols)
    #analyses_comptages_suite(df_vols, df_aeroports)
    #analyses_classements(df_vols, df_aeroports)
    analyse_par_compagnie(df_vols, df_compagnies)
    

if __name__ == "__main__":
    main()




# print("--- Lancement du test de chargement des données ---")

# # On appelle chaque fonction pour charger les données dans une variable
# df_aeroports = charger_aeroports()
# df_vols = charger_vols()
# df_compagnies = charger_compagnies()
# df_avions = charger_avions()

# # On vérifie que les données sont bien chargées en affichant les premières lignes de chaque DataFrame
# if df_aeroports is not None:
#     print("\n--- Aperçu des données d'aéroports ---")
#     print(df_aeroports.head())

# if df_vols is not None:
#     print("\n--- Aperçu des données de vols ---")
#     print(df_vols.head())

# if df_compagnies is not None:
#     print("\n--- Aperçu des données des compagnies ---")
#     print(df_compagnies.head())

# if df_avions is not None:
#     print("\n--- Aperçu des données des avions ---")
#     print(df_avions.head())