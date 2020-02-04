__author__ = 'alonitzhaki'
import json

import requests
from utils.headers import AdskCommonHeadersManager

from rest_test import app_settings as settings


class UserClient(object):
    KEY_VERSION = 'version'
    KEY_TIMESTAMP = 'timestamp'
    KEY_WEB_LANG = 'webLang'
    KEY_COUNTRY = 'country'
    KEY_DRAWING_WAS_OPENED_IN_360_WEB = 'drawingWasOpenedIn360Web'
    KEY_MODEL_BG_COLOR = 'modelBgColor'
    KEY_LAYOUT_BG_COLOR = 'layoutBgColor'
    KEY_BLOCK_EDITOR_BG_COLOR = 'blockEditorBgColor'
    KEY_DEFAULT_UNITS = 'defaultUnits'
    KEY_OPT_IN_PREFERENCES = 'optInPreferences'
    KEY_DYNAMIC_PREFS = 'dynamicPrefs'
    KEY_USER_ID = 'userId'
    KEY_CONTACT_ADDRESS = 'contactAddress'
    KEY_FIRST_NAME = 'firstName'
    KEY_LAST_NAME = 'lastName'

    PARAM_UI_PREFS_VERSION = 'uiPrefsVersion'

    def get_user_preferences(self, auth, ui_prefs_version=''):
        url = settings.MAIN_SERVER_URI + '/main/wsResources/user/preferences'

        headers = {'Content-type': 'application/json', AdskCommonHeadersManager.ADSK_AUTH_HEADER: auth,
                   'x-ads-device-type': settings.DEVICE_TYPE_HEADER}

        params = {}
        params.__setitem__(self.PARAM_UI_PREFS_VERSION, ui_prefs_version)

        try:
            return requests.get(url=url, headers=headers, params=params)
        except Exception as e:
            print('UserClient.get_user_preferences: params: ' + str(
                params) + '. Exception msg: ' + str(e.message) + '. Exception args: ' + str(e.args) + '\n')
            return None

    def post_user_preferences(self, auth, webLang='en', country='US', drawing_was_opened_in_360_web=False,
                              model_bg_color=0,
                              layout_bg_color=0, block_editor_bg_color=0, default_units=None, opt_in_preferences=None,
                              dynamic_prefs=None):
        url = settings.MAIN_SERVER_URI + '/main/wsResources/user/preferences'

        headers = {'Content-type': 'application/json', AdskCommonHeadersManager.ADSK_AUTH_HEADER: auth,
                   'x-ads-device-type': settings.DEVICE_TYPE_HEADER}

        body = {}
        body.__setitem__(self.KEY_WEB_LANG, webLang)
        body.__setitem__(self.KEY_COUNTRY, country)
        body.__setitem__(self.KEY_DRAWING_WAS_OPENED_IN_360_WEB, drawing_was_opened_in_360_web)
        body.__setitem__(self.KEY_MODEL_BG_COLOR, model_bg_color)
        body.__setitem__(self.KEY_LAYOUT_BG_COLOR, layout_bg_color)
        body.__setitem__(self.KEY_BLOCK_EDITOR_BG_COLOR, block_editor_bg_color)
        body.__setitem__(self.KEY_DEFAULT_UNITS, default_units)
        body.__setitem__(self.KEY_OPT_IN_PREFERENCES, opt_in_preferences)
        body.__setitem__(self.KEY_DYNAMIC_PREFS, dynamic_prefs)

        try:
            return requests.post(url=url, headers=headers, data=json.dumps(body))
        except Exception as e:
            print('UserClient.post_user_preferences: body: ' + str(
                body) + '. Exception msg: ' + str(e.message) + '. Exception args: ' + str(e.args) + '\n')
            return None

    def get_user_details(self, auth):
        url = settings.MAIN_SERVER_URI + '/main/wsResources/user/details'
        headers = {AdskCommonHeadersManager.ADSK_AUTH_HEADER: auth, 'x-ads-device-type': settings.DEVICE_TYPE_HEADER}

        try:
            return requests.get(url=url, headers=headers)
        except Exception as e:
            print('UserClient.get_user_details: Exception msg: ' + str(e.message) + '. Exception args: ' +
                  str(e.args) + '\n')
            return None

    def get_user_share_suggestions(self, auth):
        url = settings.MAIN_SERVER_URI + '/main/wsResources/user/shareSuggestion'
        headers = {AdskCommonHeadersManager.ADSK_AUTH_HEADER: auth, 'x-ads-device-type': settings.DEVICE_TYPE_HEADER}

        try:
            return requests.get(url=url, headers=headers)
        except Exception as e:
            print('UserClient.get_user_share_suggestions: Exception msg: ' + str(e.message) + '. Exception args: ' +
                  str(e.args) + '\n')
            return None

    def get_user_status(self, auth):
        url = settings.MAIN_SERVER_URI + '/main/wsResources/user/status'
        headers = {AdskCommonHeadersManager.ADSK_AUTH_HEADER: auth, 'x-ads-device-type': settings.DEVICE_TYPE_HEADER}

        try:
            return requests.get(url=url, headers=headers)
        except Exception as e:
            print('UserClient.get_user_status: Exception msg: ' + str(e.message) + '. Exception args: ' +
                  str(e.args) + '\n')
            return None
