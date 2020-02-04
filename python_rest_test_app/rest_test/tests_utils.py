__author__ = 'alonitzhaki'
from time import time, sleep
import httplib

from rest_test.clients.drawing_feed_client import DrawingFeedClient
from rest_test.clients.files_client import FilesManagementClient
from rest_test.clients.folders_client import FoldersManagementClient
from rest_test.clients.partition_client import PartitionClient
from rest_test.clients.poll_client import PollClient
from rest_test.clients.clients_utils import ClientUtils
from rest_test.clients.user_client import UserClient


class TestUtils(object):
    @staticmethod
    def create_file(auth, file_name, extra_data):
        files_management_client = FilesManagementClient()
        response = files_management_client.create_file_v2(auth=auth, new_drawing_name=file_name)

        status_code = ClientUtils.get_response_status_code(response)
        if not httplib.OK == status_code:
            return None, 'Expected status: ' + str(httplib.OK) + ' but got: ' + str(status_code)
        extra_data.add_test_data('create_file response', ClientUtils.get_response_body(response))

        created_file_id = ClientUtils.get_value_from_body(response, FilesManagementClient.KEY_VERSION_ID)
        if not created_file_id > 0:
            return None, 'Expected a valid file id but got: ' + str(created_file_id)
        extra_data.add_test_data('created file id', created_file_id)

        return created_file_id, ''

    @staticmethod
    def create_folder(auth, folder_name, extra_data):
        expected_code_and_description = (0, 'SUCCESS')
        folders_management_client = FoldersManagementClient()
        response = folders_management_client.create_folder_v2(auth=auth, new_folder_name=folder_name)

        status_code = ClientUtils.get_response_status_code(response)
        if not httplib.OK == status_code:
            return None, 'Expected status: ' + str(httplib.OK) + ' but got: ' + str(status_code)
        extra_data.add_test_data('create_folder response', ClientUtils.get_response_body(response))

        code_and_description = ClientUtils.get_code_and_description_from_response(response)
        if not expected_code_and_description == code_and_description:
            return None, 'Expected code and description: ' + str(expected_code_and_description) + ' but got: ' + str(
                code_and_description)

        created_folder_id = ClientUtils.get_value_from_body(response, FoldersManagementClient.KEY_FOLDER_ID)
        if not created_folder_id > 0:
            return None, 'Expected a valid folder id but got: ' + str(created_folder_id)
        extra_data.add_test_data('created folder id', created_folder_id)

        return created_folder_id, ''

    @staticmethod
    def create_external_folder(auth, host_id, folder_path, new_folder_name, extra_data):
        expected_code_and_description = (0, 'SUCCESS')
        folders_management_client = FoldersManagementClient()
        response = folders_management_client.create_external_folder_v2(auth=auth, host_id=host_id,
                                                                       folder_path=folder_path,
                                                                       new_folder_name=new_folder_name)
        status_code = ClientUtils.get_response_status_code(response)
        if not httplib.OK == status_code:
            return None, 'Expected status: ' + str(httplib.OK) + ' but got: ' + str(status_code)
        extra_data.add_test_data('create_external_folder response', ClientUtils.get_response_body(response))

        code_and_description = ClientUtils.get_code_and_description_from_response(response)
        if not expected_code_and_description == code_and_description:
            return None, 'Expected code and description: ' + str(expected_code_and_description) + ' but got: ' + str(
                code_and_description)

        return True, ''

    @staticmethod
    def get_internal_partition(auth, extra_data, partition_folder_id=0):
        partition_client = PartitionClient()
        response = partition_client.get_partition_v2(auth=auth, parent_folder_id=partition_folder_id)

        status_code = ClientUtils.get_response_status_code(response)
        if not httplib.OK == status_code:
            return None, 'Expected status: ' + str(httplib.OK) + ' but got: ' + str(status_code)
        extra_data.add_test_data('get_partition response', ClientUtils.get_response_body(response))

        file_system_entries = ClientUtils.get_value_from_body(response, PartitionClient.KEY_FILE_SYSTEM_ENTRIES)
        if file_system_entries is None:
            return None, 'Expected a non-empty partition'

        return file_system_entries, ''

    @staticmethod
    def get_entry_from_internal_file_system_entries(entry_id, internal_file_system_entries):
        for entry in internal_file_system_entries:
            if (entry[PartitionClient.KEY_TYPE] == 'FOLDER' or entry[PartitionClient.KEY_TYPE] == 'SHARED_FOLDER') and \
                            entry[PartitionClient.KEY_FOLDER_ID] == entry_id:
                return entry
            if entry[PartitionClient.KEY_TYPE] == 'DRAWING' and \
                            entry[PartitionClient.KEY_PRIMARY_VERSION_ID] == entry_id:
                return entry
        return None

    @staticmethod
    def get_first_drawing_from_internal_file_system(internal_file_system_entries):
        first_file = TestUtils.get_drawing_by_index_from_internal_file_system(internal_file_system_entries, index=0)

        if first_file is None:
            return None
        return first_file

    @staticmethod
    def get_drawing_by_index_from_internal_file_system(internal_file_system_entries, index):
        if internal_file_system_entries is None:
            return None
        file_entries = [entry for entry in internal_file_system_entries if entry[PartitionClient.KEY_TYPE] == 'DRAWING']
        if file_entries is None or len(file_entries) <= index:
            return None

        return file_entries[index]

    @staticmethod
    def get_entry_data_by_keys(entry, keys):
        return entry[keys] if isinstance(keys, str) else [entry[key] for key in keys]

    @staticmethod
    def get_external_partition(auth, extra_data, host_id, path=''):
        partition_client = PartitionClient()
        response = partition_client.get_external_partition_v2(auth=auth, host_id=host_id, path=path)

        status_code = ClientUtils.get_response_status_code(response)
        if not httplib.OK == status_code:
            return None, 'Expected status: ' + str(httplib.OK) + ' but got: ' + str(status_code)
        extra_data.add_test_data('get_external_partition response', ClientUtils.get_response_body(response))

        file_system_entries = ClientUtils.get_value_from_body(response, PartitionClient.KEY_FILE_SYSTEM_ENTRIES)
        if file_system_entries is None:
            return None, 'Expected a non-empty partition'

        return file_system_entries, ''

    @staticmethod
    def get_user_names_from_get_folder_shares_response(folder_shares_response):
        body = ClientUtils.get_response_body(folder_shares_response)
        if body is None:
            return None
        return [share_entry[FoldersManagementClient.KEY_USER_DRAWING_PREFERENCES][FoldersManagementClient.KEY_USER][
                    FoldersManagementClient.KEY_USER_NAME] for share_entry in body]

    @staticmethod
    def get_user_names_from_get_file_shares_response(file_shares_response):
        body = ClientUtils.get_response_body(file_shares_response)
        if body is None:
            return None
        return [share_entry[FilesManagementClient.KEY_USER_DRAWING_PREFERENCES][FilesManagementClient.KEY_USER][
                    FilesManagementClient.KEY_USER_NAME] for share_entry in body]

    @staticmethod
    def get_addresses_from_share_suggestions_response(share_suggestions_response):
        body = ClientUtils.get_response_body(share_suggestions_response)
        if body is None:
            return None
        return [entry[UserClient.KEY_CONTACT_ADDRESS] for entry in body]

    @staticmethod
    def get_post_from_drawing_feed_response(drawing_feed_response, post_id):
        body = ClientUtils.get_response_body(drawing_feed_response)
        if body is None:
            return None
        for post_entry in body:
            if post_entry[DrawingFeedClient.KEY_ID] == post_id:
                return post_entry
        return None

    @staticmethod
    def get_entries_names_from_file_system_entries(file_system_entries):
        return [str(entry[PartitionClient.KEY_ENTRY_NAME]) for entry in file_system_entries]

    @staticmethod
    def poll_for_upload(auth, version_id, sleep_period, timeout_in_seconds, extra_data):

        event = 'uploadcomplete'
        search_key = 'versionId'
        return_key = None
        failure_msg = 'Sharding failed'

        return TestUtils.poll_master(auth=auth, event=event, search_key=search_key, search_value=version_id,
                                     return_key=return_key, sleep_period=sleep_period,
                                     timeout_in_seconds=timeout_in_seconds,
                                     failure_msg=failure_msg, extra_data=extra_data)

    @staticmethod
    def poll_for_download(auth, download_id, sleep_period, timeout_in_seconds, extra_data):
        event = 'downloadcomplete'
        search_key = 'downloadId'
        return_key = 'defaultName'
        failure_msg = 'Reverse-Sharding failed'

        return TestUtils.poll_master(auth=auth, event=event, search_key=search_key, search_value=download_id,
                                     return_key=return_key, sleep_period=sleep_period,
                                     timeout_in_seconds=timeout_in_seconds,
                                     failure_msg=failure_msg, extra_data=extra_data)

    @staticmethod
    def poll_for_plot(auth, version_id, sleep_period, timeout_in_seconds, extra_data):
        event = 'exportcomplete'
        search_key = 'downloadId'
        return_key = 'defaultName'
        failure_msg = 'Plot failed'

        return TestUtils.poll_master(auth=auth, event=event, search_key=search_key, search_value=version_id,
                                     return_key=return_key, sleep_period=sleep_period,
                                     timeout_in_seconds=timeout_in_seconds,
                                     failure_msg=failure_msg, extra_data=extra_data)

    @staticmethod
    def poll_for_move_to_external(auth, polling_id, sleep_period, timeout_in_seconds, extra_data):
        event = 'filesystemupdated'
        search_key = 'pollingId'
        return_key = None
        failure_msg = 'Move file to external storage failed'

        return TestUtils.poll_master(auth=auth, event=event, search_key=search_key, search_value=polling_id,
                                     return_key=return_key, sleep_period=sleep_period,
                                     timeout_in_seconds=timeout_in_seconds,
                                     failure_msg=failure_msg, extra_data=extra_data)

    @staticmethod
    def poll_master(auth, extra_data, event, search_key, search_value, return_key, sleep_period, timeout_in_seconds,
                    failure_msg='polling received error code'):
        """
        returns a 2-tuple s.t.:
            first item is the requested data of caller
            second item is the error message if failed
        """
        last_notification_id = 0
        polling_start_time = int(time())
        polling_end_time = polling_start_time

        poll_client = PollClient()

        while polling_end_time - polling_start_time < timeout_in_seconds:
            poll_response = poll_client.poll(auth=auth, last_notification_id=last_notification_id, event=event)
            status_code = ClientUtils.get_response_status_code(poll_response)
            if httplib.OK != status_code:
                return None, 'Expected status: ' + str(httplib.OK) + ' but got: ' + str(status_code)
            extra_data.add_test_data('poll response', ClientUtils.get_response_body(poll_response))

            notifications = ClientUtils.get_value_from_body(poll_response, PollClient.KEY_NOTIFICATIONS)
            if notifications is not None:

                for notif in notifications:
                    notif_id = notif[PollClient.KEY_NOTIFICATION_ID]

                    if notif_id > last_notification_id:
                        last_notification_id = notif_id

                    if notif[PollClient.KEY_NOTIFICATION_TYPE].lower() == event.lower() and \
                                    notif[search_key] == search_value:
                        notif_status = notif[PollClient.KEY_NOTIFICATION_STATUS]
                        if notif_status == 0:  # Successful
                            if return_key is not None:
                                return_value = notif[return_key]
                                extra_data.add_test_data(return_key, return_value)
                                return return_value, ''
                            else:
                                return True, ''
                        elif notif_status == 2:  # Failed
                            return None, failure_msg
            polling_end_time = int(time())
            sleep(sleep_period)
        return None, 'Timeout while polling for event: ' + str(event)
