from typing import Union
import json
import logging
import sys
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
        for collection in collections:
            col_id, col_name = collection["id"], collection["name"]
            response = PostmanService().get_collection(col_id)
            filename = f"{ws_name}-{col_name}.json"
            col_detail = response.json()
            with open(filename, "w") as f:
                json.dump(col_detail, f, indent=2)
            print(f"Exported {col_name} from workspace {ws_name}")

            print(f"importing collection name : {col_name}")


if __name__ == "__main__":
    main_method()