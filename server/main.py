from flask import Flask, redirect, render_template, request
import json
from datetime import datetime

app = Flask(__name__)
SCRIPTS = ["Trouble Brewing", "Bad Moon Rising", "Sects and Violets"]

@app.route("/")
def index():
    name = request.args.get("name", "")
    message = request.args.get("message", "")
    current_votes = []
    if name != "":
        current_votes = json.load(open("votes.json", "r"))[name]
    return render_template("index.jinja", available_scripts=SCRIPTS, name=name, message=message, current_votes=current_votes)

@app.route("/vote/", methods=["POST"])
def vote():
    selected_scripts = request.form.getlist("script_checkbox")
    name = request.form.get("name").lower().replace(" ", "") #type:ignore
    print(f"LOG ({datetime.now().strftime('%H:%M:%S')}): {name} voted for {selected_scripts}")

    data = json.load(open("votes.json", "r"))
    data[name] = selected_scripts
    json.dump(data, open("votes.json", "w"), indent=4)
    
    return redirect(f"/?name={name}&message=Your+vote+has+been+cast%21")

@app.route("/scripts/<string:script_name>/")
def script(script_name: str):
    return redirect(f"https://raw.githubusercontent.com/nathan3-14/botc/refs/heads/main/scripts/{script_name}/{script_name}.png")

@app.route("/results/")
def results():
    vote_totals = {}
    for _voter, votes in json.load(open("votes.json", "r")).items():
        for voted_for_script in votes:
            if voted_for_script in vote_totals.keys():
                vote_totals[voted_for_script] += 1
            else:
                vote_totals[voted_for_script] = 1
    
    vote_totals = dict(sorted(vote_totals.items(), key=lambda item: item[1], reverse=True))
    return render_template("results.jinja", votes=vote_totals)

if __name__ == "__main__":
    app.run(port=8080, debug=True)
