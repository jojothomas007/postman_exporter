"""
Migration Validator

Compares Postman and Bruno workspaces and validates the migration.
"""

from typing import Dict, List, Any, Tuple
from .postman_parser import PostmanParser
from .bruno_parser import BrunoParser


class MigrationValidator:
    """Validates migration from Postman to Bruno."""
    
    def __init__(self, postman_path: str, bruno_path: str):
        """
        Initialize the migration validator.
        
        Args:
            postman_path: Path to the Postman workspace
            bruno_path: Path to the Bruno workspace
        """
        self.postman_parser = PostmanParser(postman_path)
        self.bruno_parser = BrunoParser(bruno_path)
        self.validation_results = []
        
    def normalize_name(self, name: str) -> str:
        """
        Normalize a name for comparison (remove spaces, convert to lowercase).
        
        Args:
            name: Name to normalize
            
        Returns:
            Normalized name
        """
        return name.lower().replace(' ', '').replace('_', '').replace('-', '')
    
    def find_matching_bruno_collection(self, postman_collection: Dict[str, Any], 
                                      bruno_collections: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Find a matching Bruno collection for a Postman collection.
        
        Args:
            postman_collection: Postman collection data
            bruno_collections: List of Bruno collections
            
        Returns:
            Matching Bruno collection or None
        """
        pm_name = self.normalize_name(postman_collection['name'])
        
        for bruno_col in bruno_collections:
            bruno_name = self.normalize_name(bruno_col['name'])
            if pm_name == bruno_name:
                return bruno_col
        
        return None
    
    def find_matching_bruno_folder(self, postman_folder: Dict[str, Any],
                                   bruno_folders: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Find a matching Bruno folder for a Postman folder.
        
        Args:
            postman_folder: Postman folder data
            bruno_folders: List of Bruno folders
            
        Returns:
            Matching Bruno folder or None
        """
        pm_name = self.normalize_name(postman_folder['name'])
        
        for bruno_folder in bruno_folders:
            bruno_name = self.normalize_name(bruno_folder['name'])
            if pm_name == bruno_name:
                return bruno_folder
        
        return None
    
    def validate_collections(self) -> List[Dict[str, Any]]:
        """
        Validate collections between Postman and Bruno.
        
        Returns:
            List of validation results
        """
        results = []
        
        postman_summary = self.postman_parser.get_workspace_summary()
        bruno_summary = self.bruno_parser.get_workspace_summary()
        
        postman_collections = postman_summary['collections']
        bruno_collections = bruno_summary['collections']
        
        # Validate collection count
        results.append({
            'postman_item_path': postman_summary['workspace_path'] + '/collections',
            'bruno_path': bruno_summary['workspace_path'] + '/collections',
            'type': 'workspace',
            'postman_count': len(postman_collections),
            'bruno_count': len(bruno_collections),
            'validation_status': 'Pass' if len(postman_collections) == len(bruno_collections) else 'Fail',
            'description': 'Collection count in workspace'
        })
        
        # Validate each collection
        for pm_col in postman_collections:
            bruno_col = self.find_matching_bruno_collection(pm_col, bruno_collections)
            
            if bruno_col:
                # Collection found - validate counts
                results.append({
                    'postman_item_path': pm_col['path'],
                    'bruno_path': bruno_col['path'],
                    'type': 'collection',
                    'postman_count': pm_col['request_count'],
                    'bruno_count': bruno_col['request_count'],
                    'validation_status': 'Pass' if pm_col['request_count'] == bruno_col['request_count'] else 'Fail',
                    'description': f"Request count in collection '{pm_col['name']}'"
                })
                
                results.append({
                    'postman_item_path': pm_col['path'],
                    'bruno_path': bruno_col['path'],
                    'type': 'collection',
                    'postman_count': pm_col['folder_count'],
                    'bruno_count': bruno_col['folder_count'],
                    'validation_status': 'Pass' if pm_col['folder_count'] == bruno_col['folder_count'] else 'Fail',
                    'description': f"Folder count in collection '{pm_col['name']}'"
                })
                
                # Validate folders within the collection
                folder_results = self.validate_folders(pm_col, bruno_col)
                results.extend(folder_results)
            else:
                # Collection not found in Bruno
                results.append({
                    'postman_item_path': pm_col['path'],
                    'bruno_path': 'NOT FOUND',
                    'type': 'collection',
                    'postman_count': pm_col['request_count'],
                    'bruno_count': 0,
                    'validation_status': 'Fail',
                    'description': f"Collection '{pm_col['name']}' not found in Bruno"
                })
        
        return results
    
    def validate_folders(self, postman_collection: Dict[str, Any],
                        bruno_collection: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Validate folders within a collection.
        
        Args:
            postman_collection: Postman collection data
            bruno_collection: Bruno collection data
            
        Returns:
            List of validation results for folders
        """
        results = []
        
        pm_folders = postman_collection.get('folders', [])
        bruno_folders = bruno_collection.get('folders', [])
        
        for pm_folder in pm_folders:
            bruno_folder = self.find_matching_bruno_folder(pm_folder, bruno_folders)
            
            if bruno_folder:
                # Folder found - validate request count
                results.append({
                    'postman_item_path': pm_folder['path'],
                    'bruno_path': bruno_folder['path'],
                    'type': 'folder',
                    'postman_count': pm_folder['request_count'],
                    'bruno_count': bruno_folder['request_count'],
                    'validation_status': 'Pass' if pm_folder['request_count'] == bruno_folder['request_count'] else 'Fail',
                    'description': f"Request count in folder '{pm_folder['name']}'"
                })
            else:
                # Folder not found in Bruno
                results.append({
                    'postman_item_path': pm_folder['path'],
                    'bruno_path': 'NOT FOUND',
                    'type': 'folder',
                    'postman_count': pm_folder['request_count'],
                    'bruno_count': 0,
                    'validation_status': 'Fail',
                    'description': f"Folder '{pm_folder['name']}' not found in Bruno"
                })
        
        return results
    
    def validate_environments(self) -> List[Dict[str, Any]]:
        """
        Validate environments and variables between Postman and Bruno.
        
        Returns:
            List of validation results
        """
        results = []
        
        postman_envs = self.postman_parser.get_environment_variables()
        bruno_envs = self.bruno_parser.get_environment_variables()
        
        # Validate environment count
        results.append({
            'postman_item_path': str(self.postman_parser.environments_path),
            'bruno_path': str(self.bruno_parser.environments_path),
            'type': 'environment',
            'postman_count': len(postman_envs),
            'bruno_count': len(bruno_envs),
            'validation_status': 'Pass' if len(postman_envs) == len(bruno_envs) else 'Fail',
            'description': 'Environment count'
        })
        
        # Validate each environment
        for pm_env in postman_envs:
            # Find matching Bruno environment
            bruno_env = None
            pm_name = self.normalize_name(pm_env['name'])
            
            for be in bruno_envs:
                if self.normalize_name(be['name']) == pm_name:
                    bruno_env = be
                    break
            
            if bruno_env:
                results.append({
                    'postman_item_path': pm_env['path'],
                    'bruno_path': bruno_env['path'],
                    'type': 'environment',
                    'postman_count': pm_env['variable_count'],
                    'bruno_count': bruno_env['variable_count'],
                    'validation_status': 'Pass' if pm_env['variable_count'] == bruno_env['variable_count'] else 'Fail',
                    'description': f"Variable count in environment '{pm_env['name']}'"
                })
            else:
                results.append({
                    'postman_item_path': pm_env['path'],
                    'bruno_path': 'NOT FOUND',
                    'type': 'environment',
                    'postman_count': pm_env['variable_count'],
                    'bruno_count': 0,
                    'validation_status': 'Fail',
                    'description': f"Environment '{pm_env['name']}' not found in Bruno"
                })
        
        # Validate global variables
        global_vars = self.postman_parser.get_global_variables()
        if global_vars:
            results.append({
                'postman_item_path': global_vars['path'],
                'bruno_path': 'N/A',
                'type': 'global_variables',
                'postman_count': global_vars['variable_count'],
                'bruno_count': 0,
                'validation_status': 'Info',
                'description': 'Global variables (Bruno does not have direct equivalent)'
            })
        
        return results
    
    def generate_validation_report(self) -> List[Dict[str, Any]]:
        """
        Generate the complete validation report.
        
        Returns:
            List of validation results
        """
        self.validation_results = []
        
        # Validate collections and folders
        collection_results = self.validate_collections()
        self.validation_results.extend(collection_results)
        
        # Validate environments
        env_results = self.validate_environments()
        self.validation_results.extend(env_results)
        
        return self.validation_results
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get a summary of validation results.
        
        Returns:
            Dictionary containing summary statistics
        """
        if not self.validation_results:
            self.generate_validation_report()
        
        total = len(self.validation_results)
        passed = sum(1 for r in self.validation_results if r['validation_status'] == 'Pass')
        failed = sum(1 for r in self.validation_results if r['validation_status'] == 'Fail')
        info = sum(1 for r in self.validation_results if r['validation_status'] == 'Info')
        
        return {
            'total_validations': total,
            'passed': passed,
            'failed': failed,
            'info': info,
            'success_rate': (passed / total * 100) if total > 0 else 0
        }
