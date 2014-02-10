#!/bin/python
import libvirt
import json
types_info = []
fname = ''
import parsing
import subprocess
import os
##<source file='/var/lib/libvirt/images/"+str(vmlocate)+"'/>   \
##			<source file='"+str(vmlocate)+"'/>		\
def create_xml(vm_name,pm_capabilities,vmlocate,hyper_type,vmid,arch):
	xml = "<domain type="+str(arch[1])+  		\
			"><name>" + vm_name + "</name>				\
			<memory >"+str(pm_capabilities[2]*test_number/1024)+"</memory>					\
			<vcpu>"+str(pm_capabilities[1])+"</vcpu>						\
			<os>							\
			<type arch='"+arch[2]+"' machine='pc'>hvm</type>		\
			<boot dev='hd'/>					\
			</os>							\
			<features>						\
			<acpi/>							\
			<apic/>							\
			<pae/>							\
			</features>						\
			<on_poweroff>destroy</on_poweroff>			\
			<on_reboot>restart</on_reboot>				\
			<on_crash>restart</on_crash>				\
			<devices>							\
			<emulator>"+str(arch[0])+"</emulator>	\
			<disk type='file' device='disk'>			\
			<driver name="+str(arch[1])+" type='raw'/>			\
			<source file='"+str(vmlocate)+"'/>		\
			<target dev='hda' bus='ide'/>				\
			<address type='drive' controller='0' bus='0' unit='0'/>	\
			</disk>							\
			</devices>						\
			</domain>"
	return xml
	
test_number = 100000	
def create(server,args):
	parsing.server_header(server,args)
	if(1):
		vm_name = str(args[0])						# name of vm
		vm_type = int(args[1])						# tid of vm
		image_type = int(args[2])					# vm id
		type_properties = types_info[vm_type-1]  		## from types file, requirements of Virtual Machine
		images_list = parsing.image_info[image_type]  #dictionary
		
		i_name=images_list[1][0]
		h=0
		if "_64" in i_name:
			h=64
		else:
			h=32

		m,avai_pm_id = find_machine(type_properties,h)			# Get the physical machine to host the VM

		if avai_pm_id == 0:
			print "capacity::",parsing.capacity_resources
			print "In need of now::",type_properties
			print "free::",parsing.free_resources
			print "NO MACHINES AVAILABLE FOR THE TASK"
			return
		print "Machine id",avai_pm_id,"selected"
		machine_addr = m[0]+'@'+m[1]

		images_list = parsing.image_info[image_type]  #dictionary
		location_user = images_list[0][0]+'@'+images_list[0][1]
		location_image = images_list[2]			#Find the location of image
		
		print "images_list",images_list
		print "where",location_user
		print "what",location_image
		print "image_name",images_list[1][0]
		namefile=images_list[1][0]
		user_loc=m[0]+"@"+m[1]
		print "user is"+"./"+images_list[1][0]
		print "where to ?"+':'.join([user_loc,"/home/"+m[0]+"/Desktop"])

		if not os.path.isfile('./'+images_list[1][0]):
#			p = subprocess.Popen(["ssh",location_user])
			print machine_addr,location_image
			try:
				print "command run:: loc to you::scp",':'.join([location_user,images_list[2]]),"."
				subprocess.call(["scp",':'.join([location_user,images_list[2]]),"."])
				
				#subprocess.call(["scp",location_user+images_list[2]," ."])
			except:
				print "not able to scp to your machine"
		try:
			print "command run :: ur to user ::scp","./"+images_list[1][0],':'.join([user_loc,"/home/"+m[0]])
			subprocess.call(["scp","./"+images_list[1][0],':'.join([user_loc,"/home/"+m[0]+"/Desktop"])])
			
			#subprocess.call(["scp","./"+images_list[1][0],m[0]+"@"+m[1]+":/home/"+m[0]])
		except:
			print "not able to scp to user's machine"
				
			#print "scp",':'.join([location_user,location_image]),':'.join([machine_addr,'/var/lib/libvirt/images/'+images_list[1][0]])
#			p.kill()
		#subprocess.call(["scp",':'.join([location_user,location_image]),'/var/lib/libvirt/images/'])



		path = 'remote+ssh://'+m[0]+'@'+m[1]+'/system'
		print "Ssh to machine location::",path
		try:
			connection = libvirt.open(path)
		except:
			print "Could Not Open Connection\n"
			return

		system_info = connection.getCapabilities()	#get PM capabilities
		node_info = connection.getInfo()
		print "HERE I AM",node_info[1],node_info[2]
		emulator_path = system_info.split("emulator>")
		
		emulator_path = emulator_path[1].split("<")[0]	#location of xen/qemu
		
		emulator1 = system_info.split("<domain type=")
	
		emulator1 = emulator1[1].split(">")[0]		#emulator present xen/qemu
		
		arch_type = system_info.split("<arch>")
		arch_type = arch_type[1].split("<")[0]

		parsing.pm_capabilities[avai_pm_id] = [emulator_path ,emulator1, arch_type] #machine id as key--- stores physical machine arch details
