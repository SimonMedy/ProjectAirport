import pandas as pd

def charger_aeroports(fichier='data/airports.csv'):
    """Charge les données des aéroports depuis un fichier CSV."""
    try:
        df = pd.read_csv(fichier, sep=';', index_col=0, decimal=',')
        print(f"✅ Fichier '{fichier}' chargé avec succès.")
        return df
    except FileNotFoundError:
        print(f"❌ ERREUR: Le fichier '{fichier}' est introuvable.")
        return None

def charger_vols(fichier='data/flights.csv'):
    """Charge les données des vols depuis un fichier CSV."""
    try:
        df = pd.read_csv(fichier, encoding='latin1')
        print(f"✅ Fichier '{fichier}' chargé avec succès.")
        return df
    except FileNotFoundError:
        print(f"❌ ERREUR: Le fichier '{fichier}' est introuvable.")
        return None

def charger_compagnies(fichier='data/airlines.json'):
    """Charge les données des compagnies aériennes depuis un fichier JSON."""
    try:
        df = pd.read_json(fichier)
        print(f"✅ Fichier '{fichier}' chargé avec succès.")
        return df
    except FileNotFoundError:
        print(f"❌ ERREUR: Le fichier '{fichier}' est introuvable.")
        return None

def charger_avions(fichier='data/planes.html'):
    """Charge les données des avions depuis un fichier HTML."""
    try:
        tables = pd.read_html(fichier, index_col=0)
        df = tables[0]
        print(f"✅ Fichier '{fichier}' chargé avec succès.")
        return df
    except FileNotFoundError:
        print(f"❌ ERREUR: Le fichier '{fichier}' est introuvable.")
        return None
    except IndexError:
        print(f"❌ ERREUR: Aucun tableau n'a été trouvé dans le fichier '{fichier}'.")
        return None

def charger_meteo(fichier='data/weather.pdf'):
    """Placeholder"""
    print(f"⚠️ Le chargement du PDF '{fichier}' n'est pas encore implémenté.")
    return None
