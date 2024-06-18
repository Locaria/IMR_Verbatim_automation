import requests
from datetime import datetime
import pandas as pd
from creds import *
import time
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

#Phrase connection
url = "https://cloud.memsource.com/web/api2/v1/auth/login"
credentials = {
    "userName": username,
    "password": password
}

# Função para autenticar e obter o token
def get_auth_token():
    url = "https://cloud.memsource.com/web/api2/v1/auth/login"
    credentials = {
        "userName": username,
        "password": password
    }

    response = requests.post(url, json=credentials)

    print("Auth response status code:", response.status_code)
    print("Auth response text:", response.text)

    if response.status_code == 200:
        token_info = response.json()
        access_token = token_info.get("token")
        print("Authentication token:", access_token)
        return access_token
    else:
        print("Failed to authenticate. Status code:", response.status_code)
        print("Response:", response.text)
        raise SystemExit

#Getting auth token
access_token = get_auth_token()

#sleep time
time.sleep(1)

# # Verificar se o token está correto
# print("Using token:", access_token)

# Config auth headers
headers = {
    "Authorization": f"Bearer {access_token}"
}

# # Log dos cabeçalhos para depuração
# print("Authorization headers:", headers)
# projects URL
get_projects_url = "https://cloud.memsource.com/web/api2/v1/projects"
print("Projects URL:", get_projects_url)
headers = {
    "Authorization": f"ApiToken {access_token}"
}
# Function to access all projects from HarrisPoll - via Phrase API
def get_projects_by_client(client_name):
    projects_list = []
    page_number = 0
    page_size = 50  # Ajuste conforme necessário

    while True:
        projects_url = f"https://cloud.memsource.com/web/api2/v1/projects?pageNumber={page_number}&pageSize={page_size}&clientName={client_name}"
        projects_response = requests.get(projects_url, headers=headers)

        if projects_response.status_code == 200:
            projects_data = projects_response.json().get('content')
            if not projects_data:
                break
            projects_list.extend(projects_data)
            page_number += 1
        else:
            raise Exception(f"Failed to fetch projects. Status code: {projects_response.status_code}, Response: {projects_response.text}")

    return projects_list

#filtering only 'Harris Poll'
client_name = "Harris Poll"
all_projects_data = get_projects_by_client(client_name)

# Create a dict list with all the data from all client's projects 
projects_list = []
for project in all_projects_data:
    project_dict = {}
    for key, value in project.items():
        if isinstance(value, dict):
            for sub_key, sub_value in value.items():
                project_dict[f"{key}.{sub_key}"] = sub_value
        else:
            project_dict[key] = value
    projects_list.append(project_dict)

#Creating the first dataframe
df = pd.DataFrame(projects_list)
columns_of_interest = [
    'internalId', 'dateCreated', 'id', 'dateDue', 'name', 'type', 
    'client.name', 'status']

#Applying columns to the df
df = df[columns_of_interest]

# Filtering projects from May,24
df['dateCreated'] = pd.to_datetime(df['dateCreated']).dt.tz_localize(None)
df['dateCreated'] = pd.to_datetime(df['dateCreated'])
df = df[df['dateCreated'] >= pd.Timestamp('2024-05-01')]

#Converting to YYYY-MM-DD
df['dateCreated'] = pd.to_datetime(df['dateCreated']).dt.strftime('%Y-%m-%d')
df['dateDue'] = pd.to_datetime(df['dateDue']).dt.strftime('%Y-%m-%d')

#Function to access the AnalysisUID from the projects
def get_analysis_uid(project_id):
    get_list_analyses_project = f"https://cloud.memsource.com/web/api2/v3/projects/{project_id}/analyses"
    response = requests.get(get_list_analyses_project, headers=headers)
    
    if response.status_code == 200:
        analyses_data = response.json()
        if analyses_data and 'content' in analyses_data and analyses_data['content']:
            return analyses_data['content'][0]['uid']
    return None

# Add column 'Analysis_uID' to the DataFrame
df['Analysis_uID'] = df['id'].apply(lambda x: get_analysis_uid(x))

# Function to sum the total words of the analysis -- this is the core of the project - the team will use this sum for the verbatims
def get_analysis_words(analyseUid):
    get_analysis = f"https://cloud.memsource.com/web/api2/v3/analyses/{analyseUid}"
    response = requests.get(get_analysis, headers=headers)
    
    if response.status_code == 200:
        analysis_data = response.json()
        total_words = 0
        if 'analyseLanguageParts' in analysis_data:
            for part in analysis_data['analyseLanguageParts']:
                if 'data' in part:
                    for key in part['data']:
                        if isinstance(part['data'][key], dict) and 'words' in part['data'][key]:
                            total_words += int(part['data'][key]['words'])
        return total_words
    return 0
df['Analysis_word_all'] = df['Analysis_uID'].apply(lambda uid: get_analysis_words(uid) if uid else 0)

#Creating Rules for naming convention -- this convetions were create by the IMR team in order to be able to classify and filter the verbatims for this project
#Funcion to create and classify project order by Master and subproject
def classify_project(name):
    if name.startswith('#'):
        return 'Subproject'
    elif name.startswith('P'):
        return 'Master Project'
    return 'Unknown'  # In case of projects that the convetion wasnt in place yet

