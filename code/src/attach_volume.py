#!/bin/python
import destroy_vm
import create_vm
import parsing
import main_file
import create_volume
import destroy_volume
import json
import rados, rbd 
import os
import libvirt
def json_out(out):
	  return json.dumps(out,indent=4)

def attach(server,arguments):
	vid=int(arguments[0])
	volid=int(arguments[1])
	machid=parsing.vm_ki_info[vid][2]
	name=parsing.mac_user_ip[machid]
	m_addr = name[0]+'@'+name[1]
	path = 'remote+ssh://'+m_addr+'/system'
	vm_na=parsing.vm_ki_info[vid][0]
	try:
	       connect = libvirt.open(path)
	       dom=connect.lookupByName(vm_na)
	       f=open("/etc/ceph/ceph.conf",'r')
	       l=f.readlines()
	       l1=f.split("\n")
	       host=l1[2].split('=')[1]
	       f.close()
	       xml="<disk type='network' device='disk'>   \
	        	<source protocol='rbd' name='rbd/"+resource_dis.VOLUME_LIST[volid]+"'> \
	                <host name="+str(a)+" port='6789'/> \
			 </source> \
			 <target dev='hdb' bus='virtio'/>  \
			</disk>"
	       dom.attachDevice(xml)
	       server.wfile.write(json_out({"status":1}))
	       create_volume.VOL_status[volid]=vid
	except:
	       server.wfile.write(json_out({"status":0}))
