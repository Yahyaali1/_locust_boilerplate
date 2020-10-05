import random
import logging
import json

from locust.user import HttpUser
from locust.exception import StopUser

from user_focused_locust_boilerplate.config import (BASE_URL, API_HEADERS, USER_POOL, USER_API_PASSWORD,
                                                    VALID_RESPONSE_CODES)
from user_focused_locust_boilerplate.locust_files.exceptions import (UserCredentialsExhaustedException,
                                                                     LoginFailureException)


class BaseUser(HttpUser):
    """
    Base User to provide abstraction for handling headers, cookies and logins
    """
    host = BASE_URL
    abstract = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.headers = API_HEADERS.copy()
        self.user_name = None
        self.password = None

    def login_user_api(self):
        raise NotImplementedError

    def pre_login_hook(self):
        self.user_name = self.get_user_from_pool()
        self.password = USER_API_PASSWORD
        self.remove_user_from_pool(self.user_name)

    def post_login_hook(self, response):
        self.update_headers(response)

    def update_headers(self, response):
        raise NotImplementedError

    @staticmethod
    def remove_user_from_pool(user_name):
        USER_POOL.remove(user_name)

    @staticmethod
    def is_valid_response(response):
        return response.status_code in VALID_RESPONSE_CODES and BaseUser.is_valid_response_data(response)

    @staticmethod
    def log_api_response(response, api_name, log_response=False):
        response_log_format = '{}_{}_{}'
        logging.info(
            response_log_format.format(
                response.status_code, api_name, 'SUCCESS' if BaseUser.is_valid_response(response) else 'FAILURE'
            )
        )

        if log_response:
            try:
                logging.info(response.json())
            except json.JSONDecodeError:
                logging.error(response.content)

    @staticmethod
    def is_valid_response_data(response):
        """
        Helper method for validating data in response body

        Parameters
        ----------
        response

        Returns
        -------
        bool: True if response body is valid, False otherwise

        """
        raise NotImplementedError

    def perform_login(self):
        """
        Calls
        1. Pre login hook
        2. Try to login using login user api
        3. Post login hook

        Returns
        -------
        response
        """
        self.pre_login_hook()
        response = self.login_user_api()
        self.log_api_response(response, api_name='LOGIN', log_response=False)

        if not self.is_valid_response(response):
            raise LoginFailureException('FAILED TO LOGIN USER')

        self.post_login_hook(response)

        return response

    @staticmethod
    def get_user_from_pool():
        """
        Load a random user_name from set of User Pool

        Returns
        -------
        user_name: str
        """
        if not USER_POOL:
            raise UserCredentialsExhaustedException('USER POOL EXHAUSTED. UNABLE TO LOAD MORE USERS')
        return random.choice(tuple(USER_POOL))

    def on_start(self):
        try:
            self.perform_login()
        except LoginFailureException:
            logging.exception(
                'Failure in user login. Shutting down user instance {}_{}'.format(self.user_name, self.password)
            )
            raise StopUser

    def restore_user_to_user_pool(self):
        """
        Restores User back to user pool for reoccurring Tests
        """
        if self.user_name and self.password:
            USER_POOL.add(self.user_name)

    def on_stop(self):
        self.restore_user_to_user_pool()
