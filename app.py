from flask import Flask, render_template, jsonify, request
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.utils import PlotlyJSONEncoder
import json
from datetime import datetime, timedelta
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

from src.data_loader import charger_aeroports, charger_vols, charger_compagnies, charger_avions

app = Flask(__name__)

class AirportAnalytics:
    def __init__(self):
        self.df_aeroports = None
        self.df_vols = None
        self.df_compagnies = None
        self.df_avions = None
        self.load_data()
    
    def load_data(self):
        try:
            self.df_aeroports = charger_aeroports()
            self.df_vols = charger_vols()
            self.df_compagnies = charger_compagnies()
            self.df_avions = charger_avions()
            
            if self.df_vols is not None:
                self.df_vols['delay_category'] = pd.cut(
                    self.df_vols['dep_delay'].fillna(0), 
                    bins=[-np.inf, 0, 15, 60, np.inf], 
                    labels=['À l\'heure', 'Retard léger', 'Retard modéré', 'Retard important']
                )
                
                self.df_vols['date'] = pd.to_datetime(
                    self.df_vols[['year', 'month', 'day']], 
                    errors='coerce'
                )
                
        except Exception as e:
            print(f"Erreur lors du chargement des données: {e}")

analytics = AirportAnalytics()

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/stats')
def get_stats():
    if analytics.df_vols is None:
        return jsonify({'error': 'Données non disponibles'})
    
    total_flights = len(analytics.df_vols)
    cancelled_flights = analytics.df_vols['dep_time'].isnull().sum()
    avg_delay = analytics.df_vols['dep_delay'].mean()
    unique_airports = analytics.df_vols['origin'].nunique()
    
    return jsonify({
        'total_flights': int(total_flights),
        'cancelled_flights': int(cancelled_flights),
        'cancellation_rate': round((cancelled_flights / total_flights) * 100, 2),
        'avg_delay': round(avg_delay, 2) if not pd.isna(avg_delay) else 0,
        'unique_airports': int(unique_airports)
    })

@app.route('/api/delay_distribution')
def delay_distribution():
    if analytics.df_vols is None:
        return jsonify({'error': 'Données non disponibles'})
    
    delay_counts = analytics.df_vols['delay_category'].value_counts()
    
    fig = px.pie(
        values=delay_counts.values,
        names=delay_counts.index,
        title="Distribution des Retards de Vol",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig.update_layout(
        height=400,
        font=dict(size=12),
        showlegend=True
    )
    
    return json.dumps(fig, cls=PlotlyJSONEncoder)

@app.route('/api/monthly_trends')
def monthly_trends():
    if analytics.df_vols is None:
        return jsonify({'error': 'Données non disponibles'})
    
    monthly_data = analytics.df_vols.groupby('month').agg({
        'dep_delay': 'mean',
        'flight': 'count'
    }).reset_index()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=monthly_data['month'],
        y=monthly_data['dep_delay'],
        mode='lines+markers',
        name='Retard Moyen (min)',
        line=dict(color='red', width=3),
        yaxis='y'
    ))
    
    fig.add_trace(go.Bar(
        x=monthly_data['month'],
        y=monthly_data['flight'],
        name='Nombre de Vols',
        opacity=0.6,
        yaxis='y2'
    ))
    
    fig.update_layout(
        title="Tendances Mensuelles: Retards vs Volume de Vols",
        xaxis_title="Mois",
        yaxis=dict(title="Retard Moyen (minutes)", side="left"),
        yaxis2=dict(title="Nombre de Vols", side="right", overlaying="y"),
        height=500,
        hovermode='x unified'
    )
    
    return json.dumps(fig, cls=PlotlyJSONEncoder)

@app.route('/api/top_routes')
def top_routes():
    if analytics.df_vols is None:
        return jsonify({'error': 'Données non disponibles'})
    
    routes = analytics.df_vols.groupby(['origin', 'dest']).agg({
        'flight': 'count',
        'dep_delay': 'mean'
    }).reset_index()
    
    routes['route'] = routes['origin'] + ' → ' + routes['dest']
    routes = routes.nlargest(15, 'flight')
    
    fig = px.scatter(
        routes,
        x='flight',
        y='dep_delay',
        hover_data=['route'],
        size='flight',
        color='dep_delay',
        title="Top 15 Routes: Volume vs Retard Moyen",
        labels={
            'flight': 'Nombre de Vols',
            'dep_delay': 'Retard Moyen (min)'
        },
        color_continuous_scale='RdYlGn_r'
    )
    
    fig.update_layout(height=500)
    
    return json.dumps(fig, cls=PlotlyJSONEncoder)

