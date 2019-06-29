#!/usr/bin/python

### MODULES ###
#import datetime
#import os
import re
#import pprint
#
#import clipboard
#import attrdict
#
from doist2 import *
from datsun import *
from loch import *
#import xz
import kbench
#
#1:battery,2:pip,3:mygen,4:myopus

### VARIABLES ###
kbench.KBDEBUG = True
DEBUG = True
DEBUG = False

"""
[PROFILE OF TODOIST]
https://doist.com/about-us/

[2007] : The year Doist’s 1st product, Todoist was launched
[25] : Different countries where Doist’s 63 team members live and work
[146,000,000 and counting] : Projects Todoist & Todoist Business users have created
[1,320,252,000 and counting] : Tasks Todoist & Todoist Business users have completed
[725,000 and counting] : New threads Twist teams have started
[0] : Dollars of funding Doist has raised

[FOUNDATION YEAR]
2007	todoist
2011	wunderlist

[SOURCE]
https://github.com/Doist/todoist-python
"""

#

import click
import argparse

"""
@click.group()
def cli():
    pass

@cli.command()
def initdb():
    click.echo('Initialized the database')

@cli.command()
def dropdb():
    click.echo('Dropped the database')
"""

###########
###  ###
###########
def abc():
	prjnow = ''
	if os.path.exists(bin4tasks):
		prjnow = xz.bin2obj(bin4tasks)[-1]
#		pprint.pprint( prjnow ) #d
		if isinstance(prjnow, dict):
			prjnow = ''
	while 1:
		prompt = 'TODO(%s)> ' % prjnow
		args = input(prompt)
		args = re.sub(' +',' ',args)
		args = args.split(' ')
		if args[-1] == '': args.pop()
		cmd = args.pop(0)
		
		if cmd in ['q','quit','exit']:
			print( 'BYE' )
			break
		elif cmd == 'lists':
			lists()
		elif cmd == 'tasks':
			if not args == []:
				prjnow = args.pop(0)
			tasks(prjnow)
		elif cmd == 'add':
			arg = ' '.join(args)
			add(arg,False)
		elif cmd == 'fin':
			ns = args
			fin(ns)
		elif cmd == 'today':
			today()
		elif cmd == 'note':
			n = args.pop(0)
			mynote = ' '.join(args)
			note(n,mynote)
		elif cmd == 'other':
			pass

#

##### DIREKT ###############
if __name__=='__main__':
	abc()
	kbench.enfin()
