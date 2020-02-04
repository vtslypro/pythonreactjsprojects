__author__ = 'alonitzhaki'

import requests
from utils.headers import AdskCommonHeadersManager

from rest_test import app_settings as settings


class PollClient(object):
    KEY_NOTIFICATIONS = 'notifications'
    KEY_NOTIFICATION_ID = 'notificationId'
    KEY_NOTIFICATION_TYPE = 'type'
    KEY_NOTIFICATION_STATUS = 'status'

    def poll(self, auth, last_notification_id, event):
        url = settings.MAIN_SERVER_URI + '/main/wsResources/poll'

        headers = {AdskCommonHeadersManager.ADSK_AUTH_HEADER: auth, 'x-ads-device-type': settings.DEVICE_TYPE_HEADER}

        params = {}
        params.__setitem__('event', event)
        params.__setitem__('lastNotificationId', last_notification_id)

        try:
            return requests.get(url=url, headers=headers, params=params)
        except Exception as e:
            print(
                'PollClient.poll: params: ' + str(
                    params) + '. Exception msg: ' + str(e.message) + '. Exception args: ' + str(e.args) + '\n')
            return None
