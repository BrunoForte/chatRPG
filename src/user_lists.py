import random

class ActiveList():
    def __init__(self, list):
        self.list = list

    def find(self, name):
        return name in self.list
    
    def randomize(self, selected_list):
            test = selected_list
            randomized = random.choice(self.list)
            #RANDOMIZAR NÃO REMOVE O QUE JÁ ESTÁ NA LISTA
            if randomized[0] in selected_list:
                randomized = random.choice(self.list)
            return randomized

class SelectedList():
    def __init__(self, list):
        self.list = list

    def find(self, name):
        return name in self.list
        
    def changeSelectedUser(self, new_user, old_user):
        self.list[old_user] = new_user