__author__ = 'alonitzhaki'
from unittest import TestCase
from time import time
import httplib

from utils.clients.main_client import MainRegisterAndLoginMixin

from rest_test.clients.clients_utils import ClientUtils
from rest_test.clients.files_client import FilesManagementClient
from rest_test.clients.partition_client import PartitionClient
from rest_test.tests_utils import TestUtils
from rest_test.extra_data_manager import ExtraDataManager


class ShareFilesTests(TestCase):
    auth = None

    user_name = 'rest_tests_share_files_' + str(int(time())) + '@autodesk.com'
    password = 'Moomoo123'
    first_name = 'Rest'
    last_name = 'Test'

    extra_data = None
    main_register_and_login_mixin = MainRegisterAndLoginMixin()
    files_management_client = FilesManagementClient()
    partition_client = PartitionClient()

    def setUp(self):
        self.extra_data = ExtraDataManager()
        self.extra_data.add_test_data('user name', self.user_name)
        if ShareFilesTests.auth is None:
            response = self.main_register_and_login_mixin.login_or_register(user_name=self.user_name,
                                                                            password=self.password,
                                                                            first_name=self.first_name,
                                                                            last_name=self.last_name)
            ShareFilesTests.auth = self.main_register_and_login_mixin.get_auth_from_login_data(response)
        self.assertIsInstance(ShareFilesTests.auth, str,
                              'Invalid auth: ' + str(ShareFilesTests.auth) + self.extra_data.get_all())

    def test_share_file(self):
        file_name = 'test_file_share_file_' + str(int(time())) + '.dwg'
        expected_code_and_description = (0, 'SUCCESS')
        user_name_to_share_with = 'rest_tests_share_with_user_' + str(int(time())) + '@autodesk.com'

        self.extra_data.add_test_data('file name', file_name)
        self.extra_data.add_test_data('user name to share with', user_name_to_share_with)

        login_data = self.main_register_and_login_mixin.login_or_register(user_name=user_name_to_share_with,
                                                                          password=self.password,
                                                                          first_name=self.first_name,
                                                                          last_name=self.last_name)
        auth_user_to_share_with = self.main_register_and_login_mixin.get_auth_from_login_data(login_data)

        self.assertIsInstance(auth_user_to_share_with, str,
                              'Invalid auth: ' + str(auth_user_to_share_with) + self.extra_data.get_all())

        created_file_id, msg = TestUtils.create_file(auth=self.auth, file_name=file_name, extra_data=self.extra_data)
        self.assertIsNotNone(created_file_id, msg + self.extra_data.get_all())

        share_response = self.files_management_client.share_file(auth=self.auth, file_id=created_file_id,
                                                                 emails=[user_name_to_share_with])
        status_code = ClientUtils.get_response_status_code(share_response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('share_file response', ClientUtils.get_response_body(share_response))

        code_desc = ClientUtils.get_code_and_description_from_response(share_response)
        self.assertEqual(expected_code_and_description, code_desc,
                         'Expected ' + str(expected_code_and_description) + ' but got: ' + str(
                             code_desc) + self.extra_data.get_all())

        file_system_entries, msg = TestUtils.get_internal_partition(auth=auth_user_to_share_with,
                                                                    extra_data=self.extra_data)
        self.assertIsNotNone(file_system_entries, msg + self.extra_data.get_all())

        shared_file = TestUtils.get_entry_from_internal_file_system_entries(created_file_id, file_system_entries)

        self.assertIsNotNone(shared_file, 'Shared file should exist in partition' + self.extra_data.get_all())

    def test_share_file_v2(self):
        file_name = 'test_file_share_file_v2_' + str(int(time())) + '.dwg'
        expected_code_and_description = (0, 'SUCCESS')
        user_name_to_share_with = 'rest_tests_share_with_user_' + str(int(time())) + '@autodesk.com'

        self.extra_data.add_test_data('file name', file_name)
        self.extra_data.add_test_data('user name to share with', user_name_to_share_with)

        login_data = self.main_register_and_login_mixin.login_or_register(user_name=user_name_to_share_with,
                                                                          password=self.password,
                                                                          first_name=self.first_name,
                                                                          last_name=self.last_name)
        auth_user_to_share_with = self.main_register_and_login_mixin.get_auth_from_login_data(login_data)

        self.assertIsInstance(auth_user_to_share_with, str,
                              'Invalid auth: ' + str(auth_user_to_share_with) + self.extra_data.get_all())

        created_file_id, msg = TestUtils.create_file(auth=self.auth, file_name=file_name, extra_data=self.extra_data)
        self.assertIsNotNone(created_file_id, msg + self.extra_data.get_all())

        share_response = self.files_management_client.share_file_v2(auth=self.auth, file_id=created_file_id,
                                                                    emails=[user_name_to_share_with])
        status_code = ClientUtils.get_response_status_code(share_response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('share_file response', ClientUtils.get_response_body(share_response))

        code_desc = ClientUtils.get_code_and_description_from_response(share_response)
        self.assertEqual(expected_code_and_description, code_desc,
                         'Expected ' + str(expected_code_and_description) + ' but got: ' + str(
                             code_desc) + self.extra_data.get_all())

        file_system_entries, msg = TestUtils.get_internal_partition(auth=auth_user_to_share_with,
                                                                    extra_data=self.extra_data)
        self.assertIsNotNone(file_system_entries, msg + self.extra_data.get_all())

        shared_file = TestUtils.get_entry_from_internal_file_system_entries(created_file_id, file_system_entries)

        self.assertIsNotNone(shared_file, 'Shared file should exist in partition' + self.extra_data.get_all())

    def test_share_file_v2_without_sharing_permissions(self):
        file_name = 'test_file_share_file_v2_without_permissions_' + str(int(time())) + '.dwg'
        expected_code_and_description = (3, 'INSUFFICIENT PERMISSIONS')
        user_name_to_share_with = 'rest_tests_share_with_user_' + str(int(time())) + '@autodesk.com'
        user_name_can_not_share_with = 'rest_tests_share_with_user_should_fail_' + str(int(time())) + '@autodesk.com'

        self.extra_data.add_test_data('file name', file_name)
        self.extra_data.add_test_data('user name to share with', user_name_to_share_with)
        self.extra_data.add_test_data('user name can not share with', user_name_can_not_share_with)

        login_data = self.main_register_and_login_mixin.login_or_register(user_name=user_name_to_share_with,
                                                                          password=self.password,
                                                                          first_name=self.first_name,
                                                                          last_name=self.last_name)
        auth_user_to_share_with = self.main_register_and_login_mixin.get_auth_from_login_data(login_data)

        self.assertIsInstance(auth_user_to_share_with, str,
                              'Invalid auth: ' + str(auth_user_to_share_with) + self.extra_data.get_all())

        login_data = self.main_register_and_login_mixin.login_or_register(user_name=user_name_can_not_share_with,
                                                                          password=self.password,
                                                                          first_name=self.first_name,
                                                                          last_name=self.last_name)
        auth_user_can_not_share_with = self.main_register_and_login_mixin.get_auth_from_login_data(login_data)

        self.assertIsInstance(auth_user_can_not_share_with, str,
                              'Invalid auth: ' + str(auth_user_can_not_share_with) + self.extra_data.get_all())

        created_file_id, msg = TestUtils.create_file(auth=self.auth, file_name=file_name, extra_data=self.extra_data)
        self.assertIsNotNone(created_file_id, msg + self.extra_data.get_all())

        share_response = self.files_management_client.share_file_v2(auth=self.auth, file_id=created_file_id,
                                                                    emails=[user_name_to_share_with], can_share=False)
        status_code = ClientUtils.get_response_status_code(share_response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('share_file response', ClientUtils.get_response_body(share_response))

        file_system_entries, msg = TestUtils.get_internal_partition(auth=auth_user_to_share_with,
                                                                    extra_data=self.extra_data)
        self.assertIsNotNone(file_system_entries, msg + self.extra_data.get_all())

        shared_file = TestUtils.get_entry_from_internal_file_system_entries(created_file_id, file_system_entries)

        self.assertIsNotNone(shared_file, 'Shared file should exist in partition' + self.extra_data.get_all())

        share_response = self.files_management_client.share_file_v2(auth=auth_user_to_share_with,
                                                                    file_id=created_file_id,
                                                                    emails=[user_name_can_not_share_with])
        status_code = ClientUtils.get_response_status_code(share_response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('share_file response', ClientUtils.get_response_body(share_response))

        code_desc = ClientUtils.get_code_and_description_from_response(share_response)
        self.assertEqual(expected_code_and_description, code_desc,
                         'Expected ' + str(expected_code_and_description) + ' but got: ' + str(
                             code_desc) + self.extra_data.get_all())

        file_system_entries, msg = TestUtils.get_internal_partition(auth=auth_user_can_not_share_with,
                                                                    extra_data=self.extra_data)
        self.assertIsNotNone(file_system_entries, msg + self.extra_data.get_all())

        shared_file = TestUtils.get_entry_from_internal_file_system_entries(created_file_id, file_system_entries)

        self.assertIsNone(shared_file,
                          'File not shared due to missing permissions should not exist in partition' + self.extra_data.get_all())

    def test_get_file_shares(self):
        file_name = 'test_file_get_file_shares_' + str(int(time())) + '.dwg'
        user_name_to_share_with = 'rest_tests_share_with_user_' + str(int(time())) + '@autodesk.com'

        self.extra_data.add_test_data('file name', file_name)
        self.extra_data.add_test_data('user name to share with', user_name_to_share_with)

        login_data = self.main_register_and_login_mixin.login_or_register(user_name=user_name_to_share_with,
                                                                          password=self.password,
                                                                          first_name=self.first_name,
                                                                          last_name=self.last_name)

        self.assertIsNotNone(login_data,
                             'Failed to register user_name_to_share_with' + self.extra_data.get_all())

        created_file_id, msg = TestUtils.create_file(auth=self.auth, file_name=file_name, extra_data=self.extra_data)
        self.assertIsNotNone(created_file_id, msg + self.extra_data.get_all())

        share_response = self.files_management_client.share_file_v2(auth=self.auth, file_id=created_file_id,
                                                                    emails=[user_name_to_share_with])
        status_code = ClientUtils.get_response_status_code(share_response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('share_file response', ClientUtils.get_response_body(share_response))

        get_shares_response = self.files_management_client.get_file_shares(auth=self.auth, file_id=created_file_id)
        status_code = ClientUtils.get_response_status_code(get_shares_response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('get_file_shares response', ClientUtils.get_response_body(get_shares_response))

        user_names = TestUtils.get_user_names_from_get_file_shares_response(get_shares_response)
        expected_user_names = [self.user_name, user_name_to_share_with]
        self.assertItemsEqual(expected_user_names, user_names, 'Expected users ' + str(
            expected_user_names) + ' to have permissions on file but got: ' + str(
            user_names) + self.extra_data.get_all())

    def test_remove_file_share(self):
        file_name = 'test_file_remove_file_share' + str(int(time())) + '.dwg'
        expected_code_and_description = (0, 'SUCCESS')
        user_name_to_share_with = 'rest_tests_share_with_user_' + str(int(time())) + '@autodesk.com'

        login_data = self.main_register_and_login_mixin.login_or_register(user_name=user_name_to_share_with,
                                                                          password=self.password,
                                                                          first_name=self.first_name,
                                                                          last_name=self.last_name)
        user_id_to_share_with = self.main_register_and_login_mixin.get_user_id_from_login_data(login_data)
        auth_user_to_share_with = self.main_register_and_login_mixin.get_auth_from_login_data(login_data)

        self.assertIsInstance(auth_user_to_share_with, str,
                              'Invalid auth: ' + str(auth_user_to_share_with) + self.extra_data.get_all())

        created_file_id, msg = TestUtils.create_file(auth=self.auth, file_name=file_name, extra_data=self.extra_data)
        self.assertIsNotNone(created_file_id, msg + self.extra_data.get_all())

        share_response = self.files_management_client.share_file_v2(auth=self.auth, file_id=created_file_id,
                                                                    emails=[user_name_to_share_with])
        status_code = ClientUtils.get_response_status_code(share_response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('share_file response', ClientUtils.get_response_body(share_response))

        delete_share_response = self.files_management_client.delete_file_share(auth=self.auth, file_id=created_file_id,
                                                                               user_id=user_id_to_share_with)
        status_code = ClientUtils.get_response_status_code(delete_share_response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('delete_file_share response',
                                      ClientUtils.get_response_body(delete_share_response))

        code_desc = ClientUtils.get_code_and_description_from_response(delete_share_response)
        self.assertEqual(expected_code_and_description, code_desc,
                         'Expected ' + str(expected_code_and_description) + ' but got: ' + str(
                             code_desc) + self.extra_data.get_all())

        file_system_entries, msg = TestUtils.get_internal_partition(auth=auth_user_to_share_with,
                                                                    extra_data=self.extra_data)
        self.assertIsNotNone(file_system_entries, msg + self.extra_data.get_all())

        shared_file = TestUtils.get_entry_from_internal_file_system_entries(created_file_id, file_system_entries)

        self.assertIsNone(shared_file,
                          'File no longer shared should not exist in partition' + self.extra_data.get_all())
