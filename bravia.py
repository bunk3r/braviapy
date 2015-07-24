#!/usr/bin/env python
import sys, getopt
import urllib2, base64, uuid
import json
# wol + SSDP
import socket


###########################################################
#
#	GLOBAL VAR & DEFINITIONS
#
###########################################################
SONYIP = "192.168.1.72"
#CLIENTID = "bunk3r:"+str(uuid.uuid4())
#CLIENTID = "bunk3r:a484c257-c10e-46b8-8ab2-411dcdcbdeea"
#NICKNAME = "bunk3r (braviapy)"
CLIENTID = 'TVSideView:eb1214c4-321d-47ab-948d-9b9ebb36354e'
NICKNAME = 'Nexus 7 (TV SideView)'


# B0:10:41:72:C6:83
macaddr = "B0:10:41:72:C6:83"

_AUTHORIZATION = json.dumps(
{	"method":"actRegister",
	"params":[
	{
		"clientid":CLIENTID,
		"nickname":NICKNAME,
		"level":"private"},[
		{
			"value":"yes",
			"function":"WOL"}
		]
	],
	"id":1,
	"version":"1.0"}
)


###########################################################
#
#	Usage
#
###########################################################
def usage ():
	print("Usage: %s (-h|--help) (-p|--pin <pin>) (-v|--verbose) (-d|--discover) (-w|--wol <macaddr>) (-r|--remote)" % sys.argv[0])

	
###########################################################
#
#	GET IP
#
###########################################################
def get_local_IP():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(('8.8.8.8', 0))  # connecting to a UDP address doesn't send packets
	local_ip_address = s.getsockname()[0]
	return local_ip_address
	
	
###########################################################
#
#	SEND XML UPNP SUBSCRIBE
#
###########################################################
def bravia_upnp_subscribe( ip, port, url):

	method = 'SUBSCRIBE'
	req = urllib2.Request('http://'+ip+':'+port+'/upnp/event/'+url)  
	req.add_header('NT', 'upnp:event')
	req.add_header('Callback', '<http://'+get_local_IP()+':8000/>')
	req.add_header('Timeout', 'Second-1800')

	req.get_method = lambda: method
	
	try:
		response = urllib2.urlopen(req)
	except urllib2.HTTPError, e:
		print "[W] HTTPError: " + str(e.code)
		
	except urllib2.URLError, e:
		print "[W] URLError: " + str(e.reason)

	else:
		for h in response.info().headers:
			if h.find("SID") > -1:
				sid=h			
		if sid:
			sid = response.headers['SID']
			return sid
		return None
		
		
###########################################################
#
#	SEND XML UPNP UNSUBSCRIBE
#
###########################################################
def bravia_upnp_unsubscribe( ip, port, url, sid):

	method = 'UNSUBSCRIBE'
	req = urllib2.Request('http://'+ip+':'+port+'/upnp/event/'+url)  
	req.add_header('SID', sid)
	req.get_method = lambda: method
	
	try:
		response = urllib2.urlopen(req)
	except urllib2.HTTPError, e:
		print "[W] HTTPError: " + str(e.code)
		
	except urllib2.URLError, e:
		print "[W] URLError: " + str(e.reason)

	else:
		tree = response.info().headers, response.read()
		#print tree
		return tree



###########################################################
#
#	SEND UPNP REQUEST
#
###########################################################
def bravia_upnp_req( ip, port, url, params, service="urn:schemas-upnp-org:service:RenderingControl:1", action="SetMute"):

	#action = 'SetMute'
	#service = 'urn:schemas-upnp-org:service:RenderingControl:1'
	
	soap = 	'<?xml version="1.0"?>'\
		'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">'\
		'<s:Body>'\
		'<m:%s xmlns:m="%s">'\
		'%s'\
		'</m:%s>'\
		'</s:Body>'\
		'</s:Envelope>' % (action, service, params, action)
	
	host = ip+":"+port
	headers = {
		'Host':host,
		'Content-length':len(soap),
		'Content-Type':'text/xml; charset="utf-8"',
		'SOAPAction':'"%s#%s"' % (service, action)
	}
	method = "POST"

	req = urllib2.Request('http://'+ip+':'+port+'/upnp/control/'+url, data=soap, headers=headers)
	req.get_method = lambda: method
	
	#print req.headers
	#print req.data
	
	try:
		response = urllib2.urlopen(req)
	except urllib2.HTTPError, e:
		print "[W] HTTPError: " + str(e.code)
		
	except urllib2.URLError, e:
		print "[W] URLError: " + str(e.reason)
		#sys.exit(1)
	else:
		tree = response.info().headers, response.read()
		#print tree
		return tree


		
