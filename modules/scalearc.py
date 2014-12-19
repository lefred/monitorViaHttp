# scalearc module for monitorViaHttp

#
# check for events
# 	http://127.0.0.1:8888/servername/scalearc?type=events&total=0
#
#        BAD if more amount of events > 0
#
# check for clusters
# 	http://127.0.0.1:8888/servername/scalearc?type=clusters&rw=1
#
#        BAD if more none or more that one node is not Read + Write
#
# check for ha
# 	http://127.0.0.1:8888/servername/scalearc?type=ha&=primary=1&secondary=1
#
#        BAD if there is no 1 primary and no 1 secondary
#
# check for license
# 	http://127.0.0.1:8888/servername/scalearc?type=license&days=313131
#
#        BAD if license expire in less than 31 days
#

import urlparse
import os
import json
import urllib2
import datetime
from dateutil.parser import parse

def parse(s):
	parsed_url = urlparse.urlparse(s.path)
	params_url = urlparse.parse_qs(parsed_url.query)
        # __TODO__ 
