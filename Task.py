class Task(object):
    def __init__(self, name, description, points, id):
        self.name = name
        self.description = description
        self.points = points
        self.id = id
    
    def __str__(self):
        return str(self.id) + " ~ *" + self.name + "* (" + str(self.points) + ")\n -> " + self.description + ""
    
    def toHTML(self):
        return "<div class=\"task\"><div class=\"row-aligned\"><h1 class=\"title\">" + self.name + "</h1> <h2 class=\"points\">" + str(self.points) + "</h2></div><p class=\"description\">" + self.description + "</p></div>"