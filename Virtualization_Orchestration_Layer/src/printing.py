#!/bin/python
import parsing
import libvirt
import create_vm
import json
import create_volume


def volume_query(server,attributes):
	parsing.server_header(server,attributes)
	try:
		vmid=(int)attributes
		print "Details of Volumes with id",vmid
		v_name = create_volume.VOLUME_LIST[vmid]
		v_size = create_volume.VOL_size[vmid]
		v_status = create_volume.VOL_status[vmid]
		if v_status==0:
			print "{volumeid:",vmid,", name: ",v_name,"size: ",v_size,"status: available"
			server.wfile.write(parsing.json_out({"vmid":vmid, "name":v_name, "size: ",v_size,"status: available"}))
		elif v_status==1:
			print "error : It is deleted"
			server.wfile.write(parsing.json_out({"error:does not exist":vmid}))
		elif v_status>1 :
			print "{vmid:",vmid,", name: ",v_name,"size: ",v_size,"status: attached","vmid :",v_status
			server.wfile.write(parsing.json_out({"vmid":vmid, "name":v_name, "size: ",v_size,"status: attached","vmid :",v_status}))

	except Exception,e:
		print str(e)
		print "error : It does not exist"
		server.wfile.write(parsing.json_out({"error:does not exist":vmid}))
		server.wfile.write(parsing.json_out({"status":0}))
#VOLUME_LIST={}
#VOL_size={}
#VOL_status={}
	


def print_images(server):		#images list
	parsing.server_header(server,200)
	print_image = []
	image = []
	for keys in parsing.image_info:
		image = [keys,parsing.image_info[keys][1]]
		print_image.append(image)
	server.wfile.write(parsing.json_out({"images":print_image}))	
	pass



def print_types(server):
	parsing.server_header(server,200)
	try:
		f = create_vm.fname
		fopen = open(f)
		server.wfile.write(parsing.json_out(json.load(fopen)))
	except Exception,e:
		print str(e)
		server.wfile.write(parsing.json_out({"status":0}))


def vm_query(server,attributes):
	parsing.server_header(server,attributes)
	try:
		vmid = int(attributes)
		print "Details of virtual machine with id",vmid
		v_name = parsing.vm_ki_info[vmid][0]
		machine_id = parsing.vm_ki_info[vmid][2]
		mtype = parsing.vm_ki_info[vmid][3]
		print "{vmid:",vmid,", name: ",v_name,"instance_type: ",machine_id,"pmid: ",mtype
		server.wfile.write(parsing.json_out({"vmid":vmid, "name":v_name, "instance_type": mtype, "pmid": machine_id}))
	except Exception,e:
		print str(e)
		server.wfile.write(parsing.json_out({"status":0}))



