__author__ = 'alonitzhaki'
import json

import requests

from rest_test import app_settings as settings


class RegisterClient(object):
    KEY_MAIL = 'mail'
    KEY_EIDM_USER_ID = 'eidmUserId'
    KEY_EIDM_USER_NAME = 'eidmUsername'

    PARAM_EMAIL = 'email'
    PARAM_PASSWORD = 'password'
    PARAM_FIRST_NAME = 'firstName'
    PARAM_LAST_NAME = 'lastName'
    PARAM_FEEDBACK = 'feedback'
    PARAM_LOCALE = 'locale'
    PARAM_UI_PREFS_VERSION = 'uiPrefsVersion'
    PARAM_MOBILE_APP_VERSION = 'mobileAppVersion'

    def register_v1(self, user_name, password, first_name, last_name, feedback=True, locale='en', ui_prefs=None):
        url = settings.MAIN_SERVER_URI + '/main/wsResources/v1/register/'

        headers = {'Content-Type': 'application/json', 'x-ads-device-type': settings.DEVICE_TYPE_HEADER}

        body = {}
        body.__setitem__(self.PARAM_EMAIL, user_name)
        body.__setitem__(self.PARAM_PASSWORD, password)
        body.__setitem__(self.PARAM_FIRST_NAME, first_name)
        body.__setitem__(self.PARAM_LAST_NAME, last_name)
        body.__setitem__(self.PARAM_FEEDBACK, feedback)
        body.__setitem__(self.PARAM_LOCALE, locale)
        body.__setitem__(self.PARAM_UI_PREFS_VERSION, ui_prefs)

        try:
            return requests.post(url=url, headers=headers, data=json.dumps(body))
        except Exception as e:
            print('RegisterClient.register_v1: body: ' + str(
                body) + '. Exception msg: ' + str(e.message) + '. Exception args: ' + str(e.args) + '\n')
            return None

    def register(self, user_name, password, first_name, last_name, feedback=True, locale='en-us'):
        url = settings.MAIN_SERVER_URI + '/main/register'

        headers = {'x-ads-device-type': settings.DEVICE_TYPE_HEADER}

        params = {}
        params.__setitem__(self.PARAM_EMAIL, user_name)
        params.__setitem__(self.PARAM_PASSWORD, password)
        params.__setitem__('firstname', first_name)
        params.__setitem__('lastname', last_name)
        params.__setitem__(self.PARAM_FEEDBACK, feedback)
        params.__setitem__(self.PARAM_LOCALE, locale)
        params.__setitem__(self.PARAM_MOBILE_APP_VERSION, 24)

        try:
            return requests.post(url=url, headers=headers, params=params)
        except Exception as e:
            print('RegisterClient.register: params: ' + str(
                params) + '. Exception msg: ' + str(e.message) + '. Exception args: ' + str(e.args) + '\n')
            return None
