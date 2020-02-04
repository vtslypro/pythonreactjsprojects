__author__ = 'alonitzhaki'
from unittest import TestCase
import httplib
from time import time, sleep

from utils.clients.main_client import MainRegisterAndLoginMixin

from rest_test import app_settings as settings
from rest_test.clients.clients_utils import ClientUtils
from rest_test.clients.external_storage_client import ExternalStorageClient
from rest_test.clients.files_client import FilesManagementClient
from rest_test.clients.folders_client import FoldersManagementClient
from rest_test.clients.partition_client import PartitionClient
from rest_test.tests_utils import TestUtils
from rest_test.extra_data_manager import ExtraDataManager


class BoxExternalFileSystemTests(TestCase):
    auth = None
    host_id = None

    user_name = 'rest_tests_box_filesystem_' + str(int(time())) + '@autodesk.com'
    password = 'Moomoo123'
    first_name = 'Rest'
    last_name = 'Test'

    service_url = 'https://dav.box.com/dav'
    folder_name = 'box_folder'
    box_user_name = settings.BOX_USER_NAME
    box_password = settings.BOX_PASSWORD

    extra_data = None
    partition_client = PartitionClient()
    external_storage_client = ExternalStorageClient()
    files_management_client = FilesManagementClient()
    folders_management_client = FoldersManagementClient()

    def setUp(self):
        self.extra_data = ExtraDataManager()
        self.extra_data.add_test_data('user name', self.user_name)
        main_register_and_login_mixin = MainRegisterAndLoginMixin()
        if BoxExternalFileSystemTests.auth is None:
            response = main_register_and_login_mixin.login_or_register(user_name=self.user_name,
                                                                       password=self.password,
                                                                       first_name=self.first_name,
                                                                       last_name=self.last_name)
            BoxExternalFileSystemTests.auth = main_register_and_login_mixin.get_auth_from_login_data(response)
        self.assertIsInstance(BoxExternalFileSystemTests.auth, str,
                              'Invalid auth: ' + str(BoxExternalFileSystemTests.auth) + self.extra_data.get_all())

        if BoxExternalFileSystemTests.host_id is None:
            connect_to_box_response = self.external_storage_client.webdav_connect_to_external_storage(auth=self.auth,
                                                                                                      folder_name=self.folder_name,
                                                                                                      service_url=self.service_url,
                                                                                                      user_name=self.box_user_name,
                                                                                                      password=self.box_password)
            status_code = ClientUtils.get_response_status_code(connect_to_box_response)
            self.assertEqual(httplib.OK, status_code,
                             'Got status code: ' + str(status_code) + self.extra_data.get_all())
            self.extra_data.add_test_data('webdav_connect_to_external_storage_response',
                                          ClientUtils.get_response_body(connect_to_box_response))

            host_id = ClientUtils.get_value_from_body(connect_to_box_response, ExternalStorageClient.KEY_HOST_ID)
            self.assertEquals(61043, host_id,
                              'expected host_id: 61043 but got: ' + str(host_id) + self.extra_data.get_all())
            BoxExternalFileSystemTests.host_id = host_id

    def test_connect_to_box(self):
        active_hosts_response = self.external_storage_client.webdav_active_hosts(auth=self.auth)
        status_code = ClientUtils.get_response_status_code(active_hosts_response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('webdav_active_hosts response',
                                      ClientUtils.get_response_body(active_hosts_response))

        active_hosts = ClientUtils.get_response_body(active_hosts_response)
        self.assertIsNotNone(active_hosts, 'active_hosts is None' + self.extra_data.get_all())

        found_host_in_active_hosts = False
        for host in active_hosts:
            if host['hostId'] == self.host_id:
                found_host_in_active_hosts = True
                break
        self.assertTrue(found_host_in_active_hosts,
                        'Expected to find hostId 61043 in active hosts' + self.extra_data.get_all())

    def test_get_partition_external_v2(self):
        expected_entries_names = ['xref with block - Standard.zip', 'LiveView_Clean.dwg', 'Permanent_Folder']

        response = self.partition_client.get_external_partition_v2(auth=self.auth, host_id=self.host_id)
        status_code = ClientUtils.get_response_status_code(response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('external_partition response', ClientUtils.get_response_body(response))

        file_system_entries = ClientUtils.get_value_from_body(response, PartitionClient.KEY_FILE_SYSTEM_ENTRIES)
        self.assertIsNotNone(file_system_entries, 'Expected non empty partition' + self.extra_data.get_all())

        file_system_entries_names = TestUtils.get_entries_names_from_file_system_entries(file_system_entries)
        self.assertItemsEqual(expected_entries_names, file_system_entries_names,
                              'Expected entries names: ' + str(expected_entries_names) + ' but got: ' + str(
                                  file_system_entries_names) + self.extra_data.get_all())

    def test_get_partition_external(self):
        expected_entries_names = ['xref with block - Standard.zip', 'LiveView_Clean.dwg', 'Permanent_Folder']

        response = self.partition_client.get_external_partition(auth=self.auth, host_id=self.host_id)
        status_code = ClientUtils.get_response_status_code(response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('external_partition response', ClientUtils.get_response_body(response))

        file_system_entries = ClientUtils.get_value_from_body(response, PartitionClient.KEY_FILE_SYSTEM_ENTRIES)
        self.assertIsNotNone(file_system_entries, 'Expected non empty partition' + self.extra_data.get_all())

        file_system_entries_names = TestUtils.get_entries_names_from_file_system_entries(file_system_entries)
        self.assertItemsEqual(expected_entries_names, file_system_entries_names,
                              'Expected entries names: ' + str(expected_entries_names) + ' but got: ' + str(
                                  file_system_entries_names) + self.extra_data.get_all())

    def test_create_rename_and_delete_external_folder_v2(self):
        folder_name = 'test_folder_external_folder_flow_' + str(int(time()))
        folder_new_name = 'test_folder_external_folder_flow_renamed_' + str(int(time()))
        permanent_folder = 'Permanent_Folder/'
        expected_code_and_description = (0, 'SUCCESS')

        self.extra_data.add_test_data('folder name', folder_name)
        self.extra_data.add_test_data('folder new name', folder_new_name)

        create_folder_response = self.folders_management_client.create_external_folder_v2(auth=self.auth,
                                                                                          host_id=self.host_id,
                                                                                          new_folder_name=folder_name,
                                                                                          folder_path=permanent_folder)

        status_code = ClientUtils.get_response_status_code(create_folder_response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('create_external_folder response',
                                      ClientUtils.get_response_body(create_folder_response))

        code_desc = ClientUtils.get_code_and_description_from_response(create_folder_response)
        self.assertEqual(expected_code_and_description, code_desc,
                         'Expected ' + str(expected_code_and_description) + ' but got: ' + str(
                             code_desc) + self.extra_data.get_all())

        file_system_entries, msg = TestUtils.get_external_partition(auth=self.auth, host_id=self.host_id,
                                                                    path=permanent_folder, extra_data=self.extra_data)
        self.assertIsNotNone(file_system_entries, msg + self.extra_data.get_all())

        file_system_entries_names = [str(entry[self.partition_client.KEY_ENTRY_NAME]) for entry in file_system_entries
                                     if entry['type'] == 'EXTERNAL_FOLDER']

        if folder_name not in file_system_entries_names:
            self.fail('Folder should have been created in external host' + self.extra_data.get_all())

        new_folder_relative_path = permanent_folder + folder_name
        self.extra_data.add_test_data('new folder relative path', new_folder_relative_path)

        rename_folder_response = self.folders_management_client.rename_external_folder_v2(auth=self.auth,
                                                                                          host_id=self.host_id,
                                                                                          path=new_folder_relative_path,
                                                                                          name=folder_new_name)
        status_code = ClientUtils.get_response_status_code(rename_folder_response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('rename_external_folder response',
                                      ClientUtils.get_response_body(rename_folder_response))

        code_desc = ClientUtils.get_code_and_description_from_response(rename_folder_response)
        self.assertEqual(expected_code_and_description, code_desc,
                         'Expected ' + str(expected_code_and_description) + ' but got: ' + str(
                             code_desc) + self.extra_data.get_all())

        file_system_entries, msg = TestUtils.get_external_partition(auth=self.auth, host_id=self.host_id,
                                                                    path=permanent_folder, extra_data=self.extra_data)
        self.assertIsNotNone(file_system_entries, msg + self.extra_data.get_all())

        file_system_entries_names = [str(entry[self.partition_client.KEY_ENTRY_NAME]) for entry in file_system_entries
                                     if entry['type'] == 'EXTERNAL_FOLDER']

        if folder_new_name not in file_system_entries_names:
            self.fail('Folder should have been renamed in external host' + self.extra_data.get_all())

        renamed_folder_relative_path = permanent_folder + folder_new_name
        self.extra_data.add_test_data('renamed folder relative path', renamed_folder_relative_path)
        delete_folder_response = self.folders_management_client.delete_external_folder_v2(auth=self.auth,
                                                                                          host_id=self.host_id,
                                                                                          path=renamed_folder_relative_path)
        status_code = ClientUtils.get_response_status_code(delete_folder_response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('delete_external_folder response',
                                      ClientUtils.get_response_body(delete_folder_response))

        code_desc = ClientUtils.get_code_and_description_from_response(delete_folder_response)
        self.assertEqual(expected_code_and_description, code_desc,
                         'Expected ' + str(expected_code_and_description) + ' but got: ' + str(
                             code_desc) + self.extra_data.get_all())

        file_system_entries, msg = TestUtils.get_external_partition(auth=self.auth, host_id=self.host_id,
                                                                    path=permanent_folder, extra_data=self.extra_data)
        self.assertIsNotNone(file_system_entries, msg + self.extra_data.get_all())

        file_system_entries_names = [str(entry[self.partition_client.KEY_ENTRY_NAME]) for entry in file_system_entries
                                     if entry['type'] == 'EXTERNAL_FOLDER']

        if folder_new_name in file_system_entries_names:
            self.fail('Folder should have been deleted, and not found in partition result' + self.extra_data.get_all())

    def test_get_external_file_info_v2(self):
        file_name_in_box_folder = 'LiveView_Clean.dwg'

        external_file_info_response = self.files_management_client.get_external_file_info_v2(auth=self.auth,
                                                                                             host_id=self.host_id,
                                                                                             path=file_name_in_box_folder)
        status_code = ClientUtils.get_response_status_code(external_file_info_response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('get_external_file_info response',
                                      ClientUtils.get_response_body(external_file_info_response))

        file_primary_version = ClientUtils.get_value_from_body(external_file_info_response,
                                                               FilesManagementClient.KEY_PRIMARY_VERSION_ID)
        file_type = ClientUtils.get_value_from_body(external_file_info_response, FilesManagementClient.KEY_TYPE)
        file_size = ClientUtils.get_value_from_body(external_file_info_response, FilesManagementClient.KEY_SIZE)
        self.assertTrue(file_primary_version > 0, 'Expected valid primary version id but got: ' + str(
            file_primary_version) + self.extra_data.get_all())
        self.assertEquals('EXTERNAL_DRAWING', file_type, 'Expected file type: EXTERNAL_DRAWING but got: ' + str(
            file_type) + self.extra_data.get_all())
        self.assertEquals(62, file_size,
                          'Expected file size: 62 but got: ' + str(file_size) + self.extra_data.get_all())

    def test_get_external_file_info(self):
        file_name_in_box_folder = 'LiveView_Clean.dwg'

        external_file_info_response = self.files_management_client.get_external_file_info(auth=self.auth,
                                                                                          host_id=self.host_id,
                                                                                          path=file_name_in_box_folder)
        status_code = ClientUtils.get_response_status_code(external_file_info_response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('get_external_file_info response',
                                      ClientUtils.get_response_body(external_file_info_response))

        file_primary_version = ClientUtils.get_value_from_body(external_file_info_response,
                                                               FilesManagementClient.KEY_PRIMARY_VERSION_ID)
        file_type = ClientUtils.get_value_from_body(external_file_info_response, FilesManagementClient.KEY_TYPE)
        file_size = ClientUtils.get_value_from_body(external_file_info_response, FilesManagementClient.KEY_SIZE)
        self.assertTrue(file_primary_version > 0, 'Expected valid primary version id but got: ' + str(
            file_primary_version) + self.extra_data.get_all())
        self.assertEquals('EXTERNAL_DRAWING', file_type, 'Expected file type: EXTERNAL_DRAWING but got: ' + str(
            file_type) + self.extra_data.get_all())
        self.assertEquals(62, file_size,
                          'Expected file size: 62 but got: ' + str(file_size) + self.extra_data.get_all())

    def test_get_external_file_provider(self):
        file_name_in_box_folder = 'LiveView_Clean.dwg'

        external_file_info_response = self.files_management_client.get_external_file_provider_v2(auth=self.auth,
                                                                                                 host_id=self.host_id,
                                                                                                 path=file_name_in_box_folder)
        status_code = ClientUtils.get_response_status_code(external_file_info_response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('get_external_file_provider response',
                                      ClientUtils.get_response_body(external_file_info_response))

        provider = ClientUtils.get_value_from_body(external_file_info_response, FilesManagementClient.KEY_PROVIDER)
        self.assertEquals('BOX', provider,
                          'Expected provider: BOX but got: ' + str(provider) + self.extra_data.get_all())

    def test_move_file_to_external_folder_rename_and_delete_it_v2(self):
        folder_name = 'test_folder_external_file_flow_' + str(int(time()))
        file_name = 'test_file_external_file_flow_' + str(int(time())) + '.dwg'
        file_new_name = 'test_file_external_file_flow_renamed_' + str(int(time())) + '.dwg'
        permanent_folder = 'Permanent_Folder/'

        self.extra_data.add_test_data('folder name', folder_name)
        self.extra_data.add_test_data('file name', file_name)
        self.extra_data.add_test_data('file new name', file_new_name)

        success_code_and_description = (0, 'SUCCESS')
        cont_async_code_and_description = (23, 'FILESYSTEM OPERATION CONTINUES ASYNCRONOUSLY')

        polling_timeout_in_seconds = 30
        delay_between_polls = 1

        success, msg = TestUtils.create_external_folder(auth=self.auth, host_id=self.host_id,
                                                        folder_path=permanent_folder,
                                                        new_folder_name=folder_name, extra_data=self.extra_data)
        self.assertIsNotNone(success, msg + self.extra_data.get_all())

        folder_name = permanent_folder + folder_name
        self.extra_data.add_test_data('folder name', folder_name)

        created_file_id, msg = TestUtils.create_file(auth=self.auth, file_name=file_name, extra_data=self.extra_data)
        self.assertIsNotNone(created_file_id, msg + self.extra_data.get_all())

        move_to_external_folder_response = self.files_management_client.move_internal_file_to_external(auth=self.auth,
                                                                                                       file_id=created_file_id,
                                                                                                       to_host_id=self.host_id,
                                                                                                       to_path=folder_name + '/')
        status_code = ClientUtils.get_response_status_code(move_to_external_folder_response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('move_internal_file_to_external response',
                                      ClientUtils.get_response_body(move_to_external_folder_response))

        code_desc = ClientUtils.get_code_and_description_from_response(move_to_external_folder_response)
        self.assertEqual(cont_async_code_and_description, code_desc,
                         'Expected ' + str(cont_async_code_and_description) + ' but got: ' + str(
                             code_desc) + self.extra_data.get_all())

        polling_id = ClientUtils.get_value_from_body(move_to_external_folder_response,
                                                     FilesManagementClient.KEY_POLLING_ID)
        self.assertTrue(polling_id > 0,
                        'Expected valid polling id, but got: ' + str(polling_id) + self.extra_data.get_all())
        self.extra_data.add_test_data('polling id', polling_id)

        successful_move, msg = TestUtils.poll_for_move_to_external(auth=self.auth, polling_id=polling_id,
                                                                   sleep_period=delay_between_polls,
                                                                   timeout_in_seconds=polling_timeout_in_seconds,
                                                                   extra_data=self.extra_data)
        self.assertIsNotNone(successful_move, msg + self.extra_data.get_all())

        sleep(5)

        file_system_entries, msg = TestUtils.get_external_partition(auth=self.auth, host_id=self.host_id,
                                                                    path=folder_name, extra_data=self.extra_data)
        self.assertIsNotNone(file_system_entries, msg + self.extra_data.get_all())

        file_system_entries_names = [str(entry[self.partition_client.KEY_ENTRY_NAME]) for entry in file_system_entries
                                     if entry['type'] == 'EXTERNAL_DRAWING']
        if file_name not in file_system_entries_names:
            self.fail('New file should have been moved to external host' + self.extra_data.get_all())

        internal_file_system_entries, msg = TestUtils.get_internal_partition(auth=self.auth, extra_data=self.extra_data)
        self.assertIsNotNone(internal_file_system_entries, msg + self.extra_data.get_all())

        file_system_entries_names = [str(entry[self.partition_client.KEY_ENTRY_NAME]) for entry in
                                     internal_file_system_entries if entry['type'] == 'DRAWING']
        if file_new_name in file_system_entries_names:
            self.fail(
                'File should have moved to external folder, and not found in internal partition result' + self.extra_data.get_all())

        file_relative_path = folder_name + '/' + file_name
        self.extra_data.add_test_data('file relative path', file_relative_path)
        rename_file_response = self.files_management_client.rename_external_file_v2(auth=self.auth,
                                                                                    host_id=self.host_id,
                                                                                    name=file_new_name,
                                                                                    path=file_relative_path)
        status_code = ClientUtils.get_response_status_code(rename_file_response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('rename_external_file response',
                                      ClientUtils.get_response_body(rename_file_response))

        code_desc = ClientUtils.get_code_and_description_from_response(rename_file_response)
        self.assertEqual(success_code_and_description, code_desc,
                         'Expected ' + str(success_code_and_description) + ' but got: ' + str(
                             code_desc) + self.extra_data.get_all())

        file_system_entries, msg = TestUtils.get_external_partition(auth=self.auth, host_id=self.host_id,
                                                                    path=folder_name, extra_data=self.extra_data)
        self.assertIsNotNone(file_system_entries, msg + self.extra_data.get_all())

        file_system_entries_names = [str(entry[self.partition_client.KEY_ENTRY_NAME]) for entry in file_system_entries
                                     if entry['type'] == 'EXTERNAL_DRAWING']

        if file_new_name not in file_system_entries_names:
            self.fail('File should have been renamed in external host' + self.extra_data.get_all())

        file_relative_path = folder_name + '/' + file_new_name
        self.extra_data.add_test_data('file relative path', file_relative_path)

        delete_file_response = self.files_management_client.delete_external_file_v2(auth=self.auth,
                                                                                    host_id=self.host_id,
                                                                                    path=file_relative_path)
        status_code = ClientUtils.get_response_status_code(delete_file_response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('delete_external_file response',
                                      ClientUtils.get_response_body(delete_file_response))

        code_desc = ClientUtils.get_code_and_description_from_response(delete_file_response)
        self.assertEqual(success_code_and_description, code_desc,
                         'Expected ' + str(success_code_and_description) + ' but got: ' + str(
                             code_desc) + self.extra_data.get_all())

        file_system_entries, msg = TestUtils.get_external_partition(auth=self.auth, host_id=self.host_id,
                                                                    path=folder_name, extra_data=self.extra_data)
        self.assertIsNotNone(file_system_entries, msg + self.extra_data.get_all())

        file_system_entries_names = [str(entry[self.partition_client.KEY_ENTRY_NAME]) for entry in file_system_entries
                                     if entry['type'] == 'EXTERNAL_DRAWING']

        if file_new_name in file_system_entries_names:
            self.fail('Folder should have been deleted, and not found in partition result' + self.extra_data.get_all())

        # Teardown - remove created folder - does not affect test results
        self.folders_management_client.delete_external_folder_v2(auth=self.auth, host_id=self.host_id,
                                                                 path=folder_name)
