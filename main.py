from typing import Union
import json
import logging
import sys
import os
from src.config import Config
from src.services.postman_service import PostmanService
from src.services.exporter import PostmanExporter
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


def main_method():
    if Config.export_workspace_list.lower() == "true":
        export_workspace_list()
    if Config.export_postman_data.lower() == "true":
        workspaces = json.load(open("output/workspace_list.json", "r"))
        exporter = PostmanExporter(skip_already_exported=Config.skip_already_exported.lower() == "true")
        for ws_id, ws_name in workspaces.items():
            exporter.export_workspace_data(ws_id, ws_name)
        # Save export status to CSV
        exporter.save_status_to_csv()


if __name__ == "__main__":
    main_method()