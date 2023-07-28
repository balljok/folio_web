# -*- coding: utf-8 -*-

"""
Modul som sköter kommuniktaion med Folios API:er
"""

import json
import logging
import os
import requests
from dotenv import load_dotenv
from foliologging import foliologging


def exception_handler(func):
    """
    Decorator för att hantera exceptions på ett enhetligt sätt.
    """

    def wrapper(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
            return response
        except requests.exceptions.ConnectionError as connection_err:
            logging.error("Connection error: %s", connection_err)
            raise ConnectionError("Folio seems to be down") from connection_err
        except requests.exceptions.Timeout as timeout_err:
            logging.error("Server timeout.")
            raise TimeoutError("Folio seems to be down") from timeout_err
        except requests.exceptions.HTTPError as http_err:
            if not str(http_err).startswith("422"):
                logging.error("HTTP error occurred: %s", http_err)
            # return response.status_code
            return int(str(http_err)[0:3])
        except Exception as err:
            logging.error("Other error occurred: %s", err)
            return None

    return wrapper


class FolioCommunication:
    """
    Klass som sköter kommunikation med Folios API:er.
    """

    def __init__(self):
        # Initialize environment variables
        env_file = os.getcwd() + "/.env"
        load_dotenv(env_file)
        self.folio_endpoint = os.environ["FOLIO_ENDPOINT"]
        self.timeout = 60
        self.username = os.environ["FOLIO_USER"]
        self.password = os.environ["FOLIO_PASSWORD"]
        self.okapi_tenant = os.environ["FOLIO_TENANT"]
        self.payload = json.dumps(
            {"username": self.username, "password": self.password}
        )

        # Define generic header without okapi token
        self.header = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "x-okapi-tenant": self.okapi_tenant,
        }

        # Fetch okapi token
        self.okapi_token = self._get_token()

        # Add okapi token to header
        self.header["x-okapi-token"] = self.okapi_token

    @exception_handler
    def _get_token(self):
        """Hämta OKAPI-token"""
        okapi_token = ""
        url = f"{self.folio_endpoint}/authn/login"

        response = requests.post(
            url, data=self.payload, headers=self.header, timeout=self.timeout
        )
        response.raise_for_status()
        okapi_token = response.headers["x-okapi-token"]
        return okapi_token

    @exception_handler
    def getData(self, path, query=None, limit=10):
        """Generell metod för att göra GET i Folio"""
        url = self.folio_endpoint + path
        if query:
            param = {"query": query, "limit": limit}
        else:
            param = {"limit": limit}

        response = requests.get(
            url,
            data=self.payload,
            headers=self.header,
            params=param,
            timeout=self.timeout,
        )
        response.raise_for_status()
        response_json = response.json()
        return response_json

    @exception_handler
    def postData(self, path, payload):
        """Generell metod för att göra POST i Folio"""
        url = self.folio_endpoint + path

        response = requests.post(
            url, data=payload, headers=self.header, timeout=self.timeout
        )
        response.raise_for_status()
        return response

    @exception_handler
    def putData(self, path, payload):
        """Generell metod för att göra PUT i Folio"""
        url = self.folio_endpoint + path
        local_header = self.header
        local_header["Accept"] = "text/plain"

        response = requests.put(
            url, data=payload, headers=local_header, timeout=self.timeout
        )
        response.raise_for_status()
        return response

    @exception_handler
    def deleteData(self, path):
        """Generell metod för att göra DELETE i Folio"""
        url = self.folio_endpoint + path
        local_header = self.header
        local_header["Accept"] = "text/plain"

        response = requests.delete(url, headers=local_header, timeout=self.timeout)
        response.raise_for_status()
        return response
