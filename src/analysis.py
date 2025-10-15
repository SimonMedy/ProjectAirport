# src/analysis.py
import pandas as pd

# ================================================================= #
#                         QUESTIONS DE COMPTAGE                       #
# ================================================================= #

def analyses_comptages_simples(df_aeroports, df_compagnies, df_avions, df_vols):
    """
    Répond à la première série de questions : comptages de base.
    """
    print("--- 1. Statistiques de base ---")
    
    if df_aeroports is not None:
        print(f"Nombre total d'aéroports : {len(df_aeroports)}")
    
    if df_compagnies is not None:
        print(f"Nombre total de compagnies : {len(df_compagnies)}")
    
    if df_avions is not None:
        print(f"Nombre total d'avions uniques : {len(df_avions)}")
        
    if df_vols is not None:
        vols_annules = df_vols['dep_time'].isnull().sum()
        print(f"Nombre de vols annulés : {vols_annules}")
        
    print("-" * 40)


def analyses_comptages_suite(df_vols, df_aeroports):
    """
    Répond aux autres questions de comptage de la question 1.
    """
    print("\n--- 1. (Suite) Statistiques de base ---")
    
    if df_vols is not None:
        departs_uniques = df_vols['origin'].nunique()
        destinations_uniques = df_vols['dest'].nunique()
        print(f"Nombre d'aéroports de départ uniques : {departs_uniques}")
        print(f"Nombre d'aéroports de destination uniques : {destinations_uniques}")

    if df_aeroports is not None:
        sans_heure_ete = df_aeroports[df_aeroports['dst'] == 'N'].shape[0]
        fuseaux_horaires = df_aeroports['tzone'].nunique()
        print(f"Nombre d'aéroports sans heure d'été : {sans_heure_ete}")
        print(f"Nombre de fuseaux horaires uniques : {fuseaux_horaires}")

    print("-" * 40)
    
def analyse_par_compagnie(df_vols, df_compagnies):
    """
    Répond à la question 3 : Analyse par compagnie.
    """
    if df_vols is None or df_compagnies is None:
        print("Données manquantes pour l'analyse par compagnie.")
        return

    print("\n--- 3. Nombre de destinations desservies par compagnie ---")
    
    # Grouper par 'carrier' et compter les destinations uniques pour chaque
    dest_par_compagnie = df_vols.groupby('carrier')['dest'].nunique().sort_values(ascending=False)
    
    # Joindre avec df_compagnies pour afficher les noms complets
    df_dest_par_compagnie = pd.merge(
        dest_par_compagnie.reset_index(),
        df_compagnies,
        on='carrier'
    )
    df_dest_par_compagnie.rename(columns={'dest': 'nombre_destinations_uniques'}, inplace=True)
    print(df_dest_par_compagnie[['name', 'nombre_destinations_uniques']].to_string(index=False))
    print("-" * 40)

    print("\n--- Destinations par compagnie et par aéroport d'origine (Top 15) ---")
    # Double groupement : par compagnie ET par aéroport d'origine
    dest_par_origine = df_vols.groupby(['carrier', 'origin'])['dest'].nunique().sort_values(ascending=False)
    print(dest_par_origine.head(15))
    print("-" * 40)
    
def analyses_filtrage_et_tri(df_vols, df_aeroports, df_compagnies):
    """
    Répond aux questions 4 et 5 : Filtrage de vols spécifiques et tri.
    """
    if df_vols is None:
        print("Données de vols manquantes pour le filtrage et le tri.")
        return

    print("\n--- 4. Vols à destination de Houston (IAH ou HOU) ---")
    vols_houston = df_vols[df_vols['dest'].isin(['IAH', 'HOU'])]
    print(f"Nombre de vols trouvés pour Houston : {len(vols_houston)}")
    print(vols_houston.head().to_string())
    print("-" * 40)

    print("\n--- 10. Analyse des vols de NYC vers Seattle (SEA) ---")
    vols_nyc_sea = df_vols[
        (df_vols['origin'].isin(['EWR', 'JFK', 'LGA'])) &
        (df_vols['dest'] == 'SEA')
    ]
    
    nombre_vols = len(vols_nyc_sea)
    compagnies_uniques = vols_nyc_sea['carrier'].nunique()
    avions_uniques = vols_nyc_sea['tailnum'].nunique()
    
    print(f"Nombre de vols de NYC vers Seattle : {nombre_vols}")
    print(f"Nombre de compagnies desservant cette destination : {compagnies_uniques}")
    print(f"Nombre d'avions uniques sur cette route : {avions_uniques}")
    print("-" * 40)
    
    if df_aeroports is not None and df_compagnies is not None:
        print("\n--- 11. Aperçu des vols triés (Destination, Origine, Compagnie) ---")
        
        df_tries = pd.merge(df_vols, df_aeroports, left_on='origin', right_on='faa', suffixes=('', '_origin'))
        df_tries.rename(columns={'name': 'origin_name'}, inplace=True)
        
        df_tries = pd.merge(df_tries, df_aeroports, left_on='dest', right_on='faa', suffixes=('', '_dest'))
        df_tries.rename(columns={'name': 'dest_name'}, inplace=True)
        
        df_tries = pd.merge(df_tries, df_compagnies, on='carrier')
        
        df_tries.sort_values(by=['dest_name', 'origin_name', 'name'], inplace=True)
        
        colonnes_a_afficher = ['dest_name', 'origin_name', 'name', 'flight', 'tailnum']
        print(df_tries[colonnes_a_afficher].head(10).to_string(index=False))
        print("-" * 40)


# ================================================================= #
#                        QUESTIONS DE CLASSEMENT                      #
# ================================================================= #

def analyses_classements(df_vols, df_aeroports):
    """
    Répond à la deuxième série de questions : classements (tops/flops).
    """
    if df_vols is None:
        print("Impossible de faire les classements, les données de vols sont manquantes.")
        return

    # --- Aéroport de départ le plus emprunté ---
    aeroport_top = df_vols['origin'].value_counts().idxmax()
    print("\n--- 2. Aéroport de départ le plus fréquenté ---")
    print(f"L'aéroport de départ le plus emprunté est : {aeroport_top}")
    print("-" * 40)

    # --- Top 10 des destinations ---
    if df_aeroports is not None:
        dest_counts = df_vols['dest'].value_counts()
        total_vols = len(df_vols)
        df_dest_counts = dest_counts.reset_index()
        df_dest_counts.columns = ['faa', 'nombre_vols']
        
        df_merged = pd.merge(df_dest_counts, df_aeroports, on='faa', how='left')
        df_merged['pourcentage'] = (df_merged['nombre_vols'] / total_vols) * 100
        df_merged['pourcentage'] = df_merged['pourcentage'].map('{:.2f}%'.format)

        print("\n--- Top 10 des destinations les plus prisées ---")
        print(df_merged[['name', 'nombre_vols', 'pourcentage']].head(10).to_string(index=False))
        
        print("\n--- Top 10 des destinations les moins prisées ---")
        print(df_merged[['name', 'nombre_vols', 'pourcentage']].tail(10).to_string(index=False))
        print("-" * 40)

    # --- Top 10 des avions ---
    avion_counts = df_vols['tailnum'].value_counts()
    print("\n--- Top 10 des avions ayant le plus décollé ---")
    print(avion_counts.head(10))
    
    print("\n--- Top 10 des avions ayant le moins décollé ---")
    print(avion_counts.tail(10))
    print("-" * 40)