#!/usr/bin/python

### MODULES ###
import datetime as dt
import re
#import pprint
#
#import clipboard
#import attrdict
#
from datsun import *
from loch import *
import xz
import xt
import kbench
import todoist
#
#1:battery,2:pip,3:mygen,4:myopus

### VARIABLES ###
kbench.KBDEBUG = True
DEBUG = True
DEBUG = False
xz.binary = True
#
cnf = xz.yml2cnf('doist.yml')
api = todoist.TodoistAPI(cnf.APIToken)
bin4lists = labomi + 'doist_lists.bin'
bin4tasks = labomi + 'doist_tasks.bin'
bin4prj   = labomi + 'doist_prjnow.txt'


#

##################
### SUBROUTINE ###
##################
def zt2dt(x):
#	tag = '2016-11-05T14:15:44.570Z'
	x = dateutil.parser.parse(x)
	x = dt.datetime(x.year,x.month,x.day,x.hour,x.minute,x.second)
	return x

def setdate(x):
	n = int(x)
	tag = xt.heute(False)
	if n < 100:
		res = tag + dt.timedelta(days=n)
	elif n < 1300:
		res = '%04d' % n
		res = [ res[0:2], res[2:4] ]
		res = dt.date( tag.year, int(res[0]), int(res[1]) )
		if res < tag:
			res = dt.date( res.year + 1, res.month, res.day )
	return res

def getpid(prj=''):
	if prj == '':
		prj = xz.txt2str(bin4prj)
	prjs = xz.bin2obj(bin4lists)
	return prjs[prj]

def gettid(prj):
	prjs = xz.bin2obj(bin4tasks)
	return prjs[prj]

#

#############
### LISTS ###
#############
def lists():
	lis = api.state['projects']
	res = {}
	api.sync()
	for dic in lis:
		id = dic['id']
		name = dic['name']
		res[name] = id
	#
	ausgabe = bin4lists.replace('.txt','.bin')
	xz.dic2txt(res,ausgabe)
	xz.obj2bin(res,bin4lists)
	xz.show(res)

#

#############
### TASKS ###
#############
def tasks(prj,see=True):
	if isinstance(prj, str):
		pid = getpid(prj)
	elif isinstance(prj, int):
		pid = prj
	api.sync()
	data = api.projects.get_data(pid)
	res = []

	headers = adic({
		'n':'n',
		'id':'tid',
		'content':'title',
		'date_added':'cdate',
		'due_date':'ddate',
	})

	for dic in data['items']:
		cdate = dic['date_added']
		ddate = dic['due']['date']
		dic['date_added'] = zt2dt(dic['date_added'])
		dic['due_date'] = xt.s2d(dic['due']['date'])
		dic['n'] = 0
		#
		info = api.items.get(id)
		try:
			dic['notes'] = info['notes'][0]
		except TypeError:
			dic['notes'] = ''
		#
		tmp = {}
		for vor,nach in headers.items():
			tmp[nach] = dic[vor]
		tmp['notes'] = dic['notes']
		res.append(tmp)

	n = 0
	res = sorted(res,key=lambda d:d['ddate'])
	for dic in res:
		n += 1
		dic['n'] = n

	### AUSGABE ###
	res.append(prj)
	xz.obj2bin(res,bin4tasks)
	res.pop()
	if see == True:
		#
		for dic in res:
			d = dic['cdate']
			dic['cdate'] = dt.date(d.year,d.month,d.day)
		tbl = xz.ldic2tbl(res,list(headers.values()))
		xz.show(tbl)

#

###########
### ADD ###
###########
def add(arg,see=True):
	if os.path.exists(arg):
		addtext(arg)
	else:
		addone(arg,see)

def addone(msg,see=True):
	m = re.match('^(\d+) ',msg)
	if m:
		tag = m.group(1)
		msg = msg.replace(tag+' ','')
		tag = setdate(tag)
		tag = str(tag)
	else:
		tag = xt.heute(False) + dt.timedelta(days=1)
	tag = str(tag)
	
	m = re.match('^(.+?) ',msg)
	tmp = m.group(1)
	if tmp in xz.bin2obj(bin4lists).keys():
		prj = tmp
		pid = getpid(tmp)
		tmp2 = len(tmp)
		msg = msg[tmp2+1:]
	else:
		prj = ''
		pid = getpid()
	
	api.items.add(msg,project_id=pid,due={'date':tag})
	api.commit()
	if see == True: tasks(pid)

def addtext(txt):
	lis = xz.txt2lis(txt)
	for x in lis: addone(x,False)
	pid = getpid()
	tasks(pid)

#

###########
### FIN ###
###########
def fin(*ns):
	pid = getpid()
	if isinstance(ns[0], list):
		ns = ns[0]
	else:
		ns = flatten(ns)
	ns = [ int(n) for n in ns ]
	db = xz.bin2obj(bin4tasks)
	db.pop()
	ddic = xz.ldic2ddic(db,'n')

#	pprint.pprint( db ) #d
	tids = [ ddic[n]['tid'] for n in ns ]
	for tid in tids:
		itm = api.items.get_by_id(tid)
		itm.complete()
		api.commit()
#	tasks(pid)

def delay(plus,*ns):
	pid = getpid()
	ns = flatten(ns)
	ns = [ int(n) for n in ns ]
	db = xz.bin2obj(bin4tasks)
	db.pop()
	ddic = xz.ldic2ddic(db,'n')
	tag = setdate(plus)

	tids = [ ddic[n]['tid'] for n in ns ]
	for tid in tids:
		itm = api.items.get_by_id(tid)
		itm.update(due={'date':tag})
		api.commit()
#	tasks(pid)

def today(prj=''):
#	pid = getpid(prj)
#	tasks(pid,False)
	db = xz.bin2obj(bin4tasks)
	db.pop()
	res = []
	tag = xt.heute(False)
#	tag = tag + dt.timedelta(days=-5)
#	print( tag )
	for dic in db:
		due = dic['ddate']
		if due <= tag:
			res.append(dic)
#		print( dic ) #d
	headers = 'n/tid/title/cdate/ddate'
	headers = headers.split('/')
	for dic in res:
		d = dic['cdate']
		dic['cdate'] = dt.date(d.year,d.month,d.day)
	tbl = xz.ldic2tbl(res,headers)
	xz.show(tbl)

#def deltext():
#def makenote():
#def get():

#

############
### NOTE ###
############
def note(n,mynote=''):
	db = xz.bin2obj(bin4tasks)
	prj = db.pop()
	dic = db[n+1]
	tid = dic['tid']
	itm = api.items.get(tid)
	#
	if os.path.exists(mynote):
		mynote = xz.txt2str(mynote)
	#
	if mynote == '':
		print( itm['notes'] )
	else:
		if itm['notes'] == []:
			note = api.notes.add(tid,mynote)
			api.commit()
		else:
			nid = itm['notes'][0]['id']
			note = api.notes.get_by_id(nid)
			note.update(content=mynote)
			api.commit()
	itm = api.items.get(tid)
	print( '<TITLE>',itm['item']['content'] )
	print( '<NOTES>' )
	print( itm['notes'][0]['content'] )

#def stat():

#

##### DIREKT ###############
if __name__=='__main__':
#	lists()
#	tasks('ag')
	add('0622 wart Test task from CLI 35')
#	delay(704,5,6)
#	today('ag')
#	note(2,'a.txt')
	kbench.enfin()
