from flask import Flask, request, send_file, render_template, redirect, url_for
import requests
import re
from creds import *

app = Flask(__name__)

def extract_project_id(url):
    pattern = re.compile(r"/show/([A-Za-z0-9]+)")
    match = pattern.search(url)
    return match.group(1) if match else None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_url = request.form['url']
        project_id = extract_project_id(user_url)
        
        # Aqui você coloca a lógica que já foi descrita anteriormente para fazer o login, obter o analyseUid e baixar o arquivo
        # Substitua esta parte com o código do processo descrito anteriormente
        
        return send_file("analysis.csv", as_attachment=True)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