@app.route('/api/airline_performance')
def airline_performance():
    if analytics.df_vols is None or analytics.df_compagnies is None:
        return jsonify({'error': 'Données non disponibles'})
    
    airline_perf = analytics.df_vols.groupby('carrier').agg({
        'dep_delay': 'mean',
        'flight': 'count',
        'dep_time': lambda x: x.isnull().sum()
    }).reset_index()
    
    airline_perf.columns = ['carrier', 'avg_delay', 'total_flights', 'cancelled']
    airline_perf['cancellation_rate'] = (airline_perf['cancelled'] / airline_perf['total_flights']) * 100
    
    airline_perf = airline_perf.merge(analytics.df_compagnies, on='carrier')
    airline_perf = airline_perf[airline_perf['total_flights'] >= 1000]
    
    fig = px.scatter(
        airline_perf,
        x='avg_delay',
        y='cancellation_rate',
        size='total_flights',
        hover_data=['name'],
        title="Performance des Compagnies Aériennes",
        labels={
            'avg_delay': 'Retard Moyen (min)',
            'cancellation_rate': 'Taux d\'Annulation (%)',
            'total_flights': 'Total Vols'
        },
        color='avg_delay',
        color_continuous_scale='RdYlGn_r'
    )
    
    fig.update_layout(height=500)
    
    return json.dumps(fig, cls=PlotlyJSONEncoder)

@app.route('/api/predict_delays')
def predict_delays():
    if analytics.df_vols is None:
        return jsonify({'error': 'Données non disponibles'})
    
    try:
        df_clean = analytics.df_vols.dropna(subset=['dep_delay', 'month', 'day', 'hour'])
        
        if len(df_clean) < 100:
            return jsonify({'error': 'Données insuffisantes pour la prédiction'})
        
        le_carrier = LabelEncoder()
        le_origin = LabelEncoder()
        
        df_model = df_clean.copy()
        df_model['carrier_encoded'] = le_carrier.fit_transform(df_model['carrier'])
        df_model['origin_encoded'] = le_origin.fit_transform(df_model['origin'])
        
        X = df_model[['month', 'day', 'hour', 'carrier_encoded', 'origin_encoded']].values
        y = df_model['dep_delay'].values
        
        model = LinearRegression()
        model.fit(X, y)
        
        predictions = {}
        for month in range(1, 13):
            X_pred = np.array([[month, 15, 12, 0, 0]])
            pred_delay = model.predict(X_pred)[0]
            predictions[month] = round(pred_delay, 2)
        
        months = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jun',
                 'Jul', 'Aoû', 'Sep', 'Oct', 'Nov', 'Déc']
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=months,
            y=list(predictions.values()),
            mode='lines+markers',
            name='Retard Prédit',
            line=dict(color='blue', width=3),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title="Prédiction des Retards par Mois",
            xaxis_title="Mois",
            yaxis_title="Retard Prédit (minutes)",
            height=400
        )
        
        return json.dumps(fig, cls=PlotlyJSONEncoder)
        
    except Exception as e:
        return jsonify({'error': f'Erreur de prédiction: {str(e)}'})

@app.route('/api/weather_impact')
def weather_impact():
    if analytics.df_vols is None:
        return jsonify({'error': 'Données non disponibles'})
    
    seasonal_delays = analytics.df_vols.groupby('month')['dep_delay'].agg(['mean', 'std']).reset_index()
    seasonal_delays['season'] = seasonal_delays['month'].apply(
        lambda x: 'Hiver' if x in [12, 1, 2] else 
                 'Printemps' if x in [3, 4, 5] else
                 'Été' if x in [6, 7, 8] else 'Automne'
    )
    
    fig = px.box(
        analytics.df_vols.dropna(subset=['dep_delay']),
        x=analytics.df_vols.dropna(subset=['dep_delay'])['month'].apply(
            lambda x: 'Hiver' if x in [12, 1, 2] else 
                     'Printemps' if x in [3, 4, 5] else
                     'Été' if x in [6, 7, 8] else 'Automne'
        ),
        y='dep_delay',
        title="Impact Saisonnier sur les Retards",
        labels={'x': 'Saison', 'dep_delay': 'Retard (minutes)'}
    )
    
    fig.update_layout(height=400)
    
    return json.dumps(fig, cls=PlotlyJSONEncoder)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)