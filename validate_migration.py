"""
Migration Validation Script

Validates the migration from Postman to Bruno workspaces and generates a CSV report.
"""

import argparse
import sys
from pathlib import Path
from src.validators.migration_validator import MigrationValidator
from src.validators.csv_report_generator import CSVReportGenerator
from src.config import Config

def main():
    """Main entry point for the migration validation script."""
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description='Validate Postman to Bruno migration',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python validate_migration.py
  python validate_migration.py -o results/validation.csv
        """
    )
   
    parser.add_argument(
        '--output', '-o',
        default='validation_report.csv',
        help='Output CSV file path (default: validation_report.csv)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    # Validate paths exist
    postman_path = Path(Config.postman_export_folder, Config.validation_workspace)
    bruno_path = Path(Config.bruno_workspace_folder, Config.validation_workspace)
    
    if not postman_path.exists():
        print(f"ERROR: Postman workspace path does not exist: {postman_path}")
        sys.exit(1)
    
    if not bruno_path.exists():
        print(f"ERROR: Bruno workspace path does not exist: {bruno_path}")
        sys.exit(1)
    
    print("=" * 60)
    print("MIGRATION VALIDATION")
    print("=" * 60)
    print(f"Postman workspace: {postman_path}")
    print(f"Bruno workspace:   {bruno_path}")
    print(f"Output file:       {args.output}")
    print("=" * 60)
    print()
    
    # Initialize validator
    if args.verbose:
        print("Initializing validator...")
    
    validator = MigrationValidator(str(postman_path), str(bruno_path))
    
    # Generate validation report
    if args.verbose:
        print("Parsing Postman workspace...")
        print("Parsing Bruno workspace...")
        print("Comparing structures...")
    
    print("Generating validation report...")
    validation_results = validator.generate_validation_report()
    
    # Get summary
    summary = validator.get_summary()
    
    # Display summary
    print()
    print(CSVReportGenerator.format_summary_table(summary))
    print()
    
    # Display failed validations
    failed_results = [r for r in validation_results if r['validation_status'] == 'Fail']
    if failed_results:
        print("FAILED VALIDATIONS:")
        print("-" * 60)
        for result in failed_results:
            print(f"  {result['type'].upper()}: {result['description']}")
            print(f"    Postman: {result['postman_count']} | Bruno: {result['bruno_count']}")
            print(f"    Path: {result['postman_item_path']}")
            print()
    
    # Generate CSV report
    CSVReportGenerator.generate_csv(validation_results, args.output)
    
    print()
    print("Validation complete!")
    
    # Exit with appropriate code
    if summary['failed'] > 0:
        print(f"\nWARNING: {summary['failed']} validation(s) failed.")
        sys.exit(1)
    else:
        print("\nSUCCESS: All validations passed!")
        sys.exit(0)


if __name__ == '__main__':
    main()
