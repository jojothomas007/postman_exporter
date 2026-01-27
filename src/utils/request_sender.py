import sys
import json
import logging
import requests
from requests.exceptions import HTTPError, RequestException

# Set up logging
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)

class RequestSender:

    def post_request_json(self, request_url:str, header:json, payload:json, auth=None) -> requests.Response:
        logger.info("Request URL: POST %s", request_url)
        logger.info("Request Headers: %s", header)
        logger.info("Request Payload: %s", payload)
        try:
            response = requests.post(
                request_url,
                headers=header,
                auth=auth,
                json=payload 
            )
            response.raise_for_status()
            logger.info("Response : %s", response.content)
            return response
        except HTTPError as http_err:
            logger.error(f"HTTP error occurred: {http_err} - {response}")
        except RequestException as req_err:
            logger.error(f"Request error occurred: {req_err} - {response}")
        except Exception as err:
            logger.error(f"An unexpected error occurred: {err} - {response}")
        return None
    
    def post_request(self, request_url:str, header:json, payload:str, auth=None) -> requests.Response:
        logger.info("Request URL: POST %s", request_url)
        logger.info("Request Headers: %s", header)
        logger.info("Request Payload: %s", payload)
        try:
            response = requests.post(
                request_url,
                headers=header,
                auth=auth,
                data=payload 
            )
            response.raise_for_status()
            logger.info("Response : %s", response.content)
            return response
        except HTTPError as http_err:
            logger.error(f"HTTP error occurred: {http_err} - {response}")
        except RequestException as req_err:
            logger.error(f"Request error occurred: {req_err} - {response}")
        except Exception as err:
            logger.error(f"An unexpected error occurred: {err} - {response}")
        return None
    
    def put_request(self, request_url:str, header:json, payload:str, auth=None) -> requests.Response:
        logger.info("Request URL: PUT %s", request_url)
        logger.info("Request Headers: %s", header)
        logger.info("Request Payload: %s", payload)
        try:
            response = requests.put(
                request_url,
                headers=header,
                auth=auth,
                data=payload 
            )
            response.raise_for_status()
            logger.info("Response : %s", response.content)
            return response
        except HTTPError as http_err:
            logger.error(f"HTTP error occurred: {http_err} - {response}")
        except RequestException as req_err:
            logger.error(f"Request error occurred: {req_err} - {response}")
        except Exception as err:
            logger.error(f"An unexpected error occurred: {err} - {response}")
        return None
    
    def put_request_json(self, request_url:str, header:json, payload:str, auth=None) -> requests.Response:
        logger.info("Request URL: PUT %s", request_url)
        logger.info("Request Headers: %s", header)
        logger.info("Request Payload: %s", payload)
        try:
            response = requests.put(
                request_url,
                headers=header,
                auth=auth,
                json=payload 
            )
            response.raise_for_status()
            logger.info("Response : %s", response.content)
            return response
        except HTTPError as http_err:
            logger.error(f"HTTP error occurred: {http_err} - {response}")
        except RequestException as req_err:
            logger.error(f"Request error occurred: {req_err} - {response}")
        except Exception as err:
            logger.error(f"An unexpected error occurred: {err} - {response}")
        return None
    
    def get_request(self, request_url:str, headers:json, auth=None) -> requests.Response:
            logger.info("Request URL: %s", request_url)
            logger.info("Request Headers: %s", headers)
            try:
                response = requests.get(
                    request_url,
                    headers=headers,
                    auth=auth
                )
                response.raise_for_status()
                logger.info("Response : %s", response.content)
                return response
            except HTTPError as http_err:
                logger.error(f"HTTP error occurred: {http_err} - {response}")
            except RequestException as req_err:
                logger.error(f"Request error occurred: {req_err} - {response}")
            except Exception as err:
                logger.error(f"An unexpected error occurred: {err} - {response}")
            return None
