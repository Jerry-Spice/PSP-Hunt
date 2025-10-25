from flask import Flask, render_template, request, redirect, url_for
import click

from Game import Game
from Task import Task
from Team import Team

import os

app = Flask(__name__)

game1 = Game("abcdef", [], "./config/tasks.json")

game_running = False

@app.route("/gameover")
def gameover():
    return render_template("gameover.html")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        team_name = request.form["teamname"]
        if team_name == "":
            return render_template("index.html", teams=game1.get_team_names(), invalid_teamname=True)
        if team_name in game1.get_team_names():
            team_id = game1.get_team_id(team_name)
            return redirect( "/" + str(team_id) )    
        game1.add_team(Team(team_name))
        team_id = game1.get_team_id(team_name)
        return redirect( "/" + str(team_id) )
    return render_template("index.html", teams=game1.get_team_names())

@app.route("/<team_id>", methods=["GET", "POST"])
def team_home(team_id):
    current_team_name = game1.get_team_names()[int(team_id)]
    return render_template("index.html", teams=game1.get_team_names(), current_team_name=current_team_name, team_id=team_id, game_running=game_running)


@app.route("/<team_id>/tasks")
def show_tasks(team_id):
    if not game_running:
        return redirect("/gameover")
    completed_tasks = game1.teams[int(team_id)].tasks_completed
    current_tasks = game1.tasks
    team_points = game1.teams[int(team_id)].points
    game2 = Game("00000", [], "")
    for task in current_tasks:
        if task not in completed_tasks:
            game2.tasks.append(task)
    
    return render_template("tasks.html", tasks=game2.tasks_to_json()["tasks"], team_id=team_id, team_points=team_points)

@app.route("/<team_id>/tasks/<id>")
def show_task(team_id, id):
    if not game_running:
        return redirect("/gameover")
    target_task = game1.task_to_json(int(id))
    return render_template("task.html", task=target_task, team_id=team_id, submission_failed=False)

@app.route("/<team_id>/submit/<id>", methods=["GET","POST"])
def submit_task(team_id, id):
    team_name = game1.teams[int(team_id)].name
    task_name = game1.tasks[int(id)].name
    
    if request.method == "POST":
        if "submission" in request.files:
            file = request.files["submission"]
            if file.filename != "":
                filename = team_name.replace(" ","") + "-" + task_name.replace(" ","") + "." + file.filename.split(".")[1]
                file.save(os.path.join("uploads", filename))
                game1.award_task(team_name, task_name, filename)
                return redirect( "/" + str(team_id) + "/tasks" )
    target_task = game1.task_to_json(int(id))
    return render_template("task.html", task=target_task, team_id=team_id, submission_failed=True)

@app.route("/admin")
def admin_login():
    return render_template("adminlogin.html", login_failed=False)

@app.route("/admin/verification", methods=["POST", "GET"])
def admin_verification():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == "jerryspice" and password == "Joshlandia15":
            return redirect("/admin/verified")
    return render_template("adminlogin.html", login_failed=True)

@app.route("/admin/verified")
def admin_verified():
    return render_template("admin.html", game_running=game_running)

@app.route("/admin/verified/toggle_game", methods=["POST", "GET"])
def admin_toggle_game_state():
    global game_running
    game_running = not game_running
    return redirect("/admin/verified")

@app.route("/scoreboard")
def scoreboard():
    teams = game1.teams.copy()
    teams = sorted(teams, key=lambda team: team.points, reverse=True)
    game2 = Game("00000", teams)
    return render_template("scoreboard.html", teams=game2.teams_to_json())
    
    


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
    