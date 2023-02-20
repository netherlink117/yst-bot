from sender import Sender
from chat import Chat
class Message:
  def __init__(self, message_id: int = None, sender: Sender = Sender(), chat: Chat = Chat(), date: int = None, text: str = None, is_edited: bool = False) -> None:
    self.message_id = message_id
    self.sender = sender
    self.chat = chat
    self.date = date
    self.text = text
    self.is_edited = is_edited

  def from_json(message_json: dict, is_edited_message: bool = False):
    message = Message(message_json["message_id"], is_edited=is_edited_message)
    if "from" in message_json:
      sender = Sender.from_json(message_json["from"])
    elif "sender": # this is for compatibility with updates.json
      sender = Sender.from_json(message_json["sender"])
    else:
      sender = Sender()
    message.sender = sender
    chat = Chat.from_json(message_json["chat"])
    message.chat = chat
    message.date = message_json["date"]
    if "text" in message_json:
      message.text = message_json["text"]
    return message
