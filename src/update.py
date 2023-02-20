from message import Message
class Update:
  def __init__(self, update_id: int = None, message: Message = Message()) -> None:
    self.update_id = update_id
    self.message = message

  def from_json(update_json: dict):
    update = Update(update_json["update_id"])
    if "edited_message" in update_json:
      message = Message.from_json(update_json["edited_message"], True)
      update.message = message
      return update
    elif "message" in update_json:
      message = Message.from_json(update_json["message"])
      update.message = message
      return update
    else:
      update.message = Message()
      return update

