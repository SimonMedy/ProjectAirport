import pandas as pd

def analyses_comptages_simples(df_aeroports, df_compagnies, df_avions, df_vols):
    print("1. Statistiques de base")
    
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
    print("1. (Suite) Statistiques de base")
    
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
    if df_vols is None or df_compagnies is None:
        print("Données manquantes pour l'analyse par compagnie.")
        return

    print("3. Nombre de destinations desservies par compagnie")
    
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

    print("GRAPHIQUE 1 : Destinations par compagnie (Top 10)")
    top_10_compagnies = df_dest_par_compagnie.head(10)
    max_destinations = top_10_compagnies['nombre_destinations_uniques'].max()
    
    for _, row in top_10_compagnies.iterrows():
        nom = row['name'][:20].ljust(20)  # Limiter à 20 caractères
        nb_dest = row['nombre_destinations_uniques']
        barre_longueur = int(nb_dest * 40 / max_destinations)  # Barre sur 40 caractères
        barre = '█' * barre_longueur
        print(f"{nom} |{barre} {nb_dest}")
    print("-" * 40)

    print("Destinations par compagnie et par aéroport d'origine (Top 15)")
    dest_par_origine = df_vols.groupby(['carrier', 'origin'])['dest'].nunique().reset_index()
    dest_par_origine = pd.merge(dest_par_origine, df_compagnies, on='carrier')
    dest_par_origine = dest_par_origine.sort_values('dest', ascending=False)
    print(dest_par_origine.head(15))
    print("-" * 40)

    print("GRAPHIQUE 2 : Top 15 Compagnie-Aéroport")
    top_15 = dest_par_origine.head(15)
    max_dest_origine = top_15['dest'].max()
    
    for _, row in top_15.iterrows():
        label = f"{row['name'][:15]}-{row['origin']}".ljust(20)
        nb_dest = row['dest']
        barre_longueur = int(nb_dest * 30 / max_dest_origine)  # Barre sur 30 caractères
        barre = '▓' * barre_longueur
        print(f"{label} |{barre} {nb_dest}")
    print("-" * 40)

    # --- TABLEAU DE SYNTHÈSE ---
    print("\n--- TABLEAU DE SYNTHÈSE : Statistiques par compagnie ---")
    synthese = df_dest_par_compagnie.copy()
    synthese['pourcentage_destinations'] = (synthese['nombre_destinations_uniques'] / 
                                           synthese['nombre_destinations_uniques'].sum() * 100).round(2)
    print(synthese.head(10)[['name', 'nombre_destinations_uniques', 'pourcentage_destinations']].to_string(index=False))
    print("-" * 40)
    
def analyses_filtrage_et_tri(df_vols, df_aeroports, df_compagnies):
    """
    Répond a la questions 4 et 5 : Filtrage de vols spécifiques et tri.
    """
    if df_vols is None:
        print("Données de vols manquantes pour le filtrage et le tri.")
        return

    print("\n--- 4/5. Vols à destination de Houston (IAH ou HOU) ---")
    vols_houston = df_vols[df_vols['dest'].isin(['IAH', 'HOU'])]
    print(f"Nombre de vols trouvés pour Houston : {len(vols_houston)}")
    print(vols_houston.head().to_string())
    print("-" * 40)

    print("\n--- Nombre de vols par destination ---")
    vols_par_destination = df_vols['dest'].value_counts().sort_values(ascending=False)
    print("Top 15 des destinations les plus fréquentées :")
    print(vols_par_destination.head(15))
    print("\n--- Graphique ASCII : Top 10 destinations ---")
    top_10_dest = vols_par_destination.head(10)
    max_vols = top_10_dest.max()
    
    for destination, nb_vols in top_10_dest.items():
        barre_longueur = int(nb_vols * 30 / max_vols)  # Barre sur 30 caractères
        barre = '█' * barre_longueur
        print(f"{destination.ljust(4)} |{barre} {nb_vols}")
    print("-" * 40)

    print("\n--- Analyse des vols de NYC vers Seattle (SEA) ---")
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
        print("\n--- Aperçu des vols triés (Destination, Origine, Compagnie) ---")
        
        df_tries = pd.merge(df_vols, df_aeroports, left_on='origin', right_on='faa', suffixes=('', '_origin'))
        df_tries.rename(columns={'name': 'origin_name'}, inplace=True)
        
        df_tries = pd.merge(df_tries, df_aeroports, left_on='dest', right_on='faa', suffixes=('', '_dest'))
        df_tries.rename(columns={'name': 'dest_name'}, inplace=True)
        
        df_tries = pd.merge(df_tries, df_compagnies, on='carrier')
        
        df_tries.sort_values(by=['dest_name', 'origin_name', 'name'], inplace=True)
        
        colonnes_a_afficher = ['dest_name', 'origin_name', 'name', 'flight', 'tailnum']
        print(df_tries[colonnes_a_afficher].head(10).to_string(index=False))
        print("-" * 40)


