from src.models import Chat, Message

def create_chat(user_id: int):
    chat = Chat(user_id=user_id)
    # Salvar no banco de dados
    return chat

def get_messages(chat_id: int):
    messages = Message.query.filter(Message.chat_id == chat_id).all()
    return messages
