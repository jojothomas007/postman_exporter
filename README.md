# Postman Exporter

A lightweight Python tool for exporting Postman collections from workspaces.

## Overview

Postman Exporter is a simple automation tool that connects to the Postman API to export collections from all your workspaces. Each collection is saved as a JSON file with a clear naming convention.

## Features

- **Workspace Discovery**: Automatically fetches all accessible workspaces
- **Collection Export**: Exports all collections from each workspace as JSON files
- **Clean Naming**: Files are named as `{workspace-name}-{collection-name}.json`
- **Robust HTTP Handling**: Built-in request utilities with error handling and logging
- **Utility Functions**: ZIP file handling for compressed data

## Prerequisites

- Python 3.12 or higher
- Poetry (for dependency management)
- Postman API key

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd postman-exporter
   ```

2. **Install dependencies using Poetry**:
   ```bash
   poetry install
   ```

3. **Set up environment variables**:
   
   Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
   
   Then edit `.env` and add your Postman API credentials:
   ```env
   postman_api_url=https://api.getpostman.com
   postman_api_key=your_postman_api_key_here
   ```

## Usage

### Export All Collections

Run the main script to export all Postman collections:

```bash
poetry run python main.py
```

This will:
1. Fetch all workspaces from your Postman account
2. Iterate through each workspace
3. Export all collections as JSON files
4. Save files with the naming format: `{workspace-name}-{collection-name}.json`

### Example Output

```
INFO:__main__:Request URL: https://api.getpostman.com/workspaces
Exported API Tests from workspace Development
importing collection name : API Tests
Exported Integration Tests from workspace QA
importing collection name : Integration Tests
```

## Project Structure

```
postman-exporter/
├── src/
│   ├── __init__.py
│   ├── config.py              # Configuration management with dotenv
│   └── utils/                 # Utility modules
│       ├── __init__.py
│       ├── request_sender.py  # HTTP request wrapper with error handling
│       └── zip_util.py        # ZIP file extraction utilities
├── tests/                     # Test files
├── references/                # Reference documentation
├── dist/                      # Distribution files
├── main.py                    # Entry point script
├── pyproject.toml             # Poetry configuration
├── poetry.lock                # Locked dependencies
├── .env.example               # Example environment variables
├── .env                       # Your environment variables (not in repo)
├── .gitignore                 # Git ignore rules
├── LICENSE                    # MIT License
└── README.md                  # This file
```

## Core Components

### Configuration (`src/config.py`)

Manages environment variables using `python-dotenv`. The Config class loads settings from the `.env` file, including:
- Postman API URL and key
- Additional integration settings (GPT, Jira, Xray, GitHub, Confluence) for future extensions

### Request Sender (`src/utils/request_sender.py`)

A robust HTTP client wrapper that provides:
- `get_request()`: GET requests with error handling
- `post_request()` / `post_request_json()`: POST requests (data/JSON)
- `put_request()` / `put_request_json()`: PUT requests (data/JSON)
- Comprehensive logging for debugging
- Exception handling for HTTP errors

### ZIP Utility (`src/utils/zip_util.py`)

Utility class for handling ZIP archives:
- `unzip()`: Extracts ZIP content and returns files as a dictionary

## Development

### Running in Debug Mode

The project includes a VS Code launch configuration for debugging:

```json
{
    "name": "main",
    "type": "debugpy",
    "request": "launch",
    "program": "${workspaceFolder}/main.py"
}
```

Press F5 in VS Code to start debugging.

### Running Tests

```bash
poetry run pytest
```

### Dependencies

The project uses minimal dependencies:
- `python-dotenv`: Environment variable management
- `requests`: HTTP library for API calls

## Environment Variables

The `.env.example` file shows the minimum required configuration:

```env
postman_api_url=https://api.getpostman.com
postman_api_key=
```

**Note**: The `config.py` file contains references to additional environment variables (Jira, Xray, GitHub, GPT, Confluence) that are not currently used by the main export functionality. These are available for future extensions.

## Output Files

Exported collections are saved in the project root directory with the format:
- `{workspace-name}-{collection-name}.json`

Example:
- `Development-API Tests.json`
- `QA-Integration Tests.json`

## Logging

The application uses Python's built-in logging module configured at INFO level. All HTTP requests and responses are logged to stdout for transparency and debugging.

## Error Handling

The `RequestSender` utility provides comprehensive error handling:
- **HTTPError**: HTTP-specific errors (4xx, 5xx responses)
- **RequestException**: General request errors (network issues, timeouts)
- **Generic Exception**: Catches unexpected errors

All errors are logged with detailed information.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Jojo Thomas** - [jojothomas007@gmail.com](mailto:jojothomas007@gmail.com)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Version History

- **0.1.1** - Current version
  - Postman collection export functionality
  - Robust HTTP request handling
  - Comprehensive logging

## Troubleshooting

### Common Issues

1. **Authentication Error**
   - Ensure your Postman API key is valid
   - Verify the API key has the necessary permissions to read workspaces and collections
   - Check that the `.env` file is in the project root

2. **Missing Dependencies**
   - Run `poetry install` to ensure all dependencies are installed
   - Make sure you're using Python 3.12 or higher

3. **Import Errors**
   - Verify the `src` package structure is intact
   - Ensure `__init__.py` files exist in the `src` and `src/utils` directories

4. **No Collections Exported**
   - Check the console output for error messages
   - Verify your Postman account has accessible workspaces and collections
   - Review the logs for HTTP errors

### Getting Help

For issues, questions, or contributions, please open an issue in the GitHub repository.