def couverture_compagnies(df_vols, df_compagnies):
    """
    Question 6 : Quelles sont les compagnies qui n'opèrent pas sur tous les aéroports d'origine ?
    Quelles sont les compagnies qui desservent l'ensemble de destinations ?
    """
    if df_vols is None or df_compagnies is None:
        print("Données manquantes pour l'analyse de couverture des compagnies.")
        return

    print("\n--- 6. Analyse des compagnies et de leur couverture ---")
    
    # Obtenir tous les aéroports d'origine et destinations uniques
    tous_aeroports_origine = set(df_vols['origin'].unique())
    toutes_destinations = set(df_vols['dest'].unique())
    
    print(f"Nombre total d'aéroports d'origine : {len(tous_aeroports_origine)}")
    print(f"Nombre total de destinations : {len(toutes_destinations)}")
    
    # Analyser chaque compagnie
    analyse_compagnies = []
    
    for carrier in df_vols['carrier'].unique():
        vols_compagnie = df_vols[df_vols['carrier'] == carrier]
        origines_compagnie = set(vols_compagnie['origin'].unique())
        destinations_compagnie = set(vols_compagnie['dest'].unique())
        
        # Joindre avec le nom de la compagnie
        nom_compagnie = df_compagnies[df_compagnies['carrier'] == carrier]['name'].iloc[0]
        
        analyse_compagnies.append({
            'carrier': carrier,
            'name': nom_compagnie,
            'nb_origines': len(origines_compagnie),
            'nb_destinations': len(destinations_compagnie),
            'couvre_toutes_origines': len(origines_compagnie) == len(tous_aeroports_origine),
            'couvre_toutes_destinations': len(destinations_compagnie) == len(toutes_destinations),
            'origines': origines_compagnie,
            'destinations': destinations_compagnie
        })
    
    df_analyse = pd.DataFrame(analyse_compagnies)
    
    # Compagnies qui n'opèrent pas sur tous les aéroports d'origine
    compagnies_pas_toutes_origines = df_analyse[~df_analyse['couvre_toutes_origines']]
    print(f"\nCompagnies qui n'opèrent PAS sur tous les aéroports d'origine ({len(compagnies_pas_toutes_origines)}) :")
    for _, row in compagnies_pas_toutes_origines.iterrows():
        print(f"  - {row['name']} : {row['nb_origines']}/{len(tous_aeroports_origine)} aéroports")
    
    # Compagnies qui desservent toutes les destinations
    compagnies_toutes_destinations = df_analyse[df_analyse['couvre_toutes_destinations']]
    print(f"\nCompagnies qui desservent TOUTES les destinations ({len(compagnies_toutes_destinations)}) :")
    for _, row in compagnies_toutes_destinations.iterrows():
        print(f"  - {row['name']} : {row['nb_destinations']} destinations")
    
    # Tableau récapitulatif
    print("\n--- TABLEAU RÉCAPITULATIF : Couverture par compagnie ---")
    tableau_recap = df_analyse[['name', 'nb_origines', 'nb_destinations']].sort_values('nb_destinations', ascending=False)
    print(tableau_recap.to_string(index=False))
    print("-" * 40)
    
    return df_analyse  # Retourner pour utilisation dans question 7