#		print emulator_path ,emulator1, arch_type
		arch = parsing.pm_capabilities[avai_pm_id]

		hyper_type = connection.getType().lower()
		print "QEMU ?? or XEN??",hyper_type
		#type_properties[2] = (type_properties[2]*test_number)/1024

		#xml = create_xml(vm_name, type_properties,"/home/chitra/Downloads/Vm-linux.img",hyper_type,image_type,arch)  ## type_properties has tid,cpu,ram,disk
		xml = create_xml(vm_name, type_properties,"/home/"+m[0]+"/Desktop/"+images_list[1][0],hyper_type,image_type,arch)  ## type_properties has tid,cpu,ram,disk
#		print xml
	
		connect_xml = connection.defineXML(xml)
		try:
			connect_xml.create()
			print "********************** CREATED A VM :D *********************" 
			vmachine_id = parsing.get_id_for_vm(avai_pm_id)	#Get Virtual Machine unique ID -- avai_pm_id is machineid!
			parsing.vm_ki_info[vmachine_id] = [vm_name, type_properties, avai_pm_id,vm_type]			#store VM vs Phy machine details..

#			print "Here are details",parsing.vm_ki_info,vmachine_id
			server.wfile.write(parsing.json_out({"vmid":vmachine_id}))
			parsing.free_resources[avai_pm_id][0] -= type_properties[1]
			parsing.free_resources[avai_pm_id][1] -= type_properties[2]
			parsing.free_resources[avai_pm_id][2] -= type_properties[3]
			#type_properties[2] = (type_properties[2]*1024)/test_number
			
			#types_info[vm_type-1][2]=types_info[vm_type-1][2]*1024/test_number
		except Exception,e:
			#type_properties[2] = (type_properties[2]*1024)/test_number
			#parsing.free_resources[avai_pm_id][0] += type_properties[1]
			#parsing.free_resources[avai_pm_id][1] += type_properties[2]
			#parsing.free_resources[avai_pm_id][2] += type_properties[3]		
			
			print str(e)
			server.wfile.write(parsing.json_out({"vmid":0}))


		print "capacity::",parsing.capacity_resources
		print "using now::",type_properties
		print "free::",parsing.free_resources
		

	else:
		server.wfile.write(parsing.json_out({"vmid":0}))
	
	
def parse_types(ff):
	f=open(ff,'r')
	global types_info
	global fname
	fname=ff
	f = open(ff)
	Typefile = json.load(f)
	print Typefile
	Typefile = Typefile['types']
	for x in Typefile:
		l = []
		for y in x:
			l.append(x[y])
		# swap cpu and disk
		cc=l[1]
		l[1]=l[3]
		l[3]=cc
		types_info.append(l)


current_pointer=100
def find_machine(ins_type,h): 
	num=parsing.all_macs
	cpu_chk = ins_type[1]	
	ram_chk = ins_type[2]	
	disk_chk = ins_type[3]
	print "type to be made::",ins_type 
	#global all_macs 
	global current_pointer 
	#all_macs=num 
	#print all_macs,current_pointer 
	tocheck=current_pointer
	current_pointer+=1 
	print "starting form here" , current_pointer 
	if current_pointer >= num+100:
		current_pointer=100
	while 1:
		if current_pointer >= num+100:
			current_pointer=100
		print "cpu_chk::",parsing.free_resources[current_pointer][0],cpu_chk
		print "ram_chk::",parsing.free_resources[current_pointer][1],ram_chk
		print "disk_chk::",parsing.free_resources[current_pointer][2],disk_chk
		if parsing.free_resources[current_pointer][0] >= cpu_chk and parsing.free_resources[current_pointer][1] >= ram_chk and parsing.free_resources[current_pointer][2] >= disk_chk and parsing.free_resources[current_pointer][3]>=h:
			#parsing.free_resources[current_pointer][0] -= cpu_chk
			#parsing.free_resources[current_pointer][1] -= ram_chk
			#parsing.free_resources[current_pointer][2] -= disk_chk 
			return parsing.mac_user_ip[current_pointer],current_pointer 
		if current_pointer==tocheck:
			return 0,0
			break 
		current_pointer+=1
