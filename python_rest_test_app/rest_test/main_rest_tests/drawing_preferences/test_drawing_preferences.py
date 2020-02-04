__author__ = 'alonitzhaki'
from unittest import TestCase
from time import time
import httplib

from utils.clients.main_client import MainRegisterAndLoginMixin

from rest_test.clients.clients_utils import ClientUtils
from rest_test.clients.files_client import FilesManagementClient
from rest_test.tests_utils import TestUtils
from rest_test.extra_data_manager import ExtraDataManager


class DrawingPreferencesTests(TestCase):
    auth = None

    user_name = 'rest_tests_drawing_preferences_' + str(int(time())) + '@autodesk.com'
    password = 'Moomoo123'
    first_name = 'Rest'
    last_name = 'Test'

    extra_data = None
    files_management_client = FilesManagementClient()

    def setUp(self):
        self.extra_data = ExtraDataManager()
        self.extra_data.add_test_data('user name', self.user_name)
        main_register_and_login_mixin = MainRegisterAndLoginMixin()
        if DrawingPreferencesTests.auth is None:
            response = main_register_and_login_mixin.login_or_register(user_name=self.user_name,
                                                                       password=self.password,
                                                                       first_name=self.first_name,
                                                                       last_name=self.last_name)
            DrawingPreferencesTests.auth = main_register_and_login_mixin.get_auth_from_login_data(response)
        self.assertIsInstance(DrawingPreferencesTests.auth, str,
                              'Invalid auth: ' + str(DrawingPreferencesTests.auth) + self.extra_data.get_all())

    def test_get_drawing_preferences(self):
        file_name = 'test_file_get_drawing_prefs_' + str(int(time())) + '.dwg'
        self.extra_data.add_test_data('file name', file_name)

        created_file_id, msg = TestUtils.create_file(auth=self.auth, file_name=file_name, extra_data=self.extra_data)
        self.assertIsNotNone(created_file_id, msg + self.extra_data.get_all())

        get_drawing_prefs_response = self.files_management_client.get_drawing_preferences(auth=self.auth,
                                                                                          file_id=created_file_id)
        status_code = ClientUtils.get_response_status_code(get_drawing_prefs_response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('get_drawing_preferences response', get_drawing_prefs_response)

        user_specific_drawing_prefs_in_response_body = ClientUtils.is_key_in_body(response=get_drawing_prefs_response,
                                                                                  nested_keys='userSpecificDrawingPreferences')
        self.assertTrue(user_specific_drawing_prefs_in_response_body,
                        'Exepected key userSpecificDrawingPreferences to exist in repsonse body' + self.extra_data.get_all())

        shared_drawing_prefs_in_response_body = ClientUtils.is_key_in_body(response=get_drawing_prefs_response,
                                                                           nested_keys='sharedDrawingPreferences')
        self.assertTrue(shared_drawing_prefs_in_response_body,
                        'Exepected key sharedDrawingPreferences to exist in repsonse body' + self.extra_data.get_all())

    def test_post_drawing_preferences(self):
        file_name = 'test_file_post_drawing_prefs' + str(int(time())) + '.dwg'
        expected_orth_on = True
        expected_line_weight_on = False
        self.extra_data.add_test_data('file name', file_name)

        created_file_id, msg = TestUtils.create_file(auth=self.auth, file_name=file_name, extra_data=self.extra_data)
        self.assertIsNotNone(created_file_id, msg + self.extra_data.get_all())

        user_specific_drawing_prefs = {}
        user_specific_drawing_prefs.__setitem__('orthoOn', expected_orth_on)
        user_specific_drawing_prefs.__setitem__('lineWeightOn', expected_line_weight_on)
        post_drawing_prefs_response = self.files_management_client.post_drawing_preferences(auth=self.auth,
                                                                                            file_id=created_file_id,
                                                                                            user_specific_drawing_preferences=user_specific_drawing_prefs)
        self.assertIsNotNone(post_drawing_prefs_response, 'Response is None' + self.extra_data.get_all())
        status_code = ClientUtils.get_response_status_code(post_drawing_prefs_response)
        self.assertEqual(httplib.NO_CONTENT, status_code,
                         'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.assertTrue(ClientUtils.is_response_body_empty(post_drawing_prefs_response),
                        'Expected empty response body but got: ' + str(
                            ClientUtils.get_response_body(post_drawing_prefs_response)) + self.extra_data.get_all())

        get_drawing_prefs_response = self.files_management_client.get_drawing_preferences(auth=self.auth,
                                                                                          file_id=created_file_id)
        status_code = ClientUtils.get_response_status_code(get_drawing_prefs_response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('get_drawing_preferences response',
                                      ClientUtils.get_response_body(get_drawing_prefs_response))

        orth_on = ClientUtils.get_value_from_body(response=get_drawing_prefs_response,
                                                  json_path='userSpecificDrawingPreferences.orthoOn')
        self.assertEqual(expected_orth_on, orth_on, 'Expected orth_on: ' + str(expected_orth_on) + 'but got: ' + str(
            orth_on) + self.extra_data.get_all())

        line_weight_on = ClientUtils.get_value_from_body(response=get_drawing_prefs_response,
                                                         json_path='userSpecificDrawingPreferences.lineWeightOn')
        self.assertEqual(expected_line_weight_on, line_weight_on,
                         'Expected line_weight_on: ' + str(expected_line_weight_on) + 'but got: ' + str(
                             line_weight_on) + self.extra_data.get_all())
