from flask import Flask, redirect, request, session, url_for, render_template
import spotipy
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)
app.secret_key = "juan_mi_clave_secreta_segura_2025"  # Clave

# Configuración de Spotify
SPOTIPY_CLIENT_ID =3 "2d71154243c54cc7a11bdfd0e1c577df"
SPOTIPY_CLIENT_SECRET = "1338c63f5c3a4a6aa6ef5fb57674907e"
SPOTIPY_REDIRECT_URI = "https://localhost:5000/callback"

SCOPE = "user-library-read playlist-read-private"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    sp_oauth = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                            client_secret=SPOTIPY_CLIENT_SECRET,
                            redirect_uri=SPOTIPY_REDIRECT_URI,
                            scope=SCOPE)
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    sp_oauth = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                            client_secret=SPOTIPY_CLIENT_SECRET,
                            redirect_uri=SPOTIPY_REDIRECT_URI,
                            scope=SCOPE)
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session["token_info"] = token_info
    return redirect(url_for('playlists'))

@app.route('/playlists')
def playlists():
    token_info = session.get("token_info", None)
    if not token_info:
        return redirect(url_for("login"))

    sp = spotipy.Spotify(auth=token_info['access_token'])
    results = sp.current_user_playlists()

    playlists = []
    for item in results['items']:
        playlists.append({
            'name': item['name'],
            'url': item['external_urls']['spotify']
        })

    return render_template('index.html', playlists=playlists)

if __name__ == '__main__':
    app.run(debug=True)
