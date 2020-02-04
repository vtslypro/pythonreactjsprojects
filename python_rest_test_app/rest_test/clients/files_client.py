__author__ = 'alonitzhaki'
import json

import requests
from utils.headers import AdskCommonHeadersManager

from rest_test import app_settings as settings


class FilesManagementClient(object):
    KEY_NAME = 'name'
    KEY_VERSION_ID = 'versionId'
    KEY_PRIMARY_WS_ID = 'primaryWsId'
    KEY_USER_DRAWING_PREFERENCES = 'usersDrawingPreferences'
    KEY_USER = 'user'
    KEY_USER_NAME = 'username'
    KEY_DRAWINGS = 'drawings'
    KEY_TITLE = 'title'
    KEY_PRIMARY_VERSION_ID = 'primaryVersionId'
    KEY_TYPE = 'type'
    KEY_SIZE = 'size'
    KEY_PROVIDER = 'provider'
    KEY_ENTRIES = 'entries'
    KEY_DOWNLOAD_ID = 'downloadId'
    KEY_REQUEST_TYPE = 'requestType'
    KEY_URL_TO_UPLOAD = 'urlToUpload'
    KEY_DATE = 'date'
    KEY_POLLING_ID = 'pollingId'

    PARAM_TEMPLATE_NAME = 'templateName'
    PARAM_PARENT_FOLDER_ID = 'parentFolderId'
    PARAM_PARENT_FOLDER_ID_TYPE = 'parentFolderIdType'
    PARAM_NEW_DRAWING_NAME = 'newDrawingName'
    PARAM_ALLOW_DUPLICATES = 'allowDuplicates'
    PARAM_ID_TYPE = 'idType'
    PARAM_TO_FOLDER_ID = 'toFolderId'
    PARAM_RENAME_TO = 'renameTo'
    PARAM_COPY_SHARES = 'copyShares'
    PARAM_NAME = 'name'
    PARAM_EMAILS = 'emails'
    PARAM_MESSAGE = 'message'
    PARAM_CAN_EDIT = 'canEdit'
    PARAM_CAN_DOWNLOAD = 'canDownload'
    PARAM_CAN_SHARE = 'canShare'
    PARAM_SHARED_USER_ID = 'sharedUserId'
    PARAM_SHARED_USER_ID_TYPE = 'sharedUserIdType'
    PARAM_SRC_ID_TYPE = 'srcIdType'

    def create_file(self, auth, template_name='', parent_folder_id=0, parent_folder_id_type='WSId',
                    new_drawing_name='', allow_duplicates=False):
        url = settings.MAIN_SERVER_URI + '/main/wsResources/files/create'

        headers = {AdskCommonHeadersManager.ADSK_AUTH_HEADER: auth, 'x-ads-device-type': settings.DEVICE_TYPE_HEADER}

        params = {}
        params.__setitem__(self.PARAM_TEMPLATE_NAME, template_name)
        params.__setitem__(self.PARAM_PARENT_FOLDER_ID, parent_folder_id)
        params.__setitem__(self.PARAM_PARENT_FOLDER_ID_TYPE, parent_folder_id_type)
        params.__setitem__(self.PARAM_NEW_DRAWING_NAME, new_drawing_name)
        params.__setitem__(self.PARAM_ALLOW_DUPLICATES, allow_duplicates)

        try:
            return requests.put(url=url, headers=headers, params=params)
        except Exception as e:
            print('FilesManagementClient.create_file: params: ' + str(
                params) + '. Exception msg: ' + str(e.message) + '. Exception args: ' + str(e.args) + '\n')
            return None

    def create_file_v2(self, auth, template_name='', parent_folder_id=0, parent_folder_id_type='WSId',
                       new_drawing_name='', allow_duplicates=False):
        url = settings.MAIN_SERVER_URI + '/main/wsResources/files/v2/create'

        headers = {'Content-type': 'application/json', AdskCommonHeadersManager.ADSK_AUTH_HEADER: auth,
                   'x-ads-device-type': settings.DEVICE_TYPE_HEADER}

        body = {}
        body.__setitem__(self.PARAM_TEMPLATE_NAME, template_name)
        body.__setitem__(self.PARAM_PARENT_FOLDER_ID, parent_folder_id)
        body.__setitem__(self.PARAM_PARENT_FOLDER_ID_TYPE, parent_folder_id_type)
        body.__setitem__(self.PARAM_NEW_DRAWING_NAME, new_drawing_name)
        body.__setitem__(self.PARAM_ALLOW_DUPLICATES, allow_duplicates)

        try:
            return requests.put(url=url, headers=headers, data=json.dumps(body))
        except Exception as e:
            print('FilesManagementClient.create_file_v2: body: ' + str(
                body) + '. Exception msg: ' + str(e.message) + '. Exception args: ' + str(e.args) + '\n')
            return None

    def delete_file_internal(self, auth, file_id, id_type='WSId'):
        url = settings.MAIN_SERVER_URI + '/main/wsResources/files/' + str(file_id)

        headers = {AdskCommonHeadersManager.ADSK_AUTH_HEADER: auth, 'x-ads-device-type': settings.DEVICE_TYPE_HEADER}

        params = {}
        params.__setitem__(self.PARAM_ID_TYPE, id_type)

        try:
            return requests.delete(url=url, headers=headers, params=params)
        except Exception as e:
            print(
                'FilesManagementClient.delete_file_internal: file id: ' + str(file_id) + '. params: ' + str(
                    params) + '. Exception msg: ' + str(e.message) + '. Exception args: ' + str(e.args) + '\n')
            return None

    def copy_file_internal(self, auth, file_id, to_folder_id, id_type='WSId', rename_to='', copy_shares=False):
        url = settings.MAIN_SERVER_URI + '/main/wsResources/files/' + str(file_id) + '/copy'

        headers = {AdskCommonHeadersManager.ADSK_AUTH_HEADER: auth, 'x-ads-device-type': settings.DEVICE_TYPE_HEADER}

        params = {}
        params.__setitem__(self.PARAM_TO_FOLDER_ID, to_folder_id)
        params.__setitem__(self.PARAM_ID_TYPE, id_type)
        params.__setitem__(self.PARAM_RENAME_TO, rename_to)
        params.__setitem__(self.PARAM_COPY_SHARES, copy_shares)

        try:
            return requests.post(url=url, headers=headers, params=params)
        except Exception as e:
            print('FilesManagementClient.copy_file_internal: file id: ' + str(file_id) + '. params: ' + str(
                params) + '. Exception msg: ' + str(e.message) + '. Exception args: ' + str(e.args) + '\n')
            return None

    def copy_file_v2_internal(self, auth, file_id, to_folder_id, id_type='WSId', rename_to='', copy_shares=False):
        url = settings.MAIN_SERVER_URI + '/main/wsResources/files/v2/' + str(file_id) + '/copy'

        headers = {'Content-type': 'application/json', AdskCommonHeadersManager.ADSK_AUTH_HEADER: auth,
                   'x-ads-device-type': settings.DEVICE_TYPE_HEADER}

        body = {}
        body.__setitem__(self.PARAM_TO_FOLDER_ID, to_folder_id)
        body.__setitem__(self.PARAM_ID_TYPE, id_type)
        body.__setitem__(self.PARAM_RENAME_TO, rename_to)
        body.__setitem__(self.PARAM_COPY_SHARES, copy_shares)

        try:
            return requests.post(url=url, headers=headers, data=json.dumps(body))
        except Exception as e:
            print('FilesManagementClient.copy_file_v2_internal: file id: ' + str(file_id) + '. body: ' + str(
                body) + '. Exception msg: ' + str(e.message) + '. Exception args: ' + str(e.args) + '\n')
            return None

    def rename_file_internal(self, auth, file_id, name, id_type='WSId'):
        url = settings.MAIN_SERVER_URI + '/main/wsResources/files/' + str(file_id) + '/rename'

        headers = {AdskCommonHeadersManager.ADSK_AUTH_HEADER: auth, 'x-ads-device-type': settings.DEVICE_TYPE_HEADER}

        params = {}
        params.__setitem__(self.PARAM_NAME, name)
        params.__setitem__(self.PARAM_ID_TYPE, id_type)

        try:
            return requests.post(url=url, headers=headers, params=params)
        except Exception as e:
            print(
                'FilesManagementClient.rename_file_internal: file id: ' + str(file_id) + '. params: ' + str(
                    params) + '. Exception msg: ' + str(e.message) + '. Exception args: ' + str(e.args) + '\n')
            return None

    def rename_file_v2_internal(self, auth, file_id, name, id_type='WSId'):
        url = settings.MAIN_SERVER_URI + '/main/wsResources/files/v2/' + str(file_id) + '/rename'

        headers = {'Content-type': 'application/json', AdskCommonHeadersManager.ADSK_AUTH_HEADER: auth,
                   'x-ads-device-type': settings.DEVICE_TYPE_HEADER}

        body = {}
        body.__setitem__(self.PARAM_NAME, name)
        body.__setitem__(self.PARAM_ID_TYPE, id_type)

        try:
            return requests.post(url=url, headers=headers, data=json.dumps(body))
        except Exception as e:
            print(
                'FilesManagementClient.rename_file_v2_internal: file id: ' + str(file_id) + '. body: ' + str(
                    body) + '. Exception msg: ' + str(e.message) + '. Exception args: ' + str(e.args) + '\n')
            return None

    def move_file_internal(self, auth, file_id, to_folder_id, id_type='WSId', src_id_type='WSId', rename_to=''):
        url = settings.MAIN_SERVER_URI + '/main/wsResources/files/' + str(file_id) + '/move'

        headers = {AdskCommonHeadersManager.ADSK_AUTH_HEADER: auth, 'x-ads-device-type': settings.DEVICE_TYPE_HEADER}

        params = {}
        params.__setitem__(self.PARAM_TO_FOLDER_ID, to_folder_id)
        params.__setitem__(self.PARAM_ID_TYPE, id_type)
        params.__setitem__(self.PARAM_SRC_ID_TYPE, src_id_type)
        params.__setitem__(self.PARAM_RENAME_TO, rename_to)

        try:
            return requests.post(url=url, headers=headers, params=params)
        except Exception as e:
            print('FilesManagementClient.move_file_internal: file id: ' + str(file_id) + '. params: ' + str(
                params) + '. Exception msg: ' + str(e.message) + '. Exception args: ' + str(e.args) + '\n')
            return None

    def share_file(self, auth, file_id, emails, id_type='WSId', message='', can_edit=True, can_download=True,
                   can_share=True):
        url = settings.MAIN_SERVER_URI + '/main/wsResources/files/' + str(file_id) + '/share'

        headers = {AdskCommonHeadersManager.ADSK_AUTH_HEADER: auth, 'x-ads-device-type': settings.DEVICE_TYPE_HEADER}

        params = {}
        params.__setitem__('email', emails)
        params.__setitem__(self.PARAM_ID_TYPE, id_type)
        params.__setitem__(self.PARAM_MESSAGE, message)
        params.__setitem__(self.PARAM_CAN_EDIT, can_edit)
        params.__setitem__(self.PARAM_CAN_DOWNLOAD, can_download)
        params.__setitem__(self.PARAM_CAN_SHARE, can_share)

        try:
            return requests.put(url=url, headers=headers, params=params)
        except Exception as e:
            print('FilesManagementClient.share_file: file id: ' + str(file_id) + '. params: ' + str(
                params) + '. Exception msg: ' + str(e.message) + '. Exception args: ' + str(e.args) + '\n')
            return None

    def share_file_v2(self, auth, file_id, emails, id_type='WSId', message='', can_edit=True, can_download=True,
                      can_share=True):
        url = settings.MAIN_SERVER_URI + '/main/wsResources/files/v2/' + str(file_id) + '/share'

        headers = {'Content-type': 'application/json', AdskCommonHeadersManager.ADSK_AUTH_HEADER: auth,
                   'x-ads-device-type': settings.DEVICE_TYPE_HEADER}

        body = {}
        body.__setitem__(self.PARAM_EMAILS, emails)
        body.__setitem__(self.PARAM_ID_TYPE, id_type)
        body.__setitem__(self.PARAM_MESSAGE, message)
        body.__setitem__(self.PARAM_CAN_EDIT, can_edit)
        body.__setitem__(self.PARAM_CAN_DOWNLOAD, can_download)
        body.__setitem__(self.PARAM_CAN_SHARE, can_share)

        try:
            return requests.put(url=url, headers=headers, data=json.dumps(body))
        except Exception as e:
            print('FilesManagementClient.share_file_v2: file id: ' + str(file_id) + '. body: ' + str(
                body) + '. Exception msg: ' + str(e.message) + '. Exception args: ' + str(e.args) + '\n')
            return None

    def get_file_shares(self, auth, file_id, id_type='WSId'):
        url = settings.MAIN_SERVER_URI + '/main/wsResources/files/' + str(file_id) + '/share'

        headers = {AdskCommonHeadersManager.ADSK_AUTH_HEADER: auth, 'x-ads-device-type': settings.DEVICE_TYPE_HEADER}

        params = {}
        params.__setitem__(self.PARAM_ID_TYPE, id_type)

        try:
            return requests.get(url=url, headers=headers, params=params)
        except Exception as e:
            print('FilesManagementClient.get_file_shares: file id: ' + str(file_id) + '. params: ' + str(
                params) + '. Exception msg: ' + str(e.message) + '. Exception args: ' + str(e.args) + '\n')
            return None

    def delete_file_share(self, auth, file_id, user_id, file_id_type='WSId', user_id_type='WSId'):
        url = settings.MAIN_SERVER_URI + '/main/wsResources/files/' + str(file_id) + '/share'

        headers = {AdskCommonHeadersManager.ADSK_AUTH_HEADER: auth, 'x-ads-device-type': settings.DEVICE_TYPE_HEADER}

        params = {}
        params.__setitem__(self.PARAM_ID_TYPE, file_id_type)
        params.__setitem__(self.PARAM_SHARED_USER_ID, user_id)
        params.__setitem__(self.PARAM_SHARED_USER_ID_TYPE, user_id_type)

        try:
            return requests.delete(url=url, headers=headers, params=params)
        except Exception as e:
            print('FilesManagementClient.delete_file_share: file id: ' + str(file_id) + '. params: ' + str(
                params) + '. shared user id: ' + str(user_id) + '. Exception msg: ' + str(
                e.message) + '. Exception args: ' + str(e.args) + '\n')
            return None

    def recent_files(self, auth, limit=10, last_file_date=-1, page=1):
        url = settings.MAIN_SERVER_URI + '/main/wsResources/files/recent'
        headers = {AdskCommonHeadersManager.ADSK_AUTH_HEADER: auth, 'x-ads-device-type': settings.DEVICE_TYPE_HEADER}

        params = {}
        params.__setitem__('limit', limit)
        params.__setitem__('lastFileDate', last_file_date)
        params.__setitem__('page', page)

        try:
            return requests.get(url=url, headers=headers, params=params)
        except Exception as e:
            print(
                'FilesManagementClient.recent_files: Exception msg: ' + str(e.message) + '. Exception args: ' + str(
                    e.args) + '\n')
            return None

    def get_timeline(self, auth, file_id, file_id_type='WSId', limit=0):
        url = settings.MAIN_SERVER_URI + '/main/wsResources/files/' + str(file_id) + '/timeline'
        headers = {AdskCommonHeadersManager.ADSK_AUTH_HEADER: auth, 'x-ads-device-type': settings.DEVICE_TYPE_HEADER}

        params = {}
        params.__setitem__(self.PARAM_ID_TYPE, file_id_type)
        params.__setitem__('limit', limit)

        try:
            return requests.get(url=url, headers=headers, params=params)
        except Exception as e:
            print('FilesManagementClient.get_timeline: file id: ' + str(file_id) + '. params: ' + str(
                params) + '. Exception msg: ' + str(e.message) + '. Exception args: ' + str(e.args) + '\n')
            return None

    def put_timeline_manual(self, auth, file_id, title, file_id_type='WSId'):
        url = settings.MAIN_SERVER_URI + '/main/wsResources/files/' + str(file_id) + '/timeline/manual'

        headers = {AdskCommonHeadersManager.ADSK_AUTH_HEADER: auth, 'x-ads-device-type': settings.DEVICE_TYPE_HEADER}

        params = {}
        params.__setitem__(self.PARAM_ID_TYPE, file_id_type)
        params.__setitem__('title', title)

        try:
            return requests.put(url=url, headers=headers, params=params)
        except Exception as e:
            print('FilesManagementClient.put_timeline_manual: file id: ' + str(file_id) + '. params: ' + str(
                params) + '. Exception msg: ' + str(e.message) + '. Exception args: ' + str(e.args) + '\n')
            return None

    def get_drawing_preferences(self, auth, file_id, file_id_type='WSId'):
        url = settings.MAIN_SERVER_URI + '/main/wsResources/files/' + str(file_id) + '/preferencesV2'

        headers = {AdskCommonHeadersManager.ADSK_AUTH_HEADER: auth, 'x-ads-device-type': settings.DEVICE_TYPE_HEADER}

        params = {}
        params.__setitem__(self.PARAM_ID_TYPE, file_id_type)

        try:
            return requests.get(url=url, headers=headers, params=params)
        except Exception as e:
            print(
                'FilesManagementClient.get_drawing_preferences: file id: ' + str(file_id) + '. params: ' + str(
                    params) + '. Exception msg: ' + str(e.message) + '. Exception args: ' + str(e.args) + '\n')
            return None

    def post_drawing_preferences(self, auth, file_id, file_id_type='WSId', user_specific_drawing_preferences={},
                                 shared_drawing_preferences={}):
        url = settings.MAIN_SERVER_URI + '/main/wsResources/files/' + str(file_id) + '/preferencesV2'

        headers = {'Content-type': 'application/json', AdskCommonHeadersManager.ADSK_AUTH_HEADER: auth,
                   'x-ads-device-type': settings.DEVICE_TYPE_HEADER}

        params = {}
        params.__setitem__(self.PARAM_ID_TYPE, file_id_type)

        body = {}
        body.__setitem__('userSpecificDrawingPreferences', user_specific_drawing_preferences)
        body.__setitem__('sharedDrawingPreferences', shared_drawing_preferences)

        try:
            return requests.post(url=url, headers=headers, params=params, data=json.dumps(body))
        except Exception as e:
            print(
                'FilesManagementClient.post_drawing_preferences: file id: ' + str(file_id) + '. params: ' + str(
                    params) + '. body: ' + str(body) + '. Exception msg: ' + str(
                    e.message) + '. Exception args: ' + str(e.args) + '\n')
            return None

    def get_url_to_upload_v1(self, auth, folder_id, file_name, file_size, version_id=0, app_id=1,
                             mobile_app_version=24):
        url = settings.MAIN_SERVER_URI + '/main/wsResources/files/urlToUpload'

        headers = {AdskCommonHeadersManager.ADSK_AUTH_HEADER: auth, AdskCommonHeadersManager.ADSK_APP_ID_HEADER: app_id,
                   'mobileAppVersion': mobile_app_version, 'x-ads-device-type': settings.DEVICE_TYPE_HEADER}

        params = {}
        params.__setitem__('folderId', folder_id)
        params.__setitem__('fileName', file_name)
        params.__setitem__('fileSize', file_size)
        params.__setitem__('versionId', version_id)

        try:
            return requests.get(url=url, headers=headers, params=params)
        except Exception as e:
            print('FilesManagementClient.get_url_to_upload_v1: params: ' + str(
                params) + '. Exception msg: ' + str(e.message) + '. Exception args: ' + str(e.args) + '\n')
            return None

    def get_url_to_upload_v2(self, auth, folder_id, file_name, file_size, version_id=0, app_id=1,
                             mobile_app_version=24):
        url = settings.MAIN_SERVER_URI + '/main/wsResources/files/v2/urlToUpload'

        headers = {AdskCommonHeadersManager.ADSK_AUTH_HEADER: auth, AdskCommonHeadersManager.ADSK_APP_ID_HEADER: app_id,
                   'mobileAppVersion': mobile_app_version, 'x-ads-device-type': settings.DEVICE_TYPE_HEADER}

        params = {}
        params.__setitem__('folderId', folder_id)
        params.__setitem__('fileName', file_name)
        params.__setitem__('fileSize', file_size)
        params.__setitem__('versionId', version_id)

        try:
            return requests.get(url=url, headers=headers, params=params)
        except Exception as e:
            print('FilesManagementClient.get_url_to_upload_v2: params: ' + str(
                params) + '. Exception msg: ' + str(e.message) + '. Exception args: ' + str(e.args) + '\n')
            return None

    def get_url_to_upload_v3(self, auth, folder_id, file_name, file_size, version_id=0, app_id=1,
                             mobile_app_version=24):
        url = settings.MAIN_SERVER_URI + '/main/wsResources/files/v3/urlToUpload'

        headers = {AdskCommonHeadersManager.ADSK_AUTH_HEADER: auth, AdskCommonHeadersManager.ADSK_APP_ID_HEADER: app_id,
                   'mobileAppVersion': mobile_app_version, 'x-ads-device-type': settings.DEVICE_TYPE_HEADER}

        params = {}
        params.__setitem__('folderId', folder_id)
        params.__setitem__('fileName', file_name)
        params.__setitem__('fileSize', file_size)
        params.__setitem__('versionId', version_id)

        try:
            return requests.get(url=url, headers=headers, params=params)
        except Exception as e:
            print('FilesManagementClient.get_url_to_upload_v3: params: ' + str(
                params) + '. Exception msg: ' + str(e.message) + '. Exception args: ' + str(e.args) + '\n')
            return None

    def upload_to_compressor(self, auth, version_id, compression_type):
        url = settings.COMPRESSOR_SERVER_URI + '/main/wsResources/files/upload'

        headers = {AdskCommonHeadersManager.ADSK_AUTH_HEADER: auth, 'x-ads-device-type': settings.DEVICE_TYPE_HEADER}

        params = {}
        params.__setitem__('versionId', version_id)
        params.__setitem__('compressionType', compression_type)

        try:
            return requests.post(url=url, headers=headers, params=params)
        except Exception as e:
            print('FilesManagementClient.upload_to_compressor: params: ' + str(
                params) + '. Exception msg: ' + str(e.message) + '. Exception args: ' + str(e.args) + '\n')
            return None

    def prepare_file_to_download(self, auth, version_id, format='dwg'):
        url = settings.COMPRESSOR_SERVER_URI + '/main/wsResources/files/prepareFileForDownload'

        headers = {'Content-type': 'application/json', AdskCommonHeadersManager.ADSK_AUTH_HEADER: auth,
                   'x-ads-device-type': settings.DEVICE_TYPE_HEADER}

        body = {}
        body.__setitem__('versionId', version_id)
        body.__setitem__('format', format)

        try:
            return requests.post(url=url, headers=headers, data=json.dumps(body))
        except Exception as e:
            print('FilesManagementClient.prepare_file_to_download: body: ' + str(
                body) + '. Exception msg: ' + str(e.message) + '. Exception args: ' + str(e.args) + '\n')
            return None

    def plot_and_send_to_mail(self, auth, version_id, send_to, message='', format='send'):
        url = settings.PLOT_SERVER_URI + '/main/wsResources/files/plotAndSendToMail'

        headers = {'Content-type': 'application/json', AdskCommonHeadersManager.ADSK_AUTH_HEADER: auth,
                   'x-ads-device-type': settings.DEVICE_TYPE_HEADER}

        body = {}
        body.__setitem__('versionId', version_id)
        body.__setitem__('sendTo', send_to)
        body.__setitem__('message', message)
        body.__setitem__('format', format)

        try:
            return requests.post(url=url, headers=headers, data=json.dumps(body))
        except Exception as e:
            print('FilesManagementClient.plot_and_send_to_mail: body: ' + str(
                body) + '. Exception msg: ' + str(e.message) + '. Exception args: ' + str(e.args) + '\n')
            return None

    def download_file(self, auth, download_id, download_file_name):
        url = settings.MAIN_SERVER_URI + '/main/wsResources/files/download'

        headers = {AdskCommonHeadersManager.ADSK_AUTH_HEADER: auth, 'x-ads-device-type': settings.DEVICE_TYPE_HEADER}

        params = {}
        params.__setitem__('newName', download_file_name)
        params.__setitem__('downloadId', download_id)

        try:
            return requests.get(url=url, headers=headers, params=params, stream=True)
        except Exception as e:
            print('FilesManagementClient.download_file: params: ' + str(
                params) + '. Exception msg: ' + str(e.message) + '. Exception args: ' + str(e.args) + '\n')
            return None

    def get_external_file_info_v2(self, auth, host_id, path):
        url = settings.MAIN_SERVER_URI + '/main/wsResources/files/v2/external/' + str(host_id)

        headers = {AdskCommonHeadersManager.ADSK_AUTH_HEADER: auth, 'x-ads-device-type': settings.DEVICE_TYPE_HEADER}

        params = {'path': path}

        try:
            return requests.get(url=url, headers=headers, params=params)
        except Exception as e:
            print(
                'FilesManagementClient.get_external_file_info_v2: host id: ' + str(host_id) + '. params: ' + str(
                    params) + '. Exception msg: ' + str(e.message) + '. Exception args: ' + str(e.args) + '\n')
            return None

    def get_external_file_info(self, auth, host_id, path):
        url = settings.MAIN_SERVER_URI + '/main/wsResources/files/external/' + str(host_id) + '/' + path

        headers = {AdskCommonHeadersManager.ADSK_AUTH_HEADER: auth, 'x-ads-device-type': settings.DEVICE_TYPE_HEADER}

        try:
            return requests.get(url=url, headers=headers)
        except Exception as e:
            print(
                'FilesManagementClient.get_external_file_info: Exception msg: ' + str(
                    e.message) + '. Exception args: ' + str(e.args) + '\n')
            return None

    def get_external_file_provider_v2(self, auth, host_id, path):
        url = settings.MAIN_SERVER_URI + '/main/wsResources/files/v2/external/' + str(host_id) + '/provider'

        headers = {AdskCommonHeadersManager.ADSK_AUTH_HEADER: auth, 'x-ads-device-type': settings.DEVICE_TYPE_HEADER}

        params = {'path': path}

        try:
            return requests.get(url=url, headers=headers, params=params)
        except Exception as e:
            print(
                'FilesManagementClient.get_external_file_provider_v2: host id: ' + str(host_id) + '. params: ' + str(
                    params) + '. Exception msg: ' + str(e.message) + '. Exception args: ' + str(e.args) + '\n')
            return None

    def move_internal_file_to_external(self, auth, file_id, to_host_id, to_path='', rename_to='', id_type='WSId'):
        url = settings.MAIN_SERVER_URI + '/main/wsResources/files/' + str(file_id) + '/moveToExternal'

        headers = {'Content-type': 'application/json', AdskCommonHeadersManager.ADSK_AUTH_HEADER: auth,
                   'x-ads-device-type': settings.DEVICE_TYPE_HEADER}

        params = {}
        params.__setitem__('toHostId', to_host_id)
        params.__setitem__('toPath', to_path)
        params.__setitem__('renameTo', rename_to)
        params.__setitem__('idType', id_type)

        try:
            return requests.post(url=url, headers=headers, params=params)
        except Exception as e:
            print(
                'FilesManagementClient.move_internal_file_to_external: file id: ' + str(file_id) + '. params: ' + str(
                    params) + '. Exception msg: ' + str(e.message) + '. Exception args: ' + str(e.args) + '\n')
            return None

    def rename_external_file_v2(self, auth, host_id, name, path='', id_type='WSId'):
        url = settings.MAIN_SERVER_URI + '/main/wsResources/files/v2/external/' + str(host_id) + '/rename'

        headers = {'Content-type': 'application/json', AdskCommonHeadersManager.ADSK_AUTH_HEADER: auth,
                   'x-ads-device-type': settings.DEVICE_TYPE_HEADER}

        body = {}
        body.__setitem__('path', path)
        body.__setitem__('name', name)
        body.__setitem__('idType', id_type)

        try:
            return requests.post(url=url, headers=headers, data=json.dumps(body))
        except Exception as e:
            print(
                'FilesManagementClient.rename_external_file_v2: host id: ' + str(host_id) + '. body: ' + str(
                    body) + '. Exception msg: ' + str(e.message) + '. Exception args: ' + str(e.args) + '\n')
            return None

    def delete_external_file_v2(self, auth, host_id, path):
        url = settings.MAIN_SERVER_URI + '/main/wsResources/files/v2/external/' + str(host_id)

        headers = {'Content-type': 'application/json', AdskCommonHeadersManager.ADSK_AUTH_HEADER: auth,
                   'x-ads-device-type': settings.DEVICE_TYPE_HEADER}

        params = {}
        params.__setitem__('path', path)

        try:
            return requests.delete(url=url, headers=headers, params=params)
        except Exception as e:
            print(
                'FilesManagementClient.delete_external_file_v2: host id: ' + str(host_id) + '. params: ' + str(
                    params) + '. Exception msg: ' + str(e.message) + '. Exception args: ' + str(e.args) + '\n')
            return None
