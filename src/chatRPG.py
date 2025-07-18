import pytchat
import threading
from currentUser import CurrentUser, createNewUser, updateUser
from voice_manager import TTSManager
from user_lists import ActiveList, SelectedList
from datetime import datetime, timedelta
from flask import Flask, render_template
from flask_socketio import SocketIO

chat = pytchat.create(video_id='bHI-5OUa2CU')
app = Flask(__name__)
socketio = SocketIO
socketio = SocketIO(app, async_mode='threading')
date_format = '%Y-%m-%d %H:%M:%S'
tts_manager = TTSManager()
selected_list = SelectedList([])
active_list = ActiveList([])
seconds_active=60
max_users = 50

@app.route('/')
def home():
    return render_template('index.html') #redirects to index.html in templates folder

@socketio.event
def connect(): #when socket connects, send data confirming connection
    socketio.emit('message_send', {'message': "Conecteado!", 'user': "User"})

@socketio.on('choose')
def chooseuser(value):
    chooseUser(value.get('choosen_user', 'User Not Found!'), value['old_id'])
    
@socketio.on('pickrandom')
def pick_Random(value):
    randomizeUser(value['old_id'])

@socketio.on('tts')
def toggle_tts(value):
    updateUser(value['user'], 'tts', value['checked'])

@socketio.on('voicename')
def choose_voice_name(value):
    updateUser(value['user'], 'voice', value['voice_name'])

def getUsers():
    while chat.is_alive():
        for c in chat.get().sync_items():
            for sublista in selected_list.list:
                if sublista.user_name == c.author.name.lower():
                    user = updateUser(sublista, 'message', c.message)
                    #selected_list.changeSelectedUser(user, selected_list.list.index(user))
                    socketio.emit('update_user', CurrentUser.serialize(user, selected_list.list.index(user)))
                    if user.tts_enabled:
                        tts_manager.text_to_audio(user.message, user.voice_name)
                    
            if c.message:
                if active_list.find(c.author.name.lower()):
                    active_list.list.remove(c.author.name.lower())
                active_list.list.append([c.author.name.lower(), datetime.strptime(c.datetime, date_format)])
                activity_threshold = datetime.now() - timedelta(seconds = seconds_active)
                oldest_user = active_list.list[0]
                if active_list.list[0][1] < activity_threshold or len(active_list.list) > max_users:
                    active_list.list.remove(oldest_user)
                    if len(active_list.list) == max_users:
                        print(oldest_user)
                        print(f'{oldest_user} was popped due to hitting max users')
                    else:
                        print(f'{oldest_user} was popped due to not talking for {seconds_active} seconds')
            print(f'{active_list.list}')
    print(f'chat closed.')

def chooseUser(user, old_id):
    if old_id.isdigit():
        selected_list.changeSelectedUser(user, int(old_id))
        socketio.emit('update_user', CurrentUser.serialize(user, old_id))
    else:
        selected_list.list.append(user)
        socketio.emit('new_user', CurrentUser.serialize(user, selected_list.list.index(user)))
    return

def randomizeUser(old_id):
    if len(active_list.list):
        user = active_list.randomize(selected_list.list)
        if user is not None:
            chooseUser(createNewUser(user), old_id)
        else:
            return print(f'Nenhuma randomização disponivel')
    else:
        return print(f'Não é possível randomizar de uma lista vazia')

def updateSelectedUser(user, field, value):
    updateUser(user, field, value)

if __name__ == '__main__':
        getUser_thread = threading.Thread(target=getUsers)
        getUser_thread.start()
        socketio.run(app)