# Add the column 'Project_Order' to the DataFrame
df['Project_Order'] = df['name'].apply(classify_project)

# Function to extract and classify the language of the project - using the columns name and project_order to create the classification
def extract_language(name):
    parts = name.split('_')
    if len(parts) >= 4:
        return parts[3]
    return None  #In case the project is still not following the name convetion

# Adding column 'Language' to the DataFrame
df['Language'] = df.apply(lambda row: extract_language(row['name']) if row['Project_Order'] == 'Subproject' else None, axis=1)

# Function to extract and create the column ProjectID
def extract_project_id(name, project_order):
    if project_order == 'Master Project':
        return name.split()[0].split('-')[0].split('_')[0]
    elif project_order == 'Subproject':
        return name.split('_')[1] if len(name.split('_')) > 1 else None
    return None

# Add column 'ProjectID' to the DataFrame
df['ProjectID'] = df.apply(lambda row: extract_project_id(row['name'], row['Project_Order']), axis=1)

# Function to extract project type from project name
def extract_project_type(name):
    if '_MTPE_' in name:
        return 'MTPE'
    elif '_MT_' in name:
        return 'MT'
    return 'Unknown'  #In case the name doesnt have MT or MTPE

# Add column 'Project_Type' to DataFrame
df['Project_Type'] = df['name'].apply(extract_project_type)

# Add a column to support the df ordering
df['Order_Helper'] = df['Project_Order'].apply(lambda x: 0 if x == 'Master Project' else 1)

# Order by 'ProjectID', 'Order_Helper', 'Project_Type' and 'Language'
df = df.sort_values(by=['ProjectID', 'Order_Helper', 'Project_Type', 'Language'])

# Removing support column
df = df.drop(columns=['Order_Helper'])

# reset the index after ordering
df = df.reset_index(drop=True)

# Filtering the df in order to have only the lines where 'Project_Order' is 'Master Project' or 'Project_Type' is 'MTPE' or 'MT'
final_df = df[(df['Project_Order'] == 'Master Project') | (df['Project_Type'].isin(['MTPE', 'MT']))]

# Remove null 'ProjectID' and making sure that 'ProjectID' is str
final_df = final_df.dropna(subset=['ProjectID'])
final_df['ProjectID'] = final_df['ProjectID'].astype(str)

# Add into the filter so we would only have all the projects that start with P - as the naming convention
final_df = final_df[final_df['ProjectID'].str.startswith('P')]

# Cosmetic updates so the Project_Type column will show Master Project instead of Unknown Atualiza o 'Project_Type' 
final_df['Project_Type'] = final_df.apply(
    lambda row: 'Master Project' if row['Project_Type'] == 'Unknown' and row['Project_Order'] == 'Master Project' else row['Project_Type'],
    axis=1
)
# Order the columns according the team request 
final_df = final_df[['ProjectID', 'Project_Type', 'dateCreated', 'name', 'Language', 'Analysis_word_all', 'Project_Order']]
final_df

# Auth and access to G-sheets 
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('C:/Users/yngrid.figlioli/Desktop/AAEE/IMR/verbetim_auto/global-ace-417010-a45b5fe90edc.json', scope)
client = gspread.authorize(creds)

# Open Verbatims G-sheet
spreadsheet_id = '1A7KjZ2sPpIHNI8u5XYqBPBkBaSiVCvqQNjx5YNA_HfQ'
spreadsheet = client.open_by_key(spreadsheet_id)

#Making sure that the final df is correct and ordered
final_df = final_df[['ProjectID', 'Project_Type', 'dateCreated', 'name', 'Language', 'Analysis_word_all', 'Project_Order']]
if final_df.empty:
    print("O DataFrame final_df está vazio.")
else:
    # Filtering first the master projects  - we'll create a tab per master project, according the requested
    if 'Project_Order' in final_df.columns:
        master_projects = final_df[final_df['Project_Order'] == 'Master Project']
    else:
        print("Coluna 'Project_Order' não encontrada no DataFrame")

    # Creting a tab per master project and adding the subprojects, using the Project_ID to match it 
    for _, master_project in master_projects.iterrows():
        project_id = master_project['ProjectID']
        project_name = master_project['name']  

        #Limiting the name of the sheet to 100 caracters, considering its being created like the project name, as requested by the team
        if len(project_name) > 100:
            project_name = project_name[:100]

        #Creating the a new sheet
        new_sheet = spreadsheet.add_worksheet(title=project_name, rows="100", cols="20")

        # Filtering the subprojects with the same ProjectID
        subprojects = final_df[final_df['ProjectID'] == project_id]

        # Converting the subprojects to a list of lists in order to insert them into the G-sheet
        subprojects_list = subprojects.values.tolist()

        #Adding the data for each subproject for each new sheet.
        new_sheet.update('A1', [subprojects.columns.values.tolist()] + subprojects_list)

    print("Sheets criadas com sucesso!")
