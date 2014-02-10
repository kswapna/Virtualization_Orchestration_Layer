#!/bin/python
import sys
import os
import random
import rados, rbd
import json

import libvirt
import json
import parsing
import subprocess
import os
import main_file
VOLUME_LIST={}
VOL_size={}
VOL_status={}
vol_id=1234
#0-- availa
#1-- deleted
#if status > 1 then its an vid i.e. it is attached to a vm cuz vmids start from 1000.

def create(server,args):
	global VOLUME_LIST
	volume_name = args[0]
	volume_size = args[1]
	actual_size = int(float(volume_size)*(1024**2))
	try:
		main_file.rbdInstance.create(main_file.ioctx,str(volume_name),actual_size)
		os.system('sudo rbd map %s --pool %s --name client.admin'%(str(volume_name),str(main_file.POOL_NAME)));
		volume_id=vol_id
		vol_id=vol_id+1
		VOLUME_LIST[vol_id]=str(volume_name)
		VOL_size[vol_id]=actual_size
		VOL_status[vol_id]=0
		print VOLUME_LIST
		server.wfile.write(parsing.json_out({"volumeid":volume_id}))
	except:
		server.wfile.write(parsing.json_out({"volumeid":0}))		

