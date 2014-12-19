monitorViaHttp
==============

HTTP monitoring endpoint 

Python webserver used to return 200 (when OK) and 500 (when not OK) to a HTTP call for
anything that you want to monitor.

This is useful when you use monitoring solutions that are not flexible or open enought
to implement new checks (aka Foglight).

If you need a new check, just create a new module. 

Currently only a test module is provided, this is how to used it::

	$ curl -i "http://127.0.0.1:8888/localhost/testviahttp?filename=TEST&content=OK"
	HTTP/1.0 500 Internal Server Error
	Server: BaseHTTP/0.3 Python/2.7.5
	Date: Fri, 19 Dec 2014 14:49:46 GMT
	Content-Type: text/plain
	X-Content-Type-Options: nosniff
	