###########################################################
#
#	Build JSON commands
#
###########################################################
def jdata_build(method, params):
	if params:
		ret =  json.dumps({"method":method,"params":[params],"id":1,"version":"1.0"})
	else:
		ret =  json.dumps({"method":method,"params":[],"id":1,"version":"1.0"})
	return ret

	

###########################################################
#
#	Remote Control
#
###########################################################
def remote_control(cookie, verbose = False):
	# get Remote IRCC commands
	print "[*] getRemoteControllerInfo"
	resp = bravia_req_json(SONYIP, "80", "sony/system", jdata_build("getRemoteControllerInfo", ""), cookie);
	data = resp['result'][1]
	commands = {}
	for item in data:
		if verbose:
			print item['value'], item['name']
		commands[item['name']] = item['value']

	print "[p] PowerOff:", commands['PowerOff']
	print "[V] VolumeUp:", commands['VolumeUp']
	print "[v] VolumeDown", commands['VolumeDown']
	print "[C] ChannelUp", commands['ChannelUp']
	print "[c] ChannelDown", commands['ChannelDown']
	for num in range(0,10):
			if commands['Num'+str(num)]:
				print "["+str(num)+"] Num"+str(num)+":", commands['Num'+str(num)]
	while True:
		num = raw_input()
		if num == '0':
			resp = bravia_req_ircc(SONYIP, "80", "sony/IRCC", commands['Num'+str(num)], cookie);
		elif num == '1':
			resp = bravia_req_ircc(SONYIP, "80", "sony/IRCC", commands['Num'+str(num)], cookie);
		elif num == '2':
			resp = bravia_req_ircc(SONYIP, "80", "sony/IRCC", commands['Num'+str(num)], cookie);
		elif num == '3':
			resp = bravia_req_ircc(SONYIP, "80", "sony/IRCC", commands['Num'+str(num)], cookie);
		elif num == '4':
			resp = bravia_req_ircc(SONYIP, "80", "sony/IRCC", commands['Num'+str(num)], cookie);
		elif num == '5':
			resp = bravia_req_ircc(SONYIP, "80", "sony/IRCC", commands['Num'+str(num)], cookie);
		elif num == '6':
			resp = bravia_req_ircc(SONYIP, "80", "sony/IRCC", commands['Num'+str(num)], cookie);
		elif num == '7':
			resp = bravia_req_ircc(SONYIP, "80", "sony/IRCC", commands['Num'+str(num)], cookie);
		elif num == '8':
			resp = bravia_req_ircc(SONYIP, "80", "sony/IRCC", commands['Num'+str(num)], cookie);
		elif num == '9':
			resp = bravia_req_ircc(SONYIP, "80", "sony/IRCC", commands['Num'+str(num)], cookie);	
		elif num == 'p':
			resp = bravia_req_ircc(SONYIP, "80", "sony/IRCC", commands['PowerOff'], cookie);
		elif num == 'V':
			resp = bravia_req_ircc(SONYIP, "80", "sony/IRCC", commands['VolumeUp'], cookie);
		elif num == 'v':
			resp = bravia_req_ircc(SONYIP, "80", "sony/IRCC", commands['VolumeDown'], cookie);
		elif num == 'C':
			resp = bravia_req_ircc(SONYIP, "80", "sony/IRCC", commands['ChannelUp'], cookie);
		elif num == 'c':
			resp = bravia_req_ircc(SONYIP, "80", "sony/IRCC", commands['ChannelDown'], cookie);	
		else:
			print "Remote Controller: exit!"
			break
	return None
	
	

