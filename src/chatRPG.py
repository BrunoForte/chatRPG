import asyncio
import pytchat
import threading
from user_pool import Pool
from datetime import datetime, timedelta
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from pytchat import LiveChat, CompatibleProcessor

chat_yt = LiveChat("qRULkFO1Z6M", processor = CompatibleProcessor())
chat = pytchat.create(video_id="qRULkFO1Z6M")
app = Flask(__name__)
socketio = SocketIO
socketio = SocketIO(app, async_mode='threading')
pool = Pool()
date_format = '%Y-%m-%d %H:%M:%S'

@app.route("/")
def home():
    return render_template('index.html')

@socketio.on("pickrandom")
def pickrandom():
    GetUsers.randomUser


class GetUsers:
    current_user = None
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

    def randomUser(self):
        try:
            self.current_user = pool.getRandom(pool.user_pool)
            socketio.emit('message_send',
                        {'message': f'{self.current_user} was picked!',
                        'current_user' :f'{self.current_user}'})
            print('random user is: ' + self.current_user)
        except Exception:
            return
        
def startGetUsers():
    global userPool
    asyncio.set_event_loop(asyncio.new_event_loop())
    userPool = GetUsers()
    userPool.run()


if __name__ == '__main__':
        getUser_thread = threading.Thread(target=startGetUsers)
        getUser_thread.start()
        socketio.run(app)