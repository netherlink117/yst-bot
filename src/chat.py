class Chat:
  def __init__(self, id: int = None, type: str = None) -> None:
    self.id = id
    self.type = type

  def from_json(chat_json: dict):
    chat = Chat(chat_json["id"], chat_json["type"])
    return chat
