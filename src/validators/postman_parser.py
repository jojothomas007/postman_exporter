"""
Postman Collection Parser

Parses Postman collection JSON files and extracts structural information
including collections, folders, requests, environments, and variables.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional


class PostmanParser:
    """Parser for Postman workspace files and collections."""
    
    def __init__(self, workspace_path: str):
        """
        Initialize the Postman parser.
        
        Args:
            workspace_path: Path to the Postman workspace directory (e.g., output/petstore)
        """
        self.workspace_path = Path(workspace_path)
        self.collections_path = self.workspace_path / "collections"
        self.environments_path = self.workspace_path / "environments"
        self.global_vars_path = self.workspace_path / "global_variables.json"
        
    def parse_collection(self, file_path: Path) -> Dict[str, Any]:
        """
        Parse a Postman collection JSON file.
        
        Args:
            file_path: Path to the collection JSON file
            
        Returns:
            Dictionary containing collection data
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def count_folders(self, items: List[Dict[str, Any]]) -> int:
        """
        Count folders in a collection or folder.
        
        A folder is an item that has 'item' array but no 'request' object.
        
        Args:
            items: List of items from collection
            
        Returns:
            Number of folders
        """
        count = 0
        for item in items:
            if 'item' in item and 'request' not in item:
                count += 1
                # Recursively count nested folders
                count += self.count_folders(item['item'])
        return count
    
    def count_requests(self, items: List[Dict[str, Any]]) -> int:
        """
        Count requests in a collection or folder.
        
        A request is an item that has a 'request' object.
        
        Args:
            items: List of items from collection
            
        Returns:
            Number of requests
        """
        count = 0
        for item in items:
            if 'request' in item:
                count += 1
            elif 'item' in item:
                # Recursively count requests in nested items
                count += self.count_requests(item['item'])
        return count
    
    def get_folder_structure(self, items: List[Dict[str, Any]], parent_path: str = "") -> List[Dict[str, Any]]:
        """
        Get hierarchical folder structure with counts.
        
        Args:
            items: List of items from collection
            parent_path: Parent path for nested items
            
        Returns:
            List of folder structures with metadata
        """
        folders = []
        for item in items:
            if 'item' in item and 'request' not in item:
                # This is a folder
                folder_name = item.get('name', 'Unnamed')
                folder_path = f"{parent_path}/{folder_name}" if parent_path else folder_name
                
                folder_info = {
                    'name': folder_name,
                    'path': folder_path,
                    'type': 'folder',
                    'request_count': self.count_requests(item['item']),
                    'folder_count': self.count_folders(item['item']),
                    'id': item.get('id', '')
                }
                folders.append(folder_info)
                
                # Recursively get nested folders
                nested_folders = self.get_folder_structure(item['item'], folder_path)
                folders.extend(nested_folders)
                
        return folders
    
    def get_collection_structure(self) -> List[Dict[str, Any]]:
        """
        Get the complete structure of all collections in the workspace.
        
        Returns:
            List of collection structures with metadata
        """
        collections = []
        
        if not self.collections_path.exists():
            return collections
        
        for collection_file in self.collections_path.glob('*.json'):
            collection_data = self.parse_collection(collection_file)
            
            collection_info = collection_data.get('info', {})
            items = collection_data.get('item', [])
            
            structure = {
                'name': collection_info.get('name', collection_file.stem),
                'path': str(collection_file),
                'type': 'collection',
                'request_count': self.count_requests(items),
                'folder_count': self.count_folders(items),
                'id': collection_info.get('_postman_id', ''),
                'folders': self.get_folder_structure(items)
            }
            
            collections.append(structure)
        
        return collections
    
    def parse_environment(self, file_path: Path) -> Dict[str, Any]:
        """
        Parse a Postman environment JSON file.
        
        Args:
            file_path: Path to the environment JSON file
            
        Returns:
            Dictionary containing environment data
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def get_environment_variables(self) -> List[Dict[str, Any]]:
        """
        Get all environment variables from the workspace.
        
        Returns:
            List of environment structures with variable counts
        """
        environments = []
        
        if not self.environments_path.exists():
            return environments
        
        for env_file in self.environments_path.glob('*.json'):
            env_data = self.parse_environment(env_file)
            
            values = env_data.get('values', [])
            
            env_info = {
                'name': env_data.get('name', env_file.stem),
                'path': str(env_file),
                'type': 'environment',
                'variable_count': len(values),
                'variables': [v.get('key', '') for v in values]
            }
            
            environments.append(env_info)
        
        return environments
    
    def get_global_variables(self) -> Optional[Dict[str, Any]]:
        """
        Get global variables from the workspace.
        
        Returns:
            Dictionary containing global variables info, or None if not found
        """
        if not self.global_vars_path.exists():
            return None
        
        with open(self.global_vars_path, 'r', encoding='utf-8') as f:
            global_data = json.load(f)
        
        values = global_data.get('values', [])
        
        return {
            'name': 'Global Variables',
            'path': str(self.global_vars_path),
            'type': 'global_variables',
            'variable_count': len(values),
            'variables': [v.get('key', '') for v in values]
        }
    
    def get_workspace_summary(self) -> Dict[str, Any]:
        """
        Get a complete summary of the Postman workspace.
        
        Returns:
            Dictionary containing workspace structure and counts
        """
        collections = self.get_collection_structure()
        environments = self.get_environment_variables()
        global_vars = self.get_global_variables()
        
        total_requests = sum(c['request_count'] for c in collections)
        total_folders = sum(c['folder_count'] for c in collections)
        
        return {
            'workspace_path': str(self.workspace_path),
            'collection_count': len(collections),
            'total_folder_count': total_folders,
            'total_request_count': total_requests,
            'environment_count': len(environments),
            'collections': collections,
            'environments': environments,
            'global_variables': global_vars
        }
