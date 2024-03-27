from flask import Flask, request, send_file, render_template, redirect, url_for, after_this_request, flash, session
import requests
import re
import os

app = Flask(__name__)
app.secret_key = 'Alohomora1!@#'

def extract_project_id(url):
    pattern = re.compile(r"/show/([A-Za-z0-9]+)")
    match = pattern.search(url)
    return match.group(1) if match else None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        auth_url = "https://cloud.memsource.com/web/api2/v1/auth/login"
        credentials = {"userName": username, "password": password}
        response = requests.post(auth_url, json=credentials)

        if response.status_code == 200:
            session['access_token'] = response.json().get("token")
            flash('You were successfully logged in')
            return redirect(url_for('index'))
        else:
            flash("Fail to authenticate. Please, enter your credentials again")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('access_token', None)
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'access_token' not in session:
        flash('User not authenticated. Returning to login')
        return redirect(url_for('login'))
    
    flash('URL page')
    
    if request.method == 'POST':
        user_url = request.form['url']
        project_id = extract_project_id(user_url)
        if not project_id:
            flash("Project ID not found in URL.")
            return render_template('index.html')

        access_token = session['access_token']

        get_list_analyses_project = f"https://cloud.memsource.com/web/api2/v3/projects/{project_id}/analyses"
        headers = {"Authorization": f"ApiToken {access_token}"}
        response = requests.get(get_list_analyses_project, headers=headers)
        if response.status_code != 200:
            flash("Failed to retrieve project information.")
            return render_template('index.html')

        analyses = response.json().get("content")
        analyseUid = analyses[0]['uid'] if analyses else None  
        if not analyseUid:
            flash("AnalyseUid not found.")
            return render_template('index.html')

        download_analysis = f"https://cloud.memsource.com/web/api2/v1/analyses/{analyseUid}/download?format=csv"
        response = requests.get(download_analysis, headers=headers, stream=True)
        if response.status_code == 200:
            file_path = "analysis.csv"
            with open(file_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)

            @after_this_request
            def cleanup(response):
                try:
                    os.remove(file_path)
                except Exception as error:
                    app.logger.error("Error removing downloaded file.", error)
                return response

            return send_file(file_path, as_attachment=True)
        else:
            flash("Failed to download analysis.")
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
