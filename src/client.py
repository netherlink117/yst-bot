from typing import List
import requests

from message import Message
from update import Update
from chat import Chat

class Client:
  def __init__(self, token: str, updates: List[Update] = [], uri = "https://api.telegram.org/bot") -> None:
    self._token = token
    self._updates = updates
    self._uri = uri

  def get_updates(self):
    updates_len = len(self._updates)
    response = None
    try:
      if updates_len > 0:
        # print(self._uri + (len(self._token) * "*") + "/getUpdates?offset={}".format(self._updates[updates_len - 1].update_id + 1))
        response = requests.get(self._uri + self._token + "/getUpdates?offset={}".format(self._updates[updates_len - 1].update_id + 1))
      else:
        # print(self._uri + (len(self._token) * "*") + "/getUpdates")
        response = requests.get(self._uri + self._token + "/getUpdates")
      response_json = response.json()
    except Exception  as e:
      if hasattr(e, 'message'):
        print(e.message)
      else:
        print(e)
      return []
    if not "result" in response_json:
      return []
    result_json = response_json["result"]
    updates = []
    if len(result_json) > 0:
      updates = Client.parse_updates_from_json(result_json)
      self._updates.extend(updates)
    return updates

  def parse_updates_from_json(updates_json: List[dict]):
    updates = []
    for update_json in updates_json:
      update = Update.from_json(update_json)
      updates.append(update)
    return updates

  def send_message(self, chat: Chat, text: str):
    if chat.id == None:
      return
    response = requests.post(self._uri + self._token + "/sendMessage", json = { "chat_id": chat.id, "text": text })
    response_json = response.json()
    # print("/sendMessage")
    # print(response_json)
    if response_json["ok"]:
      message = Message.from_json(response_json["result"])
      return message
    else:
      return None

  def send_document(self, chat: Chat, file: str, mime_type: str, caption: str = None):
    if chat.id == None:
      return
    file = [('document', (file, open(file, 'rb'), mime_type))]
    response = None
    if caption != None:
      response = requests.post(self._uri + self._token + "/sendDocument", data = { "chat_id": chat.id, "caption": caption }, files = file)
    else:
      response = requests.post(self._uri + self._token + "/sendDocument", data = { "chat_id": chat.id }, files = file)
    response_json = response.json()
    # print("/sendDocument")
    # print(response_json)
    if response_json["ok"]:
      message = Message.from_json(response_json["result"])
      return message
    else:
      return None

  def update_message_text(self, message: Message, text: str):
    if message.message_id == None:
      return
    response = requests.post(self._uri + self._token + "/editMessageText", json = { "chat_id": message.chat.id, "message_id": message.message_id, "text": text })
    response_json = response.json()
    # print("/editMessage")
    # print(response_json)
    if response_json["ok"]:
      message = Message.from_json(response_json["result"])
      return message
    else:
      return None

  def delete_message(self, message: Message):
    if message.message_id == None:
      return
    response = requests.post(self._uri + self._token + "/deleteMessage", json = { "chat_id": message.chat.id, "message_id": message.message_id })
    response_json = response.json()
    # print("/deleteMessage")
    # print(response_json)
    if response_json["ok"]:
      return message
    else:
      return None
  