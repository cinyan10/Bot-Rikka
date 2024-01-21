# discord-bot

requirements:

```
pip install discord, python-dotenv, python-valve
```

if there's an error

> File "python3.12/site-packages/valve/source/messages.py", line 379, in <module>
>     class Message(collections.Mapping):
>                   ^^^^^^^^^^^^^^^^^^^

 you can modify the `valve/source/messages.py` file in the `valve` library. Open the file and locate the line that starts with `class Message(collections.Mapping):`. Replace it with the following line:

```
pythonCopy code
class Message(collections.abc.Mapping):
```

This change ensures that the correct `Mapping` class is used