from flask import Flask, render_template, jsonify
import pandas as pd
import os
from pathlib import Path
from datetime import datetime

app = Flask(__name__)

# Configuration
EXCEL_FOLDER = 'data'  # Répertoire où vous déposez vos fichiers Excel
ALLOWED_EXTENSIONS = {'.xlsx', '.xls'}

def get_latest_excel_file():
    """Trouve le fichier Excel le plus récent dans le répertoire"""
    if not os.path.exists(EXCEL_FOLDER):
        os.makedirs(EXCEL_FOLDER)
        return None
    
    excel_files = [
        f for f in Path(EXCEL_FOLDER).iterdir()
        if f.suffix.lower() in ALLOWED_EXTENSIONS
    ]
    
    if not excel_files:
        return None
    
    # Retourne le fichier le plus récent basé sur la date de modification
    return max(excel_files, key=lambda f: f.stat().st_mtime)

def read_excel_data(file_path):
    """Lit le fichier Excel et retourne les données"""
    try:
        df = pd.read_excel(file_path)
        # Convertit les NaN en chaînes vides pour l'affichage
        df = df.fillna('')
        # Convertit les dates en format string lisible
        for col in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                df[col] = df[col].dt.strftime('%Y-%m-%d')
        return df
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier: {e}")
        return None

@app.route('/')
def index():
    """Page principale"""
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    """API pour récupérer les données Excel"""
    latest_file = get_latest_excel_file()
    
    if latest_file is None:
        return jsonify({
            'error': 'Aucun fichier Excel trouvé',
            'message': f'Veuillez déposer un fichier Excel dans le répertoire "{EXCEL_FOLDER}"'
        }), 404
    
    df = read_excel_data(latest_file)
    
    if df is None:
        return jsonify({
            'error': 'Erreur de lecture',
            'message': 'Impossible de lire le fichier Excel'
        }), 500
    
    # Informations sur le fichier
    file_info = {
        'filename': latest_file.name,
        'modified': datetime.fromtimestamp(latest_file.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
        'rows': len(df),
        'columns': list(df.columns)
    }
    
    return jsonify({
        'file_info': file_info,
        'data': df.to_dict(orient='records')
    })

if __name__ == '__main__':
    # Crée le répertoire data s'il n'existe pas
    os.makedirs(EXCEL_FOLDER, exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)
