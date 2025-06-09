import random
import pytchat
import threading
from voice_manager import TTSManager
from user_pool import Pool
from datetime import datetime, timedelta
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from pytchat import LiveChat, CompatibleProcessor

chat_yt = LiveChat("NYSZeUmjbHA", processor = CompatibleProcessor())
chat = pytchat.create(video_id="NYSZeUmjbHA")
app = Flask(__name__)
socketio = SocketIO
socketio = SocketIO(app, async_mode='threading')
pool = Pool()
date_format = '%Y-%m-%d %H:%M:%S'
current_user = None
tts_enabled = False
tts_manager = TTSManager()

class Pool():
    user_pool = {}
    seconds_active=60
    max_users = 50

@app.route("/")
def home():
    return render_template('index.html') #redirects to index.html in templates folder

@socketio.event
def connect(): #when socket connects, send data confirming connection
    socketio.emit('message_send', {'message': "Conected!", 'current_user': "User"})

@socketio.on("tts")
def toggletts(value):
    print(f"TTS: received the value " + str(value['checked']))
    tts_enabled = value['checked']

@socketio.on("pickrandom")
def pickRandom():
    randomUser()

@socketio.on("choose")
def chooseuser(value):
    current_user = value.get('choosen_user', 'User Not Found!')
    socketio.emit('message_send',
        {'message': f'{current_user} was picked!',
        'current_user' :f'{current_user}'})

@socketio.on('voicename')
def choose_voice_name(value):
    if(value['voice_name']) != None:
        update_voice_name(value['voice_name'])
        print('update voice name to: ' + value['voice_name'])


def getUsers():
    
    while chat.is_alive():
        for c in chat.get().sync_items():
            if c.author.name == current_user:
                socketio.emit('message_send',
                            {'message': f"{c.message}",
                            'current_user': f"{current_user}"})
                if pool.tts_enabled:
                    pool.tts_manager.text_to_audio(c.message)

            if c.message:
                if c.author.name.lower() in pool.user_pool:
                    pool.user_pool.pop(c.author.name.lower())
                pool.user_pool[c.author.name.lower()] = datetime.strptime(c.datetime, date_format)
                activity_threshold = datetime.now() - timedelta(seconds = pool.seconds_active)
                oldest_user = list(pool.user_pool.keys())[0]
                timelimit = pool.user_pool[oldest_user] < activity_threshold
                if pool.user_pool[oldest_user] < activity_threshold or len(pool.user_pool) > pool.max_users:
                    pool.user_pool.pop(oldest_user)
                    if len(pool.user_pool) == pool.max_users:
                        print(f"{oldest_user} was popped due to hitting max users")
                    else:
                        print(f"{oldest_user} was popped due to not talking for {pool.seconds_active} seconds")
                print(f"{pool.user_pool.keys()}")
    print(f'chat closed.')

def randomUser():
    try:
        user_pool = list(pool.user_pool.keys())
        current_user = random.choice(user_pool)
        socketio.emit('message_send',
                    {'message': f'{current_user} was picked!',
                    'current_user' :f'{current_user}'})
        print(f'random user is: ' + current_user)
    except Exception:
        print(f'{pool.user_pool}')
        return
    
def update_voice_name(voice_name):
    tts_manager.update_voice_name(voice_name)

if __name__ == '__main__':
        getUser_thread = threading.Thread(target=getUsers)
        getUser_thread.start()
        socketio.run(app)