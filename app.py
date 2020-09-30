#Framework for python web
import requests
import flask
from flask import request
from flask import render_template
import json

#The Flask app
app = flask.Flask(__name__)
#app.config["DEBUG"] = True

#Define the routes
@app.route('/', methods=['GET'])
def home():
    print("A request received")
    return "<h1>NBA Stats Website</p>"
    #return render_template("index.html")

resp_header = {
    "meta_data": {
        "author": "Sanje Divakaran",
        "ver": "1.0",
        "site": "NBA stats by Sanje"
    }
}

@app.route('/hello', methods=['GET'])
def hello():
    resp = resp_header
    resp["message"] = "Hello, welcome to NBA stats"
    return resp


@app.route('/teams', methods=['GET'])
def all_teams():
    nba_api = "https://balldontlie.io/api/v1/teams"

    api_resp = requests.get(nba_api)
    #print(resp)

    if api_resp.status_code != 200:
        err_resp = resp_header
        err_resp["message"] = ""
        return err_resp
    else:
        resp = resp_header
        jTeams = api_resp.content.decode('utf-8')
        
        resp["teams"] = json.loads(jTeams) 

        #resp["teams"] = jTeams
        return resp

    
@app.route('/teams/v2', methods=['GET'])
def all_teams_v2():
    nba_api = "https://balldontlie.io/api/v1/teams"

    api_resp = requests.get(nba_api)
    #print(resp)

    if api_resp.status_code != 200:
        err_resp = resp_header
        err_resp["message"] = ""
        return err_resp
    else:
        resp = resp_header
        jTeams = json.loads(api_resp.content.decode('utf-8'))
        
        jt_list = []

        for t in jTeams["data"]:
            print(t["abbreviation"], t["full_name"]) 
            jt = {}
            jt["abbr"] = t["abbreviation"]
            jt["name"] = t["full_name"]
            jt_list.append(jt)

        resp["teams"] = jt_list

        return resp

@app.route('/player/v2/<player_name>', methods=['GET'])
def players_search_v2(player_name):
    nba_api = "https://balldontlie.io/api/v1/players?search=" + player_name

    api_resp = requests.get(nba_api)

    if api_resp.status_code != 200:
        err_resp = resp_header
        err_resp["message"] = ""
        return err_resp
    else:
        resp = resp_header
        jResponse = json.loads(api_resp.content.decode('utf-8'))
        
        jPlayers_list = []

        for t in jResponse["data"]:
            jp = {}
            jp["first_name"] = t["first_name"]
            jp["last_name"] = t["last_name"]
            jp["position"] = t["position"]
            jt = t["team"]
            jp["team"] = jt["full_name"]
            jPlayers_list.append(jp)

        resp["players"] = jPlayers_list
        return resp


app.run()