"""
Bruno Workspace Parser

Parses Bruno workspace .bru files and extracts structural information
including collections, folders, and requests.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Any, Optional


class BrunoParser:
    """Parser for Bruno workspace files."""
    
    def __init__(self, workspace_path: str):
        """
        Initialize the Bruno parser.
        
        Args:
            workspace_path: Path to the Bruno workspace directory (e.g., bruno_workspaces/petstore)
        """
        self.workspace_path = Path(workspace_path)
        self.collections_path = self.workspace_path / "collections"
        self.environments_path = self.workspace_path / "environments"
        
    def parse_bru_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Parse a .bru file and extract metadata.
        
        Args:
            file_path: Path to the .bru file
            
        Returns:
            Dictionary containing file metadata
        """
        content = file_path.read_text(encoding='utf-8')
        
        # Extract meta information
        meta_match = re.search(r'meta\s*\{([^}]*)\}', content, re.DOTALL)
        meta = {}
        if meta_match:
            meta_content = meta_match.group(1)
            # Extract name
            name_match = re.search(r'name:\s*(.+)', meta_content)
            if name_match:
                meta['name'] = name_match.group(1).strip()
            
            # Extract type (http, graphql, etc.)
            type_match = re.search(r'type:\s*(.+)', meta_content)
            if type_match:
                meta['type'] = type_match.group(1).strip()
        
        # Check if it's a request (has http method like get, post, etc.)
        http_methods = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options']
        is_request = False
        for method in http_methods:
            if re.search(rf'^{method}\s+\{{', content, re.MULTILINE):
                is_request = True
                meta['method'] = method.upper()
                break
        
        # Extract variables
        vars_pattern = re.findall(r'vars(?::[\w-]+)?\s*\{([^}]*)\}', content, re.DOTALL)
        variables = []
        for vars_block in vars_pattern:
            # Extract key-value pairs
            var_matches = re.findall(r'(\w+)\s*:\s*([^\n]*)', vars_block)
            for key, value in var_matches:
                variables.append(key.strip())
        
        return {
            'name': meta.get('name', file_path.stem),
            'path': str(file_path),
            'type': meta.get('type', 'unknown'),
            'is_request': is_request,
            'method': meta.get('method', ''),
            'variables': variables
        }
    
    def is_collection_root(self, path: Path) -> bool:
        """
        Check if a directory contains a collection.bru file.
        
        Args:
            path: Directory path
            
        Returns:
            True if it's a collection root
        """
        return (path / "collection.bru").exists()
    
    def is_folder(self, path: Path) -> bool:
        """
        Check if a directory contains a folder.bru file.
        
        Args:
            path: Directory path
            
        Returns:
            True if it's a folder
        """
        return (path / "folder.bru").exists()
    
    def count_requests_in_directory(self, directory: Path) -> int:
        """
        Count request files in a directory (non-recursive).
        
        Args:
            directory: Directory to search
            
        Returns:
            Number of request files
        """
        count = 0
        if not directory.exists():
            return count
        
        for item in directory.iterdir():
            if item.is_file() and item.suffix == '.bru':
                # Skip collection.bru and folder.bru
                if item.name not in ['collection.bru', 'folder.bru']:
                    bru_data = self.parse_bru_file(item)
                    if bru_data['is_request']:
                        count += 1
        
        return count
    
    def count_folders_in_directory(self, directory: Path) -> int:
        """
        Count folders in a directory (non-recursive).
        
        Args:
            directory: Directory to search
            
        Returns:
            Number of folders
        """
        count = 0
        if not directory.exists():
            return count
        
        for item in directory.iterdir():
            if item.is_dir() and self.is_folder(item):
                count += 1
        
        return count
    
    def get_folder_structure(self, directory: Path, parent_path: str = "") -> List[Dict[str, Any]]:
        """
        Get hierarchical folder structure with counts.
        
        Args:
            directory: Directory to scan
            parent_path: Parent path for nested items
            
        Returns:
            List of folder structures with metadata
        """
        folders = []
        
        if not directory.exists():
            return folders
        
        for item in directory.iterdir():
            if item.is_dir() and self.is_folder(item):
                folder_bru = item / "folder.bru"
                folder_data = self.parse_bru_file(folder_bru)
                
                folder_path = f"{parent_path}/{item.name}" if parent_path else item.name
                
                # Count requests in this folder (non-recursive)
                request_count = self.count_requests_in_directory(item)
                
                # Count subfolders
                subfolder_count = self.count_folders_in_directory(item)
                
                # Recursively count all requests (including in subfolders)
                total_request_count = request_count
                for subitem in item.iterdir():
                    if subitem.is_dir() and self.is_folder(subitem):
                        total_request_count += self.count_all_requests(subitem)
                
                folder_info = {
                    'name': folder_data['name'],
                    'path': str(item),
                    'type': 'folder',
                    'request_count': total_request_count,
                    'folder_count': subfolder_count,
                    'direct_request_count': request_count
                }
                
                folders.append(folder_info)
                
                # Recursively get nested folders
                nested_folders = self.get_folder_structure(item, folder_path)
                folders.extend(nested_folders)
        
        return folders
    
    def count_all_requests(self, directory: Path) -> int:
        """
        Recursively count all requests in a directory and its subdirectories.
        
        Args:
            directory: Directory to search
            
        Returns:
            Total number of requests
        """
        count = self.count_requests_in_directory(directory)
        
        for item in directory.iterdir():
            if item.is_dir():
                count += self.count_all_requests(item)
        
        return count
    
    def count_all_folders(self, directory: Path) -> int:
        """
        Recursively count all folders in a directory and its subdirectories.
        
        Args:
            directory: Directory to search
            
        Returns:
            Total number of folders
        """
        count = self.count_folders_in_directory(directory)
        
        for item in directory.iterdir():
            if item.is_dir():
                count += self.count_all_folders(item)
        
        return count
    
    def get_collection_structure(self) -> List[Dict[str, Any]]:
        """
        Get the complete structure of all collections in the workspace.
        
        Returns:
            List of collection structures with metadata
        """
        collections = []
        
        if not self.collections_path.exists():
            return collections
        
        for item in self.collections_path.iterdir():
            if item.is_dir() and self.is_collection_root(item):
                collection_bru = item / "collection.bru"
                collection_data = self.parse_bru_file(collection_bru)
                
                # Count requests and folders
                request_count = self.count_all_requests(item)
                folder_count = self.count_all_folders(item)
                
                structure = {
                    'name': item.name,  # Use directory name instead of parsing collection.bru
                    'path': str(item),
                    'type': 'collection',
                    'request_count': request_count,
                    'folder_count': folder_count,
                    'variables': collection_data['variables'],
                    'folders': self.get_folder_structure(item)
                }
                
                collections.append(structure)
        
        return collections
    
    def parse_environment_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Parse a Bruno environment file (.yml format).
        
        Args:
            file_path: Path to the environment .yml file
            
        Returns:
            Dictionary containing environment data
        """
        content = file_path.read_text(encoding='utf-8')
        
        variables = []
        
        # Parse YAML-like format manually (simple parsing)
        # Format:
        # name: dev
        # variables:
        #   - name: var1
        #     value: val1
        
        # Check if we're in the variables section
        in_variables_section = False
        for line in content.split('\n'):
            line = line.strip()
            
            if line.startswith('variables:'):
                in_variables_section = True
                continue
            
            if in_variables_section and line.startswith('- name:'):
                # Extract variable name
                var_name = line.replace('- name:', '').strip()
                variables.append(var_name)
        
        # Extract environment name from YAML
        env_name = file_path.stem
        for line in content.split('\n'):
            if line.startswith('name:'):
                env_name = line.replace('name:', '').strip()
                break
        
        return {
            'name': env_name,
            'path': str(file_path),
            'type': 'environment',
            'variable_count': len(variables),
            'variables': variables
        }
    
    def get_environment_variables(self) -> List[Dict[str, Any]]:
        """
        Get all environment variables from the workspace.
        
        Returns:
            List of environment structures with variable counts
        """
        environments = []
        
        if not self.environments_path.exists():
            return environments
        
        for env_file in self.environments_path.glob('*.yml'):
            env_data = self.parse_environment_file(env_file)
            environments.append(env_data)
        
        return environments
    
    def get_workspace_summary(self) -> Dict[str, Any]:
        """
        Get a complete summary of the Bruno workspace.
        
        Returns:
            Dictionary containing workspace structure and counts
        """
        collections = self.get_collection_structure()
        environments = self.get_environment_variables()
        
        total_requests = sum(c['request_count'] for c in collections)
        total_folders = sum(c['folder_count'] for c in collections)
        
        return {
            'workspace_path': str(self.workspace_path),
            'collection_count': len(collections),
            'total_folder_count': total_folders,
            'total_request_count': total_requests,
            'environment_count': len(environments),
            'collections': collections,
            'environments': environments
        }
