__author__ = 'alonitzhaki'

import requests


class S3Client(object):
    def upload_to_s3(self, file_full_path, url_to_upload, method, acl, auth, date, content_type):
        headers = {}
        headers.__setitem__('x-amz-acl', acl)
        headers.__setitem__('Authorization', auth)
        headers.__setitem__('x-amz-date', date)
        headers.__setitem__('Content-Type', content_type)

        with open(file_full_path, 'rb') as f:
            try:
                if method == 'POST':
                    return requests.post(url=url_to_upload, headers=headers, data=f)
                elif method == 'PUT':
                    return requests.put(url=url_to_upload, headers=headers, data=f)
                else:
                    return None
            except Exception as e:
                print('S3Client.upload_to_s3: file: ' + str(file_full_path) + '. url: ' + str(
                    url_to_upload) + '. Exception msg: ' + str(e.message) + '. Exception args: ' + str(e.args) + '\n')
                return None
