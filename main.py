from typing import Union
import json
import logging
import sys
import os
from src.services.postman_service import PostmanService
# Set up logging
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)


def main_method():
    response = PostmanService().get_workspaces()
    workspaces = response.json().get("workspaces", [])
    for workspace in workspaces:
        ws_id, ws_name = workspace["id"], workspace["name"]
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

if __name__ == "__main__":
    main_method()