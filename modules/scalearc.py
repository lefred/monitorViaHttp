# scalearc module for monitorViaHttp

# version 0.1
# 2014 Dec 19 - frederic descamps - <lefred.descamps@gmail.com>
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

#
# Note about API KEY:
# -------------------
# The API KEY can be sent in the url via ?apikey=
# or in a file with the server's name as file name. That file must
# contain only the key. By default that file is loated in /tmp 
# please define it in this file changing the value of apikey_folder
#

import urlparse
import os
import json
import urllib2
import datetime
from dateutil.parser import parse

apikey_folder = "/tmp/"

def parse(s):
	parsed_url = urlparse.urlparse(s.path)
	params_url = urlparse.parse_qs(parsed_url.query)
	(server_name, module_name) = parsed_url.path[1:].split('/',1)
        if not params_url.has_key('apikey'):
          # we need to check if we have an api key for that server 
	  if not os.path.isfile("%s/%s" % (apikey_folder, server_name)):
                s.do_BAD_HEAD()
                return
          api_key = open("%s/%s" % (apikey_folder, server_name), 'r').read().rstrip()
        else:
	  api_key = params_url['apikey'][0]
	command = params_url['type'][0]
        scalearc_url = "https://%s/api/%s?apikey=%s" % (server_name, command, api_key)
        content=doCall(s, scalearc_url)
        if not content:
	  return
        print scalearc_url
	if command == "events":
	  eventcheck(s, content)
	elif command == "clusters":
	  clusterscheck(s, content)
	elif command == "ha":
	  hacheck(s, content)
	elif command == "license":
	  licensecheck(s, content)

def doCall(s, url):
    try:
        content = urllib2.urlopen(url).read()
    except urllib2.URLError, e:
        s.do_BAD_HEAD()
        s.wfile.write("ERROR: %s\n" % e.args)
	return False
    except urllib2.HTTPError, e:
        s.do_BAD_HEAD()
	s.wfile.write("ERROR: %s\n" % e.code)
	return False
    except:
        s.do_BAD_HEAD()
	s.wfile.write("ERROR: unkown error\n")
	return False
    return json.loads(content)

def eventcheck(s, content):
    if content["data"]["total"] == 0:
	s.do_HEAD()
        s.wfile.write("You have woken up monitorViaHttp by sending :\n\n")
        s.wfile.write("%s\n" % s.path)
        s.wfile.write("OK: No Event In ScaleArc\n\n")
	return
    else:
        s.do_BAD_HEAD()
	s.wfile.write("ERROR: Events were found in  ScaleArc\n")
	return

def clusterscheck(s, content):
    if len(content["data"]) < 1:
        s.do_BAD_HEAD()
	s.wfile.write("ERROR: no cluster data\n")
	return
    tot_rw = 0
    # check amount of Read + Write servers in the cluster
    for i in content["data"][0]["cluster_servers"]:
         if i['server_role'] == "Read + Write":
                tot_rw += 1
    if tot_rw == 1:
	s.do_HEAD()
        s.wfile.write("You have woken up monitorViaHttp by sending :\n\n")
        s.wfile.write("%s\n" % s.path)
        s.wfile.write("OK: There is only one Read + Write node\n\n")
	return
    elif tot_rw < 1:
        s.do_BAD_HEAD()
	s.wfile.write("ERROR: There is no Read + Write node\n")
	return
    else:
        s.do_BAD_HEAD()
	s.wfile.write("ERROR: More that 1 node acting as Read + Write\n")
	return

def hacheck(s, content):
    if content["data"]["local_runningas"]+content["data"]["remote_runningas"] \
       == "Running as PrimaryRunning as Secondary" or \
       content["data"]["local_runningas"]+content["data"]["remote_runningas"] \
       == "Running as SecondaryRunning as Primary":
	s.do_HEAD()
        s.wfile.write("You have woken up monitorViaHttp by sending :\n\n")
        s.wfile.write("%s\n" % s.path)
        s.wfile.write("OK: HA running with one Primary and one Secondary\n\n")
	return
    else:
        s.do_BAD_HEAD()
	s.wfile.write("ERROR: HA issue, we don't have one Primary and one Secondary\n")
	return

def licensecheck(s, content):
    lic_date = parse(content["data"]["license_expires_on"])
    difference = lic_date - datetime.datetime.now()
    if difference.days < 31:
        s.do_BAD_HEAD()
	s.wfile.write("ERROR: ScaleArc license expires in %s days\n" % difference.days)
	return
    else:
	s.do_HEAD()
        s.wfile.write("You have woken up monitorViaHttp by sending :\n\n")
        s.wfile.write("%s\n" % s.path)
        s.wfile.write("OK: ScaleArc license is still valid for %s days\n\n" % difference.days)
	return

