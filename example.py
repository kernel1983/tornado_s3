import sys
import os
import logging
import uuid
import urlparse
import urllib
import time

import tornado.options
import tornado.ioloop
import tornado.web
import tornado.httpclient as httpclient

from tornado_s3 import S3Bucket


class TestHandler(tornado.web.RequestHandler):
    def get(self):
        # send email notifaction
        """
        user_msg = EmailMessage()
        user_msg.subject = u"Test"
        user_msg.bodyHtml = "This is the test content."
        self.send("your@address.net", "user@address.net", user_msg)
        """
        pass

settings = {
    #"AmazonAccessKeyID": "00000000000000000000",
    #"AmazonSecretAccessKey": "0000000000000000000000000000000000000000",
    "debug": True,
}

application = tornado.web.Application([
    (r"/", TestHandler),
], **settings)

"""
if __name__ == "__main__":
    tornado.options.parse_command_line()
    application.listen(int(sys.argv[1]))
    tornado.ioloop.IOLoop.instance().start()
"""

s = S3Bucket("mybucket",
             access_key=settings["AmazonAccessKeyID"],
             secret_key=settings["AmazonSecretAccessKey"],
             base_url="http://s3-ap-southeast-1.amazonaws.com/mybucket")

#delete all files in bucket
for i in [key for (key, modify, etag, size) in s.listdir()]:
    del s[i]

#list all files
print [key for (key, modify, etag, size) in s.listdir()]

#create file
s.put("my file", "my content")

#download file
f = s.get("my file")
print f.body

#get file information
print f.s3_info
