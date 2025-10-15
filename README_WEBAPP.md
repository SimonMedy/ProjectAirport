# 🛩️ Airport Analytics Dashboard

## Vue d'ensemble

Cette WebApp Flask fournit une interface interactive pour analyser les données de trafic aérien avec des visualisations avancées et des capacités de prédiction. Parfait pour impressionner lors de présentations !

## ✨ Fonctionnalités

### 📊 Dashboard Interactif
- **Statistiques en temps réel** : Total des vols, annulations, retards moyens
- **Visualisations dynamiques** : Graphiques Plotly interactifs
- **Interface responsive** : Compatible mobile et desktop

### 🔍 Analyses Disponibles
1. **Distribution des retards** - Répartition par catégories
2. **Tendances mensuelles** - Évolution des retards et volume
3. **Top routes** - Routes les plus fréquentées
4. **Performance compagnies** - Comparaison des performances
5. **Prédictions** - Modèle de prédiction des retards
6. **Impact saisonnier** - Analyse par saisons

### 🤖 Intelligence Artificielle
- **Modèle prédictif** utilisant scikit-learn
- **Prédictions mensuelles** des retards
- **Recommandations automatiques** basées sur les données

## 🚀 Installation et Démarrage

### Méthode 1 : Script automatique (Recommandé)
```bash
chmod +x start_webapp.sh
./start_webapp.sh
```

### Méthode 2 : Installation manuelle
```bash
# Créer un environnement virtuel
python3 -m venv venv
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Démarrer l'application
python app.py
```

## 🌐 Accès

Une fois démarrée, l'application sera disponible sur :
- **URL principale** : http://localhost:5000
- **API endpoints** : http://localhost:5000/api/*

## 📱 Interface Utilisateur

### Design Moderne
- **Bootstrap 5** pour un design professionnel
- **Font Awesome** pour les icônes
- **Animations CSS** pour une expérience fluide
- **Couleurs gradient** pour un aspect moderne

### Sections du Dashboard
1. **Header** - Titre et navigation
2. **Statistiques** - 4 KPI principaux
3. **Alerte prédictive** - Insights automatiques
4. **Graphiques** - 6 visualisations interactives
5. **Footer** - Informations techniques

## 🔧 Architecture Technique

### Backend (Flask)
```
app.py                 # Application principale
├── AirportAnalytics  # Classe de gestion des données
├── Routes API        # Endpoints pour les données
└── Modèle ML         # Prédictions avec scikit-learn
```

### Frontend (HTML/JS)
```
templates/dashboard.html   # Interface utilisateur
├── Bootstrap 5           # Framework CSS
├── Plotly.js            # Graphiques interactifs
└── JavaScript           # Logique client
```

### Endpoints API
- `/api/stats` - Statistiques générales
- `/api/delay_distribution` - Distribution des retards
- `/api/monthly_trends` - Tendances mensuelles
- `/api/top_routes` - Routes populaires
- `/api/airline_performance` - Performance compagnies
- `/api/predict_delays` - Prédictions ML
- `/api/weather_impact` - Impact saisonnier

## 🎯 Objectifs Business

### Pour le Manager
- **Vue d'ensemble** rapide des performances
- **Identification** des problèmes potentiels
- **Prédictions** pour la planification
- **Comparaisons** entre compagnies et routes

### Aide à la Décision
- **Allocation ressources** basée sur les prédictions
- **Optimisation routes** selon les performances
- **Planification saisonnière** avec l'analyse météo
- **Benchmarking compagnies** pour les partenariats

## 🏆 Points Forts pour la Présentation

1. **Impact visuel** - Design moderne et professionnel
2. **Interactivité** - Graphiques Plotly zoomables et filtrable
3. **Intelligence** - Prédictions et recommandations automatiques
4. **Completude** - Analyses multidimensionnelles
5. **Performance** - Chargement rapide et responsive

## 🛠️ Personnalisation

### Ajouter de nouveaux graphiques
1. Créer une nouvelle route dans `app.py`
2. Ajouter l'élément HTML dans `dashboard.html`
3. Mettre à jour le JavaScript de chargement

### Modifier le style
- Éditer les styles CSS dans `dashboard.html`
- Personnaliser les couleurs Bootstrap
- Ajuster les animations et transitions

## 📈 Évolutions Possibles

- **Connexion base de données** en temps réel
- **Filtres interactifs** par période/compagnie
- **Exports PDF** des rapports
- **Alertes email** automatiques
- **API REST** complète
- **Authentication** utilisateurs

---

💡 **Conseil pour la présentation** : Démarrez par les statistiques générales, puis montrez les prédictions pour créer l'impact !