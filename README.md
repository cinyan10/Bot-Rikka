# Bot-Rikka

## CAUTION

⚠️ **Viewing this project will definitely waste your time!!!**

## Description

bot-rikka is a discord bot provides various features. Most of the codes from chatGPT

## Features

- query server info and send to your channel
- query local gokz database, get LJ top etc. 

## To Do List

- [ ] 添加中文插件指令 和 介绍文本

- [ ] Server Information with both EN and CN
  - [ ] button link

- [ ] **kz global stats**

- [x] Edit channel name to implement dynamic channel name 

- [x] info

  - [x] embedded

  -  [x] show steam profile picture

  -  [x] find player

  -  [x] jspb

- [x] leaderboard 
  - [x] jstop
  - [ ] server records holder 
  - [ ] fun stats 
  - [x] playtime rank
  - [x] gokz.cn rank

- [ ] compare ljpb

- [ ] Server Role

  > rank by skill points

- [ ] twitch stream

- [x] server status (cpu, memory, disk, net)
  -  [ ] ~~alert when memory usage too high~~

- [ ] memes generator

- [ ] whitelist
  - [ ] answer button

- [ ] **Server Trending**
  - [x] daily active player, monthly active player

- [ ] **Server Charts**

- [ ] player location map

- [ ] !help with both EN | CN text

- [ ] ban player in server

- [ ] refactor some functions with class

```python
class SteamUser
class PlayerKzStats
```
-  [x] bilibili
  -  [x] bind bilibili
  -  [ ] stream bool
  -  [ ] video bool
-  [ ] give role when user playing in server
-  [ ] Mini Games
   -  [ ] simulate long jump
      -  [ ] random with local database stats
      -  [ ] compare with others  (mini games)
   -  [ ] Rock, Paper, Scissors

## How to Use

1. Create an application in [discord](https://discord.com/developers/applications),  and get the Token

2. download the bot:

   `git clone https://github.com/cinyan10/bot-rikka.git `

   or download the zip

3. create a `.env` file in the bot folder, and set the config
   ``` 
   DISCORD_TOKEN=
   WEBHOOK_URL=
   WEBHOOK_URL_TEST=
   DB_HOST=
   DB_PORT=
   DB_PASSWORD=
   DB_USER=
   STEAM_API_KEY=
   TRENDING_WEBHOOK_URL=
   ```

4. set other configs in config.py

5. install requirements:

   ```shell
   pip install -r requirements.txt
   ```

   if there's an error

   > File "python3.12/site-packages/valve/source/messages.py", line 379, in <module>
   >  class Message(collections.Mapping):
   >                ^^^^^^^^^^^^^^^^^^^

    you can modify the `valve/source/messages.py` file in the `valve` library. Open the file and locate the line that starts with `class Message(collections.Mapping):`. Replace it with the following line:

   ```
   class Message(collections.abc.Mapping):
   ```

   This change ensures that the correct `Mapping` class is used

6. run the bot
   `python3 main.py`

7. waiting for it crash

