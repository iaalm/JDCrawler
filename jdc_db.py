#!/usr/bin/python3
# -*- coding: utf-8 -*-

import mysql.connector
from datetime import datetime

class jdc_db:
	def __init__(self):
		self.conn = mysql.connector.connect(user = 'jd',password = 'jd',host = '192.168.1.2',db = 'jd')
	def __del__(self):
		self.conn.close()
	def updateSQL(self,sql):
		cur = self.conn.cursor()
		try:
			cur.execute(sql)
		except mysql.connector.Error as e:
			print("Mysql Error:{}".format(sql))
		finally:
			self.conn.commit()
			cur.close()
	def restart(self):
		self.updateSQL('drop database jd')
		self.updateSQL('create database jd')
		self.updateSQL('use jd')
	def init_db(self):
		self.updateSQL('create table meta (k char(10) primary key,v int)')
		self.updateSQL('create table category(id int primary key,name varchar(63),parent_id int,foreign key (parent_id) references category(id))') # cann't set foreign key'
		self.updateSQL('create table item (id int primary key,name varchar(63),lname varchar(255),category_id int,foreign key (category_id) references category(id))')
		self.updateSQL('create table user (id int primary key,name varchar(31),place varchar(15))')
		self.updateSQL('create table buy (uid int,iid int,foreign key (uid) references user(id),time datetime,foreign key (iid) references item(id))')
		self.updateSQL('insert into meta values ("item_max",100001)')
		self.updateSQL('insert into meta values ("user_max",100)')
		self.updateSQL('insert into meta values ("buy",99)')
		
	def addItem(self,iid,name):
		self.updateSQL('insert into item(id,name) values ({0},"{1}")'.format(iid,name))

	def addUser(self,uid,name):
		self.updateSQL('insert into user(id,name) values ({0},"{1}")'.format(uid,name))

	def addBuy(self,user,item):
		self.updateSQL('insert into buy(uid,iid,time) values ({0},{1},"{2}")'.format(user,item[0],item[1]))

	def getUser(self):
		i = self.getMeta('user_max')
		return range(i,100-1,-1)
		
	def getMeta(self,key):
		sql = 'select v from meta where k = "{0}"'
		cur = self.conn.cursor()
		cur.execute(sql.format(key))
		try:
			res = cur.fetchone()
			if res:
				return res[0]
			else:
				return None
		except mysql.connector.Error as e:
			print("Mysql Error")
		finally:
			self.conn.commit()
			cur.close()

	def setMeta(self,key,value):
		if self.getMeta(key):
			sql = 'update meta set v = {1} where k = "{0}"'
		else:
			sql = 'insert into meta(k,v) values ("{0}",{1})'
		self.updateSQL(sql.format(key,value))
	def getBuyUpdateTime(self,user):
		sql = 'select time from buy where uid = {0} order by time desc limit 1'
		cur = self.conn.cursor()
		try:
			cur.execute(sql.format(user))
			res = cur.fetchone()
			if res:
				return res[0]
			else:
				return datetime.min
		except mysql.connector.Error as e:
			print("Mysql Error")
		finally:
			cur.close()
		
			
if __name__ == "__main__" :
	db = jdc_db()
	db.restart()
	db.init_db()
	print(db.getMeta('user_max'))
	db.setMeta('user_max',2)
	print(db.getMeta('user_max'))
	db.addItem(1,'asdf')
	db.addUser(1,'asdf')
	print(db.getBuyUpdateTime(1))
	db.addBuy(1,1,datetime.now())
	print(db.getBuyUpdateTime(1))
