from flask import Flask, request, redirect, session, render_template
import spotipy
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)
app.secret_key = "clave-secreta"  # Cámbiala por seguridad

# ⚙️ Configuración de tu app de Spotify
CLIENT_ID = "TU_CLIENT_ID"
CLIENT_SECRET = "TU_CLIENT_SECRET"
REDIRECT_URI = "http://localhost:8888/callback"

SCOPE = "user-read-playback-state user-modify-playback-state user-read-currently-playing streaming"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    sp_oauth = SpotifyOAuth(client_id=CLIENT_ID,
                            client_secret=CLIENT_SECRET,
                            redirect_uri=REDIRECT_URI,
                            scope=SCOPE)
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route("/callback")
def callback():
    sp_oauth = SpotifyOAuth(client_id=CLIENT_ID,
                            client_secret=CLIENT_SECRET,
                            redirect_uri=REDIRECT_URI,
                            scope=SCOPE)
    code = request.args.get("code")
    token_info = sp_oauth.get_access_token(code)
    session["token_info"] = token_info
    return redirect("/player")

@app.route("/token")
def get_token():
    token_info = session.get("token_info", None)
    if not token_info:
        return {"error": "No token"}
    return {"access_token": token_info["access_token"]}

@app.route("/player")
def player():
    return render_template("player.html")

if __name__ == "__main__":
    app.run(port=8888, debug=True)
