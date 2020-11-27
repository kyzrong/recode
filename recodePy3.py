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

var_write_file = ['serial_recode.txt']

opts, args = getopt.getopt(sys.argv[1:],"hc:p:f:",["help"])
for op, value in opts:
	if op == "-c":
		v_port = str(value)
	if op == '-p':
		v_so_port[0] = int(value)
	if op == '-f':
		var_write_file[0] = value
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
		

def T_write_file(data):
	try:
		f = open(var_write_file[0],'ab')
	except:
		print 'Open file Faile:',var_write_file[0]
		return False
		
	try:
		f.write(binascii.b2a_hex(data))
		f.write('<RE>')
		print binascii.b2a_hex(data)
		f.close()
	except:
		print 'Faile to write recode to file:',var_write_file[0]
		return False

		
def usage():
	print '''
	how to use(v1.0):2017-6-27 19:48:30
		
        '''
	content = input("Return to continue.")
	
			
def T_read():
	while True:
		cur_string = ser.read(1)
		if cur_string != '':
			var_list_read.append(cur_string)

def T_write():
	while True:
		while len(var_list_write) > 0:
			ser.write(var_list_write[0])
			del var_list_write[0]
		time.sleep(0.01)
	
def middle_server():
	port_str = str(v_so_port[0])
	port = int(port_str)
	time_out = 100
	while True:
		try:
			the_socket = socket.socket()
			the_socket.bind(('0.0.0.0',port))
			the_socket.listen(1)
			print 'Listening on port:',port
		except:
			print 'Binging port Faile:',port
			time.sleep(1)
			continue
			
		try:
			conn,addr = the_socket.accept()
			print 'Accept from:',addr
		except socket.timeout:
			conn.close()
			continue

		conn.settimeout(time_out)
		while True:
			try:
				data = conn.recv(1)
				if len(data) != 0:		#不判断接收失败
					var_list_write.append(data)
					T_write_file(data)	#将数据写入文件
				elif len(data) == 0:
					conn.close()
					break
			except:
				break
				
			try:
				while len(var_list_read) > 0:
					conn.send(var_list_read[0])
					del var_list_read[0]
			except:
				pass
			time.sleep(0.01)

def s_term():
	ser.open()
		#print "Serial error."
	print "Enter the terminator mode.Ctrl+z to exit."
	try:
		thread.start_new_thread(T_read,())
		thread.start_new_thread(T_write,())
		thread.start_new_thread(middle_server,())
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

def main():
	pass
	
if __name__ == '__main__':
	main()