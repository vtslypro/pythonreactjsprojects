__author__ = 'alonitzhaki'

import requests
from utils.headers import AdskCommonHeadersManager

from rest_test import app_settings as settings


class StorageClient(object):
    def download_file(self, auth, file_id, folder_id='@root', wait_for_response=False):
        url = settings.COMPRESSOR_SERVER_URI + '/main/storage/files/v1/folder/' + str(folder_id) + '/file/' + str(
            file_id)

        headers = {AdskCommonHeadersManager.ADSK_AUTH_HEADER: auth, 'x-ads-device-type': settings.DEVICE_TYPE_HEADER}

        params = {}
        params.__setitem__('waitForResponse', wait_for_response)

        try:
            return requests.get(url=url, headers=headers, params=params)
        except Exception as e:
            print('StorageClient.download_file: file id: ' + str(file_id) + '. folder id: ' + str(
                folder_id) + '. params: ' + str(params) + '. Exception msg: ' + str(
                e.message) + '. Exception args: ' + str(e.args) + '\n')
            return None
