import pytchat
import threading
import random
from currentUser import CurrentUser
from voice_manager import TTSManager
from user_pool import Pool
from datetime import datetime, timedelta
from flask import Flask, render_template
from flask_socketio import SocketIO

chat = pytchat.create(video_id="0ZpNYS6NRkk")
app = Flask(__name__)
socketio = SocketIO
socketio = SocketIO(app, async_mode='threading')
date_format = '%Y-%m-%d %H:%M:%S'
tts_manager = TTSManager()
current_users = {}
pool = Pool()

@app.route("/")
def home():
    return render_template('index.html') #redirects to index.html in templates folder

@socketio.event
def connect(): #when socket connects, send data confirming connection
    sendMessage('User', 'Conected!')

@socketio.on("choose")
def chooseuser(value):
    chooseUser(value.get('choosen_user', 'User Not Found!'))
    
@socketio.on("pickrandom")
def pick_Random():
    randomUser()

@socketio.on("tts")
def toggle_tts(value):
    updateTts(value['user'], value['checked'])

@socketio.on('voicename')
def choose_voice_name(value):
    updateVoiceName(value['user'], value['voice_name'])

def getUsers():
    while chat.is_alive():
        for c in chat.get().sync_items():
            if c.author.name.lower() in current_users.keys():
                user = c.author.name.lower()
                current_users[user] = CurrentUser(message=c.message)
                sendMessage(user, current_users[user].message)
                if current_users[user].tts_enabled:
                    tts_manager.text_to_audio(current_users[user].message, current_users[user].voice_name)

            if c.message:
                if c.author.name.lower() in pool.user_pool:
                    pool.user_pool.pop(c.author.name.lower())
                pool.user_pool[c.author.name.lower()] = datetime.strptime(c.datetime, date_format)
                activity_threshold = datetime.now() - timedelta(seconds = pool.seconds_active)
                oldest_user = list(pool.user_pool.keys())[0]
                if pool.user_pool[oldest_user] < activity_threshold or len(pool.user_pool) > pool.max_users:
                    pool.user_pool.pop(oldest_user)
                    if len(pool.user_pool) == pool.max_users:
                        print(f"{oldest_user} was popped due to hitting max users")
                    else:
                        print(f"{oldest_user} was popped due to not talking for {pool.seconds_active} seconds")
            print(f'{pool.user_pool}')
    print(f'chat closed.')

def chooseUser(user):
    try:
        if user in current_users.keys():
            selectedUser(user, f'{user} foi selecionado!')
        else:
            current_users[user] = CurrentUser()
            newUser(user, f'{user} foi selecionado!')
        print(f'usuário selecionado foi: ' + user)
    except Exception as e:
        print(f"{e}")
        return

def randomUser():
    try:
        user = random.choice(list(pool.user_pool.keys())) 
        if user in current_users.keys():
            selectedUser(user, f'{user} foi selecionado!')
        else:
            current_users[user] = CurrentUser()
            newUser(user, f'{user} foi selecionado!')
        print(f'usuário randomizado foi: ' + user)
    except Exception as e:
        print(f'cant get random user: {e}')
        return

def updateTts(user, checked):
    if user.lower() in current_users.keys():
        current_users[user.lower()] = CurrentUser(tts_enabled= checked)
        print(f"TTS: received the value " + str(checked))

def updateVoiceName(user, voice_name):
    if user.lower() in current_users.keys():
        current_users[user.lower()] = CurrentUser(voice_name = voice_name)
        print('update voice name to: ' + voice_name)

def newUser(user, message):
    socketio.emit('new_user', {
        'user': f'{user}',
        'message': f'{message}'})

def selectedUser(user, message):
    socketio.emit('selected_user', {
        'user': f'{user}',
        'message': f'{message}'})
    
def sendMessage(user, message):
    socketio.emit('message_send', {
        'user': f'{user}',
        'message': f'{message}'})

if __name__ == '__main__':
        getUser_thread = threading.Thread(target=getUsers)
        getUser_thread.start()
        socketio.run(app)