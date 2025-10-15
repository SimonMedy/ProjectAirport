#!/bin/bash

echo "🚀 Démarrage de l'Airport Analytics Dashboard"
echo "=============================================="

# Vérifier si Python est installé
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé"
    exit 1
fi

# Créer un environnement virtuel si il n'existe pas
if [ ! -d "venv" ]; then
    echo "📦 Création de l'environnement virtuel..."
    python3 -m venv venv
fi

# Activer l'environnement virtuel
echo "🔧 Activation de l'environnement virtuel..."
source venv/bin/activate

# Installer les dépendances
echo "📥 Installation des dépendances..."
pip install -r requirements.txt

# Démarrer l'application
echo "🌐 Démarrage de l'application Flask..."
echo "📊 Dashboard disponible sur: http://localhost:5000"
echo "⏹️  Appuyez sur Ctrl+C pour arrêter"
echo ""

python app.py