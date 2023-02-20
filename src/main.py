#!/usr/local/bin/python3
import json
from json import JSONEncoder
import subprocess
from pathlib import Path
import re
from time import sleep
import threading

from client import Client
from update import Update

class CustomEncoder(JSONEncoder):
  def default(self, o):
    return o.__dict__

class Bot:
  def __init__(self, downloads_path: str, data_path: str = "", update_frecuency: int = 60) -> None:
    # set hardcoded variables
    self.downloads_path = downloads_path
    self.data_path = data_path
    self._update_frecuency = update_frecuency
    # set users
    user = None
    try:
      with open(self.data_path + "/users.txt", "r") as reader:
        user = reader.readline()
    except:
      user = input("Enter valid Telegram users (pipe separated |) to honor requests: ")
      Path(self.data_path).mkdir(parents=True, exist_ok=True)
      with open(self.data_path + "/users.txt", "w") as writer:
        writer.write(user)
    self._users = user
    # set bot telegram token
    token = None
    try:
      with open(self.data_path + "/token.txt", "r") as reader:
        token = reader.readline()
    except:
      token = input("Enter a valid telegram bot token: ")
      Path(self.data_path).mkdir(parents=True, exist_ok=True)
      with open(self.data_path + "/token.txt", "w") as writer:
        writer.write(token)
    # initialize client
    self._updates = None
    try:
      with open(self.data_path + "/updates.json", "r") as reader:
        self._updates = json.load(reader)
    except:
      Path(self.data_path).mkdir(parents=True, exist_ok=True)
      with open(self.data_path+ "/updates.json", "w") as writer:
        self._updates = []
        json.dump(self._updates, writer, indent=2)
    self._updates = Client.parse_updates_from_json(self._updates)
    self.client = Client(token, self._updates)
    
  def start(self):
    while True:
      self.update()
      sleep(self._update_frecuency)

  def update(self):
    newer = False
    for update in self.client.get_updates():
      # self._dispatch(update)
      thr = threading.Thread(target=self._dispatch, kwargs= { 'update': update })
      thr.start()
      self._updates.append(update)
      newer = True
    if newer:
        with open(self.data_path + "/updates.json", "w") as writer:
          json.dump(self._updates, writer, indent=2, cls=CustomEncoder)

  def _dispatch(self, update: Update):
    if update.message.message_id == None:
      print("Aborted reason: No message")
      return None
    if (re.match("/^(" + self._users + ")$/", update.message.sender.username, flags=re.I)):
      # abort
      print("Aborted reason: User {}".format(update.message.sender.username))
      return None
    elif self._users.split('|')[0] != '':
      # abort
      print("Aborted reason: User {}".format(update.message.sender.username))
      return None
    if update.message.is_edited:
      print("Aborted reason: Message is edited")
      return None
    text = update.message.text
    if text == None:
      return None
    if (re.match("^https.*youtu(\.be|be).*$", text, flags=re.I)):
      print ("Youtube video")
      self.client.delete_message(update.message)
      message_ack = self.client.send_message(update.message.chat, "{}\nStatus: Running downloader...".format(text))
      psub = subprocess.Popen(["yt-dlp", "--no-playlist", "--ignore-errors", "--add-metadata", "--output" , self.downloads_path + "/%(extractor)s/%(uploader)s/%(width)sx%(height)s/%(upload_date)s %(id)s.%(ext)s", text])
      pcod = psub.wait()
      if (pcod == 1):
        print("Error")
      elif (pcod == 0):
        print("Success")
      else:
        print("Exitcode: {}".format(pcod))
      if pcod == 0:
        # psubn = subprocess.Popen(["bash", "-c", "ytvideopath '" + text + "'"], stdout=subprocess.PIPE)
        psubn = subprocess.Popen(["yt-dlp", "--quiet", "--no-playlist", "--no-warnings", "--ignore-errors", "--simulate", "--print=filename", "--output" , self.downloads_path + "/%(extractor)s/%(uploader)s/%(width)sx%(height)s/%(upload_date)s %(id)s.%(ext)s", text], stdout=subprocess.PIPE)
        output, outerr = psubn.communicate()
        filename = output.decode("utf-8").replace("\n", "")
        filesize = Bot.get_file_size_mb(filename)
        print()
        print(str(filesize) + " - " + filename)
        print()
        if filesize < 50:
          message_ack_updated = self.client.update_message_text(message_ack, "{}\nStatus: Uploading video...".format(text))
          message_media = self.client.send_document(update.message.chat, filename, "video/mp4", "{}".format(text))
          message_ack_deleted = self.client.delete_message(message_ack_updated)
          if message_media != None and message_ack_deleted != None:
            print("Message media sent and message ACK deleted")
        else:
          message_ack_updated = self.client.update_message_text(message_ack, "{}\nStatus: Video file to big to upload.".format(text))
          if message_ack_updated != None:
            print("Message ACK updated")
      else:
        message_ack_updated = self.client.update_message_text(message_ack, "{}\nStatus: Error.".format(text))
        print("Message error sent")
    elif(re.match("^https.*tiktok.*$", text)):
      print ("Tiktok video")
      self.client.delete_message(update.message)
      message_ack = self.client.send_message(update.message.chat, "{}\nStatus: Running downloader...".format(text))
      psub = subprocess.Popen(["yt-dlp", "--no-playlist", "--ignore-errors", "--add-metadata", "--output" , self.downloads_path + "/%(extractor)s/%(uploader)s/%(width)sx%(height)s/%(upload_date)s %(id)s.%(ext)s", text])
      pcod = psub.wait()
      if (pcod == 1):
        print("Error")
      elif (pcod == 0):
        print("Success")
      else:
        print("Exitcode: {}".format(pcod))
      if pcod == 0:
        psubn = subprocess.Popen(["yt-dlp", "--quiet", "--no-playlist", "--no-warnings", "--ignore-errors", "--simulate", "--print=filename", "--output" , self.downloads_path + "/%(extractor)s/%(uploader)s/%(width)sx%(height)s/%(upload_date)s %(id)s.%(ext)s", text], stdout=subprocess.PIPE)
        output, outerr = psubn.communicate()
        filename = output.decode("utf-8").replace("\n", "")
        filesize = Bot.get_file_size_mb(filename)
        print()
        print(str(filesize) + " - " + filename)
        print()
        if filesize < 50:
          message_ack_updated = self.client.update_message_text(message_ack, "{}\nStatus: Uploading tiktok video...".format(text))
          message_media = self.client.send_document(update.message.chat, filename, "video/mp4", "n{}".format(text))
          message_ack_deleted = self.client.delete_message(message_ack_updated)
          if message_media != None and message_ack_deleted != None:
            print("Message media sent and message ACK deleted")
        elif filesize == 9999:
          message_ack_updated = self.client.update_message_text(message_ack, "{}\nStatus: Unexpected error or file not found to upload.".format(text))
          if message_ack_updated != None:
            print("Message ACK updated")
        else:
          message_ack_updated = self.client.update_message_text(message_ack, "{}\nStatus: Video file to big to upload.".format(text))
          if message_ack_updated != None:
            print("Message ACK updated")
      else:
        message_ack_updated = self.client.update_message_text(message_ack, "{}\nStatus: Error.".format(text))
        print("Message error sent")

  def get_file_size_mb(file_path: str):
    try:
      return round(Path(file_path).stat().st_size / (1024 * 1024), 2)
    except:
      return 9999

bot = Bot("/tmp", "/st-bot/data", update_frecuency=5)
bot.start()