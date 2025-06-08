import pytchat
import pytz
import asyncio
from datetime import datetime, timedelta
from flask import Flask, render_template
from flask_socketio import SocketIO, emit


chat = pytchat.create(video_id="mIr5aD27FH0")
app = Flask(__name__)
socketio = SocketIO(app, async_mode='threading')
user_pool = {}

class Bot():
    user_pool = {}
    current_user = None
    author_name = None
    message = None
    seconds_active=60
    max_users = 50

while chat.is_alive():
    self = Bot()
    for c in chat.get().sync_items():
        if c.author.name == self.current_user:
            socketio.emit('message_send',
                        {'message': f"{c.message}",
                        'current_user': f"{self.current_user}"})
            if self.tts_enabled:
                self.tts_manager.text_to_audio(c.message)

        if c.message:
            if c.author.name.lower() in self.user_pool:
                user_pool.pop(c.author.name.lower())
            self.user_pool[c.author.name.lower()] = c.datetime
            activity_threshold = datetime.now(pytz.utc) - timedelta(seconds = self.seconds_active)
            oldest_user = list(self.user_pool.keys())[0]
            if self.user_pool[oldest_user].replace(tzinfo=pytz.utc) < activity_threshold or len(self.user_pool) > self.max_users:
                self.user_pool.pop(oldest_user)
                if len(self.user_pool) == self.max_users:
                    print(f"{oldest_user} was popped due to hitting max users")
                else:
                    print(f"{oldest_user} was popped due to not talking for {self.seconds_active} seconds")



        print(f"{c.datetime} [{c.author.name}]- {c.message}")
