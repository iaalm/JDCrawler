#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
import json
import socket
from datetime import datetime
import urllib.request
import urllib.parse

def getItem(id):
	url = 'http://item.jd.com/{0}.html'.format(id)
	pattern = re.compile('<a href="'+ url + '" >([^<]*)</a>')
	urllib.request.socket.setdefaulttimeout(10)
	try:
		data = urllib.request.urlopen(url).read().decode('gbk')
	except urllib.error.HTTPError:
		return None
	except UnicodeDecodeError:
		data = ""
	except http.client.IncompleteRead:
		continue
	except socket.timeout:
		data = ""
		print("time out")
	name = pattern.search(data)
	if name:
		return name.group(1)
	else:
		return None
	
def getUser(user):
	url = 'http://me.jd.com/{0}.html'.format(user)
	pattern = re.compile('<div class="user-msg"><a href="/{}.html"><strong>([^<]*)</strong></a>'.format(user))
	urllib.request.socket.setdefaulttimeout(10)
	try:
		data = urllib.request.urlopen(url).read().decode('utf-8')
	except UnicodeDecodeError:
		data = ""
		print("decode error")
	except socket.timeout:
		data = ""
		print("time out")
	name = pattern.search(data)
	if name:
		return name.group(1)
	else:
		return None
	
def getPin(user):
	url = 'http://me.jd.com/{0}.html'.format(user)
	pattern = re.compile("'pin':'([a-z0-9]*)'")
	urllib.request.socket.setdefaulttimeout(10)
	try:
		data = urllib.request.urlopen(url).read().decode('utf-8')
	except UnicodeDecodeError:
		data = ""
		print("decode error")
	except socket.timeout:
		data = ""
		print("time out")
	name = pattern.search(data)
	if name:
		return name.group(1)
	else:
		return None
		
def getBuy(user,time):
	pin = getPin(user)
	url = 'http://me.jd.com/events'
	urllib.request.socket.setdefaulttimeout(10)
	flag = True
	count = 1
	while flag:
		data = {'pin':pin,'t':'{}'.format(count),'type':'0'}
		postData = urllib.parse.urlencode(data).encode('utf-8')
		req = urllib.request.Request(url,postData)
		req.add_header('Content-Type','application/x-www-form-urlencoded')
		try:
			data = urllib.request.urlopen(req).read().decode('utf-8')
		except UnicodeDecodeError:
			data = ""
			print("decode error")
		except socket.timeout:
			data = ""
			print("time out")
		data = data.replace("'",'"')
		jData = json.loads(data)
		flag = not jData['endFlag']
		for i in jData['data']:
			t = datetime.strptime(i['content']["properties"]["buyTime"],'%Y-%m-%d %H:%M:%S')
			if(t <= time):
				flag = False
				break
			item = i['content']['skuId']
			yield [item,t]
		count = count + 1


if __name__ == "__main__" :
	print(getUser(146543894))
#	for i in getBuy(146543894,datetime.min):
#		print(i)

