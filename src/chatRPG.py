import pytchat
import threading
from currentUser import CurrentUser, createNewUser, updateUser
from userType import UserType
from voice_manager import TTSManager
from user_lists import ActiveList, SelectedList
from datetime import datetime, timedelta
from flask import Flask, render_template
from flask_socketio import SocketIO

chat = pytchat.create(video_id='4NcJP_FZ1Lk')
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
    sendMessage(CurrentUser('User', message='Conectado!'))

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
            if selected_list.find(c.author.name.lower()):
                user = (c.author.name.lower(), c.message)
                selected_list.insert()
                #sendMessage(user)
                if selected_list[user].tts_enabled:
                    tts_manager.text_to_audio(selected_list[user].message, selected_list[user].voice_name)

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

def chooseUser(user, oldId):
    if oldId:
        selected_list.changeSelectedUser(user, oldId)
        sendMessage(user)
    else:
        selected_list.list.append(user)
        sendMessage(user)
    return

def randomizeUser(oldId):
    user = active_list.randomize(selected_list.list)
    chooseUser(createNewUser(user[0]), oldId)
    return

def updateSelectedUser(user, field, value):
    updateUser(user, field, value)
    
def sendMessage(user):
    if user.user_type == UserType.NEW:
        socketio.emit('new_user', CurrentUser.serialize(user))
    else:
        socketio.emit('message_send', CurrentUser.serialize(user))

if __name__ == '__main__':
        getUser_thread = threading.Thread(target=getUsers)
        getUser_thread.start()
        socketio.run(app)