__author__ = 'alonitzhaki'
from unittest import TestCase
import httplib

from time import time

from utils.clients.main_client import MainRegisterAndLoginMixin

from rest_test.tests_utils import TestUtils
from rest_test.clients.clients_utils import ClientUtils
from rest_test.clients.partition_client import PartitionClient
from rest_test.extra_data_manager import ExtraDataManager


class GetPartitionTests(TestCase):
    auth = None

    user_name = 'rest_tests_partition_' + str(int(time())) + '@autodesk.com'
    first_name = 'Rest'
    last_name = 'Test'
    password = 'Moomoo123'

    extra_data = None
    partition_client = PartitionClient()

    def setUp(self):
        self.extra_data = ExtraDataManager()
        self.extra_data.add_test_data('user name', self.user_name)
        main_register_and_login_mixin = MainRegisterAndLoginMixin()
        if GetPartitionTests.auth is None:
            response = main_register_and_login_mixin.login_or_register(user_name=self.user_name, password=self.password,
                                                                       first_name=self.first_name,
                                                                       last_name=self.last_name)
            GetPartitionTests.auth = main_register_and_login_mixin.get_auth_from_login_data(response)
        self.assertIsInstance(GetPartitionTests.auth, str,
                              'Invalid auth: ' + str(GetPartitionTests.auth) + self.extra_data.get_all())

    def test_get_partition_v2_root_internal(self):
        expected_entries_names = ['Clean Canvas.dwg', 'Dog House Plan Sample.dwg', 'Drive Roller Assembly Sample.dwg',
                                  'Geospatial Sample.dwg', 'Villa Project Sample.dwg']

        response = self.partition_client.get_partition_v2(auth=self.auth)
        status_code = ClientUtils.get_response_status_code(response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('get_partition response', ClientUtils.get_response_body(response))

        file_system_entries = ClientUtils.get_value_from_body(response, PartitionClient.KEY_FILE_SYSTEM_ENTRIES)
        self.assertIsNotNone(file_system_entries, 'Expected non empty partition' + self.extra_data.get_all())

        file_system_entries_names = TestUtils.get_entries_names_from_file_system_entries(file_system_entries)
        self.assertItemsEqual(expected_entries_names, file_system_entries_names,
                              'Expected entries names: ' + str(expected_entries_names) + ' but got: ' + str(
                                  file_system_entries_names) + self.extra_data.get_all())

    def test_get_partition_root_internal(self):
        expected_entries_names = ['Clean Canvas.dwg', 'Dog House Plan Sample.dwg', 'Drive Roller Assembly Sample.dwg',
                                  'Geospatial Sample.dwg', 'Villa Project Sample.dwg']

        response = self.partition_client.get_partition(auth=self.auth)
        status_code = ClientUtils.get_response_status_code(response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('get_partition response', ClientUtils.get_response_body(response))

        file_system_entries = ClientUtils.get_value_from_body(response, PartitionClient.KEY_FILE_SYSTEM_ENTRIES)
        self.assertIsNotNone(file_system_entries, 'Expected non empty partition' + self.extra_data.get_all())

        file_system_entries_names = TestUtils.get_entries_names_from_file_system_entries(file_system_entries)
        self.assertItemsEqual(expected_entries_names, file_system_entries_names,
                              'Expected entries names: ' + str(expected_entries_names) + ' but got: ' + str(
                                  file_system_entries_names) + self.extra_data.get_all())

    def test_get_partition_v2_path_internal(self):
        expected_entries_names = ['Clean Canvas.dwg', 'Dog House Plan Sample.dwg', 'Drive Roller Assembly Sample.dwg',
                                  'Geospatial Sample.dwg', 'Villa Project Sample.dwg']

        response = self.partition_client.get_partition_path_v2(auth=self.auth, path='')
        status_code = ClientUtils.get_response_status_code(response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('response', response)

        file_system_entries = ClientUtils.get_value_from_body(response, PartitionClient.KEY_FILE_SYSTEM_ENTRIES)
        self.assertIsNotNone(file_system_entries, 'Expected non empty partition' + self.extra_data.get_all())

        file_system_entries_names = TestUtils.get_entries_names_from_file_system_entries(file_system_entries)
        self.assertItemsEqual(expected_entries_names, file_system_entries_names,
                              'Expected entries names: ' + str(expected_entries_names) + ' but got: ' + str(
                                  file_system_entries_names) + self.extra_data.get_all())

    def test_get_partition_path_internal(self):
        expected_entries_names = ['Clean Canvas.dwg', 'Dog House Plan Sample.dwg', 'Drive Roller Assembly Sample.dwg',
                                  'Geospatial Sample.dwg', 'Villa Project Sample.dwg']

        response = self.partition_client.get_partition_path(auth=self.auth, path='')
        status_code = ClientUtils.get_response_status_code(response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('response', response)

        file_system_entries = ClientUtils.get_value_from_body(response, PartitionClient.KEY_FILE_SYSTEM_ENTRIES)
        self.assertIsNotNone(file_system_entries, 'Expected non empty partition' + self.extra_data.get_all())

        file_system_entries_names = TestUtils.get_entries_names_from_file_system_entries(file_system_entries)
        self.assertItemsEqual(expected_entries_names, file_system_entries_names,
                              'Expected entries names: ' + str(expected_entries_names) + ' but got: ' + str(
                                  file_system_entries_names) + self.extra_data.get_all())
