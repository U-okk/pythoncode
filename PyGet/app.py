import os
from flask import Flask, redirect, url_for, session, render_template, request
import google_auth_oauthlib.flow
from google.oauth2.credentials import Credentials

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your own secret key

CLIENT_SECRETS_FILE = "client_secrets.json"  # Replace with the path to your client_secrets.json
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
TOKEN_FILE = 'token.json'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index')
def login():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if creds and creds.valid:
        return redirect(url_for('welcome'))
    
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES)
    flow.redirect_uri = url_for('callback', _external=True)

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')

    session['state'] = state
    return redirect(authorization_url)

@app.route('/callback')
def callback():
    state = session['state']
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = url_for('callback', _external=True)

    authorization_response = request.url

    # Exchange the authorization code for credentials
    flow.fetch_token(authorization_response=authorization_response)

    creds = flow.credentials

    with open(TOKEN_FILE, 'w') as token:
        token.write(creds.to_json())

    return redirect(url_for('welcome'))

@app.route('/welcome')
def welcome():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if creds and creds.valid:
        return f"<h1>Welcome! You have successfully logged in using Google.</h1>"
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
