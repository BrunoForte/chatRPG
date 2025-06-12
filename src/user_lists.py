import random

class ActiveList():
    def __init__(self, list):
        self.list = list

    def find(self, name):
        return name in self.list
    
    def randomize(self, selected_list):
            selected_user_names = {user.user_name for user in selected_list}
            all_available_names = {item[0] for item in self.list}
            available_names = list(all_available_names - selected_user_names)
            if not available_names:
                print('WARNING: Todos os usuários disponívels já foram selecionados, nenhuma randomização disponivel')
                return None
            return random.choice(available_names)
            
class SelectedList():
    def __init__(self, list):
        self.list = list

    def find(self, name):
        return name in self.list
        
    def changeSelectedUser(self, new_user, old_user):
        self.list[old_user] = new_user