###########################################################
#
#	WAKE ON LAN
#
###########################################################
def wakeonlan(ethernet_address):
	import struct
	addr_byte = ethernet_address.split(':')
	hw_addr = struct.pack('BBBBBB', int(addr_byte[0], 16),
	int(addr_byte[1], 16),
	int(addr_byte[2], 16),
	int(addr_byte[3], 16),
	int(addr_byte[4], 16),
	int(addr_byte[5], 16))
	msg = b'\xff' * 6 + hw_addr * 16
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	s.sendto(msg, ('<broadcast>', 9))
	s.close()



###########################################################
#
#	DISCOVER IP VIA SSDP PROTOCOL (UDP 1900 PORT)
#
###########################################################
def DISCOVER_via_SSDP (service = "urn:schemas-sony-com:service:ScalarWebAPI:1"):
	import select, re
	SSDP_ADDR = "239.255.255.250";
	SSDP_PORT = 1900;
	SSDP_MX = 1;
	SSDP_ST = service;

	ssdpRequest = "M-SEARCH * HTTP/1.1\r\n" + \
		"HOST: %s:%d\r\n" % (SSDP_ADDR, SSDP_PORT) + \
		"MAN: \"ssdp:discover\"\r\n" + \
		"MX: %d\r\n" % (SSDP_MX, ) + \
		"ST: %s\r\n" % (SSDP_ST, ) + "\r\n";

	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	#select.select([sock], [], [], 10)
	sock.settimeout(5.0)
	dest = socket.gethostbyname(SSDP_ADDR)
	sock.sendto(ssdpRequest, (dest, SSDP_PORT))
	sock.settimeout(5.0)
	try: 
		data = sock.recv(1000)
	except socket.timeout:
		print "No Bravia found (timed out)!"
		sys.exit(1)
	response = data.decode('utf-8')
	match = re.search(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", response)
	if match:                      
		return match.group()
	else:
		return SONYIP



###########################################################
#
#	GET COOKIE FROM SONY BRAVIA TV via HTTP
#		- if pin passed sends Basic Authentication
#		- otherwise tries to get cookie
#
###########################################################
def bravia_auth ( ip, port, url, params, pin ):
	req = urllib2.Request('http://'+ip+':'+port+'/'+url, params)
	cookie = None
	response = None
	
	if pin:
		username = ''
		base64string = base64.encodestring('%s:%s' % (username, pin)).replace('\n', '')
		req.add_header("Authorization", "Basic %s" % base64string)
		req.add_header("Connection", "keep-alive")
		
	try:
		response = urllib2.urlopen(req)
		
	except urllib2.HTTPError, e:
		print "[W] HTTPError: " + str(e.code)
		return None
		
	except urllib2.URLError, e:
		print "[W] URLError: " + str(e.reason)
		return None
    	#sys.exit(1)
		
	else: 
		for h in response.info().headers:
			if h.find("Set-Cookie") > -1:
				cookie=h			
		if cookie:
			cookie = response.headers['Set-Cookie']
			return cookie
		#html = response.info().items(),response.read()
		#print "[i] Response:", html
		return None
		

###########################################################
#
#	SEND JSON REQUEST via HTTP (cookie required)
#
###########################################################
def bravia_req_json( ip, port, url, params, cookie ):
	req = urllib2.Request('http://'+ip+':'+port+'/'+url, params)
	req.add_header('Cookie', cookie)
	try:
		response = urllib2.urlopen(req)
		
	except urllib2.HTTPError, e:
		print "[W] HTTPError: " + str(e.code)
		
	except urllib2.URLError, e:
		print "[W] URLError: " + str(e.reason)
		#sys.exit(1)

	else:
		#json 2 dictionary
		html = json.load(response)
		#print "[i] Response:", html
		return html

	
	

###########################################################
#
#	SEND APPLIST REQUEST via HTTP (cookie required)
#
###########################################################
def bravia_applist( ip, port, url, params, cookie ):
	req = urllib2.Request('http://'+ip+':'+port+'/'+url, params)
	req.add_header('Cookie', cookie)
	# applist requires GET not POST
	if url == "DIAL/sony/applist":
		req.get_method = lambda: 'GET'
	try:
		response = urllib2.urlopen(req)
		
	except urllib2.HTTPError, e:
		print "[W] HTTPError: " + str(e.code)
		
	except urllib2.URLError, e:
		print "[W] URLError: " + str(e.reason)
		#sys.exit(1)

	else:
		# write to applist.xml
		file = open ('applist.xml', 'w')
		data = response.read()
		file.write(data)
		file.close()
		return data
	
###########################################################
#
#	SEND IRCC REQUEST via HTTP (cookie required)
#
###########################################################
def bravia_req_ircc( ip, port, url, params, cookie ):
	req = urllib2.Request('http://'+ip+':'+port+'/'+url, "<?xml version=\"1.0\"?><s:Envelope xmlns:s=\"http://schemas.xmlsoap.org/soap/envelope/\" s:encodingStyle=\"http://schemas.xmlsoap.org/soap/encoding/\"><s:Body><u:X_SendIRCC xmlns:u=\"urn:schemas-sony-com:service:IRCC:1\"><IRCCCode>"+params+"</IRCCCode></u:X_SendIRCC></s:Body></s:Envelope>")
	req.add_header('SOAPACTION', 'urn:schemas-sony-com:service:IRCC:1#X_SendIRCC')
	req.add_header('Cookie', cookie)
	
	try:
		response = urllib2.urlopen(req)
	except urllib2.HTTPError, e:
		print "[W] HTTPError: " + str(e.code)
		
	except urllib2.URLError, e:
		print "[W] URLError: " + str(e.reason)
		#sys.exit(1)
	else:
		tree = response.read()
		return tree


	
###########################################################
#
#	SEND DIAL - UPNP REQ
#	methods
#		GET 	= get status
#		POST 	= start app
#		DELETE	= stop app
#
###########################################################
def bravia_dial_req( ip, port, method = "GET", app="YouTube" ):

	headers = {
		'Origin':'package:com.google.android.youtube',
		'Host':ip
	}

	url = app
	if method == "DELETE":
		url = app+"/run"

	req = urllib2.Request('http://'+ip+':'+port+'/DIAL/apps/'+url, headers=headers)
	req.get_method = lambda: method
	
	#print req.headers
	
	try:
		response = urllib2.urlopen(req)
	except urllib2.HTTPError, e:
		print "[W] HTTPError: " + str(e.code)
		
	except urllib2.URLError, e:
		print "[W] URLError: " + str(e.reason)
		#sys.exit(1)
	else:
		tree = response.info().headers, response.read()
		#print tree
		return tree
		
	
###########################################################
#
#	[MAIN]
#
###########################################################
def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hp:vdw:r", ["help", "pin=", "verbose", "discover", "wol=", "remote"])

	except getopt.GetoptError as err:
		print str(err)
		usage()
		sys.exit(2)

	output = None
	verbose = False
	remote = False
	wol = False
	
	pin = "0000"
	
	for o, a in opts:
		if o == "-v":
			verbose = True
		elif o in ("-h", "--help"):
			usage()
			sys.exit()
		elif o in ("-p", "--pin"):
			pin = a
		elif o in ("-d", "--discover"):
			found = DISCOVER_via_SSDP()
			if found:
				print "Bravia found on", found
			else:
				print "Bravia NOT found!"
			sys.exit()
		elif o in ("-w", "--wol"):
			macaddr = a
			wol = True
		elif o in ("-r", "--remote"):
			remote = True
		else:
			assert False, "unhandled option"

	if wol:
		wakeonlan(macaddr)
		sys.exit()

	# first request (AUTH 1)	
	print "[*] AccessControl"
	cookie = bravia_auth(SONYIP, "80", "sony/accessControl", _AUTHORIZATION, None );
	# send PIN if not cookie
	if not cookie:
		print "Sending PIN ", str(pin)
		cookie = bravia_auth(SONYIP, "80", "sony/accessControl", _AUTHORIZATION, pin );
		# exit if not cookie again (NO AUTH)
		if not cookie:
			print "Pairing failed!"
			sys.exit(0)
	else:
		print "Registered!"
		print "CLIENTID=%s" % (CLIENTID)
		print "NICKNAME=%s" % (NICKNAME)
		if verbose:
			print "Cookie:", cookie

	if remote:
		remote_control(cookie, verbose);
		sys.exit()
	

	#
	# JSON STUFF
	#
	print "[*] getPlayingContent"
	resp = bravia_req_json(SONYIP, "80", "sony/avContent", jdata_build("getPlayingContentInfo", None), cookie);
	data = resp['result']
	for item in data:
		try:
			print "Program Title:", item["programTitle"]
			print "Title:", item["title"]
			print "MediaType:", item["programMediaType"]
		except KeyError:
			print "key error"
			print json.dumps(resp.get('result'), indent=4)
			pass
	if verbose:
		print "RESULT: ", json.dumps(data), "\n"

	raw_input()
		
	print "[*] getSystemInformation"
	resp = bravia_req_json(SONYIP, "80", "sony/system", jdata_build("getSystemInformation", None), cookie);
	if not resp.get('error'):
		print json.dumps(resp.get('result'), indent=4)
	else:
		print "JSON request error", json.dumps(resp, indent=4)
	
	raw_input()
	
	print "[*] getNetworkSettings"
	resp = bravia_req_json(SONYIP, "80", "sony/system", jdata_build("getNetworkSettings", None), cookie);
	if not resp.get('error'):
		print json.dumps(resp.get('result'), indent=4)
	else:
		print "JSON request error", json.dumps(resp, indent=4)

	raw_input()
		
	print "[*] getMethodTypes"
	resp = bravia_req_json(SONYIP, "80", "sony/system", jdata_build("getMethodTypes", "1.0"), cookie);
	if not resp.get('error'):
		# __ results __ NOT __ result __
		print json.dumps(resp.get('results'), indent=4)
	else:
		print "JSON request error", json.dumps(resp, indent=4)

	raw_input()
	
	print "[*] getWolMode"
	resp = bravia_req_json(SONYIP, "80", "sony/system", jdata_build("getWolMode", None), cookie);
	if not resp.get('error'):
		print json.dumps(resp.get('result'), indent=4)
	else:
		print "JSON request error", json.dumps(resp, indent=4)
	
	raw_input()
	
	print "[*] AppList!"
	resp = bravia_applist(SONYIP, "80", "DIAL/sony/applist", "", cookie);
	print resp
	
	raw_input()
	#
	# DIAL STUFF
	#
	print "[*] DIAL - YouTube status"
	resp = bravia_dial_req( SONYIP, "80", "GET", "YouTube" )
	print resp
	raw_input()
	
	print "[*] DIAL - YouTube start (on TV)"
	resp = bravia_dial_req( SONYIP, "80", "POST", "YouTube" )
	print resp
	raw_input()

	print "[*] DIAL - YouTube status"
	resp = bravia_dial_req( SONYIP, "80", "GET", "YouTube" )
	print resp
	raw_input()

	print "[*] DIAL - YouTube stop"
	resp = bravia_dial_req( SONYIP, "80", "DELETE", "YouTube" )
	print resp
	raw_input()
	
	#
	# UPNP STUFF
	#
	print "[*] UPNP - SUBSCRIBE test"
	sid = bravia_upnp_subscribe(SONYIP, "52323", "RenderingControl");
	if sid:
		print sid
	else:
		print "no sid in response!"
	raw_input()	
	
	# mute
	print "[*] UPNP - SetMute 1 test"
	upnp_req = "<InstanceID>0</InstanceID><Channel>Master</Channel><DesiredMute>1</DesiredMute>"
	resp = bravia_upnp_req(SONYIP, "52323", "RenderingControl", upnp_req, "urn:schemas-upnp-org:service:RenderingControl:1", 'SetMute');
	print resp
	raw_input()
	
	# unmute
	print "[*] UPNP - SetMute 0 test"
	upnp_req = "<InstanceID>0</InstanceID><Channel>Master</Channel><DesiredMute>0</DesiredMute>"
	resp = bravia_upnp_req(SONYIP, "52323", "RenderingControl", upnp_req, "urn:schemas-upnp-org:service:RenderingControl:1", 'SetMute');
	print resp
	raw_input()

	print "[*] UPNP - UNSUBSCRIBE test"
	resp = bravia_upnp_unsubscribe(SONYIP, "52323", "RenderingControl", sid);
	print resp
	#sys.exit()
	raw_input()
	
if __name__ == "__main__":
	main()
