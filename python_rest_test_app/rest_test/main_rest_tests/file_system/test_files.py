__author__ = 'alonitzhaki'
from unittest import TestCase
import httplib
from time import time

from utils.clients.main_client import MainRegisterAndLoginMixin

from rest_test.clients.clients_utils import ClientUtils
from rest_test.clients.files_client import FilesManagementClient
from rest_test.clients.partition_client import PartitionClient
from rest_test.tests_utils import TestUtils
from rest_test.extra_data_manager import ExtraDataManager


class FilesTests(TestCase):
    auth = None

    user_name = 'rest_tests_manage_files_' + str(int(time())) + '@autodesk.com'
    password = 'Moomoo123'
    first_name = 'Rest'
    last_name = 'Test'

    extra_data = None
    files_management_client = FilesManagementClient()

    def setUp(self):
        self.extra_data = ExtraDataManager()
        self.extra_data.add_test_data('user name', self.user_name)
        main_register_and_login_mixin = MainRegisterAndLoginMixin()
        if FilesTests.auth is None:
            response = main_register_and_login_mixin.login_or_register(user_name=self.user_name,
                                                                       password=self.password,
                                                                       first_name=self.first_name,
                                                                       last_name=self.last_name)
            FilesTests.auth = main_register_and_login_mixin.get_auth_from_login_data(response)
        self.assertIsInstance(FilesTests.auth, str,
                              'Invalid auth: ' + str(FilesTests.auth) + self.extra_data.get_all())

    def test_create_file(self):
        file_name = 'test_file_create_file_' + str(int(time())) + '.dwg'
        self.extra_data.add_test_data('file name', file_name)

        create_file_response = self.files_management_client.create_file(auth=self.auth, new_drawing_name=file_name)
        status_code = ClientUtils.get_response_status_code(create_file_response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('create_file response', ClientUtils.get_response_body(create_file_response))

        response_file_id, response_file_name = ClientUtils.get_multiple_values_from_body(create_file_response, [
            FilesManagementClient.KEY_VERSION_ID, FilesManagementClient.KEY_NAME])
        self.assertTrue(response_file_id > 0,
                        'Expected valid file id but got: ' + str(response_file_id) + self.extra_data.get_all())
        self.assertEqual(file_name, response_file_name, 'Expected file name: ' + str(file_name) + 'but got: ' + str(
            response_file_name) + self.extra_data.get_all())

        self.extra_data.add_test_data('response file id', response_file_id)
        self.extra_data.add_test_data('response file name', response_file_name)

        file_system_entries, msg = TestUtils.get_internal_partition(auth=self.auth, extra_data=self.extra_data)
        self.assertIsNotNone(file_system_entries, msg + self.extra_data.get_all())

        entry = TestUtils.get_entry_from_internal_file_system_entries(response_file_id, file_system_entries)
        self.assertIsNotNone(entry, 'Created file should exist in partition' + self.extra_data.get_all())

        partition_file_name = TestUtils.get_entry_data_by_keys(entry=entry, keys=PartitionClient.KEY_ENTRY_NAME)
        self.assertEqual(file_name, partition_file_name, 'Expected file name: ' + str(file_name) + 'but got: ' + str(
            partition_file_name) + self.extra_data.get_all())

        partition_nitrous_id = TestUtils.get_entry_data_by_keys(entry=entry, keys=PartitionClient.KEY_NITROUS_ID)
        self.assertIsNotNone(partition_nitrous_id, 'Expected nitrous ID not None' + self.extra_data.get_all())

    def test_create_file_v2(self):
        file_name = 'test_file_create_file_v2_' + str(int(time())) + '.dwg'
        self.extra_data.add_test_data('file name', file_name)

        create_file_response = self.files_management_client.create_file_v2(auth=self.auth, new_drawing_name=file_name)
        status_code = ClientUtils.get_response_status_code(create_file_response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('create_file response', ClientUtils.get_response_body(create_file_response))

        response_file_id, response_file_name = ClientUtils.get_multiple_values_from_body(create_file_response, [
            FilesManagementClient.KEY_VERSION_ID, FilesManagementClient.KEY_NAME])
        self.assertTrue(response_file_id > 0,
                        'Expected valid file id but got: ' + str(response_file_id) + self.extra_data.get_all())
        self.assertEqual(file_name, response_file_name, 'Expected file name: ' + str(file_name) + 'but got: ' + str(
            response_file_name) + self.extra_data.get_all())

        self.extra_data.add_test_data('response file id', response_file_id)
        self.extra_data.add_test_data('response file name', response_file_name)

        file_system_entries, msg = TestUtils.get_internal_partition(auth=self.auth, extra_data=self.extra_data)
        self.assertIsNotNone(file_system_entries, msg + self.extra_data.get_all())

        entry = TestUtils.get_entry_from_internal_file_system_entries(response_file_id, file_system_entries)
        self.assertIsNotNone(entry, 'Created file should exist in partition' + self.extra_data.get_all())

        partition_file_name = TestUtils.get_entry_data_by_keys(entry=entry, keys=PartitionClient.KEY_ENTRY_NAME)
        self.assertEqual(file_name, partition_file_name, 'Expected file name: ' + str(file_name) + 'but got: ' + str(
            partition_file_name) + self.extra_data.get_all())

        partition_nitrous_id = TestUtils.get_entry_data_by_keys(entry=entry, keys=PartitionClient.KEY_NITROUS_ID)
        self.assertIsNotNone(partition_nitrous_id, 'Expected nitrous ID not None' + self.extra_data.get_all())

    def test_rename_file_internal(self):
        file_name = 'test_file_rename_file_internal_' + str(int(time())) + '.dwg'
        file_new_name = 'test_file_rename_file_internal_renamed_' + str(int(time())) + '.dwg'
        expected_code_and_description = (0, 'SUCCESS')

        self.extra_data.add_test_data('file name', file_name)
        self.extra_data.add_test_data('file new name', file_new_name)

        created_file_id, msg = TestUtils.create_file(auth=self.auth, file_name=file_name, extra_data=self.extra_data)
        self.assertIsNotNone(created_file_id, msg + self.extra_data.get_all())

        rename_file_response = self.files_management_client.rename_file_internal(auth=self.auth,
                                                                                 file_id=created_file_id,
                                                                                 name=file_new_name)
        status_code = ClientUtils.get_response_status_code(rename_file_response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('rename_file_internal response',
                                      ClientUtils.get_response_body(rename_file_response))

        code_desc = ClientUtils.get_code_and_description_from_response(rename_file_response)
        self.assertEqual(expected_code_and_description, code_desc,
                         'Expected ' + str(expected_code_and_description) + ' but got: ' + str(
                             code_desc) + self.extra_data.get_all())

        file_system_entries, msg = TestUtils.get_internal_partition(auth=self.auth, extra_data=self.extra_data)
        self.assertIsNotNone(file_system_entries, msg + self.extra_data.get_all())

        entry = TestUtils.get_entry_from_internal_file_system_entries(created_file_id, file_system_entries)

        self.assertIsNotNone(entry, 'Renamed file should exist in partition' + self.extra_data.get_all())
        partition_file_name = TestUtils.get_entry_data_by_keys(entry=entry, keys=PartitionClient.KEY_ENTRY_NAME)
        self.assertEqual(file_new_name, partition_file_name,
                         'Expected file name: ' + str(file_new_name) + ' but got: ' + str(
                             partition_file_name) + self.extra_data.get_all())

    def test_rename_file_v2_internal(self):
        file_name = 'test_file_rename_file_v2_internal_' + str(int(time())) + '.dwg'
        file_new_name = 'test_file_rename_file_v2_internal_renamed_' + str(int(time())) + '.dwg'
        expected_code_and_description = (0, 'SUCCESS')

        self.extra_data.add_test_data('file name', file_name)
        self.extra_data.add_test_data('file new name', file_new_name)

        created_file_id, msg = TestUtils.create_file(auth=self.auth, file_name=file_name, extra_data=self.extra_data)
        self.assertIsNotNone(created_file_id, msg + self.extra_data.get_all())

        rename_file_response = self.files_management_client.rename_file_v2_internal(auth=self.auth,
                                                                                    file_id=created_file_id,
                                                                                    name=file_new_name)
        status_code = ClientUtils.get_response_status_code(rename_file_response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('rename_file_internal response',
                                      ClientUtils.get_response_body(rename_file_response))

        code_desc = ClientUtils.get_code_and_description_from_response(rename_file_response)
        self.assertEqual(expected_code_and_description, code_desc,
                         'Expected ' + str(expected_code_and_description) + ' but got: ' + str(
                             code_desc) + self.extra_data.get_all())

        file_system_entries, msg = TestUtils.get_internal_partition(auth=self.auth, extra_data=self.extra_data)
        self.assertIsNotNone(file_system_entries, msg + self.extra_data.get_all())

        entry = TestUtils.get_entry_from_internal_file_system_entries(created_file_id, file_system_entries)

        self.assertIsNotNone(entry, 'Renamed file should exist in partition' + self.extra_data.get_all())
        partition_file_name = TestUtils.get_entry_data_by_keys(entry=entry, keys=PartitionClient.KEY_ENTRY_NAME)
        self.assertEqual(file_new_name, partition_file_name,
                         'Expected file name: ' + str(file_new_name) + ' but got: ' + str(
                             partition_file_name) + self.extra_data.get_all())

    def test_copy_file_internal(self):
        file_name = 'test_file_copy_file_internal_' + str(int(time())) + '.dwg'
        file_new_name = 'test_file_copy_file_internal_copy' + str(int(time())) + '.dwg'
        expected_code_and_description = (0, 'SUCCESS')

        self.extra_data.add_test_data('file name', file_name)
        self.extra_data.add_test_data('file new name', file_new_name)

        created_file_id, msg = TestUtils.create_file(auth=self.auth, file_name=file_name, extra_data=self.extra_data)
        self.assertIsNotNone(created_file_id, msg + self.extra_data.get_all())

        copy_file_response = self.files_management_client.copy_file_internal(auth=self.auth, file_id=created_file_id,
                                                                             to_folder_id=0,
                                                                             rename_to=file_new_name)
        status_code = ClientUtils.get_response_status_code(copy_file_response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('copy_file_internal response', ClientUtils.get_response_body(copy_file_response))

        code_desc = ClientUtils.get_code_and_description_from_response(copy_file_response)
        self.assertEqual(expected_code_and_description, code_desc,
                         'Expected ' + str(expected_code_and_description) + ' but got: ' + str(
                             code_desc) + self.extra_data.get_all())

        copied_file_id = ClientUtils.get_value_from_body(copy_file_response, FilesManagementClient.KEY_PRIMARY_WS_ID)
        self.assertTrue(copied_file_id > 0, 'Expected valid copied file id but got: ' + str(
            copied_file_id) + self.extra_data.get_all())
        self.extra_data.add_test_data('copied file id', copied_file_id)

        file_system_entries, msg = TestUtils.get_internal_partition(auth=self.auth, extra_data=self.extra_data)
        self.assertIsNotNone(file_system_entries, msg + self.extra_data.get_all())

        entry_src = TestUtils.get_entry_from_internal_file_system_entries(entry_id=created_file_id,
                                                                          internal_file_system_entries=file_system_entries)
        entry_copy = TestUtils.get_entry_from_internal_file_system_entries(entry_id=copied_file_id,
                                                                           internal_file_system_entries=file_system_entries)
        self.assertIsNotNone(entry_src, 'Source file should still exist in partition' + self.extra_data.get_all())
        self.assertIsNotNone(entry_copy, 'Copied file should exist in partition' + self.extra_data.get_all())

        entry_src_name = TestUtils.get_entry_data_by_keys(entry=entry_src, keys=PartitionClient.KEY_ENTRY_NAME)
        entry_copy_name = TestUtils.get_entry_data_by_keys(entry=entry_copy, keys=PartitionClient.KEY_ENTRY_NAME)
        self.assertEqual(file_name, entry_src_name, 'Expected source file name: ' + str(file_name) + ' but got: ' + str(
            entry_src_name) + self.extra_data.get_all())
        self.assertEqual(file_new_name, entry_copy_name, 'Expected copy file name: ' + str(
            file_new_name) + ' but got: ' + str(entry_copy_name) + self.extra_data.get_all())

    def test_copy_file_v2_internal(self):
        file_name = 'test_file_copy_file_v2_internal_' + str(int(time())) + '.dwg'
        file_new_name = 'test_file_copy_file_v2_internal_copy' + str(int(time())) + '.dwg'
        expected_code_and_description = (0, 'SUCCESS')

        self.extra_data.add_test_data('file name', file_name)
        self.extra_data.add_test_data('file new name', file_new_name)

        created_file_id, msg = TestUtils.create_file(auth=self.auth, file_name=file_name, extra_data=self.extra_data)
        self.assertIsNotNone(created_file_id, msg + self.extra_data.get_all())

        copy_file_response = self.files_management_client.copy_file_v2_internal(auth=self.auth, file_id=created_file_id,
                                                                                to_folder_id=0,
                                                                                rename_to=file_new_name)
        status_code = ClientUtils.get_response_status_code(copy_file_response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('copy_file_internal response', ClientUtils.get_response_body(copy_file_response))

        code_desc = ClientUtils.get_code_and_description_from_response(copy_file_response)
        self.assertEqual(expected_code_and_description, code_desc,
                         'Expected ' + str(expected_code_and_description) + ' but got: ' + str(
                             code_desc) + self.extra_data.get_all())

        copied_file_id = ClientUtils.get_value_from_body(copy_file_response, FilesManagementClient.KEY_PRIMARY_WS_ID)
        self.assertTrue(copied_file_id > 0, 'Expected valid copied file id but got: ' + str(
            copied_file_id) + self.extra_data.get_all())
        self.extra_data.add_test_data('copied file id', copied_file_id)

        file_system_entries, msg = TestUtils.get_internal_partition(auth=self.auth, extra_data=self.extra_data)
        self.assertIsNotNone(file_system_entries, msg + self.extra_data.get_all())

        entry_src = TestUtils.get_entry_from_internal_file_system_entries(entry_id=created_file_id,
                                                                          internal_file_system_entries=file_system_entries)
        entry_copy = TestUtils.get_entry_from_internal_file_system_entries(entry_id=copied_file_id,
                                                                           internal_file_system_entries=file_system_entries)
        self.assertIsNotNone(entry_src, 'Source file should still exist in partition' + self.extra_data.get_all())
        self.assertIsNotNone(entry_copy, 'Copied file should exist in partition' + self.extra_data.get_all())

        entry_src_name = TestUtils.get_entry_data_by_keys(entry=entry_src, keys=PartitionClient.KEY_ENTRY_NAME)
        entry_copy_name = TestUtils.get_entry_data_by_keys(entry=entry_copy, keys=PartitionClient.KEY_ENTRY_NAME)
        self.assertEqual(file_name, entry_src_name, 'Expected source file name: ' + str(file_name) + ' but got: ' + str(
            entry_src_name) + self.extra_data.get_all())
        self.assertEqual(file_new_name, entry_copy_name, 'Expected copy file name: ' + str(
            file_new_name) + ' but got: ' + str(entry_copy_name) + self.extra_data.get_all())

    def test_move_file_internal(self):
        expected_code_and_description = (0, 'SUCCESS')
        file_name = 'test_file_move_file_internal_' + str(int(time())) + '.dwg'
        folder_name = 'test_folder_move_file_internal_' + str(int(time()))

        self.extra_data.add_test_data('file name', file_name)
        self.extra_data.add_test_data('folder name', folder_name)

        created_folder_id, msg = TestUtils.create_folder(auth=self.auth, folder_name=folder_name,
                                                         extra_data=self.extra_data)
        self.assertIsNotNone(created_folder_id, msg + self.extra_data.get_all())

        created_file_id, msg = TestUtils.create_file(auth=self.auth, file_name=file_name, extra_data=self.extra_data)
        self.assertIsNotNone(created_file_id, msg + self.extra_data.get_all())

        move_file_response = self.files_management_client.move_file_internal(auth=self.auth,
                                                                             file_id=created_file_id,
                                                                             to_folder_id=created_folder_id)
        status_code = ClientUtils.get_response_status_code(move_file_response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('move_file_internal response', ClientUtils.get_response_body(move_file_response))

        code_desc = ClientUtils.get_code_and_description_from_response(move_file_response)
        self.assertEqual(expected_code_and_description, code_desc,
                         'Expected ' + str(expected_code_and_description) + ' but got: ' + str(
                             code_desc) + self.extra_data.get_all())

        file_system_entries, msg = TestUtils.get_internal_partition(auth=self.auth,
                                                                    partition_folder_id=created_folder_id,
                                                                    extra_data=self.extra_data)
        self.assertIsNotNone(file_system_entries, msg + self.extra_data.get_all())

        entry = TestUtils.get_entry_from_internal_file_system_entries(created_file_id, file_system_entries)

        self.assertIsNotNone(entry, 'File should have moved to the new folder' + self.extra_data.get_all())
        partition_file_name = TestUtils.get_entry_data_by_keys(entry=entry, keys=PartitionClient.KEY_ENTRY_NAME)
        self.assertEqual(file_name, partition_file_name,
                         'Expected file name: ' + str(file_name) + ' but got: ' + str(
                             partition_file_name) + self.extra_data.get_all())

        file_system_entries, msg = TestUtils.get_internal_partition(auth=self.auth, extra_data=self.extra_data)
        self.assertIsNotNone(file_system_entries, msg + self.extra_data.get_all())

        entry = TestUtils.get_entry_from_internal_file_system_entries(created_file_id, file_system_entries)

        self.assertIsNone(entry, 'File should no longer appear in root folder' + self.extra_data.get_all())

    def test_delete_file_internal(self):
        file_name = 'test_file_delete_file_internal_' + str(int(time())) + '.dwg'
        expected_code_and_description = (0, 'SUCCESS')

        self.extra_data.add_test_data('file name', file_name)

        created_file_id, msg = TestUtils.create_file(auth=self.auth, file_name=file_name, extra_data=self.extra_data)
        self.assertIsNotNone(created_file_id, msg + self.extra_data.get_all())

        delete_file_response = self.files_management_client.delete_file_internal(auth=self.auth,
                                                                                 file_id=created_file_id)
        status_code = ClientUtils.get_response_status_code(delete_file_response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('delete_file_internal response',
                                      ClientUtils.get_response_body(delete_file_response))

        code_desc = ClientUtils.get_code_and_description_from_response(delete_file_response)
        self.assertEqual(expected_code_and_description, code_desc,
                         'Expected ' + str(expected_code_and_description) + ' but got: ' + str(
                             code_desc) + self.extra_data.get_all())

        file_system_entries, msg = TestUtils.get_internal_partition(auth=self.auth, extra_data=self.extra_data)
        self.assertIsNotNone(file_system_entries, msg + self.extra_data.get_all())

        entry = TestUtils.get_entry_from_internal_file_system_entries(created_file_id, file_system_entries)

        self.assertIsNone(entry, 'Deleted file should not be in partition' + self.extra_data.get_all())

    def test_recent_files(self):
        response = self.files_management_client.recent_files(self.auth)
        status_code = ClientUtils.get_response_status_code(response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('response', ClientUtils.get_response_body(response))

        self.assertTrue(ClientUtils.is_key_in_body(response, 'limit'),
                        'Expected key limit in response body' + self.extra_data.get_all())
        self.assertTrue(ClientUtils.is_key_in_body(response, 'lastFileDate'),
                        'Expected key lastFileDate in response body' + self.extra_data.get_all())
        self.assertTrue(ClientUtils.is_key_in_body(response, 'page'),
                        'Expected key page in response body' + self.extra_data.get_all())

        drawings = ClientUtils.get_value_from_body(response, FilesManagementClient.KEY_DRAWINGS)
        self.assertTrue(len(drawings) > 0, 'Expected at least one drawing in response body' + self.extra_data.get_all())
