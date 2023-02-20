class Sender:
  def __init__(self, id: int = None, is_bot: bool = None, first_name: str = None, username: str = None) -> None:
    self.id = id
    self.is_bot = is_bot
    self.first_name = first_name
    self.username = username

  def from_json(sender_json: dict):
    sender = Sender(sender_json["id"], sender_json["is_bot"], sender_json["first_name"])
    if "username" in sender_json:
      sender.username = sender_json["username"]
    return sender
