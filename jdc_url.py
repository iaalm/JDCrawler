#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
import urllib.request
import urllib.parse

def getItem(id):
	url = 'http://item.jd.com/{0}.html'.format(id)
	pattern = re.compile('<a href="'+ url + '" >([^<]*)</a>')
	urllib.request.socket.setdefaulttimeout(10)
	try:
		data = urllib.request.urlopen(url).read().decode('gbk')
	except UnicodeDecodeError:
		data = ""
	except socket.timeout:
		data = ""
		print("time out")
	name = pattern.search(data)
	if name:
		return name.group(1)
	else:
		return None

if __name__ == "__main__" :
	print(getItem(125342))

