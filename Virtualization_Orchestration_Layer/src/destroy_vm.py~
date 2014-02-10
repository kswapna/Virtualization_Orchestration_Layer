#!/bin/python
import parsing
import create_vm
import libvirt
test_number=100000

def destroy(server,attributes):
	parsing.server_header(server,attributes)
	try:
		vmid = int(attributes[0])
		print "Deleting virtual machine with id",vmid
		print "iski pm::",parsing.vm_ki_info[vmid][2]
		v_name = parsing.vm_ki_info[vmid][0]
		machine_id = parsing.vm_ki_info[vmid][2]

		iski_pm = parsing.mac_user_ip[machine_id]
		iski_pm_add = iski_pm[0]+'@'+iski_pm[1]
		
		path = 'remote+ssh://'+iski_pm_add+'/system'
		print "Delete from machine ::",path
		connection = libvirt.open(path)
		try:
			r = connection.lookupByName(v_name)
		except:
			print "The said virtual machine does not exist on any physical machine."

		pp=parsing.vm_ki_info[vmid][3]			#store VM vs Phy machine details..
		iske_pm_ki_id=parsing.vm_ki_info[vmid][2]			#store VM vs Phy machine details..
		print "vm_type=====",pp
		print "cpu",parsing.free_resources[iske_pm_ki_id][0],create_vm.types_info[pp-1][1]
		print "ram",parsing.free_resources[iske_pm_ki_id][1],create_vm.types_info[pp-1][2]
		print "disk",parsing.free_resources[iske_pm_ki_id][2],create_vm.types_info[pp-1][3]
		
		parsing.free_resources[iske_pm_ki_id][0]+=create_vm.types_info[pp-1][1]
		parsing.free_resources[iske_pm_ki_id][1]+=create_vm.types_info[pp-1][2]
		parsing.free_resources[iske_pm_ki_id][2]+=create_vm.types_info[pp-1][3]
		#free_resources[iske_pm_ki_id][2]*1024/test_number+=types_info[pp-1][3]


		
		if r.isActive():
			r.destroy()
		r.undefine()

		print "capacity::",parsing.capacity_resources
		print "deleting now::",create_vm.types_info[pp-1]
		print "free::",parsing.free_resources


		del parsing.vm_ki_info[vmid]

		

		print "VM is Deleted an undefined"

		server.wfile.write(parsing.json_out({"status":1}))
	except:
		server.wfile.write(parsing.json_out({"status":0}))


