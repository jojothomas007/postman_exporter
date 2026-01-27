import logging
import zipfile
import io
import sys

# Set up logging
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)

class ZipUtil:

    def unzip(self, zip_content) -> dict:
        zip_content = io.BytesIO(zip_content)
        files_dict = {}
        with zipfile.ZipFile(zip_content, 'r') as zip_ref:
            # List all files in the ZIP archive
            logger.info(zip_ref.filelist)
            # Extract and process each file in the ZIP archive
            for file in zip_ref.namelist():
                with zip_ref.open(file) as extracted_file:
                    files_dict[file] = extracted_file.read()
                    print(f"Content of {file}:")
                    print(extracted_file.read().decode('utf-8'))
        return files_dict

                