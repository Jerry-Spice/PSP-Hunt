from Task import Task


class Team(object):
    def __init__(self, name, points=0):
        self.name = name
        self.points = points
        self.tasks_completed = []
        self.submissions = []
    
    def __str__(self):
        return "*" + self.name + "* (" + str(self.points) +")"
    
    def add_task(self, task : Task, submission):
        # If the submissions and the task exist
        if submission is not None and task is not None:
            # Add it and add the points
            self.tasks_completed.append(task)
            self.submissions.append(submission)
            self.points += task.points

    # Return a task and submission for this team
    # [task, submission]
    def get_task(self, id):
        if id < 0 or id >= len(self.tasks_completed):
            return None
        return [self.tasks[id], self.submissions[id]]
    
    