# st-bot
This is a bot designed to run on a container, to download videos via telegram.
## Features
Currently it can download youtube shorts and tiktok videos, due the size limitation of the telegram api.
## How to install
To install there are some requirements for containers, there are no other requirements than containers being able to run in the PC.
1. Clone this repository inside you collections' folder.
```bash
mkdir st-bot
cd st-bot
git clone https://github.com/netherlink117/st-bot.git
```
2. Copy your token inside the `data` folder in a `token.txt` file. Optionally if you want the bot to work only for you, put your user names inside a `users.txt` file separated by the pipe character `|`.
3. Create images and build to containers. This uses docker composer to create the container, and is the last step, this might take long depending the network speed and machine power, specially for the first time runing it.
```bash
docker-compose up -d --build
```
Now everything should be in place and the bot should asnswer to tiktok and youtube links.
## Disclaimer
This project is in no way affiliated with, authorized, maintained or endorsed by Youtube, Tiktok, or any of its affiliates or subsidiaries.

This is an independent and unofficial project, and the tools described are downloaded from they own sources and they are not included on this repository. Use at your own risk.
## License
The code shared on this repository is shared under the [The Unlicense](https://unlicense.org) license.
