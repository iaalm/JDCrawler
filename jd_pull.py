#!/usr/bin/python3
# -*- coding: utf-8 -*-

from jddb import jddb
import jd


if __name__ == "__main__" :
	db = jddb()
	id = 1006547
	fail = 0
	while fail < 100 or id < 1000000 :
		name = jd.getItem(id)
		if name:
			db.addItem(id,name)
			print ("{0}:{1}".format(id,name))
			fail = 0
		else:
			fail = fail + 1
		id = id + 1
