import json
import os
import csv
from datetime import datetime
from typing import List, Dict
from src.services.postman_service import PostmanService


class PostmanExporter:
    """Handles the export of Postman data including collections, environments, and global variables."""
    
    def __init__(self):
        self.postman_service = PostmanService()
        self.export_status: List[Dict[str, str]] = []
    
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
            self.export_status.append({
                "workspace": workspace_name,
                "name": "Globals",
                "type": "global_variables",
                "status": "success",
                "export_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        except Exception as e:
            print(f"Error exporting global variables from workspace {workspace_name}: {e}")
            self.export_status.append({
                "workspace": workspace_name,
                "name": "Globals",
                "type": "global_variables",
                "status": "failed",
                "export_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
    
    def export_collections(self, collections: list, workspace_name: str) -> None:
        """Export collections from a workspace.
        
        Args:
            collections: List of collection metadata
            workspace_name: The name of the workspace
        """
        for collection in collections:
            col_name = collection.get("name", "Unknown")
            try:
                col_id = collection["uid"]
                print(f"importing collection name : {col_name}")
                response = self.postman_service.get_collection(col_id)
                col_detail = response.json().get("collection", {})
                filename = os.path.join("output", workspace_name, "collections", f"{col_name}.json")
                os.makedirs(os.path.dirname(filename), exist_ok=True)
                with open(filename, "w") as f:
                    json.dump(col_detail, f, indent=2)
                print(f"Exported {col_name} from workspace {workspace_name}")
                self.export_status.append({
                    "workspace": workspace_name,
                    "name": col_name,
                    "type": "collection",
                    "status": "success",
                    "export_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
            except Exception as e:
                print(f"Error exporting collection {col_name} from workspace {workspace_name}: {e}")
                self.export_status.append({
                    "workspace": workspace_name,
                    "name": col_name,
                    "type": "collection",
                    "status": "failed",
                    "export_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
    
    def export_environments(self, environments: list, workspace_name: str) -> None:
        """Export environments from a workspace.
        
        Args:
            environments: List of environment metadata
            workspace_name: The name of the workspace
        """
        for environment in environments:
            env_name = environment.get("name", "Unknown")
            try:
                env_id = environment["uid"]
                print(f"importing environment name : {env_name}")
                response = self.postman_service.get_environment(env_id)
                env_detail = response.json().get("environment", {})
                filename = os.path.join("output", workspace_name, "environments", f"{env_name}.json")
                os.makedirs(os.path.dirname(filename), exist_ok=True)
                with open(filename, "w") as f:
                    json.dump(env_detail, f, indent=2)
                print(f"Exported {env_name} from workspace {workspace_name}")
                self.export_status.append({
                    "workspace": workspace_name,
                    "name": env_name,
                    "type": "environment",
                    "status": "success",
                    "export_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
            except Exception as e:
                print(f"Error exporting environment {env_name} from workspace {workspace_name}: {e}")
                self.export_status.append({
                    "workspace": workspace_name,
                    "name": env_name,
                    "type": "environment",
                    "status": "failed",
                    "export_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
    
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
    
    def save_status_to_csv(self, filename: str = "output/export_status.csv") -> None:
        """Save export status to a CSV file (appends if file exists).
        
        Args:
            filename: Path to the CSV file to save status
        """
        if not self.export_status:
            print("No export status to save")
            return
        
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        # Check if file exists to determine if we need to write header
        file_exists = os.path.isfile(filename)
        
        with open(filename, "a", newline='', encoding='utf-8') as f:
            fieldnames = ["export_time", "workspace", "name", "type", "status"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            # Write header only if file is new
            if not file_exists:
                writer.writeheader()
            
            writer.writerows(self.export_status)
        
        print(f"Export status {'appended to' if file_exists else 'saved to'} {filename}")
        
        # Print summary
        total = len(self.export_status)
        success = sum(1 for item in self.export_status if item["status"] == "success")
        failed = total - success
        print(f"\nExport Summary: {success} successful, {failed} failed out of {total} total items")

