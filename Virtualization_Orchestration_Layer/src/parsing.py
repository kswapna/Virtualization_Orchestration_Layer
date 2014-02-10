#!/bin/python
import json
import libvirt
import os
import create_vm
import destroy_vm
import printing
import create_volume
import destroy_volume
import main_file


mac_user_ip = {}
image_info  = {}
capacity_resources = {}
free_resources = {}
vm_ki_info = {}
all_vm_in_pm = {}
pm_capabilities = {}
vmid_start=1000
all_macs=0


def server_header(server,url):
	server.send_response(200)
	server.send_header("content-type","application/json")
	server.end_headers()
	pass

def json_out(out):
	return json.dumps(out,indent=4)


def get_id_for_vm(pmid):
	global vmid_start
	print "here"
	vmid_start = vmid_start + 1
	if pmid not in all_vm_in_pm:
		all_vm_in_pm[pmid] = []
		all_vm_in_pm[pmid].append(vmid_start)
	else:
		all_vm_in_pm[pmid].append(vmid_start)
	return vmid_start

def url_parse(server,url):
	print "details",vm_ki_info
	print url
	host_name = url
	if '?' in url:
		host_name, args = url.split('?')
	url_comps = host_name.split('/')
	print url_comps
	if 'create' in url_comps and 'vm' in url_comps:
		received_args = []
		arg_split = args.split('&')
		for i in xrange(0,3):
			received_args.append((arg_split[i].split('='))[1])
		print received_args
		create_vm.create(server,received_args)
	elif 'destroy' in url_comps and 'vm' in url_comps:
		received_args = []
		arg_split = args.split('=')
		received_args.append(arg_split[1])
		destroy_vm.destroy(server,received_args)
		pass
	elif 'query' in url_comps and 'vm' in url_comps:
		received_args = int(args.split('=')[1])
		printing.vm_query(server,received_args)


	elif 'query' in url_comps and 'volume' in url_comps:
		received_args = int(args.split('=')[1])
		printing.volume_query(server,received_args)

	elif 'types' in url_comps:
		printing.print_types(server)
	
	elif 'list' in url_comps:
		#print "here"
		printing.print_images(server)

	elif 'create' in url_comps and 'volume' in url_comps:
		received_args = []
		arg_split = args.split('&')
		for i in xrange(0,2):
			received_args.append((arg_split[i].split('='))[1])
		print received_args
		print "yayayayaya"
		create_volume.create(server,received_args)
		#main_file.create(server,received_args)

	elif 'destroy' in url_comps and 'volume' in url_comps:
		received_args = []
		arg_split = args.split('=')
		received_args.append(arg_split[1])
		destroy_volume.destroy(server,received_args)
		#main_file.destroy(server,received_args)
		pass

	elif 'attach' in url_comps and 'volume' in url_comps:
		received_args = []
		arg_split = args.split('&')
		for i in xrange(0,2):
			received_args.append((arg_split[i].split('='))[1])
		print received_args
		print "yayayayaya"
		attach_volume.attach(server,received_args)

	elif 'detach' in url_comps and 'volume' in url_comps:
		received_args = []
		arg_split = args.split('=')
		received_args.append(arg_split[1])
		detach_vm.detach(server,received_args)
		pass


#http://server/volume/create?=name=test-volume&size=10
#http://server/volume/destroy?volumeid=volumeid

	

def get_resource_info(m,mid):
	path  = 'remote+ssh://'+m[0]+'@'+m[1]+'/system'
	try:
		connection = libvirt.open(path)
	except:
		print "Could not open connection to machine",m[0]+'@'+m[1]
		global all_macs
		all_macs-=1
		return
	try:

		os.system("ssh "+m[0]+'@'+m[1]+ " -C 'df -h --total | grep total' > disk") 
		os.system("ssh "+m[0]+'@'+m[1]+ " -C ' free -m | head -n2 | tail -n1 ' > sp1") 
		os.system("ssh "+m[0]+'@'+m[1]+ " -C ' nproc ' > cpu1") 
		os.system("ssh "+m[0]+'@'+m[1]+ " -C ' grep flags /proc/cpuinfo | grep \" lm \"' > hard")
	except Exception,e: 
		print str(e) 
		return
	pm_info = connection.getInfo() 

	sp = open('disk')    #  disk
	content = sp.read() 
	content = content.split() 
	print content
	sp.close() 


	de=open('sp1')        #ram
	fram=de.read() 
	print fram.split() 
	print fram,fram.split()[3] 
	ram=int(fram.split()[3]) 
	de.close() 


	de=open("cpu1")       #cpu
	cpu=int(de.read()) 
	de.close()
	
	o=open('hard')        # check_hardware
	hardw=o.read() 
	if (hardw==''): 
		hardd=32
	else: 
		hardd=64 
	o.close()

 
	capacity_resources[mid]=[cpu,ram,int(content[1][:-1]),hardd] 
	free_resources[mid]=[cpu,ram,int(content[1][:-1]),hardd] 
	print "These are the free resources of this machine address",free_resources[mid],mid,m[0]+"@"+m[1]





#'''		os.system("ssh "+m[0]+'@'+m[1]+ " -C 'df -h --total | grep total' > disk")
#	except Exception,e:
#		print str(e)
#
#	node_info = connection.getInfo()
#	c_ram = node_info[1]		#capacity of ram
#	c_cpu = node_info[7] 		#number of cpu's
#	diskfile = open('disk')
#	content = diskfile.read()
#	content = content.split()
#	print content
#	c_memory = int(content[1][:-1])
#	diskfile.close()
#
#	capacity_resources[mid] = [ c_cpu, c_ram, c_memory]
#	free_resources[mid] = [ c_cpu, c_ram, c_memory]
#
#	print "frree",free_resources[mid],mid
#	print c_cpu, c_ram
#
#	print "MACHINE",free_resources[mid],mid
#
#'''



machineid = 100
def parse_pm(ff):
	global mac_user_ip
	f = open(ff,'r')
	global all_macs	
	global machineid
	for l in f.readlines():
		all_macs+=1
		line=l.split('@')
		mac_user_ip[machineid]=line
		line[1]=line[1].rstrip('\n')
		get_resource_info(line,machineid)
		machineid=machineid+1
	f.close()
	pass

imageid = 1
def parse_image(ff):
	global image_info
	global imageid
	f = open(ff,'r')
	for l in f.readlines():
		line=l.split(':')
		user,ip=line[0].split('@')
		loc=line[1].split('/')
		name=loc[len(loc)-1]
		name=name.rstrip('\n')
		loc=line[1]
		loc=loc.rstrip('\n')
		global image_info
		image_info[imageid]=[user,ip],[name],loc
		print "yeah",image_info[imageid]
		imageid=imageid+1
	f.close()

