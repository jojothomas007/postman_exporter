"""
CSV Report Generator

Generates CSV reports from validation results.
"""

import csv
from pathlib import Path
from typing import List, Dict, Any


class CSVReportGenerator:
    """Generates CSV reports from validation results."""
    
    @staticmethod
    def generate_csv(validation_results: List[Dict[str, Any]], output_file: str) -> None:
        """
        Generate a CSV report from validation results.
        
        Args:
            validation_results: List of validation result dictionaries
            output_file: Path to the output CSV file
        """
        if not validation_results:
            print("No validation results to write.")
            return
        
        # Define CSV columns
        fieldnames = [
            'postman_item_path',
            'bruno_path',
            'type',
            'postman_count',
            'bruno_count',
            'validation_status',
            'description'
        ]
        
        # Write CSV file
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Write header
            writer.writeheader()
            
            # Write rows
            for result in validation_results:
                # Create row with all required fields
                row = {
                    'postman_item_path': result.get('postman_item_path', ''),
                    'bruno_path': result.get('bruno_path', ''),
                    'type': result.get('type', ''),
                    'postman_count': result.get('postman_count', 0),
                    'bruno_count': result.get('bruno_count', 0),
                    'validation_status': result.get('validation_status', ''),
                    'description': result.get('description', '')
                }
                writer.writerow(row)
        
        print(f"CSV report generated: {output_path}")
    
    @staticmethod
    def format_summary_table(summary: Dict[str, Any]) -> str:
        """
        Format a summary as a text table.
        
        Args:
            summary: Summary dictionary from validator
            
        Returns:
            Formatted table string
        """
        lines = []
        lines.append("=" * 60)
        lines.append("VALIDATION SUMMARY")
        lines.append("=" * 60)
        lines.append(f"Total Validations: {summary['total_validations']}")
        lines.append(f"Passed:            {summary['passed']}")
        lines.append(f"Failed:            {summary['failed']}")
        lines.append(f"Info:              {summary['info']}")
        lines.append(f"Success Rate:      {summary['success_rate']:.2f}%")
        lines.append("=" * 60)
        
        return "\n".join(lines)
