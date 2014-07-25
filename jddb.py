#!/usr/bin/python3
# -*- coding: utf-8 -*-

import mysql.connector

class jddb:
	def __init__(self):
		self.conn = mysql.connector.connect(user = 'jd',password = 'jd',host = '192.168.1.2',db = 'jd')
	def __del__(self):
		self.conn.close()
	def addItem(self,id,name):
		try:
			sql = 'insert into item value ({0},"{1}")'
			cur = self.conn.cursor()
			cur.execute(sql.format(id,name))
			self.conn.commit()
			cur.close()
		except mysql.connector.Error as e:
			print("Mysql Error")

