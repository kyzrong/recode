#coding:utf-8
import thread
import serial
import string
import getopt
import serial.tools.list_ports
import sys,os,time
import io
import msvcrt
import binascii
import socket

ser = serial.Serial()
v_port= ''
v_baudrate = 115200
v_bytesize = 8
v_parity = 'N'
v_stopbits = 1
v_timeout = 0.1
v_xonxoff = 0
v_rtscts = 0
v_string = ''
v_file_write = ''
v_file_read = ''
v_port_list = []
v_baudrate_list = [115200,19200,9600]

v_so_port = [9090]

#写列表
var_list_write = []
#读列表
var_list_read = []

sleepTime = 0.1
var_write_file = ['serial_recode.txt']

opts, args = getopt.getopt(sys.argv[1:],"hc:f:t:",["help"])
for op, value in opts:
	if op == "-c":
		v_port = str(value)
	if op == '-f':
		var_write_file[0] = value
	if op == '-t':
		sleepTime = float(value)
	if op == '-h' or op == '--help':
		usage()

ser.port    =   v_port
ser.baudrate=   v_baudrate
ser.bytesize=   v_bytesize
ser.parity  =   v_parity
ser.stopbits=   v_stopbits
ser.timeout =   v_timeout
ser.xonxoff =   v_xonxoff
ser.rtscts  =   v_rtscts		
		

		
def usage():
	print '''
	how to use(v1.0):2017-6-27 19:48:30
		
        '''
	content = input("Return to continue.")
	

def T_write():
	try:
		f = open(var_write_file[0],'rb')
	except:
		print 'Can\'t open recode file:',var_write_file[0]
		return False
	
	#try:
	file_data = f.read()
	f.close()
	for line in file_data.split('<RE>'):
		#print binascii.a2b_hex(line)
		print line,
		ser.write(line)
		
		time.sleep(sleepTime)
	# except:
		# print 'Send recode data false.',var_write_file[0]
	
		
def s_term():
	ser.open()
		#print "Serial error."
	print "Enter the terminator mode.Ctrl+z to exit."
	try:
		thread.start_new_thread(T_write,())
	except:
		print "Error: Unable to start thread."

	while 1:
		time.sleep(0.1)				

def show_info():
	print ""
	print "Com:",ser.port,"|Baudrate:",ser.baudrate,"|Parity:",ser.parity,\
	"|bytesiZe:",ser.bytesize,"|Stopbits:",ser.stopbits,"|Timeout:",ser.timeout,\
	"|xOnxoff:",ser.xonxoff,"|Rtscts:",ser.rtscts
	
show_info()
s_term()
	
