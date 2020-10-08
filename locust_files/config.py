# Locust test Global Settings

import logging

BASE_URL = ''
API_HEADERS = {}

VALID_RESPONSE_CODES = [200]
USER_CREDENTIALS_FILE_NAME = 'users.txt'
USER_API_PASSWORD = 'locust_sample'

try:
    from locust_files.local_config import *
except ImportError:
    logging.warning('Missing Local Configs')


def fetch_data_from_file(file_name):
    try:
        with open(file_name, 'r') as file_reader:
            return file_reader.readlines()
    except FileNotFoundError:
        logging.warning('Invalid User Credentials ')
        return []


USER_POOL = set(fetch_data_from_file(USER_CREDENTIALS_FILE_NAME))


