#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from jdc_db import jdc_db
import jdc_url

def init(db):
	db.restart()
	db.init_db()

def item(db):
	failMax = 100
	i = db.getMeta('item_max')
	fail = 0
	try:
		while fail < failMax :
			name = jdc_url.getItem(i)
			if name:
				db.addItem(i,name)
				print ("{0}:{1}".format(i,name))
				fail = 0
			else:
				fail = fail + 1
			i = i + 1
	except KeyboardInterrupt:
			pass
	finally:		
		db.setMeta('item_max',i - fail)

def user(db):
	failMax = 100
	i = db.getMeta('user_max')
	fail = 0
	try:
		while fail < failMax :
			name = jdc_url.getUser(i)
			if name:
				db.addUser(i,name)
				print ("{0}:{1}".format(i,name))
				fail = 0
			else:
				fail = fail + 1
			i = i + 1
	except KeyboardInterrupt:
			pass
	finally:		
		db.setMeta('user_max',i - fail)
def buy(db):
	try:
		for user in db.getUser():
			time = db.getBuyUpdateTime(user)
			for item in jdc_url.getBuy(user,time):
				db.addBuy(user,item)
	except KeyboardInterrupt:
		db.setMeta('buy_max',user)
	db.setMeta('buy_max',99)

def start(db):
	init(db)
	item(db)
	user(db)
	buy(db)

def all(db):
	item(db)
	user(db)
	buy(db)

if __name__ == "__main__" :
	db = jdc_db()
	fl = {'init':init,'item':item,'user':user,'buy':buy,'start':start,'all':all}
	#try:
	fl[sys.argv[1]](db)
#	except:
#		pass
