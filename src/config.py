import json
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    postman_api_url: str = os.environ.get("postman_api_url")
    postman_api_key: str = os.environ.get("postman_api_key")
    export_workspace_list: str = os.environ.get("export_workspace_list", "false")
    export_postman_data: str = os.environ.get("export_postman_data", "false")
    skip_already_exported: str = os.environ.get("skip_already_exported", "false")
    import_global_variables_to_bruno: str = os.environ.get("import_global_variables_to_bruno", "false")
    bruno_workspace_folder: str = os.environ.get("bruno_workspace_folder")

