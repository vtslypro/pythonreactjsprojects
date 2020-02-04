__author__ = 'alonitzhaki'
from unittest import TestCase
from time import time
import httplib

from utils.clients.main_client import MainRegisterAndLoginMixin

from rest_test.clients.clients_utils import ClientUtils
from rest_test.clients.folders_client import FoldersManagementClient
from rest_test.tests_utils import TestUtils
from rest_test.extra_data_manager import ExtraDataManager


class ShareFolderTests(TestCase):
    auth = None

    user_name = 'rest_tests_share_folders_' + str(int(time())) + '@autodesk.com'
    first_name = 'Rest'
    last_name = 'Test'
    password = 'Moomoo123'

    extra_data = None
    main_register_and_login = MainRegisterAndLoginMixin()
    folders_management_client = FoldersManagementClient()

    def setUp(self):
        self.extra_data = ExtraDataManager()
        self.extra_data.add_test_data('user name', self.user_name)
        if ShareFolderTests.auth is None:
            response = self.main_register_and_login.login_or_register(user_name=self.user_name, password=self.password,
                                                                      first_name=self.first_name,
                                                                      last_name=self.last_name)
            ShareFolderTests.auth = self.main_register_and_login.get_auth_from_login_data(response)
        self.assertIsInstance(ShareFolderTests.auth, str,
                              'Invalid auth: ' + str(ShareFolderTests.auth) + self.extra_data.get_all())

    def test_share_folder(self):
        folder_name = 'test_folder_share_folder_' + str(int(time()))
        expected_code_and_description = (0, 'SUCCESS')

        user_name_to_share_with = 'rest_tests_share_with_user' + str(int(time())) + '@autodesk.com'

        self.extra_data.add_test_data('folder name', folder_name)
        self.extra_data.add_test_data('user name to share with', user_name_to_share_with)

        login_data = self.main_register_and_login.login_or_register(user_name=user_name_to_share_with,
                                                                    password=self.password,
                                                                    first_name=self.first_name,
                                                                    last_name=self.last_name)
        auth_user_to_share_with = self.main_register_and_login.get_auth_from_login_data(login_data)

        self.assertIsInstance(auth_user_to_share_with, str,
                              'Invalid auth: ' + str(auth_user_to_share_with) + self.extra_data.get_all())

        created_folder_id, msg = TestUtils.create_folder(auth=self.auth, folder_name=folder_name,
                                                         extra_data=self.extra_data)
        self.assertIsNotNone(created_folder_id, msg + self.extra_data.get_all())

        share_response = self.folders_management_client.share_folder(auth=self.auth, folder_id=created_folder_id,
                                                                     emails=[user_name_to_share_with])
        status_code = ClientUtils.get_response_status_code(share_response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('share_folder response', ClientUtils.get_response_body(share_response))

        code_desc = ClientUtils.get_code_and_description_from_response(share_response)
        self.assertEqual(expected_code_and_description, code_desc,
                         'Expected ' + str(expected_code_and_description) + ' but got: ' + str(
                             code_desc) + self.extra_data.get_all())

        file_system_entries, msg = TestUtils.get_internal_partition(auth=auth_user_to_share_with,
                                                                    extra_data=self.extra_data)
        self.assertIsNotNone(file_system_entries, msg + self.extra_data.get_all())

        shared_folder = TestUtils.get_entry_from_internal_file_system_entries(created_folder_id, file_system_entries)

        self.assertIsNotNone(shared_folder, 'Shared folder should exist in partition' + self.extra_data.get_all())

    def test_share_folder_without_sharing_permissions(self):
        folder_name = 'test_folder_share_folder_without_permissions_' + str(int(time()))
        expected_code_and_description = (3, 'INSUFFICIENT PERMISSIONS')

        user_name_to_share_with = 'rest_tests_share_with_user' + str(int(time())) + '@autodesk.com'
        user_name_can_not_share_with = 'rest_tests_share_with_user_should_fail' + str(int(time())) + '@autodesk.com'

        self.extra_data.add_test_data('folder name', folder_name)
        self.extra_data.add_test_data('user name to share with', user_name_to_share_with)
        self.extra_data.add_test_data('user name can not share with', user_name_can_not_share_with)

        login_data = self.main_register_and_login.login_or_register(user_name=user_name_to_share_with,
                                                                    password=self.password,
                                                                    first_name=self.first_name,
                                                                    last_name=self.last_name)
        auth_user_to_share_with = self.main_register_and_login.get_auth_from_login_data(login_data)

        self.assertIsInstance(auth_user_to_share_with, str,
                              'Invalid auth: ' + str(auth_user_to_share_with) + self.extra_data.get_all())

        login_data = self.main_register_and_login.login_or_register(user_name=user_name_can_not_share_with,
                                                                    password=self.password,
                                                                    first_name=self.first_name,
                                                                    last_name=self.last_name)
        auth_user_can_not_share_with = self.main_register_and_login.get_auth_from_login_data(login_data)

        self.assertIsInstance(auth_user_can_not_share_with, str,
                              'Invalid auth: ' + str(auth_user_can_not_share_with) + self.extra_data.get_all())

        created_folder_id, msg = TestUtils.create_folder(auth=self.auth, folder_name=folder_name,
                                                         extra_data=self.extra_data)
        self.assertIsNotNone(created_folder_id, msg + self.extra_data.get_all())

        share_response = self.folders_management_client.share_folder(auth=self.auth, folder_id=created_folder_id,
                                                                     emails=[user_name_to_share_with], can_share=False)
        status_code = ClientUtils.get_response_status_code(share_response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('share_folder response', ClientUtils.get_response_body(share_response))

        file_system_entries, msg = TestUtils.get_internal_partition(auth=auth_user_to_share_with,
                                                                    extra_data=self.extra_data)
        self.assertIsNotNone(file_system_entries, msg + self.extra_data.get_all())

        shared_folder = TestUtils.get_entry_from_internal_file_system_entries(created_folder_id, file_system_entries)

        self.assertIsNotNone(shared_folder, 'Shared folders should exist in partition' + self.extra_data.get_all())

        share_response = self.folders_management_client.share_folder(auth=auth_user_to_share_with,
                                                                     folder_id=created_folder_id,
                                                                     emails=[user_name_can_not_share_with])
        status_code = ClientUtils.get_response_status_code(share_response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('share_folder response', ClientUtils.get_response_body(share_response))

        code_desc = ClientUtils.get_code_and_description_from_response(share_response)
        self.assertEqual(expected_code_and_description, code_desc,
                         'Expected ' + str(expected_code_and_description) + ' but got: ' + str(
                             code_desc) + self.extra_data.get_all())

        file_system_entries, msg = TestUtils.get_internal_partition(auth=auth_user_can_not_share_with,
                                                                    extra_data=self.extra_data)
        self.assertIsNotNone(file_system_entries, msg + self.extra_data.get_all())

        shared_folder = TestUtils.get_entry_from_internal_file_system_entries(created_folder_id, file_system_entries)

        self.assertIsNone(shared_folder,
                          'Folder not shared due to missing permissions should not exist in partition' + self.extra_data.get_all())

    def test_get_folder_shares(self):
        folder_name = 'test_folder_get_folder_shares_' + str(int(time()))
        user_name_to_share_with = 'rest_tests_share_with_user' + str(int(time())) + '@autodesk.com'

        self.extra_data.add_test_data('folder name', folder_name)
        self.extra_data.add_test_data('user name to share with', user_name_to_share_with)

        login_data = self.main_register_and_login.login_or_register(user_name=user_name_to_share_with,
                                                                    password=self.password,
                                                                    first_name=self.first_name,
                                                                    last_name=self.last_name)
        self.assertIsNotNone(login_data,
                             'Failed to register user_name_to_share_with' + self.extra_data.get_all())

        created_folder_id, msg = TestUtils.create_folder(auth=self.auth, folder_name=folder_name,
                                                         extra_data=self.extra_data)
        self.assertIsNotNone(created_folder_id, msg + self.extra_data.get_all())

        share_response = self.folders_management_client.share_folder(auth=self.auth, folder_id=created_folder_id,
                                                                     emails=[user_name_to_share_with])
        status_code = ClientUtils.get_response_status_code(share_response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('share_folder response', ClientUtils.get_response_body(share_response))

        get_shares_response = self.folders_management_client.get_folder_shares(auth=self.auth,
                                                                               folder_id=created_folder_id)
        status_code = ClientUtils.get_response_status_code(get_shares_response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + '. user_name: ' + str(
            self.user_name) + '. folder_name: ' + str(folder_name) + '. created_folder_id: ' + str(
            created_folder_id) + '. user_name_to_share_with' + str(user_name_to_share_with))

        user_names = TestUtils.get_user_names_from_get_folder_shares_response(get_shares_response)
        expected_user_names = [self.user_name, user_name_to_share_with]
        self.assertItemsEqual(expected_user_names, user_names, 'Expected users ' + str(
            expected_user_names) + ' to have permissions on folder but got: ' + str(
            user_names) + self.extra_data.get_all())

    def test_remove_folder_share(self):
        folder_name = 'test_folder_remove_folder_share_' + str(int(time()))
        expected_code_and_description = (0, 'SUCCESS')

        user_name_to_share_with = 'rest_tests_share_with_user' + str(int(time())) + '@autodesk.com'

        self.extra_data.add_test_data('folder name', folder_name)
        self.extra_data.add_test_data('user name to share with', user_name_to_share_with)

        login_data = self.main_register_and_login.login_or_register(user_name=user_name_to_share_with,
                                                                    password=self.password,
                                                                    first_name=self.first_name,
                                                                    last_name=self.last_name)
        user_id_to_share_with = self.main_register_and_login.get_user_id_from_login_data(login_data)
        auth_user_to_share_with = self.main_register_and_login.get_auth_from_login_data(login_data)

        self.assertIsInstance(auth_user_to_share_with, str,
                              'Invalid auth: ' + str(auth_user_to_share_with) + self.extra_data.get_all())

        created_folder_id, msg = TestUtils.create_folder(auth=self.auth, folder_name=folder_name,
                                                         extra_data=self.extra_data)
        self.assertIsNotNone(created_folder_id, msg + self.extra_data.get_all())

        share_response = self.folders_management_client.share_folder(auth=self.auth, folder_id=created_folder_id,
                                                                     emails=[user_name_to_share_with])
        status_code = ClientUtils.get_response_status_code(share_response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('share_folder response', ClientUtils.get_response_body(share_response))

        delete_share_response = self.folders_management_client.delete_folder_share(auth=self.auth,
                                                                                   folder_id=created_folder_id,
                                                                                   user_id=user_id_to_share_with)
        status_code = ClientUtils.get_response_status_code(delete_share_response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('deleted_folder_share response',
                                      ClientUtils.get_response_body(delete_share_response))

        code_desc = ClientUtils.get_code_and_description_from_response(delete_share_response)
        self.assertEqual(expected_code_and_description, code_desc,
                         'Expected ' + str(expected_code_and_description) + ' but got: ' + str(
                             code_desc) + self.extra_data.get_all())

        file_system_entries, msg = TestUtils.get_internal_partition(auth=auth_user_to_share_with,
                                                                    extra_data=self.extra_data)
        self.assertIsNotNone(file_system_entries, msg + self.extra_data.get_all())

        shared_folder = TestUtils.get_entry_from_internal_file_system_entries(created_folder_id, file_system_entries)

        self.assertIsNone(shared_folder,
                          'Folder no longer shared should not exist in partition' + self.extra_data.get_all())
