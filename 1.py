import code
import random
import string
import time
from time import sleep
from flask import Flask
from tinydb import TinyDB, Query
from threading import Thread
from os import system

clear = lambda: system("cls")

db = TinyDB('db.json')
User = Query()

app = Flask(__name__)


def close_code(name: str):
    db.update({"is_effective": False}, User.name == name)


def create_codes(effective_time: str):
    timestamp = int(time.time())

    sentence_list = random.sample(string.ascii_lowercase+string.ascii_uppercase, 6)

    for char in str(timestamp)[:4]:
        insert_position = random.randint(0, len(sentence_list))
        sentence_list.insert(insert_position, char)

    activation_code = ''.join(sentence_list)
    print(activation_code)
    db.insert({"name": activation_code, "create_time": time.time(), "effective_time": effective_time,
               "is_effective": True})


@app.route("/join/<activation_code>")
def join(activation_code: str) -> str:
    _code = db.search(User.name == activation_code)

    if _code == list():
        return "NULL"

    elif _code[0]["is_effective"] is False:
        return "noteff"

    db.update({"is_effective": False}, User.name == activation_code)

    return "OK"


if __name__ == '__main__':
    thread = Thread(target=app.run, kwargs={"port": 5000, "host": "0.0.0.0"})
    thread.daemon = True
    thread.start()
    console = code.InteractiveConsole(globals())

    sleep(2)
    console.interact("")
