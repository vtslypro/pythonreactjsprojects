__author__ = 'alonitzhaki'
from unittest import TestCase
from time import time
import httplib

from utils.clients.main_client import MainRegisterAndLoginMixin

from rest_test.clients.files_client import FilesManagementClient
from rest_test.clients.clients_utils import ClientUtils
from rest_test.tests_utils import TestUtils
from rest_test.clients.user_client import UserClient
from rest_test.extra_data_manager import ExtraDataManager


class UserShareSuggestionsTest(TestCase):
    auth = None

    user_name = 'rest_tests_user_share_suggestions_' + str(int(time())) + '@autodesk.com'
    first_name = 'Rest'
    last_name = 'Test'
    password = 'Moomoo123'

    extra_data = None
    user_client = UserClient()
    files_management_client = FilesManagementClient()
    main_register_and_login_mixin = MainRegisterAndLoginMixin()

    def setUp(self):
        self.extra_data = ExtraDataManager()
        self.extra_data.add_test_data('user name', self.user_name)
        if UserShareSuggestionsTest.auth is None:
            response = self.main_register_and_login_mixin.login_or_register(user_name=self.user_name,
                                                                            password=self.password,
                                                                            first_name=self.first_name,
                                                                            last_name=self.last_name)
            UserShareSuggestionsTest.auth = self.main_register_and_login_mixin.get_auth_from_login_data(response)
        self.assertIsInstance(UserShareSuggestionsTest.auth, str,
                              'Invalid auth: ' + str(UserShareSuggestionsTest.auth) + self.extra_data.get_all())

    def test_get_user_share_suggestions(self):
        file_name = 'test_file_get_user_share_suggestions' + str(int(time())) + '.dwg'
        user_name_to_share_with = 'rest_tests_share_with_user' + str(int(time())) + '@autodesk.com'
        first_name_share_with = 'Rest'
        last_name_share_with = 'Test'
        password_share_with = 'Moomoo123'

        self.extra_data.add_test_data('file name', file_name)
        self.extra_data.add_test_data('user name to share with', user_name_to_share_with)

        created_file_id, msg = TestUtils.create_file(auth=self.auth, file_name=file_name, extra_data=self.extra_data)
        self.assertIsNotNone(created_file_id, msg + self.extra_data.get_all())

        login_data = self.main_register_and_login_mixin.login_or_register(user_name=user_name_to_share_with,
                                                                          password=password_share_with,
                                                                          first_name=first_name_share_with,
                                                                          last_name=last_name_share_with)
        self.assertIsNotNone(login_data,
                             'Failed to register user_name_to_share_with' + self.extra_data.get_all())

        share_response = self.files_management_client.share_file_v2(auth=self.auth, file_id=created_file_id,
                                                                    emails=[user_name_to_share_with])
        status_code = ClientUtils.get_response_status_code(share_response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('share_file response', ClientUtils.get_response_body(share_response))

        user_share_suggestions_response = self.user_client.get_user_share_suggestions(auth=self.auth)
        status_code = ClientUtils.get_response_status_code(user_share_suggestions_response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('get_user_share_suggestions response',
                                      ClientUtils.get_response_body(user_share_suggestions_response))

        response_contact_addresses = TestUtils.get_addresses_from_share_suggestions_response(
            user_share_suggestions_response)
        self.assertTrue(len(response_contact_addresses) == 1, 'Expected 1 share suggestion only but got: ' + str(
            response_contact_addresses) + self.extra_data.get_all())
