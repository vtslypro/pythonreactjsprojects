__author__ = 'alonitzhaki'

import requests
from utils.headers import AdskCommonHeadersManager

from rest_test import app_settings as settings


class XrefsClient(object):
    def get_all_xrefs(self, auth, version_id, map_xrefs=True, check_up_to_date=False):
        url = settings.MAIN_SERVER_URI + '/main/wsResources/xrefs/all'

        headers = {AdskCommonHeadersManager.ADSK_AUTH_HEADER: auth, 'x-ads-device-type': settings.DEVICE_TYPE_HEADER}

        params = {}
        params.__setitem__('versionId', version_id)
        params.__setitem__('mapXrefs', map_xrefs)
        params.__setitem__('checkUpToDate', check_up_to_date)

        try:
            return requests.get(url=url, headers=headers, params=params)
        except Exception as e:
            print('XrefsClient.get_all_xrefs: params: ' + str(
                params) + '. Exception msg: ' + str(e.message) + '. Exception args: ' + str(e.args) + '\n')
            return None

    def update_xref(self, auth, host_version_id, mapped_version_id, ref_path, ref_type='REF_XREF_TYPE'):
        url = settings.MAIN_SERVER_URI + '/main/wsResources/xrefs/update'

        headers = {AdskCommonHeadersManager.ADSK_AUTH_HEADER: auth, 'x-ads-device-type': settings.DEVICE_TYPE_HEADER}

        params = {}
        params.__setitem__('hostVersionId', host_version_id)
        params.__setitem__('mappedVersionId', mapped_version_id)
        params.__setitem__('refPath', ref_path)
        params.__setitem__('refType', ref_type)

        try:
            return requests.post(url=url, headers=headers, params=params)
        except Exception as e:
            print('XrefsClient.update_xref: params: ' + str(
                params) + '. Exception msg: ' + str(e.message) + '. Exception args: ' + str(e.args) + '\n')
            return None
