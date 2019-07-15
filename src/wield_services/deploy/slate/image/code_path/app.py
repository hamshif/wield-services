from flask import Flask
from random import randint


app = Flask(__name__)

SERVICE_NAME = 'slate'


@app.route("/")
def hello():
    return show_something(SERVICE_NAME)


def show_something(service_name):
    r = randint(0, 9)
    text = f"\nNaknik Yerkarak\nWielding {service_name}\nHello World!\n{r}"
    return text
