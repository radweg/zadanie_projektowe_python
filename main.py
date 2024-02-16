import io
from flask import Flask, render_template, request, redirect, url_for, session, send_file
from data import get_data_from_api
import matplotlib.pyplot as plt
import requests

app = Flask(__name__)
app.secret_key = 'super_secret_key'

# Prosta baza danych symulująca użytkowników
users = {'admin': 'admin', 'user': 'admin'}


api_endpoint = get_data_from_api()
df = api_endpoint['WHO']


plot = plt.bar(df.keys(),df.values())
img=io.BytesIO()
plt.savefig(img,format='png')
img.seek(0)
plt.close()

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username in users and users[username] == password:
        session['username'] = username  # Zapisz zalogowanego użytkownika w sesji
        return redirect(url_for('dashboard'))
    else:
        return 'Błędne dane logowania. Spróbuj ponownie.'

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        username = session['username']

        try:
            return send_file(img,mimetype='image/png')
        except requests.RequestException as e:
            return f'Błąd podczas pobierania danych z API: {str(e)}'
    else:
        return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)