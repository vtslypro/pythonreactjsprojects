__author__ = 'alonitzhaki'
import httplib
from time import time, sleep
from unittest import TestCase

from utils.clients.main_client import MainRegisterAndLoginMixin

from rest_test import app_settings as settings
from rest_test.clients.clients_utils import ClientUtils
from rest_test.clients.files_client import FilesManagementClient
from rest_test.clients.partition_client import PartitionClient
from rest_test.clients.poll_client import PollClient
from rest_test.clients.s3_client import S3Client
from rest_test.clients.xrefs_client import XrefsClient
from rest_test.mail_utils import GmailClient
from rest_test.tests_utils import TestUtils
from rest_test.extra_data_manager import ExtraDataManager


class ShardingTests(TestCase):
    auth = None

    user_name = 'rest_tests_sharding_' + str(int(time())) + '@autodesk.com'
    password = 'Moomoo123'
    first_name = 'Rest'
    last_name = 'Test'

    extra_data = None
    files_management_client = FilesManagementClient()
    s3_client = S3Client()
    poll_client = PollClient()

    def setUp(self):
        self.extra_data = ExtraDataManager()
        self.extra_data.add_test_data('user name', self.user_name)
        main_register_and_login_mixin = MainRegisterAndLoginMixin()
        if ShardingTests.auth is None:
            response = main_register_and_login_mixin.login_or_register(user_name=self.user_name,
                                                                       password=self.password,
                                                                       first_name=self.first_name,
                                                                       last_name=self.last_name)
            ShardingTests.auth = main_register_and_login_mixin.get_auth_from_login_data(response)
        self.assertIsInstance(ShardingTests.auth, str,
                              'Invalid auth: ' + str(ShardingTests.auth) + self.extra_data.get_all())

    def test_get_url_to_upload_v1(self):
        file_name = 'LiveView_Clean.dwg'
        file_size = 64128

        url_to_upload_response = self.files_management_client.get_url_to_upload_v1(auth=self.auth, folder_id=0,
                                                                                   file_name=file_name,
                                                                                   file_size=file_size)
        status_code = ClientUtils.get_response_status_code(url_to_upload_response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('get_url_to_upload response',
                                      ClientUtils.get_response_body(url_to_upload_response))

        version_id = ClientUtils.get_value_from_body(url_to_upload_response, FilesManagementClient.KEY_VERSION_ID)
        request_type = ClientUtils.get_value_from_body(url_to_upload_response, FilesManagementClient.KEY_REQUEST_TYPE)
        upload_url = ClientUtils.get_value_from_body(url_to_upload_response, FilesManagementClient.KEY_URL_TO_UPLOAD)
        header_x_amz_date = ClientUtils.get_value_from_body(url_to_upload_response, json_path='headers.x-amz-date')
        header_x_amz_acl = ClientUtils.get_value_from_body(url_to_upload_response, json_path='headers.x-amz-acl')
        header_authorization = ClientUtils.get_value_from_body(url_to_upload_response,
                                                               json_path='headers.Authorization')
        headers_content_type = ClientUtils.get_value_from_body(url_to_upload_response, json_path='headers.Content-Type')

        self.assertTrue(version_id > 0,
                        'Expected valid version id but got: ' + str(version_id) + self.extra_data.get_all())
        self.extra_data.add_test_data('version id', version_id)

        self.assertEqual('PUT', request_type,
                         'Expected request type PUT but got: ' + str(request_type) + self.extra_data.get_all())

        self.assertTrue(len(upload_url) > 0,
                        'Expected non empty upload url but got: ' + str(upload_url) + self.extra_data.get_all())

        self.assertTrue(header_x_amz_date > 0,
                        'Expected valid date but got: ' + str(header_x_amz_date) + self.extra_data.get_all())

        self.assertEqual('authenticated-read', header_x_amz_acl,
                         'Expected x-amz-acl header: authenticated-read but got: ' + str(
                             header_x_amz_acl) + self.extra_data.get_all())

        self.assertTrue(len(header_authorization) > 0, 'Expected at least one authorization header but got: ' + str(
            header_authorization) + self.extra_data.get_all())

        self.assertEqual('application/octet-stream', headers_content_type,
                         'Expected content-type header: ' + str(headers_content_type) + ' but got: ' + str(
                             headers_content_type) + self.extra_data.get_all())

    def test_upload_file_to_s3_and_compress_dwg(self):
        file_name = 'LiveView_Clean.dwg'
        file_full_path = settings.BASE_DIR + '/rest_test/main_rest_tests/sharding/testfiles/' + file_name
        file_size = 64128
        compression_type = 1
        polling_timeout_in_seconds = 30
        delay_between_polls = 1

        self.upload_file_to_s3_and_compress(compression_type, delay_between_polls, file_full_path, file_name, file_size,
                                            polling_timeout_in_seconds)

    def test_upload_file_to_s3_and_compress_bmp(self):
        file_name = 'BMP-25.bmp'
        file_full_path = settings.BASE_DIR + '/rest_test/main_rest_tests/sharding/testfiles/' + file_name
        file_size = 264978
        compression_type = 4
        polling_timeout_in_seconds = 30
        delay_between_polls = 1

        self.upload_file_to_s3_and_compress(compression_type, delay_between_polls, file_full_path, file_name, file_size,
                                            polling_timeout_in_seconds)

    def test_upload_file_to_s3_and_compress_jpg(self):
        file_name = 'background.jpg'
        file_full_path = settings.BASE_DIR + '/rest_test/main_rest_tests/sharding/testfiles/' + file_name
        file_size = 87965
        compression_type = 4
        polling_timeout_in_seconds = 30
        delay_between_polls = 1

        self.upload_file_to_s3_and_compress(compression_type, delay_between_polls, file_full_path, file_name, file_size,
                                            polling_timeout_in_seconds)

    def test_upload_file_to_s3_and_compress_png(self):
        file_name = 'PngImage.png'
        file_full_path = settings.BASE_DIR + '/rest_test/main_rest_tests/sharding/testfiles/' + file_name
        file_size = 44454
        compression_type = 4
        polling_timeout_in_seconds = 30
        delay_between_polls = 1

        self.upload_file_to_s3_and_compress(compression_type, delay_between_polls, file_full_path, file_name, file_size,
                                            polling_timeout_in_seconds)

    def test_upload_file_to_s3_and_compress_gif(self):
        file_name = 'GifImage.gif'
        file_full_path = settings.BASE_DIR + '/rest_test/main_rest_tests/sharding/testfiles/' + file_name
        file_size = 42340
        compression_type = 4
        polling_timeout_in_seconds = 30
        delay_between_polls = 1

        self.upload_file_to_s3_and_compress(compression_type, delay_between_polls, file_full_path, file_name, file_size,
                                            polling_timeout_in_seconds)

    def test_upload_file_to_s3_and_compress_tif(self):
        file_name = 'TifImage.tif'
        file_full_path = settings.BASE_DIR + '/rest_test/main_rest_tests/sharding/testfiles/' + file_name
        file_size = 71189
        compression_type = 4
        polling_timeout_in_seconds = 30
        delay_between_polls = 1

        self.upload_file_to_s3_and_compress(compression_type, delay_between_polls, file_full_path, file_name, file_size,
                                            polling_timeout_in_seconds)

    # --- Currently sharding of font files is not working, un-comment when fixed ---
    # def test_upload_file_to_s3_and_compress_ttf(self):
    #     file_name = '47564.ttf'
    #     file_full_path = settings.BASE_DIR + '/rest_test/main_rest_tests/sharding/testfiles/' + file_name
    #     file_size = 16086
    #     compression_type = 5
    #     polling_timeout_in_seconds = 30
    #     delay_between_polls = 1
    #
    #     self.upload_file_to_s3_and_compress(compression_type, delay_between_polls, file_full_path, file_name, file_size,
    #                                         polling_timeout_in_seconds)

    def test_upload_file_to_s3_and_compress_pdf(self):
        file_name = 'LineTransparency.pdf'
        file_full_path = settings.BASE_DIR + '/rest_test/main_rest_tests/sharding/testfiles/' + file_name
        file_size = 59041
        compression_type = 11
        polling_timeout_in_seconds = 30
        delay_between_polls = 1

        self.upload_file_to_s3_and_compress(compression_type, delay_between_polls, file_full_path, file_name, file_size,
                                            polling_timeout_in_seconds)

    def test_upload_file_to_s3_and_compress_shx(self):
        file_name = 'mvt-mirym.shx'
        file_full_path = settings.BASE_DIR + '/rest_test/main_rest_tests/sharding/testfiles/' + file_name
        file_size = 27058
        compression_type = 5
        polling_timeout_in_seconds = 30
        delay_between_polls = 1

        self.upload_file_to_s3_and_compress(compression_type, delay_between_polls, file_full_path, file_name, file_size,
                                            polling_timeout_in_seconds)

    def upload_file_to_s3_and_compress(self, compression_type, delay_between_polls, file_full_path, file_name,
                                       file_size, polling_timeout_in_seconds):
        url_to_upload_response = self.files_management_client.get_url_to_upload_v1(auth=self.auth, folder_id=0,
                                                                                   file_name=file_name,
                                                                                   file_size=file_size)
        status_code = ClientUtils.get_response_status_code(url_to_upload_response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('get_url_to_upload response',
                                      ClientUtils.get_response_body(url_to_upload_response))
        version_id = ClientUtils.get_value_from_body(url_to_upload_response, FilesManagementClient.KEY_VERSION_ID)
        request_type = ClientUtils.get_value_from_body(url_to_upload_response, FilesManagementClient.KEY_REQUEST_TYPE)
        upload_url = ClientUtils.get_value_from_body(url_to_upload_response, FilesManagementClient.KEY_URL_TO_UPLOAD)
        header_x_amz_acl = ClientUtils.get_value_from_body(url_to_upload_response, json_path='headers.x-amz-acl')
        header_authorization = ClientUtils.get_value_from_body(url_to_upload_response,
                                                               json_path='headers.Authorization')
        header_content_type = ClientUtils.get_value_from_body(url_to_upload_response, json_path='headers.Content-Type')
        header_x_amz_date = ClientUtils.get_value_from_body(url_to_upload_response, json_path='headers.x-amz-date')
        self.extra_data.add_test_data('version id', version_id)
        self.extra_data.add_test_data('request type', request_type)
        self.extra_data.add_test_data('upload url', upload_url)
        self.extra_data.add_test_data('header x_amz_acl', header_x_amz_acl)
        self.extra_data.add_test_data('header authorization', header_authorization)
        self.extra_data.add_test_data('header content_type', header_content_type)
        self.extra_data.add_test_data('header x_amz_date', header_x_amz_date)

        upload_to_s3_response = self.s3_client.upload_to_s3(file_full_path=file_full_path, url_to_upload=upload_url,
                                                            method=request_type, acl=header_x_amz_acl,
                                                            auth=header_authorization,
                                                            date=header_x_amz_date, content_type=header_content_type)
        status_code = ClientUtils.get_response_status_code(upload_to_s3_response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())

        upload_to_compressor_response = self.files_management_client.upload_to_compressor(auth=self.auth,
                                                                                          version_id=version_id,
                                                                                          compression_type=compression_type)
        status_code = ClientUtils.get_response_status_code(upload_to_compressor_response)
        self.assertEqual(httplib.NO_CONTENT, status_code,
                         'Got status code: ' + str(status_code) + self.extra_data.get_all())

        successful_upload, msg = TestUtils.poll_for_upload(auth=self.auth, version_id=version_id,
                                                           sleep_period=delay_between_polls,
                                                           timeout_in_seconds=polling_timeout_in_seconds,
                                                           extra_data=self.extra_data)
        self.assertIsNotNone(successful_upload, msg + self.extra_data.get_all())

        return version_id

    def test_download_file(self):
        polling_timeout_in_seconds = 30
        delay_between_polls = 1

        file_system_entries, msg = TestUtils.get_internal_partition(auth=self.auth, extra_data=self.extra_data)
        self.assertIsNotNone(file_system_entries, msg + self.extra_data.get_all())
        entry = TestUtils.get_first_drawing_from_internal_file_system(file_system_entries)
        self.extra_data.add_test_data('entry', entry)

        version_id_to_download = TestUtils.get_entry_data_by_keys(entry, 'versionId')
        self.assertTrue(version_id_to_download > 0,
                        'Expected valid version id but got: ' + str(version_id_to_download) + self.extra_data.get_all())
        self.extra_data.add_test_data('version id to download', version_id_to_download)

        prepare_file_to_download_response = self.files_management_client.prepare_file_to_download(auth=self.auth,
                                                                                                  version_id=version_id_to_download)
        status_code = ClientUtils.get_response_status_code(prepare_file_to_download_response)
        self.assertEqual(httplib.ACCEPTED, status_code,
                         'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('prepare_file_to_download response',
                                      ClientUtils.get_response_body(prepare_file_to_download_response))

        download_id = ClientUtils.get_value_from_body(prepare_file_to_download_response,
                                                      FilesManagementClient.KEY_DOWNLOAD_ID)
        self.assertIsInstance(download_id, unicode, 'Expected unicode download id but got: ' + str(
            download_id) + self.extra_data.get_all())
        self.extra_data.add_test_data('download id', download_id)

        default_name, msg = TestUtils.poll_for_download(auth=self.auth, download_id=download_id,
                                                        sleep_period=delay_between_polls,
                                                        timeout_in_seconds=polling_timeout_in_seconds,
                                                        extra_data=self.extra_data)
        self.assertIsNotNone(default_name, msg + self.extra_data.get_all())

        download_response = self.files_management_client.download_file(auth=self.auth, download_id=download_id,
                                                                       download_file_name=default_name)
        status_code = ClientUtils.get_response_status_code(download_response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())

        downloaded_content = ClientUtils.get_response_raw_content(download_response)
        self.assertIsNotNone(downloaded_content, 'Expected non empty content download' + self.extra_data.get_all())

    def test_plot_and_send_to_mail(self):  # workflow for web-client plotting
        polling_timeout_in_seconds = 30
        delay_between_polls = 1
        send_to = settings.GMAIL_USER_NAME
        password = settings.GMAIL_PASSWORD

        file_system_entries, msg = TestUtils.get_internal_partition(auth=self.auth, extra_data=self.extra_data)
        self.assertIsNotNone(file_system_entries, msg + self.extra_data.get_all())
        entry = TestUtils.get_first_drawing_from_internal_file_system(file_system_entries)
        self.extra_data.add_test_data('entry', entry)

        version_id_to_plot = TestUtils.get_entry_data_by_keys(entry, 'versionId')
        self.assertTrue(version_id_to_plot > 0,
                        'Expected valid version id but got: ' + str(version_id_to_plot) + self.extra_data.get_all())
        self.extra_data.add_test_data('version id to plot', version_id_to_plot)

        plot_and_send_to_mail_response = self.files_management_client.plot_and_send_to_mail(auth=self.auth,
                                                                                            version_id=version_id_to_plot,
                                                                                            send_to=send_to)
        status_code = ClientUtils.get_response_status_code(plot_and_send_to_mail_response)
        self.assertEqual(httplib.ACCEPTED, status_code,
                         'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('plot_and_send_to_mail response',
                                      ClientUtils.get_response_body(plot_and_send_to_mail_response))

        download_id = ClientUtils.get_value_from_body(plot_and_send_to_mail_response,
                                                      FilesManagementClient.KEY_DOWNLOAD_ID)
        self.assertIsInstance(download_id, unicode,
                              'Expected unicode download id but got: ' + str(download_id) + self.extra_data.get_all())
        self.extra_data.add_test_data('download id', download_id)

        default_name, msg = TestUtils.poll_for_plot(auth=self.auth, version_id=download_id,
                                                    sleep_period=delay_between_polls,
                                                    timeout_in_seconds=polling_timeout_in_seconds,
                                                    extra_data=self.extra_data)

        self.assertIsNotNone(default_name, msg + self.extra_data.get_all())

        sleep(20)  # wait for email to be sent

        gmail_client = GmailClient()
        try:
            gmail_client.connect_to_account(send_to, password)
        except Exception as e:
            self.fail(
                'Could not connect to mail account ' + str(
                    send_to) + ' to verify mail was sent after plot. Exception msg: ' + str(
                    e.message) + '. Exception args: ' + str(e.args) + self.extra_data.get_all())
        self.assertTrue(gmail_client.open_label('INBOX'),
                        'Failed to open INBOX label in ' + str(send_to) + self.extra_data.get_all())
        expected_mail_subject = default_name + ' was sent to you by ' + self.first_name + ' ' + self.last_name
        self.extra_data.add_test_data('expected mail subject', expected_mail_subject)
        self.assertIsNotNone(gmail_client.search_mails_in_label(subject_to_search=expected_mail_subject),
                             'Could not find sent mail in ' + str(send_to) + ' INBOX' + self.extra_data.get_all())

    def test_plot_and_download(self):  # workflow for mobile-client plotting
        polling_timeout_in_seconds = 30
        delay_between_polls = 1

        file_system_entries, msg = TestUtils.get_internal_partition(auth=self.auth, extra_data=self.extra_data)
        self.assertIsNotNone(file_system_entries, msg + self.extra_data.get_all())
        entry = TestUtils.get_first_drawing_from_internal_file_system(file_system_entries)
        self.extra_data.add_test_data('entry', entry)

        version_id_to_plot = TestUtils.get_entry_data_by_keys(entry, 'versionId')
        self.assertTrue(version_id_to_plot > 0,
                        'Expected integer version id but got: ' + str(version_id_to_plot) + self.extra_data.get_all())
        self.extra_data.add_test_data('version id to plot', version_id_to_plot)

        prepare_file_to_plot_response = self.files_management_client.prepare_file_to_download(auth=self.auth,
                                                                                              version_id=version_id_to_plot,
                                                                                              format='plot')
        status_code = ClientUtils.get_response_status_code(prepare_file_to_plot_response)
        self.assertEqual(httplib.ACCEPTED, status_code,
                         'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('prepare_file_to_download response',
                                      ClientUtils.get_response_body(prepare_file_to_plot_response))

        download_id = ClientUtils.get_value_from_body(prepare_file_to_plot_response,
                                                      FilesManagementClient.KEY_DOWNLOAD_ID)
        self.assertIsInstance(download_id, unicode, 'Expected unicode download id but got: ' + str(
            download_id) + self.extra_data.get_all())
        self.extra_data.add_test_data('download id', download_id)

        default_name, msg = TestUtils.poll_for_download(auth=self.auth, download_id=download_id,
                                                        sleep_period=delay_between_polls,
                                                        timeout_in_seconds=polling_timeout_in_seconds,
                                                        extra_data=self.extra_data)
        self.assertIsNotNone(default_name, msg + self.extra_data.get_all())

        download_response = self.files_management_client.download_file(auth=self.auth, download_id=download_id,
                                                                       download_file_name=default_name)
        status_code = ClientUtils.get_response_status_code(download_response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())

        downloaded_content = ClientUtils.get_response_raw_content(download_response)
        self.assertIsNotNone(downloaded_content, 'Expected non empty content download' + self.extra_data.get_all())

    def test_get_xrefs_uploaded_as_zip(self):
        zip_file_name_without_extension = 'xref with block - Standard'
        zip_file_name = zip_file_name_without_extension + '.zip'
        zip_file_full_path = settings.BASE_DIR + '/rest_test/main_rest_tests/sharding/testfiles/' + zip_file_name
        zip_file_size = 108960

        file_name_with_xrefs = 'xref with block.dwg'
        file_xref_name = '\one block.dwg'

        compression_type = 8
        polling_timeout_in_seconds = 60
        delay_between_polls = 2

        self.upload_file_to_s3_and_compress(compression_type, delay_between_polls, zip_file_full_path, zip_file_name, zip_file_size,
                                            polling_timeout_in_seconds)

        # Must wait for all files in zip to upload. No better way, since urlToUpload resource returns only 1 version id
        sleep(20)

        root_file_system_entries, msg = TestUtils.get_internal_partition(auth=self.auth, extra_data=self.extra_data)
        self.assertIsNotNone(root_file_system_entries, msg + self.extra_data.get_all())

        xrefs_folder_version_id = None
        for entry in root_file_system_entries:
            if entry['name'] == zip_file_name_without_extension and entry['type'] == 'FOLDER':
                xrefs_folder_version_id = entry[PartitionClient.KEY_FOLDER_ID]  # created when zip was uploaded
                break
        self.assertIsNotNone(xrefs_folder_version_id, 'Expected a new folder created named ' + str(
            zip_file_name_without_extension) + self.extra_data.get_all())
        self.extra_data.add_test_data('xrefs folder version id', xrefs_folder_version_id)

        file_system_entries, msg = TestUtils.get_internal_partition(auth=self.auth,
                                                                    partition_folder_id=xrefs_folder_version_id,
                                                                    extra_data=self.extra_data)
        self.assertIsNotNone(file_system_entries, msg + self.extra_data.get_all())

        file_with_xrefs_version_id = None
        for entry in file_system_entries:
            if entry['name'] == file_name_with_xrefs and entry['type'] == 'DRAWING':
                file_with_xrefs_version_id = entry[PartitionClient.KEY_PRIMARY_VERSION_ID]
                break
        self.assertIsNotNone(file_with_xrefs_version_id, 'Expected the new file named ' + str(
            file_name_with_xrefs) + ' uploaded into folder' + self.extra_data.get_all())
        self.extra_data.add_test_data('file with xrefs version id', file_with_xrefs_version_id)

        xrefs_client = XrefsClient()
        get_xrefs_response = xrefs_client.get_all_xrefs(auth=self.auth, version_id=file_with_xrefs_version_id)
        status_code = ClientUtils.get_response_status_code(get_xrefs_response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())

        response_xrefs = ClientUtils.get_response_body(get_xrefs_response)
        self.assertIsNotNone(response_xrefs,
                             'Expected non empty get_all_xrefs response body' + self.extra_data.get_all())

        self.assertTrue(len(response_xrefs) > 0,
                        'Expected at least one xref, but got: ' + str(response_xrefs) + self.extra_data.get_all())
        self.extra_data.add_test_data('get_all_xrefs response', response_xrefs)

        for xref in response_xrefs:
            xref_name = xref['name']
            xref_is_missing = xref['missing']
            xref_type = xref['type']
            self.assertEqual(file_xref_name, xref_name,
                             'Expected xref name: ' + str(file_xref_name) + ' but got: ' + str(
                                 xref_name) + self.extra_data.get_all())
            self.assertFalse(xref_is_missing,
                             'Xref was uploaded to s3, should not be missing' + self.extra_data.get_all())
            self.assertIsNotNone(xref_type, 'Expected non empty xref type' + self.extra_data.get_all())

    def test_get_xrefs_all_missing(self):
        file_name = 'xref with block.dwg'
        file_full_path = settings.BASE_DIR + '/rest_test/main_rest_tests/sharding/testfiles/file_with_xref/' + file_name
        file_size = 64687
        file_xref_name = '\one block.dwg'

        compression_type = 1
        polling_timeout_in_seconds = 60
        delay_between_polls = 2

        version_id = self.upload_file_to_s3_and_compress(compression_type, delay_between_polls, file_full_path,
                                                         file_name, file_size,
                                                         polling_timeout_in_seconds)

        xrefs_client = XrefsClient()
        get_xrefs_response = xrefs_client.get_all_xrefs(auth=self.auth, version_id=version_id)
        status_code = ClientUtils.get_response_status_code(get_xrefs_response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())

        response_xrefs = ClientUtils.get_response_body(get_xrefs_response)
        self.assertIsNotNone(response_xrefs,
                             'Expected non empty get_all_xrefs response body' + self.extra_data.get_all())

        self.assertTrue(len(response_xrefs) > 0, 'Expected at least one xref, but got: ' + str(
            response_xrefs) + self.extra_data.get_all())
        self.extra_data.add_test_data('get_all_xrefs response', response_xrefs)

        for xref in response_xrefs:
            xref_name = xref['name']
            xref_is_missing = xref['missing']
            xref_type = xref['type']
            self.assertEqual(file_xref_name, xref_name,
                             'Expected xref name: ' + str(file_xref_name) + ' but got: ' + str(
                                 xref_name) + self.extra_data.get_all())
            self.assertTrue(xref_is_missing,
                            'Xref was not uploaded to s3, should be missing' + self.extra_data.get_all())
            self.assertIsNotNone(xref_type,
                                 'Expected non empty xref type' + self.extra_data.get_all())
