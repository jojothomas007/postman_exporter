import json
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    postman_api_url: str = os.environ["postman_api_url"]
    postman_api_key: str = os.environ["postman_api_key"]
