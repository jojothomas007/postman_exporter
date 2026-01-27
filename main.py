from typing import Union
import json
import logging
import sys
import os
from src.config import Config
from src.services.postman_service import PostmanService
# Set up logging
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)

def export_workspace_list():
    response = PostmanService().get_workspaces()
    workspaces = response.json().get("workspaces", [])
    print(f"Exporting workspace list")
    json.dump(workspaces, open("output/workspaces.json", "w"), indent=2)
    ws_list_json = {}
    for workspace in workspaces:
        ws_id, ws_name = workspace["id"], workspace["name"]
        ws_list_json[ws_id] = ws_name
    json.dump(ws_list_json, open("output/workspace_list.json", "w"), indent=2)
    print(f"Exported workspace list")
        
def export_postman_data(workspaces:dict):
    for ws_id, ws_name in workspaces.items():
        response = PostmanService().get_workspace(ws_id)   
        ws = response.json().get("workspace", {})
        collections = ws.get("collections", [])
        environments = ws.get("environments", [])
        for collection in collections:
            col_id, col_name = collection["id"], collection["name"]
            print(f"importing collection name : {col_name}")
            response = PostmanService().get_collection(col_id)
            col_detail = response.json()
            filename = os.path.join("output", ws_name, "collections", f"{col_name}.json")
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, "w") as f:
                json.dump(col_detail, f, indent=2)
            print(f"Exported {col_name} from workspace {ws_name}")
        for environment in environments:
            env_id, env_name = environment["id"], environment["name"]
            print(f"importing environment name : {env_name}")
            response = PostmanService().get_environment(env_id)
            env_detail = response.json()
            filename = os.path.join("output", ws_name, "environments", f"{env_name}.json")
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, "w") as f:
                json.dump(env_detail, f, indent=2)
            print(f"Exported {env_name} from workspace {ws_name}")
        

def main_method():
    if Config.export_workspace_list.lower() == "true":
        export_workspace_list()
    if Config.export_postman_data.lower() == "true":
        workspaces = json.load(open("output/workspace_list.json", "r"))
        export_postman_data(workspaces)


if __name__ == "__main__":
    main_method()