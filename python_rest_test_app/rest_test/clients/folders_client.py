__author__ = 'alonitzhaki'
import json

import requests
from utils.headers import AdskCommonHeadersManager

from rest_test import app_settings as settings


class FoldersManagementClient(object):
    KEY_FOLDER_ID = 'folderId'
    KEY_USER_DRAWING_PREFERENCES = 'usersDrawingPreferences'
    KEY_USER = 'user'
    KEY_USER_NAME = 'username'

    PARAM_NEW_FOLDER_NAME = 'newFolderName'
    PARAM_PARENT_FOLDER_ID = 'parentFolderId'
    PARAM_PARENT_FOLDER_ID_TYPE = 'parentFolderIdType'
    PARAM_ID_TYPE = 'idType'
    PARAM_NAME = 'name'
    PARAM_EMAILS = 'email'
    PARAM_MESSAGE = 'message'
    PARAM_CAN_EDIT = 'canEdit'
    PARAM_CAN_DOWNLOAD = 'canDownload'
    PARAM_CAN_SHARE = 'canShare'
    PARAM_SHARED_USER_ID = 'sharedUserId'
    PARAM_SHARED_USER_ID_TYPE = 'sharedUserIdType'
    PARAM_PATH = 'path'

    def create_folder(self, auth, new_folder_name, parent_folder_id=0, parent_folder_id_type='WSId'):
        url = settings.MAIN_SERVER_URI + '/main/wsResources/folders/create'

        headers = {AdskCommonHeadersManager.ADSK_AUTH_HEADER: auth, 'x-ads-device-type': settings.DEVICE_TYPE_HEADER}

        params = {}
        params.__setitem__(self.PARAM_NEW_FOLDER_NAME, new_folder_name)
        params.__setitem__(self.PARAM_PARENT_FOLDER_ID, parent_folder_id)
        params.__setitem__(self.PARAM_PARENT_FOLDER_ID_TYPE, parent_folder_id_type)

        try:
            return requests.put(url=url, headers=headers, params=params)
        except Exception as e:
            print('FoldersManagementClient.create_folder: params: ' + str(
                params) + '. Exception msg: ' + str(e.message) + '. Exception args: ' + str(e.args) + '\n')
            return None

    def create_folder_v2(self, auth, new_folder_name, parent_folder_id=0, parent_folder_id_type='WSId'):
        url = settings.MAIN_SERVER_URI + '/main/wsResources/folders/v2/create'

        headers = {'Content-type': 'application/json', AdskCommonHeadersManager.ADSK_AUTH_HEADER: auth,
                   'x-ads-device-type': settings.DEVICE_TYPE_HEADER}

        body = {}
        body.__setitem__(self.PARAM_NEW_FOLDER_NAME, new_folder_name)
        body.__setitem__(self.PARAM_PARENT_FOLDER_ID, parent_folder_id)
        body.__setitem__(self.PARAM_PARENT_FOLDER_ID_TYPE, parent_folder_id_type)

        try:
            return requests.put(url=url, headers=headers, data=json.dumps(body))
        except Exception as e:
            print('FoldersManagementClient.create_folder_v2: body: ' + str(
                body) + '. Exception msg: ' + str(e.message) + '. Exception args: ' + str(e.args) + '\n')
            return None

    def delete_folder(self, auth, folder_id, id_type='WSId'):
        url = settings.MAIN_SERVER_URI + '/main/wsResources/folders/' + str(folder_id)

        headers = {AdskCommonHeadersManager.ADSK_AUTH_HEADER: auth, 'x-ads-device-type': settings.DEVICE_TYPE_HEADER}

        params = {}
        params.__setitem__(self.PARAM_ID_TYPE, id_type)

        try:
            return requests.delete(url=url, headers=headers, params=params)
        except Exception as e:
            print('FoldersManagementClient.delete_folder: folder id: ' + str(folder_id) + '. params: ' + str(
                params) + '. Exception msg: ' + str(e.message) + '. Exception args: ' + str(e.args) + '\n')
            return None

    def rename_folder(self, auth, folder_id, name, id_type='WSId'):
        url = settings.MAIN_SERVER_URI + '/main/wsResources/folders/' + str(folder_id) + '/rename'

        headers = {AdskCommonHeadersManager.ADSK_AUTH_HEADER: auth, 'x-ads-device-type': settings.DEVICE_TYPE_HEADER}

        params = {}
        params.__setitem__(self.PARAM_NAME, name)
        params.__setitem__(self.PARAM_ID_TYPE, id_type)

        try:
            return requests.post(url=url, headers=headers, params=params)
        except Exception as e:
            print('FoldersManagementClient.rename_folder: folder id: ' + str(folder_id) + '. params: ' + str(
                params) + '. Exception msg: ' + str(e.message) + '. Exception args: ' + str(e.args) + '\n')
            return None

    def rename_folder_v2(self, auth, folder_id, name, id_type='WSId'):
        url = settings.MAIN_SERVER_URI + '/main/wsResources/folders/v2/' + str(folder_id) + '/rename'

        headers = {'Content-type': 'application/json', AdskCommonHeadersManager.ADSK_AUTH_HEADER: auth,
                   'x-ads-device-type': settings.DEVICE_TYPE_HEADER}

        body = {}
        body.__setitem__(self.PARAM_NAME, name)
        body.__setitem__(self.PARAM_ID_TYPE, id_type)

        try:
            return requests.post(url=url, headers=headers, data=json.dumps(body))
        except Exception as e:
            print(
                'FoldersManagementClient.rename_folder_v2: folder id: ' + str(folder_id) + '. body: ' + str(
                    body) + '. Exception msg: ' + str(e.message) + '. Exception args: ' + str(e.args) + '\n')
            return None

    def share_folder(self, auth, folder_id, emails, id_type='WSId', message='', can_edit=True, can_download=True,
                     can_share=True):
        url = settings.MAIN_SERVER_URI + '/main/wsResources/folders/' + str(folder_id) + '/share'

        headers = {AdskCommonHeadersManager.ADSK_AUTH_HEADER: auth, 'x-ads-device-type': settings.DEVICE_TYPE_HEADER}

        params = {}
        params.__setitem__(self.PARAM_EMAILS, emails)
        params.__setitem__(self.PARAM_ID_TYPE, id_type)
        params.__setitem__(self.PARAM_MESSAGE, message)
        params.__setitem__(self.PARAM_CAN_EDIT, can_edit)
        params.__setitem__(self.PARAM_CAN_DOWNLOAD, can_download)
        params.__setitem__(self.PARAM_CAN_SHARE, can_share)

        try:
            return requests.put(url=url, headers=headers, params=params)
        except Exception as e:
            print('FoldersManagementClient.share_folder: folder id: ' + str(folder_id) + '. params: ' + str(
                params) + '. Exception msg: ' + str(e.message) + '. Exception args: ' + str(e.args) + '\n')
            return None

    def get_folder_shares(self, auth, folder_id, id_type='WSId'):
        url = settings.MAIN_SERVER_URI + '/main/wsResources/folders/' + str(folder_id) + '/share'

        headers = {AdskCommonHeadersManager.ADSK_AUTH_HEADER: auth, 'x-ads-device-type': settings.DEVICE_TYPE_HEADER}

        params = {}
        params.__setitem__(self.PARAM_ID_TYPE, id_type)

        try:
            return requests.get(url=url, headers=headers, params=params)
        except Exception as e:
            print(
                'FoldersManagementClient.get_folder_shares: folder id: ' + str(folder_id) + '. params: ' + str(
                    params) + '. Exception msg: ' + str(e.message) + '. Exception args: ' + str(e.args) + '\n')
            return None

    def delete_folder_share(self, auth, folder_id, user_id, folder_id_type='WSId', user_id_type='WSId'):
        url = settings.MAIN_SERVER_URI + '/main/wsResources/folders/' + str(folder_id) + '/share'

        headers = {AdskCommonHeadersManager.ADSK_AUTH_HEADER: auth, 'x-ads-device-type': settings.DEVICE_TYPE_HEADER}

        params = {}
        params.__setitem__(self.PARAM_ID_TYPE, folder_id_type)
        params.__setitem__(self.PARAM_SHARED_USER_ID, user_id)
        params.__setitem__(self.PARAM_SHARED_USER_ID_TYPE, user_id_type)

        try:
            return requests.delete(url=url, headers=headers, params=params)
        except Exception as e:
            print(
                'FoldersManagementClient.delete_folder_share: folder id: ' + str(folder_id) + '. params: ' + str(
                    params) + '. Exception msg: ' + str(e.message) + '. Exception args: ' + str(e.args) + '\n')
            return None

    def delete_external_folder_v2(self, auth, host_id, path):
        url = settings.MAIN_SERVER_URI + '/main/wsResources/folders/v2/external/' + str(host_id)

        headers = {'Content-type': 'application/json', AdskCommonHeadersManager.ADSK_AUTH_HEADER: auth,
                   'x-ads-device-type': settings.DEVICE_TYPE_HEADER}

        params = {}
        params.__setitem__(self.PARAM_PATH, path)

        try:
            return requests.delete(url=url, headers=headers, params=params)
        except Exception as e:
            print(
                'FoldersManagementClient.delete_external_folder_v2: host id: ' + str(host_id) + '. params: ' + str(
                    params) + '. Exception msg: ' + str(e.message) + '. Exception args: ' + str(e.args) + '\n')
            return None

    def delete_external_folder(self, auth, host_id, path):
        url = settings.MAIN_SERVER_URI + '/main/wsResources/folders/external/' + str(host_id) + '/' + path

        headers = {AdskCommonHeadersManager.ADSK_AUTH_HEADER: auth, 'x-ads-device-type': settings.DEVICE_TYPE_HEADER}

        try:
            return requests.delete(url=url, headers=headers)
        except Exception as e:
            print('FoldersManagementClient.delete_external_folder: host id: ' + str(
                host_id) + '. Exception msg: ' + str(e.message) + '. Exception args: ' + str(e.args) + '\n')
            return None

    def create_external_folder_v2(self, auth, host_id, new_folder_name, folder_path, parent_folder_id=0,
                                  parent_folder_id_type='wsId'):
        url = settings.MAIN_SERVER_URI + '/main/wsResources/folders/v2/external/' + str(host_id) + '/create'

        headers = {'Content-type': 'application/json', AdskCommonHeadersManager.ADSK_AUTH_HEADER: auth,
                   'x-ads-device-type': settings.DEVICE_TYPE_HEADER}

        body = {}
        body.__setitem__('folderPath', folder_path)
        body.__setitem__(self.PARAM_NEW_FOLDER_NAME, new_folder_name)
        body.__setitem__(self.PARAM_PARENT_FOLDER_ID, parent_folder_id)
        body.__setitem__(self.PARAM_PARENT_FOLDER_ID_TYPE, parent_folder_id_type)

        try:
            return requests.put(url=url, headers=headers, data=json.dumps(body))
        except Exception as e:
            print(
                'FoldersManagementClient.create_external_folder_v2: host id: ' + str(host_id) + '. body: ' + str(
                    body) + '. Exception msg: ' + str(e.message) + '. Exception args: ' + str(e.args) + '\n')
            return None

    def rename_external_folder_v2(self, auth, host_id, path, name):
        url = settings.MAIN_SERVER_URI + '/main/wsResources/folders/v2/external/' + str(host_id) + '/rename'

        headers = {'Content-type': 'application/json', AdskCommonHeadersManager.ADSK_AUTH_HEADER: auth,
                   'x-ads-device-type': settings.DEVICE_TYPE_HEADER}

        body = {}
        body.__setitem__(self.PARAM_PATH, path)
        body.__setitem__(self.PARAM_NAME, name)

        try:
            return requests.post(url=url, headers=headers, data=json.dumps(body))
        except Exception as e:
            print(
                'FoldersManagementClient.rename_external_folder_v2: host id: ' + str(host_id) + '. body: ' + str(
                    body) + '. Exception msg: ' + str(e.message) + '. Exception args: ' + str(e.args) + '\n')
            return None
