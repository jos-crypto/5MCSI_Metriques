from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)                                                                                                                  

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
    return jsonify(results=results) # extraire uniquement les dates et température du jour

@app.route("/api/commits/")
def commits_api():
    url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"
    response = urlopen(url)
    raw = response.read()
    commits = json.loads(raw.decode("utf-8"))

    minutes = {}

    for commit in commits:
        date = commit.get("commit", {}).get("author", {}).get("date")
        if date:
            minute = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ").minute
            minutes[minute] = minutes.get(minute, 0) + 1

    results = []
    for minute in sorted(minutes):
        results.append({
            "minute": str(minute),
            "count": minutes[minute]
        })

    return jsonify(results=results)

# ---------- PAGE COMMITS ----------
@app.route("/commits/")
def commits():
    return render_template("commits.html")
  
@app.route("/histogramme/")
def monhistogramme():
    return render_template("histogramme.html") # histogramme

  
@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html") # route pour graphique html
  
@app.route("/contact/")
def contact():
    return render_template("contact.html")
  
@app.route('/')
def hello_world():
    return render_template('hello.html') # comm2
if __name__ == "__main__":
  app.run(debug=True)
