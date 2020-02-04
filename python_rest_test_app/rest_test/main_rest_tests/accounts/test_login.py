__author__ = 'alonitzhaki'

from unittest import TestCase

from time import time
import httplib

from rest_test.clients.clients_utils import ClientUtils
from rest_test.clients.login_client import LoginClient
from rest_test.clients.register_client import RegisterClient
from rest_test.extra_data_manager import ExtraDataManager


# from utils.clients.main_client import MainLoginV2Mixin


class LoginTests(TestCase):
    eidm_user_id = None
    user_name = 'rest_tests_login_' + str(int(time())) + '@autodesk.com'
    first_name = 'Rest'
    last_name = 'Test'
    valid_password = 'Moomoo123'
    wrong_password = 'wrong_password'
    empty_password = None

    extra_data = None
    login_client = LoginClient()

    def setUp(self):
        self.extra_data = ExtraDataManager()
        self.extra_data.add_test_data('user name', self.user_name)
        register_client = RegisterClient()
        if LoginTests.eidm_user_id is None:
            response = register_client.register_v1(user_name=self.user_name, password=self.valid_password,
                                                   first_name=self.first_name, last_name=self.last_name)
            status_code = ClientUtils.get_response_status_code(response)
            self.assertEqual(httplib.OK, status_code,
                             'Got status code: ' + str(status_code) + self.extra_data.get_all())
            self.extra_data.add_test_data('register response', ClientUtils.get_response_body(response))

            LoginTests.eidm_user_id = ClientUtils.get_value_from_body(response, RegisterClient.KEY_EIDM_USER_ID)
            self.assertIsNotNone(LoginTests.eidm_user_id,
                                 'Expected Eidm user id not None, Register failed in setup' + self.extra_data.get_all())

    def test_login_v2_valid_credentials(self):
        response = self.login_client.login_v2(user_name=self.user_name, password=self.valid_password)

        status_code = ClientUtils.get_response_status_code(response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())

        response_user_name = ClientUtils.get_value_from_body(response, LoginClient.KEY_USER_INFO + '.' +
                                                             LoginClient.KEY_USERNAME)
        self.assertEqual(self.user_name, response_user_name,
                         'Expected user_name: ' + str(self.user_name) + ' but got: ' + str(response_user_name))

        response_eidm_user_id = ClientUtils.get_value_from_body(response, LoginClient.KEY_USER_INFO + '.' +
                                                                LoginClient.KEY_EIDM_USER_ID)
        self.assertEqual(LoginTests.eidm_user_id, response_eidm_user_id,
                         'Expected eidm user id: ' + str(self.eidm_user_id) + ' but got: ' + str(
                             response_eidm_user_id) + self.extra_data.get_all())

    def test_login_v2_incorrect_credentials(self):
        response = self.login_client.login_v2(user_name=self.user_name, password=self.wrong_password)
        status_code = ClientUtils.get_response_status_code(response)
        self.assertEqual(httplib.UNAUTHORIZED, status_code,
                         'Got status code: ' + str(status_code) + self.extra_data.get_all())

    def test_login_v2_no_password(self):
        response = self.login_client.login_v2(user_name=self.user_name, password=self.empty_password)
        status_code = ClientUtils.get_response_status_code(response)
        self.assertEqual(httplib.UNAUTHORIZED, status_code,
                         'Got status code: ' + str(status_code) + self.extra_data.get_all())
