__author__ = 'alonitzhaki'

from jsonpath_rw import parse


class ClientUtils(object):
    KEY_CODE = 'code'
    KEY_DESCRIPTION = 'description'

    @staticmethod
    def get_response_status_code(response):
        try:
            return response.status_code
        except Exception as e:
            print('ClientUtils.get_response_status_code: Exception msg: ' + str(e.message) + '. Exception args: ' + str(
                e.args) + '\n')
            return None

    @staticmethod
    def get_response_body(response):
        try:
            return response.json()
        except Exception as e:
            print(
                'ClientUtils.get_response_body: Exception msg: ' + str(e.message) + '. Exception args: ' + str(
                    e.args) + '\n')
            return None

    @staticmethod
    def get_response_raw_content(response):
        try:
            return response.raw
        except Exception as e:
            print(
                'ClientUtils.get_response_raw_content: Exception msg: ' + str(
                    e.message) + '. Exception args: ' + str(e.args) + '\n')
            return None

    @staticmethod
    def is_response_body_empty(response):
        '''
        assumes response is not None
        returns True if and only if response has no body
        '''
        try:
            response.json()
        except ValueError:  # execption raised iff response has no body
            return True
        return False

    @staticmethod
    def get_code_and_description_from_response(response):
        body = ClientUtils.get_response_body(response)
        try:
            return body[ClientUtils.KEY_CODE], body[ClientUtils.KEY_DESCRIPTION]
        except Exception as e:
            print(
                'ClientUtils.get_code_and_description_from_response: Exception msg: ' + str(
                    e.message) + '. Exception args: ' + str(e.args) + '\n')
            return None

    @staticmethod
    def is_key_in_body(response, nested_keys):
        if ClientUtils.get_value_from_body(response, nested_keys) is None:
            return False
        return True

    @staticmethod
    def get_value_from_body(response, json_path):
        body = ClientUtils.get_response_body(response)

        search_expression = parse(json_path)

        result = [match.value for match in search_expression.find(body)]

        if len(result) == 1:
            return result[0]
        return result

    @staticmethod
    def get_multiple_values_from_body(response, json_path_list):
        if isinstance(json_path_list, str):  # a single nested_keys entry, no list to iterate over
            return ClientUtils.get_value_from_body(response, json_path_list)

        values_list = []

        for nested_keys_entry in json_path_list:
            values_list.append(ClientUtils.get_value_from_body(response, nested_keys_entry))

        return values_list

    @staticmethod
    def get_ticket_value_from_authorization_header(auth):
        try:
            return auth.split(' ')[1]
        except Exception as e:
            print(
                'ClientUtils.get_ticket_value_from_authorization_header: Exception msg: ' + str(
                    e.message) + '. Exception args: ' + str(e.args) + '\n')
            return None
