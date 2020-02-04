from __future__ import absolute_import
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# SECRET_KEY = '282c8ab0-ca9b-441a-bc56-7e205a9c440e'

MAIN_SERVER_URI = os.getenv('MAIN_SERVER_URI', 'http://127.0.0.1:8080')
COMPRESSOR_SERVER_URI = os.getenv('COMPRESSOR_SERVER_URI', 'http://127.0.0.1:8080')
PLOT_SERVER_URI = os.getenv('PLOT_SERVER_URI', 'http://127.0.0.1:8080')

BOX_USER_NAME = 'acad360.rest.tests@gmail.com'
BOX_PASSWORD = 'jvP24AKfwgVjvbuNCFgG'


GMAIL_USER_NAME = 'acad360.rest.tests@gmail.com'
GMAIL_PASSWORD = 'jvP24AKfwgVjvbuNCFgG'


DEVICE_TYPE_HEADER = 'REST Test Python'


#LOG_LEVEL = 'DEBUG'
#
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': True,
#     'formatters': {
#         'json': {
#             '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
#             'fmt': '%(levelname)s %(asctime)s %(module)s %(process)d %(message)s %(pathname)s $(lineno)d $(funcName)s '
#                    ' %(http_user_agent)s %(exc_info)s'
#         },
#         'verbose': {
#             'format': '%(asctime)s %(levelname)s %(module)s %(process)d %(thread)d %(message)s'
#         },
#         'simple': {
#             'fmt': '%(levelname)s %(asctime)s %(module)s %(process)d %(message)s %(pathname)s $(lineno)d $(funcName)s  '
#                    '%(http_user_agent)s '
#         },
#     },
#     'handlers': {
#         'json_file': {
#             'level': 'DEBUG',
#             'class': 'logging.handlers.RotatingFileHandler',
#             'filename': os.getenv('TA_APP_LOG_PATH', os.path.join(BASE_DIR, 'logs', 'app_json.log')),
#             'maxBytes': 100000,
#             'backupCount': 5,
#             'formatter': 'json',
#         },
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#             'formatter': 'json',
#         },
#         'simple_file': {
#             'level': 'DEBUG',
#             'class': 'logging.handlers.RotatingFileHandler',
#             'filename': os.getenv('TA_SIMPLE_LOG_PATH', os.path.join(BASE_DIR, 'logs', 'app_simple.log')),
#             'maxBytes': 100000,
#             'backupCount': 5,
#             'formatter': 'simple',
#         },
#     },
#     'loggers': {
#         'app': {
#             'handlers': ['json_file', 'simple_file'],
#             'level': LOG_LEVEL
#         }
#     }
# }

