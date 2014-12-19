#!/usr/bin/python
import time
import BaseHTTPServer
import urlparse
import importlib
import os
import sys

HOST_NAME = 'localhost'
PORT_NUMBER = 8888

sys.path.extend([os.path.dirname(os.path.realpath(__file__)) + '/modules'])

#
# expected url arguments is: http://server:port/server_name_or_ip/module?arg1=val1&arg2=val2
#


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
	s.send_header("Content-Type","text/plain")
	s.send_header("X-Content-Type-Options", "nosniff")
        s.end_headers()

    def do_BAD_HEAD(s):
	s.send_response(500)
	s.send_header("Content-Type", "text/plain")
	s.send_header("X-Content-Type-Options", "nosniff")
        s.end_headers()

    def do_GET(s):
        # parse the url
        parsed_url = urlparse.urlparse(s.path)
        (server_name, module_name) = parsed_url.path[1:].split('/',1) 
        try:
		my_mod=importlib.import_module(module_name)
        except:
		s.do_BAD_HEAD()
		print "Unexpected error:", sys.exc_info()
		print "Error loading module %s" % module_name
                return
        my_mod.parse(s)

if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
