__author__ = 'alonitzhaki'

from unittest import TestCase
from time import time
import httplib

from utils.clients.main_client import MainLoginV2Mixin

from rest_test.clients.clients_utils import ClientUtils
from rest_test.clients.register_client import RegisterClient
from rest_test.extra_data_manager import ExtraDataManager


class RegisterTests(TestCase):
    user_name = 'rest_tests_register_' + str(int(time())) + '@autodesk.com'
    first_name = 'Rest'
    last_name = 'Test'
    valid_password = 'Moomoo123'
    invalid_password = 'a'
    empty_password = ''

    extra_data = None
    register_client = RegisterClient()
    main_login_v2_mixin = MainLoginV2Mixin()

    def setUp(self):
        self.extra_data = ExtraDataManager()
        self.extra_data.add_test_data('user name', self.user_name)

    def test_register_v1_valid(self):
        response = self.register_client.register_v1(user_name=self.user_name, password=self.valid_password,
                                                    first_name=self.first_name,
                                                    last_name=self.last_name)
        status_code = ClientUtils.get_response_status_code(response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('register response', ClientUtils.get_response_body(response))

        eidm_user_id = ClientUtils.get_value_from_body(response, RegisterClient.KEY_EIDM_USER_ID)
        self.assertIsNotNone(eidm_user_id, 'Expected eidm user id in response but got None' + self.extra_data.get_all())
        self.assertTrue(len(eidm_user_id) > 0, 'Expected a non-empty string as eidm user id but got: ' + str(
            eidm_user_id) + self.extra_data.get_all())

        eidm_user_name = ClientUtils.get_value_from_body(response, RegisterClient.KEY_EIDM_USER_NAME)
        self.assertIsNotNone(eidm_user_name, 'Expected eidm user name in response but got None' + self.extra_data.get_all())
        self.assertTrue(len(eidm_user_name) > 0, 'Expected a non-empty string as eidm user name but got: ' + str(
            eidm_user_name) + self.extra_data.get_all())

        email = ClientUtils.get_value_from_body(response, RegisterClient.KEY_MAIL)
        self.assertEquals(self.user_name, email, 'Expected user_name: ' + str(self.user_name) + ' but got: ' + str(
            email) + self.extra_data.get_all())

    def test_register_v1_valid_account_already_exists(self):
        self.make_sure_user_already_registered(self.user_name, self.valid_password)

        response = self.register_client.register_v1(user_name=self.user_name, password=self.valid_password,
                                                    first_name=self.first_name,
                                                    last_name=self.last_name)
        status_code = ClientUtils.get_response_status_code(response)
        self.assertEqual(httplib.OK, status_code, 'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('register response', ClientUtils.get_response_body(response))

        email = ClientUtils.get_value_from_body(response, RegisterClient.KEY_MAIL)
        self.assertEquals(self.user_name, email, 'Expected user_name: ' + str(self.user_name) + ' but got: ' + str(
            email) + self.extra_data.get_all())

    def make_sure_user_already_registered(self, user_name, password):
        login_data = self.main_login_v2_mixin.login_request(user_name=user_name, password=password)
        user_id = self.main_login_v2_mixin.get_user_id_from_login_data(login_data)
        self.assertIsNotNone(user_id,
                             'Expected user_id not None. user probably does not exist yet, ' +
                             'previous register test probably failed' + self.extra_data.get_all())

    def test_register_v1_invalid_password(self):
        expected_code_and_description = (2, 'PASSWORD REJECTED')

        response = self.register_client.register_v1(user_name=self.user_name, password=self.invalid_password,
                                                    first_name=self.first_name,
                                                    last_name=self.last_name)
        status_code = ClientUtils.get_response_status_code(response)
        self.assertEqual(httplib.BAD_REQUEST, status_code,
                         'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('register response', ClientUtils.get_response_body(response))

        code_desc = ClientUtils.get_code_and_description_from_response(response)
        self.assertEqual(expected_code_and_description, code_desc,
                         'Expected ' + str(expected_code_and_description) + ' but got: ' + str(
                             code_desc) + self.extra_data.get_all())

    def test_register_v1_empty_password(self):
        expected_code_and_description = (400, 'One or more parameters are missing.')

        response = self.register_client.register_v1(user_name=self.user_name, password=self.empty_password,
                                                    first_name=self.first_name,
                                                    last_name=self.last_name)
        status_code = ClientUtils.get_response_status_code(response)
        self.assertEqual(httplib.BAD_REQUEST, status_code,
                         'Got status code: ' + str(status_code) + self.extra_data.get_all())
        self.extra_data.add_test_data('register response', ClientUtils.get_response_body(response))

        code_desc = ClientUtils.get_code_and_description_from_response(response)
        self.assertEqual(expected_code_and_description, code_desc,
                         'Expected ' + str(expected_code_and_description) + ' but got: ' + str(
                             code_desc) + self.extra_data.get_all())
