import os
from flask import Flask
from flask_cors import CORS
from config import Config
from model_manager import ModelManager

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

def load_model_startup():
    """ This function runs at application startup it loads all of the model found in the configuration """
    model_manager = ModelManager()
    model_manager.load_models(configuration=app.config["MODELS"])