"""
Accesso alle stored procedures sul db della smartgrid
"""

import boto

class S3Bucket(object):

    def __init__(self, bucket_owner = ''):
        self.connected = False
        try:
            #self.conn = boto.connect_s3()

            EUWest = 'eu-west-1'
            self.conn = boto.s3.connect_to_region(EUWest)

            self.connected = True

            bucket_name = 'erp-attachments.{owner}.it'.format(owner=bucket_owner)
            self.bucket = self.conn.get_bucket(bucket_name)
        except Exception as e:
            message = "S3 connection error: {err}".format(err=str(e))
            raise Exception(message)


    def getFileAsString(self, file_path):
        if not self.connected:
            raise Exception('s3 not connected')

        try:
            fileObj = self.bucket.get_key(file_path)
            if not fileObj:
                raise Exception('no such a file as {file_path} on s3 bucket'.format(file_path=file_path))
            return fileObj.get_contents_as_string()
        except Exception as e:
            message = "cannot get file {file} from s3. Error {err}".format(file=file_path, err=str(e))
            raise Exception(message)
