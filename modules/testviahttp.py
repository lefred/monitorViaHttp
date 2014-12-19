# test module for monitorViaHttp

# check in file located in /tmp for a value 
# (server name is just printed for the rest ignored
# so url looks like:
#
# http://127.0.0.1:8888/servername/testviahttp?filename=val&content=val

import urlparse
import os

def parse(s):
	parsed_url = urlparse.urlparse(s.path)
	params_url = urlparse.parse_qs(parsed_url.query)
        if not os.path.isfile("/tmp/%s" % params_url['filename'][0]):
		s.do_BAD_HEAD()
		return 
       	current_content = open("/tmp/%s" % params_url['filename'][0], 'r').read().rstrip()
       	if current_content == params_url['content'][0]:
       	    s.do_HEAD()
       	    s.wfile.write("You have woken up monitorViaHttp by sending :\n\n")
       	    s.wfile.write("%s\n" % s.path)
	else:
	    s.do_BAD_HEAD()
