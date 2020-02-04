__author__ = 'alonitzhaki'
from unittest import TestCase
import httplib

from time import time

from utils.clients.main_client import MainRegisterAndLoginMixin

from rest_test.extra_data_manager import ExtraDataManager
from rest_test.clients.clients_utils import ClientUtils
from rest_test.clients.user_client import UserClient


class UserPreferencesTests(TestCase):
    auth = None

    user_name = 'rest_tests_user_preferences_' + str(int(time())) + '@autodesk.com'
    first_name = 'Rest'
    last_name = 'Test'
    password = 'Moomoo123'

    extra_data = None
    user_preferences_client = UserClient()

    def setUp(self):
        self.extra_data = ExtraDataManager()
        self.extra_data.add_test_data('user name', self.user_name)
        main_register_and_login_mixin = MainRegisterAndLoginMixin()
        if UserPreferencesTests.auth is None:
            response = main_register_and_login_mixin.login_or_register(user_name=self.user_name,
                                                                       password=self.password,
                                                                       first_name=self.first_name,
                                                                       last_name=self.last_name)
            UserPreferencesTests.auth = main_register_and_login_mixin.get_auth_from_login_data(response)
        self.assertIsInstance(UserPreferencesTests.auth, str,
                              'Invalid auth: ' + str(UserPreferencesTests.auth) + self.extra_data.get_all())

    def test_get_user_preferences(self):
        response = self.user_preferences_client.get_user_preferences(auth=self.auth)

        status_code = ClientUtils.get_response_status_code(response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('get_user_preferences response', ClientUtils.get_response_body(response))

        version = ClientUtils.get_value_from_body(response, UserClient.KEY_VERSION)
        self.assertIsInstance(version, int,
                              'Expected an integer version but got: ' + str(version) + self.extra_data.get_all())

    def test_post_user_preferences(self):
        expected_country = 'UK'

        response = self.user_preferences_client.post_user_preferences(auth=self.auth, country=expected_country)
        self.assertIsNotNone(response, 'Response is None. user_name: ' + str(self.user_name))
        status_code = ClientUtils.get_response_status_code(response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.assertTrue(ClientUtils.is_response_body_empty(response),
                        'Expected empty body in response but got ' + str(
                            ClientUtils.get_response_body(response)) + self.extra_data.get_all())

        get_user_preferences_response = self.user_preferences_client.get_user_preferences(auth=self.auth)
        status_code = ClientUtils.get_response_status_code(get_user_preferences_response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('get_user_preferences_response',
                                      ClientUtils.get_response_body(get_user_preferences_response))

        country = ClientUtils.get_value_from_body(get_user_preferences_response, UserClient.KEY_COUNTRY)
        self.assertEqual(expected_country, country,
                         'Expected changed country: ' + str(expected_country) + ' but got: ' + str(
                             country) + self.extra_data.get_all())
