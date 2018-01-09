import tornado
import tornado.web
from tornado import gen
from tornado.options import options

import motor
import gridfs

import os
import base64
import uuid
import os
import os.path

from tornado.options import define

define("server_port", default=8000, type=int, help="The server port")
define("db_host", default="localhost", help="Database host")
define("db_port", default=27017, help="Database port")

settings = dict(
    db = motor.motor_tornado.MotorClient().wjh_model
)

class FileHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @gen.coroutine
    def get(self,filename):
        db = self.settings['db']
        fs = motor.MotorGridFSBucket(db)
        try:
            #file_id = yield fs.upload_from_stream(filename)
            grid_out = yield fs.open_download_stream_by_name(filename)
        except gridfs.NoFile:
            raise tornado.web.HTTPError(404)
        yield grid_out.stream_to_handler(self)
        self.finish()

application = tornado.web.Application([(r"/wjh_model/(.*)", FileHandler)], **settings)

def main():
    tornado.options.parse_command_line()
    #application.listen(options.server_port)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.server_port)
    tornado.ioloop.IOLoop.instance().start()
    return 0

if __name__ == '__main__':
    main()