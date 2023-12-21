import os
from flask import Flask
from dotenv import load_dotenv

load_dotenv()

user = os.environ["DB_USERNAME"]
pwd = os.environ["DB_PASSWORD"]
app = Flask(__name__)
API_GPT = 'the url to your gpt api'

DEBUG = True