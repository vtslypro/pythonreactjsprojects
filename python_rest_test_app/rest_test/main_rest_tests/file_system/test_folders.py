__author__ = 'alonitzhaki'
from unittest import TestCase
import httplib
from time import time

from utils.clients.main_client import MainRegisterAndLoginMixin

from rest_test.clients.clients_utils import ClientUtils
from rest_test.clients.folders_client import FoldersManagementClient
from rest_test.clients.partition_client import PartitionClient
from rest_test.tests_utils import TestUtils
from rest_test.extra_data_manager import ExtraDataManager


class FolderTests(TestCase):
    auth = None

    user_name = 'rest_tests_manage_folders_' + str(int(time())) + '@autodesk.com'
    first_name = 'Rest'
    last_name = 'Test'
    password = 'Moomoo123'

    extra_data = None
    folders_management_client = FoldersManagementClient()

    def setUp(self):
        self.extra_data = ExtraDataManager()
        self.extra_data.add_test_data('user name', self.user_name)
        main_register_and_login = MainRegisterAndLoginMixin()
        if FolderTests.auth is None:
            response = main_register_and_login.login_or_register(user_name=self.user_name, password=self.password,
                                                                 first_name=self.first_name,
                                                                 last_name=self.last_name)
            FolderTests.auth = main_register_and_login.get_auth_from_login_data(response)
        self.assertIsInstance(FolderTests.auth, str,
                              'Invalid auth: ' + str(FolderTests.auth) + self.extra_data.get_all())

    def test_create_folder(self):
        folder_name = 'test_folder_create_folder_' + str(int(time()))
        expected_code_and_description = (0, 'SUCCESS')

        self.extra_data.add_test_data('folder name', folder_name)

        create_folder_response = self.folders_management_client.create_folder(auth=self.auth,
                                                                              new_folder_name=folder_name)
        status_code = ClientUtils.get_response_status_code(create_folder_response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('create_folder response', ClientUtils.get_response_body(create_folder_response))

        code_desc = ClientUtils.get_code_and_description_from_response(create_folder_response)
        self.assertEqual(expected_code_and_description, code_desc,
                         'Expected ' + str(expected_code_and_description) + ' but got: ' + str(
                             code_desc) + self.extra_data.get_all())

        response_folder_id = ClientUtils.get_value_from_body(create_folder_response,
                                                             FoldersManagementClient.KEY_FOLDER_ID)
        self.assertTrue(response_folder_id > 0,
                        'Expected valid folder id but got: ' + str(response_folder_id) + self.extra_data.get_all())
        self.extra_data.add_test_data('response folder id', response_folder_id)

        file_system_entries, msg = TestUtils.get_internal_partition(auth=self.auth, extra_data=self.extra_data)
        self.assertIsNotNone(file_system_entries, msg + self.extra_data.get_all())

        entry = TestUtils.get_entry_from_internal_file_system_entries(response_folder_id, file_system_entries)

        self.assertIsNotNone(entry, 'Created folder should exist in partition' + self.extra_data.get_all())
        partition_folder_name = TestUtils.get_entry_data_by_keys(entry=entry, keys=PartitionClient.KEY_ENTRY_NAME)
        self.assertEqual(folder_name, partition_folder_name,
                         'Expected folder name: ' + str(folder_name) + ' but got: ' + str(
                             partition_folder_name) + self.extra_data.get_all())

    def test_create_folder_v2(self):
        folder_name = 'test_folder_create_folder_v2_' + str(int(time()))
        expected_code_and_description = (0, 'SUCCESS')

        self.extra_data.add_test_data('folder name', folder_name)

        create_folder_response = self.folders_management_client.create_folder_v2(auth=self.auth,
                                                                                 new_folder_name=folder_name)
        status_code = ClientUtils.get_response_status_code(create_folder_response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('create_folder response', ClientUtils.get_response_body(create_folder_response))

        code_desc = ClientUtils.get_code_and_description_from_response(create_folder_response)
        self.assertEqual(expected_code_and_description, code_desc,
                         'Expected ' + str(expected_code_and_description) + ' but got: ' + str(
                             code_desc) + self.extra_data.get_all())

        response_folder_id = ClientUtils.get_value_from_body(create_folder_response,
                                                             FoldersManagementClient.KEY_FOLDER_ID)
        self.assertTrue(response_folder_id > 0,
                        'Expected valid folder id but got: ' + str(response_folder_id) + self.extra_data.get_all())
        self.extra_data.add_test_data('response folder id', response_folder_id)

        file_system_entries, msg = TestUtils.get_internal_partition(auth=self.auth, extra_data=self.extra_data)
        self.assertIsNotNone(file_system_entries, msg + self.extra_data.get_all())

        entry = TestUtils.get_entry_from_internal_file_system_entries(response_folder_id, file_system_entries)

        self.assertIsNotNone(entry, 'Created folder should exist in partition' + self.extra_data.get_all())
        partition_folder_name = TestUtils.get_entry_data_by_keys(entry=entry, keys=PartitionClient.KEY_ENTRY_NAME)
        self.assertEqual(folder_name, partition_folder_name,
                         'Expected folder name: ' + str(folder_name) + ' but got: ' + str(
                             partition_folder_name) + self.extra_data.get_all())

    def test_rename_folder(self):
        folder_name = 'test_folder_rename_folder_' + str(int(time()))
        folder_new_name = 'test_folder_rename_folder_renamed_' + str(int(time()))
        expected_code_and_description = (0, 'SUCCESS')

        self.extra_data.add_test_data('folder name', folder_name)
        self.extra_data.add_test_data('folder new name', folder_new_name)

        created_folder_id, msg = TestUtils.create_folder(auth=self.auth, folder_name=folder_name,
                                                         extra_data=self.extra_data)
        self.assertIsNotNone(created_folder_id, msg + self.extra_data.get_all())

        rename_folder_response = self.folders_management_client.rename_folder(auth=self.auth,
                                                                              folder_id=created_folder_id,
                                                                              name=folder_new_name)
        status_code = ClientUtils.get_response_status_code(rename_folder_response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('rename_folder response', ClientUtils.get_response_body(rename_folder_response))

        code_desc = ClientUtils.get_code_and_description_from_response(rename_folder_response)
        self.assertEqual(expected_code_and_description, code_desc,
                         'Expected ' + str(expected_code_and_description) + ' but got: ' + str(
                             code_desc) + self.extra_data.get_all())

        file_system_entries, msg = TestUtils.get_internal_partition(auth=self.auth, extra_data=self.extra_data)
        self.assertIsNotNone(file_system_entries, msg + self.extra_data.get_all())

        entry = TestUtils.get_entry_from_internal_file_system_entries(created_folder_id, file_system_entries)

        self.assertIsNotNone(entry, 'Renamed folder should exist in partition' + self.extra_data.get_all())
        partition_folder_name = TestUtils.get_entry_data_by_keys(entry=entry,
                                                                 keys=PartitionClient.KEY_ENTRY_NAME)
        self.assertEqual(folder_new_name, partition_folder_name,
                         'Expected folder name: ' + str(folder_new_name) + ' but got: ' + str(
                             partition_folder_name) + self.extra_data.get_all())

    def test_rename_folder_v2(self):
        folder_name = 'test_folder_rename_folder_v2_' + str(int(time()))
        folder_new_name = 'test_folder_rename_folder_v2_renamed_' + str(int(time()))
        expected_code_and_description = (0, 'SUCCESS')

        self.extra_data.add_test_data('folder name', folder_name)
        self.extra_data.add_test_data('folder new name', folder_new_name)

        created_folder_id, msg = TestUtils.create_folder(auth=self.auth, folder_name=folder_name,
                                                         extra_data=self.extra_data)
        self.assertIsNotNone(created_folder_id, msg + self.extra_data.get_all())

        rename_folder_response = self.folders_management_client.rename_folder_v2(auth=self.auth,
                                                                                 folder_id=created_folder_id,
                                                                                 name=folder_new_name)
        status_code = ClientUtils.get_response_status_code(rename_folder_response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('rename_folder response', ClientUtils.get_response_body(rename_folder_response))

        code_desc = ClientUtils.get_code_and_description_from_response(rename_folder_response)
        self.assertEqual(expected_code_and_description, code_desc,
                         'Expected ' + str(expected_code_and_description) + ' but got: ' + str(
                             code_desc) + self.extra_data.get_all())

        file_system_entries, msg = TestUtils.get_internal_partition(auth=self.auth, extra_data=self.extra_data)
        self.assertIsNotNone(file_system_entries, msg + self.extra_data.get_all())

        entry = TestUtils.get_entry_from_internal_file_system_entries(created_folder_id, file_system_entries)

        self.assertIsNotNone(entry, 'Renamed folder should exist in partition' + self.extra_data.get_all())
        partition_folder_name = TestUtils.get_entry_data_by_keys(entry=entry,
                                                                 keys=PartitionClient.KEY_ENTRY_NAME)
        self.assertEqual(folder_new_name, partition_folder_name,
                         'Expected folder name: ' + str(folder_new_name) + ' but got: ' + str(
                             partition_folder_name) + self.extra_data.get_all())

    def test_delete_folder(self):
        folder_name = 'test_folder_delete_folder_' + str(int(time()))
        expected_code_and_description = (0, 'SUCCESS')

        self.extra_data.add_test_data('folder name', folder_name)

        created_folder_id, msg = TestUtils.create_folder(auth=self.auth, folder_name=folder_name,
                                                         extra_data=self.extra_data)
        self.assertIsNotNone(created_folder_id, msg + self.extra_data.get_all())

        delete_folder_response = self.folders_management_client.delete_folder(auth=self.auth,
                                                                              folder_id=created_folder_id)
        status_code = ClientUtils.get_response_status_code(delete_folder_response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('delete_folder response', ClientUtils.get_response_body(delete_folder_response))

        code_desc = ClientUtils.get_code_and_description_from_response(delete_folder_response)
        self.assertEqual(expected_code_and_description, code_desc,
                         'Expected ' + str(expected_code_and_description) + ' but got: ' + str(
                             code_desc) + self.extra_data.get_all())

        file_system_entries, msg = TestUtils.get_internal_partition(auth=self.auth, extra_data=self.extra_data)
        self.assertIsNotNone(file_system_entries, msg + self.extra_data.get_all())

        entry = TestUtils.get_entry_from_internal_file_system_entries(created_folder_id, file_system_entries)

        self.assertIsNone(entry, 'Deleted folder should not exist in partition' + self.extra_data.get_all())
