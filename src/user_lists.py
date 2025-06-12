import random

class ActiveList():
    def __init__(self, list):
        self.list = list

    def find(self, name):
        return name in self.list
    
    def randomize(self, selected_list):
        while True:
            randomized = random.choice(self.list)
            if randomized not in selected_list:
                return randomized

class SelectedList():
    def __init__(self, list):
        self.list = list

    def find(self, name):
        return name in self.list
        
    def changeSelectedUser(self, newUser, oldUser):
        self.list[oldUser] = newUser