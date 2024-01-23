# discord-bot

### Todo

- [x] info
  - [x] embedded
  - [x] show steam profile picture
  - [ ] kz global stats
  
- [x] leaderboard
  - [x] jumpstats top
  - [ ] server records holder
  - [ ] global points
  - [ ] gokz.cn rank 
  
- [ ] bilibili

  - [ ] bind bilibili
  - [ ] stream bool
  - [ ] video bool

- [ ] Server Role

  - [ ] rank by skill point

    > Top 10: **Legend**
    >
    > 8.0+: **Master**
    >
    > 7.5+: **Professional**
    >
    > 7.0+: **Expert**
    >
    > 6.0+: **Skilled**

- [ ] stream twitch

- [ ] server status (cpu, memory, disk, net)
  - [ ] alert when memory usage too high

- [ ] memes generator

- [ ] whitelist

  - [ ] plugin
  - [ ] question in discord


```markdown
> [!CAUTION]
> Reading this project will definitely waste your precious time!!!
```

requirements:

```shell
pip install -r requirements.txt
```

if there's an error

> File "python3.12/site-packages/valve/source/messages.py", line 379, in <module>
>     class Message(collections.Mapping):
>                   ^^^^^^^^^^^^^^^^^^^

 you can modify the `valve/source/messages.py` file in the `valve` library. Open the file and locate the line that starts with `class Message(collections.Mapping):`. Replace it with the following line:

```
class Message(collections.abc.Mapping):
```

This change ensures that the correct `Mapping` class is used