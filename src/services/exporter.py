import json
import os
from src.services.postman_service import PostmanService


class PostmanExporter:
    """Handles the export of Postman data including collections, environments, and global variables."""
    
    def __init__(self):
        self.postman_service = PostmanService()
    
    def export_global_variables(self, workspace_id: str, workspace_name: str) -> None:
        """Export global variables from a workspace.
        
        Args:
            workspace_id: The ID of the workspace
            workspace_name: The name of the workspace
        """
        try:
            response = self.postman_service.get_global_variables(workspace_id)
            global_variables_details = response.json()
            global_variables_details["name"] = "Globals"
            global_variables_details["id"] = "sampleid"
            filename = os.path.join("output", workspace_name, "global_variables.json")
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, "w") as f:
                json.dump(global_variables_details, f, indent=2)
            print(f"Exported global variables from workspace {workspace_name}")
        except Exception as e:
            print(f"Error exporting global variables from workspace {workspace_name}: {e}")
    
    def export_collections(self, collections: list, workspace_name: str) -> None:
        """Export collections from a workspace.
        
        Args:
            collections: List of collection metadata
            workspace_name: The name of the workspace
        """
        try:
            for collection in collections:
                col_id, col_name = collection["uid"], collection["name"]
                print(f"importing collection name : {col_name}")
                response = self.postman_service.get_collection(col_id)
                col_detail = response.json().get("collection", {})
                filename = os.path.join("output", workspace_name, "collections", f"{col_name}.json")
                os.makedirs(os.path.dirname(filename), exist_ok=True)
                with open(filename, "w") as f:
                    json.dump(col_detail, f, indent=2)
                print(f"Exported {col_name} from workspace {workspace_name}")
        except Exception as e:
            print(f"Error exporting collection {col_name} from workspace {workspace_name}: {e}")
    
    def export_environments(self, environments: list, workspace_name: str) -> None:
        """Export environments from a workspace.
        
        Args:
            environments: List of environment metadata
            workspace_name: The name of the workspace
        """
        try:
            for environment in environments:
                env_id, env_name = environment["uid"], environment["name"]
                print(f"importing environment name : {env_name}")
                response = self.postman_service.get_environment(env_id)
                env_detail = response.json().get("environment", {})
                filename = os.path.join("output", workspace_name, "environments", f"{env_name}.json")
                os.makedirs(os.path.dirname(filename), exist_ok=True)
                with open(filename, "w") as f:
                    json.dump(env_detail, f, indent=2)
                print(f"Exported {env_name} from workspace {workspace_name}")
        except Exception as e:
            print(f"Error exporting environment {env_name} from workspace {workspace_name}: {e}")
    
    def export_workspace_data(self, workspace_id: str, workspace_name: str) -> None:
        """Export all data from a single workspace.
        
        Args:
            workspace_id: The ID of the workspace
            workspace_name: The name of the workspace
        """
        response = self.postman_service.get_workspace(workspace_id)
        ws = response.json().get("workspace", {})
        collections = ws.get("collections", [])
        environments = ws.get("environments", [])
        
        # Export global variables
        self.export_global_variables(ws.get("id"), workspace_name)
        
        # Export collections
        self.export_collections(collections, workspace_name)
        
        # Export environments
        self.export_environments(environments, workspace_name)
