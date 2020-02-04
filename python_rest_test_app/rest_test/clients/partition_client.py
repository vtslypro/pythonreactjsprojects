__author__ = 'alonitzhaki'

import requests
from utils.headers import AdskCommonHeadersManager

from rest_test import app_settings as settings


class PartitionClient(object):
    KEY_ROOT_PATH = 'rootPath'
    KEY_HAS_MORE = 'hasMore'
    KEY_FILE_SYSTEM_ENTRIES = 'fileSystemEntries'
    KEY_OWNER_ID = 'ownerId'
    KEY_ENTRY_NAME = 'name'
    KEY_PRIMARY_VERSION_ID = 'primaryVersionId'
    KEY_FOLDER_ID = 'folderId'
    KEY_TYPE = 'type'
    KEY_NITROUS_ID = 'nitrousId'

    PARAM_ID_TYPE = 'idType'
    PARAM_PATH = 'path'
    PARAM_OFFSET = 'offset'
    PARAM_LIMIT = 'limit'
    PARAM_WITH_SHARES = 'withShares'
    PARAM_SORT_DRAWINGS = 'sortDrawings'
    PARAM_ORDER = 'order'
    PARAM_LIKE_TERM = 'likeTerm'

    def get_partition_v2(self, auth, parent_folder_id=0, app_id=1, id_type='WSId', offset=0, limit=30,
                         with_shares=False,
                         sort_drawings=True, order='', like_term=''):

        url = settings.MAIN_SERVER_URI + '/main/wsResources/folders/v2/' + str(parent_folder_id) + '/partition'

        headers = {AdskCommonHeadersManager.ADSK_AUTH_HEADER: auth,
                   AdskCommonHeadersManager.ADSK_APP_ID_HEADER: app_id, 'x-ads-device-type': settings.DEVICE_TYPE_HEADER}

        params = {}
        params.__setitem__(self.PARAM_ID_TYPE, id_type)
        params.__setitem__(self.PARAM_OFFSET, offset)
        params.__setitem__(self.PARAM_LIMIT, limit)
        params.__setitem__(self.PARAM_WITH_SHARES, with_shares)
        params.__setitem__(self.PARAM_SORT_DRAWINGS, sort_drawings)
        params.__setitem__(self.PARAM_ORDER, order)
        params.__setitem__(self.PARAM_LIKE_TERM, like_term)

        try:
            return requests.get(url=url, headers=headers, params=params)
        except Exception as e:
            print(
                'PartitionClient.get_partition_v2: folder id: ' + str(parent_folder_id) + '. params: ' + str(
                    params) + '. Exception msg: ' + str(e.message) + '. Exception args: ' + str(e.args) + '\n')
            return None

    def get_partition(self, auth, parent_folder_id=0, app_id=1, id_type='WSId', offset=0, limit=30, order='',
                      like_term=''):

        url = settings.MAIN_SERVER_URI + '/main/wsResources/folders/' + str(parent_folder_id) + '/partition'

        headers = {AdskCommonHeadersManager.ADSK_AUTH_HEADER: auth,
                   AdskCommonHeadersManager.ADSK_APP_ID_HEADER: app_id, 'x-ads-device-type': settings.DEVICE_TYPE_HEADER}

        params = {}
        params.__setitem__(self.PARAM_ID_TYPE, id_type)
        params.__setitem__(self.PARAM_OFFSET, offset)
        params.__setitem__(self.PARAM_LIMIT, limit)
        params.__setitem__(self.PARAM_ORDER, order)
        params.__setitem__(self.PARAM_LIKE_TERM, like_term)

        try:
            return requests.get(url=url, headers=headers, params=params)
        except Exception as e:
            print('PartitionClient.get_partition: folder id: ' + str(parent_folder_id) + '. params: ' + str(
                params) + '. Exception msg: ' + str(e.message) + '. Exception args: ' + str(e.args) + '\n')
            return None

    def get_partition_path_v2(self, auth, app_id=1, path='', offset=0, limit=30, order='', like_term=''):

        url = settings.MAIN_SERVER_URI + '/main/wsResources/folders/v2/path/' + path + '/partition'

        headers = {AdskCommonHeadersManager.ADSK_AUTH_HEADER: auth,
                   AdskCommonHeadersManager.ADSK_APP_ID_HEADER: app_id, 'x-ads-device-type': settings.DEVICE_TYPE_HEADER}

        params = {}
        params.__setitem__(self.PARAM_OFFSET, offset)
        params.__setitem__(self.PARAM_LIMIT, limit)
        params.__setitem__(self.PARAM_ORDER, order)
        params.__setitem__(self.PARAM_LIKE_TERM, like_term)

        try:
            return requests.get(url=url, headers=headers, params=params)
        except Exception as e:
            print('PartitionClient.get_partition_path_v2: path: ' + str(path) + '. params: ' + str(
                params) + '. Exception msg: ' + str(e.message) + '. Exception args: ' + str(e.args) + '\n')
            return None

    def get_partition_path(self, auth, app_id=1, path='', offset=0, limit=30, order='', like_term=''):

        url = settings.MAIN_SERVER_URI + '/main/wsResources/folders/path/' + path + '/partition'

        headers = {AdskCommonHeadersManager.ADSK_AUTH_HEADER: auth,
                   AdskCommonHeadersManager.ADSK_APP_ID_HEADER: app_id, 'x-ads-device-type': settings.DEVICE_TYPE_HEADER}

        params = {}
        params.__setitem__(self.PARAM_OFFSET, offset)
        params.__setitem__(self.PARAM_LIMIT, limit)
        params.__setitem__(self.PARAM_ORDER, order)
        params.__setitem__(self.PARAM_LIKE_TERM, like_term)

        try:
            return requests.get(url=url, headers=headers, params=params)
        except Exception as e:
            print('PartitionClient.get_partition_path: path: ' + str(path) + '. params: ' + str(
                params) + '. Exception msg: ' + str(e.message) + '. Exception args: ' + str(e.args) + '\n')
            return None

    def get_external_partition_v2(self, auth, host_id, app_id=1, path='', offset=0, limit=30, with_shares=False,
                                  order=''):

        url = settings.MAIN_SERVER_URI + '/main/wsResources/folders/v2/external/' + str(host_id) + '/partition'

        headers = {AdskCommonHeadersManager.ADSK_AUTH_HEADER: auth,
                   AdskCommonHeadersManager.ADSK_APP_ID_HEADER: app_id, 'x-ads-device-type': settings.DEVICE_TYPE_HEADER}

        params = {}
        params.__setitem__(self.PARAM_PATH, path)
        params.__setitem__(self.PARAM_OFFSET, offset)
        params.__setitem__(self.PARAM_LIMIT, limit)
        params.__setitem__(self.PARAM_WITH_SHARES, with_shares)
        params.__setitem__(self.PARAM_ORDER, order)

        try:
            return requests.get(url=url, headers=headers, params=params)
        except Exception as e:
            print('PartitionClient.get_external_partition_v2: host_id: ' + str(host_id) + '. params: ' + str(
                params) + '. Exception msg: ' + str(e.message) + '. Exception args: ' + str(e.args) + '\n')
            return None

    def get_external_partition(self, auth, host_id, app_id=1, path='', offset=0, limit=30, order=''):

        url = settings.MAIN_SERVER_URI + '/main/wsResources/folders/external/' + str(
            host_id) + '/' + path + '/partition'

        headers = {AdskCommonHeadersManager.ADSK_AUTH_HEADER: auth,
                   AdskCommonHeadersManager.ADSK_APP_ID_HEADER: app_id, 'x-ads-device-type': settings.DEVICE_TYPE_HEADER}

        params = {}
        params.__setitem__(self.PARAM_OFFSET, offset)
        params.__setitem__(self.PARAM_LIMIT, limit)
        params.__setitem__(self.PARAM_ORDER, order)

        try:
            return requests.get(url=url, headers=headers, params=params)
        except Exception as e:
            print('PartitionClient.get_external_partition: host_id: ' + str(host_id) + '. path: ' + str(
                path) + '. params: ' + str(params) + '. Exception msg: ' + str(e.message) + '. Exception args: ' + str(
                e.args) + '\n')
            return None
