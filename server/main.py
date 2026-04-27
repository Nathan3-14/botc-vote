from flask import Flask, redirect, render_template, request, make_response
import json
from datetime import datetime

app = Flask(__name__)
SCRIPTS = json.load(open("options.json", "r"))

@app.route("/")
def index():
    name = request.args.get("name", "")
    message = request.args.get("message", "")
    current_votes = []
    if name != "":
        try:
            current_votes = json.load(open("votes.json", "r"))[name]
        except KeyError:
            pass
    return render_template("index.jinja", available_scripts=SCRIPTS, name=name, message=message, current_votes=current_votes)

@app.route("/vote/", methods=["POST"])
def vote():
    selected_scripts = request.form.getlist("script_checkbox")
    name = request.form.get("name").lower().replace(" ", "") #type:ignore
    print(f"LOG ({datetime.now().strftime('%H:%M:%S')}): {name} voted for {selected_scripts}")

    data = json.load(open("votes.json", "r"))
    data[name] = selected_scripts
    json.dump(data, open("votes.json", "w"), indent=4)
    
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
        return redirect(f"/suggest?message=%27{script_name}%27+suggested")
    else:
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
    return render_template("results.jinja", votes=vote_totals)



@app.route("/scripts/<string:script_name>/")
def script(script_name: str):
    return redirect(f"https://raw.githubusercontent.com/nathan3-14/botc/refs/heads/main/scripts/{script_name}/{script_name}.png")



@app.route("/dev1721/")
def dev():
    return render_template("dev.jinja", message=request.args.get("message", ""))

@app.route("/dev1721/see_vote_json/")
def see_vote_json():
    return make_response(json.load(open("votes.json", "r")))

@app.route("/dev1721/reset_vote_json/")
def reset_vote_json():
    json.dump({}, open("votes.json", "w"))
    return redirect("/dev1721/?message=Vote+json+reset")

@app.route("/dev1721/see_suggest_json/")
def see_suggest_json():
    return make_response(json.load(open("suggested_scripts.json", "r")))

@app.route("/dev1721/reset_suggest_json/")
def reset_suggest_json():
    json.dump([], open("suggested_scripts.json", "w"))
    return redirect("/dev1721/?message=Suggested+json+reset")

if __name__ == "__main__":
    app.run(port=8080, debug=True)
