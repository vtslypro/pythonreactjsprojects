__author__ = 'alonitzhaki'
from unittest import TestCase

from time import time
import httplib

from utils.clients.main_client import MainRegisterAndLoginMixin
from rest_test.extra_data_manager import ExtraDataManager
from rest_test.clients.clients_utils import ClientUtils
from rest_test.clients.user_client import UserClient


class UserDetailsTest(TestCase):
    auth = None

    user_name = 'rest_tests_user_details_' + str(int(time())) + '@autodesk.com'
    first_name = 'Rest'
    last_name = 'Test'
    password = 'Moomoo123'

    extra_data = None
    user_client = UserClient()

    def setUp(self):
        self.extra_data = ExtraDataManager()
        self.extra_data.add_test_data('user name', self.user_name)
        main_register_and_login_mixin = MainRegisterAndLoginMixin()
        if UserDetailsTest.auth is None:
            response = main_register_and_login_mixin.login_or_register(user_name=self.user_name,
                                                                       password=self.password,
                                                                       first_name=self.first_name,
                                                                       last_name=self.last_name)
            UserDetailsTest.auth = main_register_and_login_mixin.get_auth_from_login_data(response)
        self.assertIsInstance(UserDetailsTest.auth, str,
                              'Invalid auth: ' + str(UserDetailsTest.auth) + self.extra_data.get_all())

    def test_get_user_details(self):
        response = self.user_client.get_user_details(auth=self.auth)
        status_code = ClientUtils.get_response_status_code(response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())

        self.assertTrue(len(response.history) > 1,
                        'Expected at least one redirect url in response history. response history: ' + str(
                            response.history) + self.extra_data.get_all())

    def test_user_status(self):
        response = self.user_client.get_user_status(auth=self.auth)
        status_code = ClientUtils.get_response_status_code(response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('get_user_status response', ClientUtils.get_response_body(response))

        status = ClientUtils.get_value_from_body(response, 'status')
        self.assertEqual(1, status, 'Expected status: 1 but got: ' + str(status) + self.extra_data.get_all())
