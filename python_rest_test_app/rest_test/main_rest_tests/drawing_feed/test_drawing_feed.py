__author__ = 'alonitzhaki'
from unittest import TestCase
import httplib
from time import time

from utils.clients.main_client import MainRegisterAndLoginMixin

from rest_test.extra_data_manager import ExtraDataManager
from rest_test.clients.clients_utils import ClientUtils
from rest_test.clients.drawing_feed_client import DrawingFeedClient
from rest_test.tests_utils import TestUtils


class DrawingFeedTests(TestCase):
    auth = None

    user_name = 'rest_tests_drawing_feed_' + str(int(time())) + '@autodesk.com'
    first_name = 'Rest'
    last_name = 'Test'
    password = 'Moomoo123'

    extra_data = None
    drawing_feed_client = DrawingFeedClient()

    def setUp(self):
        self.extra_data = ExtraDataManager()
        self.extra_data.add_test_data('user name', self.user_name)
        main_register_and_login_mixin = MainRegisterAndLoginMixin()
        if DrawingFeedTests.auth is None:
            response = main_register_and_login_mixin.login_or_register(user_name=self.user_name, password=self.password,
                                                                       first_name=self.first_name,
                                                                       last_name=self.last_name)
            DrawingFeedTests.auth = main_register_and_login_mixin.get_auth_from_login_data(response)
        self.assertIsInstance(DrawingFeedTests.auth, str,
                              'Invalid auth: ' + str(DrawingFeedTests.auth) + self.extra_data.get_all())

    def test_new_post(self):
        file_name = 'test_file_new_post_' + str(int(time())) + '.dwg'
        comment_body = 'test_comment_body'
        self.extra_data.add_test_data('file name', file_name)

        created_file_id, msg = TestUtils.create_file(auth=self.auth, file_name=file_name, extra_data=self.extra_data)
        self.assertIsNotNone(created_file_id, msg + self.extra_data.get_all())

        new_post_response = self.drawing_feed_client.new_post(auth=self.auth, file_id=created_file_id,
                                                              post_body=comment_body)

        status_code = ClientUtils.get_response_status_code(new_post_response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('new_post response', ClientUtils.get_response_body(new_post_response))

        post_status = ClientUtils.get_value_from_body(new_post_response, DrawingFeedClient.KEY_STATUS)
        self.assertEqual('open', post_status,
                         'Expected post status: open but got: ' + str(post_status) + self.extra_data.get_all())
        post_body = ClientUtils.get_value_from_body(new_post_response, DrawingFeedClient.KEY_BODY)
        self.assertEqual(comment_body, post_body, 'Expected post body: ' + str(comment_body) + ' but got: ' + str(
            post_body) + self.extra_data.get_all())
        post_id = ClientUtils.get_value_from_body(new_post_response, DrawingFeedClient.KEY_ID)
        self.assertIsInstance(post_id, unicode,
                              'Expected unicode post id but got: ' + str(post_id) + self.extra_data.get_all())
        self.extra_data.add_test_data('post id', post_id)

        get_feed_response = self.drawing_feed_client.get_drawing_feed(auth=self.auth, file_id=created_file_id)
        status_code = ClientUtils.get_response_status_code(get_feed_response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('get_drawing_feed response', ClientUtils.get_response_body(get_feed_response))

        post = TestUtils.get_post_from_drawing_feed_response(get_feed_response, post_id)
        self.assertIsNotNone(post, 'Expected non-empty post' + self.extra_data.get_all())
        self.extra_data.add_test_data('post', post)

        post_status = post['status']
        self.assertEqual('open', post_status,
                         'Expected post status: open but got: ' + str(post_status) + self.extra_data.get_all())
        post_body = post['body']
        self.assertEqual(comment_body, post_body, 'Expected post body: ' + str(comment_body) + 'but got: ' + str(
            post_body) + self.extra_data.get_all())
        post_actor_name = post['actor']['name']
        user_full_name = self.first_name + ' ' + self.last_name
        self.assertEqual(user_full_name, post_actor_name,
                         'Expected post actor: ' + str(user_full_name) + 'but got: ' + str(
                             post_actor_name) + self.extra_data.get_all())

    def test_update_post(self):
        file_name = 'test_file_update_post_' + str(int(time())) + '.dwg'
        comment_body = 'test_comment_body'
        updated_post_status = 'closed'
        self.extra_data.add_test_data('file name', file_name)

        created_file_id, msg = TestUtils.create_file(auth=self.auth, file_name=file_name, extra_data=self.extra_data)
        self.assertIsNotNone(created_file_id, msg + self.extra_data.get_all())

        new_post_response = self.drawing_feed_client.new_post(auth=self.auth, file_id=created_file_id,
                                                              post_body=comment_body)
        status_code = ClientUtils.get_response_status_code(new_post_response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('new_post response', ClientUtils.get_response_body(new_post_response))

        post_id = ClientUtils.get_value_from_body(new_post_response, DrawingFeedClient.KEY_ID)
        self.assertIsInstance(post_id, unicode,
                              'Expected unicode post id but got: ' + str(post_id) + self.extra_data.get_all())
        self.extra_data.add_test_data('post id', post_id)

        update_post_response = self.drawing_feed_client.update_post(auth=self.auth, file_id=created_file_id,
                                                                    post_id=post_id,
                                                                    post_status=updated_post_status)
        status_code = ClientUtils.get_response_status_code(update_post_response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('update_post response', ClientUtils.get_response_body(update_post_response))

        response_post_id = ClientUtils.get_value_from_body(update_post_response, DrawingFeedClient.KEY_ID)
        self.assertEqual(post_id, response_post_id, 'Expected post_id: ' + str(post_id) + ' but got: ' + str(
            response_post_id) + self.extra_data.get_all())

        self.assertTrue(ClientUtils.is_key_in_body(update_post_response, 'updated'),
                        'Expected key "updated" to exist in response body' + self.extra_data.get_all())

        get_feed_response = self.drawing_feed_client.get_drawing_feed(auth=self.auth, file_id=created_file_id)
        status_code = ClientUtils.get_response_status_code(get_feed_response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('get_drawing_feed response', ClientUtils.get_response_body(get_feed_response))

        post = TestUtils.get_post_from_drawing_feed_response(get_feed_response, post_id)
        self.assertIsNotNone(post, 'Expected non empty post' + self.extra_data.get_all())
        self.extra_data.add_test_data('post', post)

        post_status = post['status']
        self.assertEqual(updated_post_status, post_status, 'Expected updated post status: ' + str(
            updated_post_status) + ' but got: ' + str(post_status) + self.extra_data.get_all())

    def test_new_post_old_api(self):
        file_name = 'test_file_new_post_' + str(int(time())) + '.dwg'
        comment_body = 'test_comment_body'
        self.extra_data.add_test_data('file name', file_name)

        created_file_id, msg = TestUtils.create_file(auth=self.auth, file_name=file_name, extra_data=self.extra_data)
        self.assertIsNotNone(created_file_id, msg + self.extra_data.get_all())

        new_post_response = self.drawing_feed_client.new_post_old_api(auth=self.auth, file_id=created_file_id,
                                                                      post_body=comment_body)

        status_code = ClientUtils.get_response_status_code(new_post_response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('new_post response', ClientUtils.get_response_body(new_post_response))

        post_status = ClientUtils.get_value_from_body(new_post_response, DrawingFeedClient.KEY_STATUS)
        self.assertEqual('open', post_status,
                         'Expected post status: open but got: ' + str(post_status) + self.extra_data.get_all())
        post_body = ClientUtils.get_value_from_body(new_post_response, DrawingFeedClient.KEY_BODY)
        self.assertEqual(comment_body, post_body, 'Expected post body: ' + str(comment_body) + ' but got: ' + str(
            post_body) + self.extra_data.get_all())
        post_id = ClientUtils.get_value_from_body(new_post_response, DrawingFeedClient.KEY_ID)
        self.assertIsInstance(post_id, unicode,
                              'Expected unicode post id but got: ' + str(post_id) + self.extra_data.get_all())
        self.extra_data.add_test_data('post id', post_id)

        get_feed_response = self.drawing_feed_client.get_drawing_feed_old_api(auth=self.auth, file_id=created_file_id)
        status_code = ClientUtils.get_response_status_code(get_feed_response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('get_drawing_feed response', ClientUtils.get_response_body(get_feed_response))

        post = TestUtils.get_post_from_drawing_feed_response(get_feed_response, post_id)
        self.assertIsNotNone(post, 'Expected non-empty post' + self.extra_data.get_all())
        self.extra_data.add_test_data('post', post)

        post_status = post['status']
        self.assertEqual('open', post_status,
                         'Expected post status: open but got: ' + str(post_status) + self.extra_data.get_all())
        post_body = post['body']
        self.assertEqual(comment_body, post_body, 'Expected post body: ' + str(comment_body) + 'but got: ' + str(
            post_body) + self.extra_data.get_all())
        post_actor_name = post['actor']['name']
        user_full_name = self.first_name + ' ' + self.last_name
        self.assertEqual(user_full_name, post_actor_name,
                         'Expected post actor: ' + str(user_full_name) + 'but got: ' + str(
                             post_actor_name) + self.extra_data.get_all())

    def test_update_post_old_api(self):
        file_name = 'test_file_update_post_' + str(int(time())) + '.dwg'
        comment_body = 'test_comment_body'
        updated_post_status = 'closed'
        self.extra_data.add_test_data('file name', file_name)

        created_file_id, msg = TestUtils.create_file(auth=self.auth, file_name=file_name, extra_data=self.extra_data)
        self.assertIsNotNone(created_file_id, msg + self.extra_data.get_all())

        new_post_response = self.drawing_feed_client.new_post_old_api(auth=self.auth, file_id=created_file_id,
                                                                      post_body=comment_body)
        status_code = ClientUtils.get_response_status_code(new_post_response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('new_post response', ClientUtils.get_response_body(new_post_response))

        post_id = ClientUtils.get_value_from_body(new_post_response, DrawingFeedClient.KEY_ID)
        self.assertIsInstance(post_id, unicode,
                              'Expected unicode post id but got: ' + str(post_id) + self.extra_data.get_all())
        self.extra_data.add_test_data('post id', post_id)

        update_post_response = self.drawing_feed_client.update_post_old_api(auth=self.auth, file_id=created_file_id,
                                                                            post_id=post_id,
                                                                            post_status=updated_post_status)
        status_code = ClientUtils.get_response_status_code(update_post_response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('update_post response', ClientUtils.get_response_body(update_post_response))

        response_post_id = ClientUtils.get_value_from_body(update_post_response, DrawingFeedClient.KEY_ID)
        self.assertEqual(post_id, response_post_id, 'Expected post_id: ' + str(post_id) + ' but got: ' + str(
            response_post_id) + self.extra_data.get_all())

        self.assertTrue(ClientUtils.is_key_in_body(update_post_response, 'updated'),
                        'Expected key "updated" to exist in response body' + self.extra_data.get_all())

        get_feed_response = self.drawing_feed_client.get_drawing_feed_old_api(auth=self.auth, file_id=created_file_id)
        status_code = ClientUtils.get_response_status_code(get_feed_response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('get_drawing_feed response', ClientUtils.get_response_body(get_feed_response))

        post = TestUtils.get_post_from_drawing_feed_response(get_feed_response, post_id)
        self.assertIsNotNone(post, 'Expected non empty post' + self.extra_data.get_all())
        self.extra_data.add_test_data('post', post)

        post_status = post['status']
        self.assertEqual(updated_post_status, post_status, 'Expected updated post status: ' + str(
            updated_post_status) + ' but got: ' + str(post_status) + self.extra_data.get_all())