def destinations_exclusives(df_vols, df_compagnies):
    """
    Question 7 : Quelles sont les destinations qui sont exclusives à certaines compagnies ?
    """
    if df_vols is None or df_compagnies is None:
        print("Données manquantes pour l'analyse des destinations exclusives.")
        return

    print("\n--- 7. Destinations exclusives à certaines compagnies ---")
    
    # Analyser chaque compagnie et ses destinations
    analyse_compagnies = []
    for carrier in df_vols['carrier'].unique():
        vols_compagnie = df_vols[df_vols['carrier'] == carrier]
        destinations_compagnie = set(vols_compagnie['dest'].unique())
        nom_compagnie = df_compagnies[df_compagnies['carrier'] == carrier]['name'].iloc[0]
        
        analyse_compagnies.append({
            'carrier': carrier,
            'name': nom_compagnie,
            'destinations': destinations_compagnie
        })
    
    # Pour chaque destination, compter combien de compagnies la desservent
    destinations_par_compagnie = {}
    for row in analyse_compagnies:
        for dest in row['destinations']:
            if dest not in destinations_par_compagnie:
                destinations_par_compagnie[dest] = []
            destinations_par_compagnie[dest].append(row['name'])
    
    # Trouver les destinations exclusives (servies par une seule compagnie)
    destinations_exclusives = {dest: compagnies for dest, compagnies in destinations_par_compagnie.items() if len(compagnies) == 1}
    
    print(f"Nombre de destinations exclusives : {len(destinations_exclusives)}")
    print("Destinations exclusives :")
    for dest, compagnies in sorted(destinations_exclusives.items()):
        print(f"  - {dest} : exclusivement desservie par {compagnies[0]}")
    
    # Destinations les moins desservies (2-3 compagnies)
    destinations_peu_desservies = {dest: compagnies for dest, compagnies in destinations_par_compagnie.items() if 2 <= len(compagnies) <= 3}
    print(f"\nDestinations peu desservies (2-3 compagnies) : {len(destinations_peu_desservies)}")
    for dest, compagnies in sorted(list(destinations_peu_desservies.items())[:10]):  # Top 10
        print(f"  - {dest} : {len(compagnies)} compagnies ({', '.join(compagnies)})")
    print("-" * 40)


def vols_principales_compagnies(df_vols, df_compagnies):
    """
    Question 8 : Filtrer le vol pour trouver ceux exploités par United, American ou Delta ?
    """
    if df_vols is None or df_compagnies is None:
        print("Données manquantes pour l'analyse des principales compagnies.")
        return

    print("\n--- 8. Vols exploités par United, American ou Delta ---")
    
    # Identifier les codes des compagnies principales
    codes_recherches = []
    compagnies_principales = ['United Air Lines Inc.', 'American Airlines Inc.', 'Delta Air Lines Inc.']
    
    for nom_compagnie in compagnies_principales:
        code = df_compagnies[df_compagnies['name'].str.contains(nom_compagnie, case=False, na=False)]['carrier']
        if not code.empty:
            codes_recherches.extend(code.tolist())
            print(f"Code trouvé pour {nom_compagnie} : {code.tolist()}")
    
    if codes_recherches:
        vols_principales_compagnies = df_vols[df_vols['carrier'].isin(codes_recherches)]
        print(f"\nNombre total de vols pour United/American/Delta : {len(vols_principales_compagnies)}")
        
        # Répartition par compagnie
        repartition = vols_principales_compagnies['carrier'].value_counts()
        print("\nRépartition par compagnie :")
        for carrier, nb_vols in repartition.items():
            nom = df_compagnies[df_compagnies['carrier'] == carrier]['name'].iloc[0]
            pourcentage = (nb_vols / len(vols_principales_compagnies)) * 100
            print(f"  - {nom} ({carrier}) : {nb_vols} vols ({pourcentage:.1f}%)")
        
        # Graphique ASCII de la répartition
        print("\n--- Graphique ASCII : Répartition United/American/Delta ---")
        max_vols = repartition.max()
        for carrier, nb_vols in repartition.items():
            nom = df_compagnies[df_compagnies['carrier'] == carrier]['name'].iloc[0][:15]
            barre_longueur = int(nb_vols * 30 / max_vols)
            barre = '█' * barre_longueur
            print(f"{nom.ljust(15)} |{barre} {nb_vols}")
        
        # Échantillon des vols filtrés
        print(f"\n--- Échantillon des vols filtrés (10 premiers) ---")
        colonnes_affichage = ['carrier', 'flight', 'origin', 'dest', 'dep_time', 'arr_time']
        print(vols_principales_compagnies[colonnes_affichage].head(10).to_string(index=False))
    else:
        print("Aucune des compagnies principales trouvée dans les données.")
    
    print("-" * 40)

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