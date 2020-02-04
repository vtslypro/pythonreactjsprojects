__author__ = 'alonitzhaki'
import json

import requests
from utils.headers import AdskCommonHeadersManager

from rest_test import app_settings as settings
from rest_test.clients.clients_utils import ClientUtils


class DrawingFeedClient(object):
    KEY_STATUS = 'status'
    KEY_BODY = 'body'
    KEY_ID = 'id'
    KEY_POST_NUMBER = 'postNumber'

    def get_drawing_feed(self, auth, file_id):
        url = settings.MAIN_SERVER_URI + '/main/wsResources/drawingfeed/file/' + str(file_id)

        headers = {AdskCommonHeadersManager.ADSK_AUTH_HEADER: auth, 'x-ads-device-type': settings.DEVICE_TYPE_HEADER}

        try:
            return requests.get(url=url, headers=headers)
        except Exception as e:
            print('DrawingFeedClient.get_drawing_feed: file id: ' + str(
                file_id) + '. Exception msg: ' + str(e.message) + '. Exception args: ' + str(e.args) + '\n')
            return None

    def new_post(self, auth, file_id, post_body):
        url = settings.MAIN_SERVER_URI + '/main/wsResources/drawingfeed/file/' + str(file_id)

        headers = {'Content-type': 'application/json', AdskCommonHeadersManager.ADSK_AUTH_HEADER: auth,
                   'x-ads-device-type': settings.DEVICE_TYPE_HEADER}

        body = {}
        body.__setitem__('body', post_body)

        try:
            return requests.post(url=url, headers=headers, data=json.dumps(body))
        except Exception as e:
            print('DrawingFeedClient.new_post: file_id: ' + str(file_id) + '. body: ' + str(
                body) + '. Exception msg: ' + str(e.message) + '. Exception args: ' + str(e.args) + '\n')
            return None

    def update_post(self, auth, file_id, post_id, post_status):
        url = settings.MAIN_SERVER_URI + '/main/wsResources/drawingfeed/file/' + str(file_id) + '/comment/' + str(
            post_id)

        headers = {'Content-type': 'application/json', AdskCommonHeadersManager.ADSK_AUTH_HEADER: auth,
                   'x-ads-device-type': settings.DEVICE_TYPE_HEADER}

        body = {}
        body.__setitem__('status', post_status)

        try:
            return requests.put(url=url, headers=headers, data=json.dumps(body))
        except Exception as e:
            print('DrawingFeedClient.update_post: file id: ' + str(file_id) + '. post id: ' + str(
                post_id) + '. body: ' + str(body) + '. Exception msg: ' + str(e.message) + '. Exception args: ' + str(
                e.args) + '\n')
            return None

    def get_drawing_feed_old_api(self, auth, file_id):
        url = settings.MAIN_SERVER_URI + '/main/drawingfeed/v1/file/' + str(file_id)

        ticket = ClientUtils.get_ticket_value_from_authorization_header(auth)
        headers = {}
        headers.__setitem__('ticket', ticket)
        headers.__setitem__('isMobile', True)
        headers.__setitem__('x-ads-device-type', settings.DEVICE_TYPE_HEADER)

        try:
            return requests.get(url=url, headers=headers)
        except Exception as e:
            print('DrawingFeedClient.get_drawing_feed_old_api: file id: ' + str(
                file_id) + '. Exception msg: ' + str(e.message) + '. Exception args: ' + str(e.args) + '\n')
            return None

    def new_post_old_api(self, auth, file_id, post_body):
        url = settings.MAIN_SERVER_URI + '/main/drawingfeed/v1/file/' + str(file_id)

        ticket = ClientUtils.get_ticket_value_from_authorization_header(auth)
        headers = {}
        headers.__setitem__('Content-type', 'application/json')
        headers.__setitem__('ticket', ticket)
        headers.__setitem__('isMobile', True)
        headers.__setitem__('x-ads-device-type', settings.DEVICE_TYPE_HEADER)

        body = {}
        body.__setitem__('body', post_body)

        try:
            return requests.post(url=url, headers=headers, data=json.dumps(body))
        except Exception as e:
            print('DrawingFeedClient.new_post_old_api: file_id: ' + str(file_id) + '. body: ' + str(
                body) + '. Exception msg: ' + str(e.message) + '. Exception args: ' + str(e.args) + '\n')
            return None

    def update_post_old_api(self, auth, file_id, post_id, post_status):
        url = settings.MAIN_SERVER_URI + '/main/drawingfeed/v1/file/' + str(file_id) + '/comment/' + str(
            post_id)

        ticket = ClientUtils.get_ticket_value_from_authorization_header(auth)
        headers = {}
        headers.__setitem__('Content-type', 'application/json')
        headers.__setitem__('ticket', ticket)
        headers.__setitem__('isMobile', True)
        headers.__setitem__('x-ads-device-type', settings.DEVICE_TYPE_HEADER)

        body = {}
        body.__setitem__('status', post_status)

        try:
            return requests.put(url=url, headers=headers, data=json.dumps(body))
        except Exception as e:
            print('DrawingFeedClient.update_post_old_api: file id: ' + str(file_id) + '. post id: ' + str(
                post_id) + '. body: ' + str(body) + '. Exception msg: ' + str(e.message) + '. Exception args: ' + str(
                e.args) + '\n')
            return None
