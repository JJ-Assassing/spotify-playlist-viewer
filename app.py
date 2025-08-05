from flask import Flask, request, jsonify
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

# Autenticación con Spotify
client_credentials_manager = SpotifyClientCredentials(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET")
)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Ruta raíz
@app.route('/')
def home():
    return "API de FJ MUSIC funcionando correctamente."

# Ruta de búsqueda
@app.route('/search')
def search():
    query = request.args.get('query', '')
    if not query:
        return jsonify({'error': 'Falta el parámetro "query".'}), 400

    results = sp.search(q=query, type='track', limit=5)
    canciones = []

    for item in results['tracks']['items']:
        canciones.append({
            'nombre': item['name'],
            'artista': item['artists'][0]['name'],
            'imagen': item['album']['images'][0]['url'],
            'preview': item['preview_url'],
            'spotify_url': item['external_urls']['spotify']
        })

    return jsonify(canciones)

if __name__ == '__main__':
    app.run(debug=True)
