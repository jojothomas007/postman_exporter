import json
import logging
import base64
import requests
from requests.auth import HTTPBasicAuth
from src.config import Config
from src.utils.request_sender import RequestSender
import sys

# Set up logging
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)

class PostmanService:
    def __init__(self):
        self.request_sender:RequestSender = RequestSender()
        self.postman_api_url = Config.postman_api_url
        self.postman_api_key = Config.postman_api_key
        self.headers = {
            "Authorization": f"Bearer {self.postman_api_key}",
            "Content-Type": "application/json"
        }

    def get_workspaces(self) -> requests.Response:
        request_url = f"{self.postman_api_url}/workspaces"
        response = self.request_sender.get_request(request_url, self.headers, None)
        return response
        
    def get_workspace(self, id) -> requests.Response:
        request_url = f"{self.postman_api_url}/workspaces/{id}"
        response = self.request_sender.get_request(request_url, self.headers, None)
        return response

    def get_collections(self) -> requests.Response:
        request_url = f"{self.postman_api_url}/collections"
        response = self.request_sender.get_request(request_url, self.headers, None)
        return response

    def get_collection(self, id:str) -> requests.Response:
        request_url = f"{self.postman_api_url}/collections/{id}"
        response = self.request_sender.get_request(request_url, self.headers, None)
        return response

    def get_environments(self) -> requests.Response:
        request_url = f"{self.postman_api_url}/environments"
        response = self.request_sender.get_request(request_url, self.headers, None)
        return response

    def get_environment(self, id:str) -> requests.Response:
        request_url = f"{self.postman_api_url}/environments/{id}"
        response = self.request_sender.get_request(request_url, self.headers, None)
        return response
    
    def get_global_variables(self, workspaceId:str) -> requests.Response:
        request_url = f"{self.postman_api_url}/workspaces/{workspaceId}/global-variables"
        response = self.request_sender.get_request(request_url, self.headers, None)
        return response
    