from Task import Task
from Team import Team
from typing import List
import json

class Game(object):
    def __init__(self, gameid, teams : List[Team], task_config=""):
        self.gameid = gameid
        self.teams = teams
        self.task_config = task_config
        self.tasks = self.load_task_config(self.task_config)
    
    def add_team(self, new_team):
        if new_team is not None:
            self.teams.append(new_team)
    
    def remove_team(self, team_name):
        # If we're really looking for a team
        if team_name is not None and team_name != "":
            # Loop through the teams
            for team in self.teams:
                # And check their names. If we found it
                if team.name == team_name:
                    # Remove that team
                    self.teams.remove(team)
    
    def award_task(self, team_name : str, task_name : str, submission):
        # Find the task to remove
        for current_task in self.tasks:
            if current_task.name == task_name:
                # Find the team to award points to
                for current_team in self.teams:
                    if current_team.name == team_name:
                        current_team.add_task(current_task, submission)
    
    def get_team_id(self, team_name):
        counter = 0
        for team in self.teams:
            if counter >= len(self.teams):
                return -1
            if team.name == team_name:
                return counter
            counter += 1
                    
    def load_task_config(self, task_config_file) -> List[Task] :
        tasks = []
        if task_config_file != "":
            with open(task_config_file, "r") as f:
                # Read file
                file_data = f.read()
                # Convert to JSON
                task_info = json.loads(file_data)["tasks"]
                # Loop through JSON objects
                for task in task_info:
                    tasks.append(
                        # Create each task and add to list
                        Task(task["name"],
                                task["description"],
                                int(task["points"]),
                                len(tasks)
                    ))
                f.close()
            # Send list of Task objects back
        return tasks

    def team_to_json(self, id):
        return {
            "name": self.teams[id].name, 
            "points": self.teams[id].points
        }
    def teams_to_json(self):
        teams_json = []
        for i in range(len(self.teams)):
            teams_json.append(self.team_to_json(i))
        return teams_json
    
    def get_team_names(self) -> List[str]:
        names = []
        for team in self.teams:
            names.append(team.name)
        return names
    
    def task_to_json(self, id):
        return {
            "name": self.tasks[id].name, 
            "description": self.tasks[id].description, 
            "points": self.tasks[id].points,
            "id": self.tasks[id].id
        }
        
        
    def tasks_to_json(self) -> str: 
        message = {"tasks": []}
        for task in self.tasks:
            message["tasks"].append(
                {"name": task.name, 
                 "description": task.description, 
                 "points": task.points,
                 "id": task.id
                })
        return message
    
    def __str__(self):
        message = "Game: " + self.gameid + "\nTeams:\n"
        for team in self.teams:
            message += " - " + str(team) + "\n"
        message += "\nTasks:\n"
        for task in self.tasks:
            message += " - " + str(task) + "\n"
        return message