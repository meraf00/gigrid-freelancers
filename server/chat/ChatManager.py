import sys
from model import db, Message, Chat, ContentType
sys.path.append('..')


class ChatManager:
    def __init__(self, user_id: str):
        self.user_id = user_id

    def initiate_chat(self, receiver_id) -> str:
        """
        Create new chat between two users

        receiver_id: the second user in the chat

        Returns: the created chat id
        """
        chat = Chat(user_1=self.user_id, user_2=receiver_id)

        db.session.add(chat)
        db.session.commit()

        return chat.id

    def send_message(self, chat_id, content, content_type=ContentType.TEXT):
        """
        Save message under chat_id

        chat_id: chat containing two users
        sender_id: the user id of sender of the message
        content: the message sent
        content_type: specifies how to interpret the content, (default = 'TEXT')        
        """

        msg = Message(chat_id=chat_id,
                      sender_id=self.user_id,
                      content=content,
                      content_type=content_type)

        db.session.add(msg)
        db.session.commit()
    