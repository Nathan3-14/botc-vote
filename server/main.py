import os
from typing import Literal
from flask import Flask, redirect, render_template, request, make_response, send_file
import json
from datetime import datetime

app = Flask(__name__)
SCRIPT_FILE = "options/3_overlaps.json"
SCRIPTS = json.load(open(SCRIPT_FILE, "r"))

def log(message: str, type: Literal["error", "info", "warn"]="info") -> None:
    now = datetime.now()
    year = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")
    message_formatted = f"[{type}] {time} - {message}"
    
    if not os.path.exists("logs"):
        os.mkdir("logs")
    open(f"logs/{year}.log", "a").write(message_formatted + "\n")
    
    print(message_formatted)

@app.route("/")
def index():
    name = request.args.get("name", "")
    current_votes = []
    if name != "":
        try:
            current_votes = json.load(open("votes.json", "r"))[name]
        except KeyError:
            pass
    return render_template("index.jinja", available_scripts=SCRIPTS, name=name, current_votes=current_votes, message=request.args.get("message", ""))

@app.route("/vote/", methods=["POST"])
def vote():
    selected_scripts = request.form.getlist("script_checkbox")
    name = request.form.get("name").lower().replace(" ", "") #type:ignore

    data = json.load(open("votes.json", "r"))
    data[name] = selected_scripts
    json.dump(data, open("votes.json", "w"), indent=4)
    
    log(f"{name} voted for {selected_scripts}")
    return redirect(f"/?name={name}&message=Your+vote+has+been+cast%21%20You+can+change+it+below.")

@app.route("/suggest/", methods=["GET", "POST"])
def suggest():
    method = request.method
    if method == "GET":
        return render_template("suggest.jinja", message=request.args.get("message", ""))
    elif method == "POST":
        script_name = request.form.get("suggestion")
        script_name_fixed = script_name.lower().replace(" ", "_") #type:ignore
        scripts = set(json.load(open("suggested_scripts.json", "r")))
        scripts.add(script_name_fixed)
        json.dump(list(scripts), open("suggested_scripts.json", "w"))
        
        log(f"{script_name} was suggested")
        return redirect(f"/suggest?message=%27{script_name}%27+suggested")
    else:
        log(f"Method {method} was used on /suggest/", "error")
        return redirect(f"/?message=Incorrect+method+for+%2Fsuggest%2F+%28{method}%29")

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

    return render_template("results.jinja", votes=vote_totals, message=request.args.get("message", ""))



@app.route("/scripts/<string:script_name>/")
def script(script_name: str):
    return redirect(f"https://raw.githubusercontent.com/nathan3-14/botc/refs/heads/main/scripts/{script_name}/{script_name}.png")



@app.route("/dev1721/")
def dev():
    log("Dev page accessed", "warn")
    return render_template("dev.jinja", message=request.args.get("message", ""))



@app.route("/dev1721/vote_json")
def vote_json():
    log("Vote JSON accessed", "warn")
    raw_json = json.load(open("votes.json", "r"))
    formatted_json = json.dumps(raw_json, indent=4)
    return render_template("dev_vote_json.jinja", vote_json=formatted_json, message=request.args.get("message", ""))

@app.route("/dev1721/vote_json/download")
def download_vote_json():
    return send_file("votes.json")

@app.route("/dev1721/vote_json/reset")
def reset_vote_json():
    json.dump({}, open("votes.json", "w"))
    log("Vote JSON reset", "warn")
    return redirect("/dev1721/vote_json?message=Vote+JSON+Succesfully+Reset")



@app.route("/dev1721/suggest_json")
def suggets_json():
    log("Suggest JSON accessed", "warn")
    raw_json = json.load(open("suggested_scripts.json", "r"))
    formatted_json = json.dumps(raw_json, indent=4)
    return render_template("dev_suggest_json.jinja", suggest_json=formatted_json, message=request.args.get("message", ""))

@app.route("/dev1721/suggest_json/download")
def download_suggest_json():
    return send_file("suggested_scripts.json")

@app.route("/dev1721/suggest_json/reset")
def reset_suggest_json():
    json.dump({}, open("suggested_scripts.json", "w"))
    log("Suggest JSON reset", "warn")
    return redirect("/dev1721/suggest_json?message=Suggest+JSON+Succesfully+Reset")



@app.route("/dev1721/logs")
def access_logs():
    log("Logs list accessed", "warn")
    return render_template("logs.jinja", logs=os.listdir("logs"), message=request.args.get("message", ""))

@app.route("/dev1721/logs/get/<string:log_file>")
def access_log(log_file: str):
    log(f"{log_file} accessed", "warn")
    return make_response(open(f"logs/{log_file}", "r").read().replace("\n", "<br>"))

@app.route("/dev1721/logs/reset/<string:log_file>")
def reset_log(log_file: str):
    open(f"logs/{log_file}", "w").close()
    log(f"{log_file} reset", "warn")
    return redirect(f"/dev1721/logs?message={log_file}+reset+successfully")



if __name__ == "__main__":
    app.run(port=8080, debug=True)
