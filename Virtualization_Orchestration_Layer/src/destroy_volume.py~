#!/bin/python

import sys
import os
import random
import rados, rbd
import json

import parsing
import create_vm
import libvirt
import create_volume
import main_file

def destroy(server,args):
	#global VOLUME_LIST
	print create_volume.VOLUME_LIST
	volume_id = int(args[0])
	if volume_id in create_volume.VOLUME_LIST:
		volume_name=str(create_volume.VOLUME_LIST[int(volume_id)])
	else:
		print "here\n"
		server.wfile.write(parsing.json_out({"status":0}))
	os.system('sudo rbd unmap /dev/rbd/%s/%s'%(main_file.POOL_NAME,volume_name))
	main_file.rbdInstance.remove(main_file.ioctx,volume_name)
	del create_volume.VOLUME_LIST[int(volume_id)]
	server.wfile.write(parsing.json_out({"status":1}))
