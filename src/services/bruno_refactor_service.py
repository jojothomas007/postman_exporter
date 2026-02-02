import json
import logging
import os
import sys
from pathlib import Path
from typing import Dict, List, Any
from ruamel.yaml import YAML
from src.config import Config

# Set up logging
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)


class BrunoRefactorService:
    """Service to refactor Bruno workspace structure and files."""
    
    def __init__(self):
        """Initialize the Bruno Refactor Service."""
        self.bruno_workspace_folder = Config.bruno_workspace_folder
        self.yaml = YAML()
    
    def import_global_variables(self, workspace_name: str) -> None:
        """
        Import global variables to Bruno workspace.
        
        Args:
            workspace_name: Name of the workspace to refactor
        """
        workspace_path = Path(self.bruno_workspace_folder) / workspace_name
        
        if not workspace_path.exists():
            logger.error(f"Bruno workspace folder not found: {workspace_path}")
            return
        
        collections_path = workspace_path / "collections" / workspace_name
        
        # Step 1: Rename collection files and remove bruno.json files
        self._rename_collection_files(collections_path)
        
        # # Step 2: Reorganize workspace structure
        # new_collection_path = self._reorganize_workspace_structure(
        #     workspace_path, workspace_name, collections_path
        # )
        
        # Step 3: Create bruno.json configuration
        self._create_bruno_json(collections_path, workspace_name)
        
        # Step 4: Create collection.bru with global variables
        self._create_collection_bru(collections_path, workspace_name)

        # Step 5: update workspace.yml file
        self._update_workspace_yml(workspace_path, workspace_name)
    
    def _rename_collection_files(self, collections_path: Path) -> None:
        """
        Rename collection.bru files to folder.bru and remove bruno.json files.
        
        Args:
            collections_path: Path to the collections directory
        """
        if not collections_path.exists():
            logger.warning(f"Collections path does not exist: {collections_path}")
            return
        
        for folder in collections_path.iterdir():
            if not folder.is_dir():
                continue
            
            # Rename collection.bru to folder.bru
            collection_file = folder / "collection.bru"
            if collection_file.exists():
                new_collection_file = folder / "folder.bru"
                collection_file.rename(new_collection_file)
                logger.info(f"Renamed {collection_file} to {new_collection_file}")
            
            # Remove bruno.json file
            bruno_json_file = folder / "bruno.json"
            if bruno_json_file.exists():
                bruno_json_file.unlink()
                logger.info(f"Removed {bruno_json_file}")
    
    def _reorganize_workspace_structure(
        self, workspace_path: Path, workspace_name: str, collections_path: Path
    ) -> Path:
        """
        Reorganize workspace structure by creating a new collection folder.
        
        Args:
            workspace_path: Path to the workspace
            workspace_name: Name of the workspace
            collections_path: Path to the collections directory
            
        Returns:
            Path to the new collection folder
        """
        # Create temporary folder for reorganization
        temp_collection_path = workspace_path / workspace_name
        temp_collection_path.mkdir(exist_ok=True)
        logger.info(f"Created temporary collections folder: {temp_collection_path}")
        
        # Move all items from collections folder to temporary folder
        for item in collections_path.iterdir():
            if item.is_dir():
                new_item_path = temp_collection_path / item.name
                item.rename(new_item_path)
                logger.info(f"Moved {item} to {new_item_path}")
        
        # Move temporary folder into collections folder
        final_collection_path = collections_path / workspace_name
        temp_collection_path.rename(final_collection_path)
        logger.info(f"Moved {temp_collection_path} to {final_collection_path}")
        
        return final_collection_path
    
    def _create_bruno_json(self, collection_path: Path, workspace_name: str) -> None:
        """
        Create bruno.json configuration file.
        
        Args:
            collection_path: Path to the collection directory
            workspace_name: Name of the workspace
        """
        bruno_json_path = collection_path / "bruno.json"
        bruno_config = {
            "version": "1",
            "name": workspace_name,
            "type": "collection",
            "ignore": [
                "node_modules",
                ".git"
            ]
        }
        
        with open(bruno_json_path, "w", encoding="utf-8") as f:
            json.dump(bruno_config, f, indent=2)
        
        logger.info(f"Created bruno.json file: {bruno_json_path}")
    
    def _create_collection_bru(self, collection_path: Path, workspace_name: str) -> None:
        """
        Create collection.bru file with global variables from Postman.
        
        Args:
            collection_path: Path to the collection directory
            workspace_name: Name of the workspace
        """
        global_val_path = Path("output") / workspace_name / "global_variables.json"
        
        try:
            with open(global_val_path, "r", encoding="utf-8") as f:
                global_variables = json.load(f).get("values", [])
            logger.info(f"Loaded global variables from: {global_val_path}")
        except FileNotFoundError:
            logger.warning(f"Global variables file not found: {global_val_path}")
            global_variables = []
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse global variables JSON: {e}")
            global_variables = []
        
        # Build collection configuration
        collection_config = "vars:pre-request{" + self._build_variables_dict(global_variables) + "\n}"
        
        collection_bru_path = collection_path / "collection.bru"
        with open(collection_bru_path, "w", encoding="utf-8") as f:
            f.write(collection_config)
        
        logger.info(f"Created collection.bru file with global variables: {collection_bru_path}")
    
    def _build_variables_dict(self, global_variables: List[Dict[str, Any]]) -> str:
        """
        Build a dictionary of variables from global variables list.
        
        Args:
            global_variables: List of global variable dictionaries
            
        Returns:
            Dictionary mapping variable names to values
        """
        variables = ""
        for variable in global_variables:
            variables = variables + f"\n{variable['key']}: {variable['value']}"
        return variables

    def _update_workspace_yml(self, workspace_path: Path, workspace_name: str) -> None:
        """
        Update workspace.yml file with correct collection details.
        
        Args:
            workspace_path: Path to the workspace
            workspace_name: Name of the workspace
        """
        workspace_yml_path = workspace_path / "workspace.yml"
        data = {}
        with open(workspace_yml_path, "r", encoding="utf-8") as f:
            data = self.yaml.load(f)
        data["collections"] = [{"name": workspace_name, "path": "collections\\" + workspace_name}]
        with open(workspace_yml_path, "w", encoding="utf-8") as f:
            self.yaml.dump(data, f)
        logger.info(f"Updated workspace.yml file: {workspace_yml_path}")