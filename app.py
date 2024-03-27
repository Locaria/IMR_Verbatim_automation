from flask import Flask, request, send_file, render_template, redirect, url_for, after_this_request
import requests
import re
from creds import username, password  # Assegure-se de que suas credenciais estão importadas corretamente

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
        if not project_id:
            return "Project ID not found in URL.", 400

        # Autenticação e obtenção do token
        auth_url = "https://cloud.memsource.com/web/api2/v1/auth/login"
        credentials = {
            "userName": username,
            "password": password
        }
        response = requests.post(auth_url, json=credentials)
        if response.status_code != 200:
            return "Failed to authenticate.", 401
        access_token = response.json().get("token")

        # Obtenção da lista de análises para extrair o analyseUid
        get_list_analyses_project = f"https://cloud.memsource.com/web/api2/v3/projects/{project_id}/analyses"
        headers = {"Authorization": f"ApiToken {access_token}"}
        response = requests.get(get_list_analyses_project, headers=headers)
        if response.status_code != 200:
            return "Failed to retrieve project information.", 400

        analyses = response.json().get("content")
        analyseUid = analyses[0]['uid'] if analyses else None  # Supondo que você queira o primeiro UID
        if not analyseUid:
            return "AnalyseUid not found.", 400

        # Fazer o download do arquivo de análise
        download_analysis = f"https://cloud.memsource.com/web/api2/v1/analyses/{analyseUid}/download?format=csv"
        response = requests.get(download_analysis, headers=headers)
        if response.status_code != 200:
            return "Failed to download analysis.", 400

        # Salvar o arquivo de análise localmente
        file_path = "analysis.csv"
        with open(file_path, "wb") as file:
            file.write(response.content)

        # Remover o arquivo após o envio
        @after_this_request
        def remove_file(response):
            try:
                os.remove(file_path)
            except Exception as error:
                app.logger.error("Error removing downloaded file.", error)
            return response

        # Enviar o arquivo para o usuário
        return send_file(file_path, as_attachment=True)

    # Mostrar o formulário para submissão da URL
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
