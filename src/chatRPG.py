import pytchat
import threading
import random
from currentUser import CurrentUser
from voice_manager import TTSManager
from user_pool import Pool
from datetime import datetime, timedelta
from flask import Flask, render_template
from flask_socketio import SocketIO

chat = pytchat.create(video_id="fG_DN3QJoAA")
app = Flask(__name__)
socketio = SocketIO
socketio = SocketIO(app, async_mode='threading')
date_format = '%Y-%m-%d %H:%M:%S'
tts_manager = TTSManager()
current_users = {}
#current_user = CurrentUser()
pool = Pool()

@app.route("/")
def home():
    return render_template('index.html') #redirects to index.html in templates folder

@socketio.event
def connect(): #when socket connects, send data confirming connection
    socketio.emit('message_send', {'message': "Conected!", 'current_user': "User"})

@socketio.on("tts")
def toggletts(value):
    if value['user'].lower() in current_users.keys():
        current_users[value['user'].lower()] = CurrentUser(tts_enabled= value['checked'])
        print(f"TTS: received the value " + str(value['checked']))

@socketio.on("pickrandom")
def pickRandom():
    randomUser()

@socketio.on("choose")
def chooseuser(value):
    user = value.get('choosen_user', 'User Not Found!')
    try:
        current_users[user] = CurrentUser()
    except Exception as e:
        print(f"{e}")
    socketio.emit('message_send',
        {'message': f'{user} was picked!',
        'current_user' :f'{user}'})

@socketio.on('voicename')
def choose_voice_name(value):
    if value['user'].lower() in current_users.keys():
        current_users[value['user'].lower()] = CurrentUser(voice_name = value['voice_name'])
        print('update voice name to: ' + value['voice_name'])

def getUsers():
    
    while chat.is_alive():
        for c in chat.get().sync_items():
            if c.author.name.lower() in current_users.keys():
                user = c.author.name.lower()
                current_users[user] = CurrentUser(message=c.message)
                socketio.emit('message_send',
                            {'message': f"{current_users[user].message}",
                            'current_user': f"{user}"})
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
    print(f'chat closed.')

def randomUser():
    try:
        user_pool = list(pool.user_pool.keys())
        user = random.choice(user_pool)
        current_users[user] = CurrentUser()
        pool.user_pool.pop(user)
        socketio.emit('message_send',
                    {'message': f'{user} foi selecionado!',
                    'current_user' :f'{user}'})
        print(f'random user is: ' + user)
    except Exception as e:
        print(f'cant get random user: {e}')
        return
    
def update_voice_name(user, voice_name):
    current_users[user] = CurrentUser(voice_name = voice_name)

def create_current_user(user_name):
    return type(user_name, (object,), {'tts_enabled': True, 'voice_name': 'random', 'message': None})

if __name__ == '__main__':
        getUser_thread = threading.Thread(target=getUsers)
        getUser_thread.start()
        socketio.run(app)