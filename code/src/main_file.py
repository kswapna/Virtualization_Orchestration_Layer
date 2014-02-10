#!/bin/python
import BaseHTTPServer
import sys
from SocketServer import ThreadingMixIn
#import clean
PORT_NUMBER = 80
import create_vm
import parsing
import sys
import os
import random
import rados, rbd
HOST_NAME='kswapna' #todo
radosConn=rados.Rados(conffile='/etc/ceph/ceph.conf')
radosConn.connect()
POOL_NAME="rbd"
if POOL_NAME not in radosConn.list_pools():
	radosConn.create_pool(POOL_NAME)
ioctx = radosConn.open_ioctx(POOL_NAME)
rbdInstance = rbd.RBD()


class Handler_class(BaseHTTPServer.BaseHTTPRequestHandler):
	def do_GET(self):
		""" Respond to a GET request."""
		if (self.path[:4] not in ["/vm/","/pm/","/vol"]) and (self.path[:7] != "/image/"):
			return
			self.send_error(404,"File Not Found")
		else:
			parsing.url_parse(self,self.path)

def main():
	phy_machines = sys.argv[1]
	image_file = sys.argv[2]
	vm_type = sys.argv[3]

	parsing.parse_pm(phy_machines)
	parsing.parse_image(image_file)
	create_vm.parse_types(vm_type)
	
	#Starting Server
	server_address = ('', PORT_NUMBER)
	httpd = BaseHTTPServer.HTTPServer(server_address, Handler_class)
	#global rbdInstance
	



	print "Server Started at port", PORT_NUMBER
#	httpd.serve_forever()
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		clean_server()
		pass
	httpd.server_close()



def clean_server():
	try:
		print "Cleaning all virtual machines"
		for vmid in parsing.vm_ki_info:
			v_name = parsing.vm_ki_info[vmid][0]
			machine_id = parsing.vm_ki_info[vmid][2]
	
			remote_machine = parsing.mac_user_ip[machine_id]
			remote_machine_add = remote_machine[0]+'@'+remote_machine[1]
			path = 'remote+ssh://'+remote_machine_add+'/system'
			print "Remote ssh to virtual machine location",path
			connection = libvirt.open(path)
			try:
				r = connection.lookupByName(v_name)
			except:
				print "The ",v_name,"virtual machine does not exist on any physical machine."
			if r.isActive():
				r.destroy()
			r.undefine()
#		del parsing.vm_ki_info[vmid]
		print "Virtual machines deleted and domain undefined."

	except Exception,e:
		print str(e)

VOLUME_LIST={}

'''def create(server,args):
	global VOLUME_LIST
	volume_name = args[0]
	volume_size = args[1]
	actual_size = int(float(volume_size)*(1024**2))
	rbdInstance.create(ioctx,str(volume_name),actual_size)
	os.system('sudo rbd map %s --pool %s --name client.admin'%(str(volume_name),str(POOL_NAME)));
	volume_id=len(VOLUME_LIST)
	VOLUME_LIST[int(volume_id)]=str(volume_name)
	print VOLUME_LIST
	server.wfile.write(parsing.json_out({"volumeid":volume_id}))
	#return jsonify(volumeid=volume_id)


def destroy(server,args):
	global VOLUME_LIST
	print VOLUME_LIST
	volume_id = int(args[0])
	if volume_id in VOLUME_LIST:
		volume_name=str(VOLUME_LIST[int(volume_id)])
	else:
		print "here\n"
		server.wfile.write(parsing.json_out({"status":0}))
		#return jsonify(status=0)
	os.system('sudo rbd unmap /dev/rbd/%s/%s'%(POOL_NAME,volume_name))
	rbdInstance.remove(ioctx,volume_name)
	del VOLUME_LIST[int(volume_id)]
	server.wfile.write(parsing.json_out({"status":1}))



'''





if __name__ == "__main__":
	main()
