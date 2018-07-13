import os
import paramiko
import xlsxwriter
import socket
import re
import sys
import time
import telnetlib

username = raw_input('Enter username for device login:')
password = raw_input('Enter the corresponding password:')
print "......"

f1 = open('devices.txt','r')
devices = f1.readlines()

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
data = []
x=[]
z=[]

def connectviatelnet(iprcv):
    try:
        print "Connecting using Telnet"
        print iprcv
        telnet = telnetlib.Telnet(iprcv)
        telnet.read_until("Username: ")
        telnet.write(username + '\r')
        telnet.read_until("Password: ")
        telnet.write(password + '\r')
        telnet.write("term length 0"+ "\r\n")
        telnet.write("show start" + "\r\n")
        time.sleep(2)
        telnet.write('exit' '\r\n')
        output=telnet.read_all()
        x=output.split(',')
        print x
        telnet.close()
    except Exception as e:
        output = "Command is not working"
        data[-1].append(output)

for device in devices:
    listoflist=[]
    column = device.split()
    data.append([column[0]])
    ip=column[1]
    data[-1].append(column[1])
    print column[0]
    xls=[]
    try:
        ssh.connect(column[1], username=username, password=password,timeout=5)
        remote_conn = ssh.invoke_shell()
        buff = ''
        while not buff.endswith('>'):
            resp = remote_conn.recv(9999)
            print resp
            buff+= resp
        remote_conn.send("term length 0")
        remote_conn.send("\n")
        buff = ''
        while not buff.endswith('>'):
            resp = remote_conn.recv(9999)
            print resp
            buff+= resp
        
        
        remote_conn.send("show start")
        remote_conn.send("\n")
        buff = ''
        while not buff.endswith('>'):
            resp = remote_conn.recv(9999)
            #print resp
            buff+= resp
        print buff
        ssh.close()
    except socket.error, e:
        connectviatelnet(ip)
    except paramiko.SSHException:
        output = "Issues with SSH service"
        data[-1].append(output)
    except paramiko.AuthenticationException:
        output = "Authentication Failed"
        data[-1].append(output)
        continue
    
   
 #data is of datastructure List of List to serve as input for xlsxwriter
    
f1.close()


print "Data Generated"


