from flask import Flask
from random import randint


app = Flask(__name__)


@app.route("/")
def hello():
    return show_something()


def show_something():
    r = randint(0, 9)
    text = f"\nNaknik\nWielding Slate\nHello World!\n{r}"
    return text
