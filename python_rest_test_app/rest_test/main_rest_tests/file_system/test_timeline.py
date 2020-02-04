__author__ = 'alonitzhaki'
from unittest import TestCase
from time import time
import httplib

from utils.clients.main_client import MainRegisterAndLoginMixin

from rest_test.clients.clients_utils import ClientUtils
from rest_test.clients.files_client import FilesManagementClient
from rest_test.tests_utils import TestUtils
from rest_test.extra_data_manager import ExtraDataManager


class TimelineTests(TestCase):
    auth = None

    user_name = 'rest_tests_timeline_' + str(int(time())) + '@autodesk.com'
    password = 'Moomoo123'
    first_name = 'Rest'
    last_name = 'Test'

    extra_data = None
    files_management_client = FilesManagementClient()

    def setUp(self):
        self.extra_data = ExtraDataManager()
        self.extra_data.add_test_data('user name', self.user_name)
        main_register_and_login_mixin = MainRegisterAndLoginMixin()
        if TimelineTests.auth is None:
            response = main_register_and_login_mixin.login_or_register(user_name=self.user_name,
                                                                       password=self.password,
                                                                       first_name=self.first_name,
                                                                       last_name=self.last_name)
            TimelineTests.auth = main_register_and_login_mixin.get_auth_from_login_data(response)
        self.assertIsInstance(TimelineTests.auth, str,
                              'Invalid auth: ' + str(TimelineTests.auth) + self.extra_data.get_all())

    def test_timeline_manual(self):
        file_name = 'test_file_timeline_manual_' + str(int(time())) + '.dwg'
        title = 'test_title_' + str(int(time()))

        self.extra_data.add_test_data('file name', file_name)
        self.extra_data.add_test_data('title', title)

        created_file_id, msg = TestUtils.create_file(auth=self.auth, file_name=file_name, extra_data=self.extra_data)
        self.assertIsNotNone(created_file_id, msg + self.extra_data.get_all())

        manual_timeline_response = self.files_management_client.put_timeline_manual(auth=self.auth,
                                                                                    file_id=created_file_id,
                                                                                    title=title)
        status_code = ClientUtils.get_response_status_code(manual_timeline_response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('put_timeline_manual response',
                                      ClientUtils.get_response_body(manual_timeline_response))

        response_title = ClientUtils.get_value_from_body(manual_timeline_response, FilesManagementClient.KEY_TITLE)
        self.assertEqual(title, response_title, 'Expected title: ' + str(title) + ' but got: ' + str(
            response_title) + self.extra_data.get_all())

        get_timeline_response = self.files_management_client.get_timeline(auth=self.auth, file_id=created_file_id)
        status_code = ClientUtils.get_response_status_code(get_timeline_response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('get_timeline response', ClientUtils.get_response_body(get_timeline_response))

        response_entries = ClientUtils.get_value_from_body(get_timeline_response, FilesManagementClient.KEY_ENTRIES)
        self.assertIsNotNone(response_entries, 'Expected non empty entries' + self.extra_data.get_all())
        self.assertTrue(len(response_entries) == 2, 'Expected exactly 2 entries in response body but got: ' + str(
            response_entries) + self.extra_data.get_all())
        self.extra_data.add_test_data('response entries', response_entries)

        entry = response_entries[0]
        if entry['title'] != title:
            entry = response_entries[1]

        entry_primary_id = entry['primaryVersionId']
        self.assertEqual(created_file_id, entry_primary_id,
                         'Expected file id: ' + str(created_file_id) + ' but got: ' + str(
                             entry_primary_id) + self.extra_data.get_all())
        entry_title = entry['title']
        self.assertEqual(title, entry_title,
                         'Expected title: ' + str(title) + ' but got: ' + str(entry_title) + self.extra_data.get_all())

        users_drawing_prefs_in_response_body = ClientUtils.is_key_in_body(get_timeline_response,
                                                                          'usersDrawingPreferences')
        self.assertTrue(users_drawing_prefs_in_response_body,
                        'Expected usersDrawingPreferences in response body' + self.extra_data.get_all())
