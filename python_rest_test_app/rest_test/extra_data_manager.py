__author__ = 'alonitzhaki'
from time import time


class ExtraDataManager(object):

    def __init__(self):
        self.extra_data = []
        self.extra_data.append(('test start time', str(int(time()))))

    def add_test_data(self, name, value):
        self.extra_data.append((str(name), str(value)))

    def get_all(self):
        separation_line = '\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -'
        output = separation_line + '\nTest Extra Data:\n\n'
        for entry in self.extra_data:
            output = output + entry[0] + ': ' + entry[1] + '\n\n'
        output = output + 'test end time: ' + str(int(time())) + '\n'

        return output
