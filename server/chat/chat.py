import os
import sys
from typing import Optional

from flask import Blueprint, render_template, request, url_for, redirect, jsonify
from flask_login import login_required, current_user

from flask_socketio import SocketIO, join_room

from model import User, Chat, Message
from auth import AuthenticationManager
from .ChatManager import ChatManager

sys.path.append('..')

chat_bp = Blueprint('chat_bp', __name__,
                    static_folder='static', template_folder='templates')

socketio = SocketIO()


def load_user(token: str) -> Optional[User]:
    auth_manager = AuthenticationManager(os.getenv('FLASK_SECRET_KEY'))
    user_id = auth_manager.verify_token(token)
    if user_id:
        user = User.get(user_id)
        if user.token == token:
            return user


@chat_bp.route('/')
def message():
    return render_template('messages.html')


@chat_bp.route('/', methods=['POST'])
def get_messages():
    user_token = request.json.get("authentication_token")
    user = load_user(user_token)

    if not user:
        return ""

    chat_id = request.json.get('chat_id')
    chat = Chat.get(chat_id)

    if not chat:
        return ""

    result = []
    for message in chat.messages:
        print(type(message.time_stamp))
        result.append({
            "id": message.id,
            "content": message.content,
            "content_type": message.content_type,
            "timestamp": message.time_stamp,
            "sent": user.id == message.sender_id
        })

    return jsonify(result)


@ socketio.on('join')
def handle_join(data):
    token = data.get('authentication_token', '')
    user = load_user(token)

    if user:
        chat_ids = [chat.id for chat in user.chats]

        for chat_id in chat_ids:
            join_room(chat_id)
        join_room(user.id)

        socketio.emit('online_announcement',
                      {
                          'user_id': user.id
                      },
                      rooms=chat_ids)


@ socketio.on('send_message')
def handle_message(data):
    token = data.get('authentication_token', '')
    user = load_user(token)

    if not user:
        return

    message = data["message"]
    chat_id = data['chat_id']

    chat = Chat.get(int(chat_id))
    chat_mgr = ChatManager(user.id)

    if not chat:
        return

    chat_mgr.send_message(chat_id, message)
    socketio.emit('receive_message',
                  {
                      'chat_id': chat_id,
                      'from': user.id,
                      'message': message
                  },
                  rooms=chat_id)
