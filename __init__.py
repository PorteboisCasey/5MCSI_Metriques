from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html') 
  
@app.route("/contact/")
def MaPremiereAPI():
    return render_template('contact.html')

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def monhistogramme():
    return render_template("histogramme.html")

@app.route('/commits-data/')
def get_commits_data():
    try:
        print("Tentative de récupération des commits...")
        response = urlopen('https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits')
        raw_content = response.read()
        json_content = json.loads(raw_content.decode('utf-8'))
        print(f"Nombre de commits récupérés : {len(json_content)}")
        
        # Créer un dictionnaire pour compter les commits par minute
        commits_by_minute = {}
        
        for commit in json_content:
            date_string = commit['commit']['author']['date']
            print(f"Date du commit : {date_string}")
            date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
            minute_key = f"{date_object.hour:02d}:{date_object.minute:02d}"
            
            if minute_key in commits_by_minute:
                commits_by_minute[minute_key] += 1
            else:
                commits_by_minute[minute_key] = 1
        
        # Convertir en liste pour le graphique
        results = [{'minute': k, 'count': v} for k, v in sorted(commits_by_minute.items())]
        print(f"Données formatées : {results}")
        return jsonify(results=results)
    except Exception as e:
        print(f"Erreur : {str(e)}")
        return jsonify(error=str(e)), 500

@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
        date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
        minutes = date_object.minute
        return jsonify({'minutes': minutes})

@app.route("/commits/")
def commits_graph():
    return render_template("commits.html")
  
if __name__ == "__main__":
  app.run(debug=True)
#commit
