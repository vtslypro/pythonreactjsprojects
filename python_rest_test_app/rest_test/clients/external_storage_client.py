__author__ = 'alonitzhaki'
import json

import requests
from utils.headers import AdskCommonHeadersManager

from rest_test import app_settings as settings


class ExternalStorageClient(object):
    KEY_HOST_ID = 'hostId'

    PARAM_FOLDER_NAME = 'foldername'
    PARAM_URL = 'url'
    PARAM_USER_NAME = 'username'
    PARAM_PASSWORD = 'password'

    def webdav_connect_to_external_storage(self, auth, folder_name, service_url, user_name, password):
        url = settings.MAIN_SERVER_URI + '/main/wsResources/externalStorage/webdav'

        headers = {'Content-type': 'application/json', AdskCommonHeadersManager.ADSK_AUTH_HEADER: auth,
                   'x-ads-device-type': settings.DEVICE_TYPE_HEADER}

        body = {}
        body.__setitem__(self.PARAM_FOLDER_NAME, folder_name)
        body.__setitem__(self.PARAM_URL, service_url)
        body.__setitem__(self.PARAM_USER_NAME, user_name)
        body.__setitem__(self.PARAM_PASSWORD, password)

        try:
            return requests.post(url=url, headers=headers, data=json.dumps(body))
        except Exception as e:
            print(
                'ExternalStorageClient.webdav_connect_to_external_storage: Exception msg: ' + str(
                    e.message) + '. Exception args: ' + str(
                    e.args) + '\n')
            return None

    def webdav_active_hosts(self, auth):
        url = settings.MAIN_SERVER_URI + '/main/wsResources/externalStorage/webdav/activeHosts'

        headers = {AdskCommonHeadersManager.ADSK_AUTH_HEADER: auth, 'x-ads-device-type': settings.DEVICE_TYPE_HEADER}

        try:
            return requests.get(url=url, headers=headers)
        except Exception as e:
            print(
                'ExternalStorageClient.webdav_active_hosts: Exception msg: ' + str(
                    e.message) + '. Exception args: ' + str(
                    e.args) + '\n')
            return None
