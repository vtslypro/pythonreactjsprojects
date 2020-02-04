from subprocess import call
import os

from rest_test import app_settings as settings


class RestTestRunner(object):
    @staticmethod
    def run_tests():
        root_tests_dir = settings.BASE_DIR + '/rest_test/main_rest_tests'
        execute_command = ['py.test', '--junitxml', 'reports/junit.xml']
        suites_str = os.getenv('TEST_SUITES', None)
        if suites_str is not None:
            suites = suites_str.split(',')
            for suite in suites:
                suite_path = root_tests_dir + '/' + str(suite)
                execute_command.append(suite_path)
        else:
            execute_command.append(root_tests_dir)
        print('Running Main python rest tests. Executed command: ' + str(execute_command) + '\n')
        call(execute_command)
