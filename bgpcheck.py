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

f1 = open('device.txt','r')



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
        telnet.write("show ip bgp summary" + "\r\n")
        time.sleep(2)
        telnet.write('exit' '\r\n')
        output=telnet.read_all()
        x=output.split(',')
        for y in x[4].splitlines():
          z.append(y.split())
        for i in 1,2,3:
          z.pop(0)
        z.pop()
        for explodelist in z:
            data.append([None])
            data[-1].append(None)
            data[-1].append(explodelist[0])
            data[-1].append(explodelist[2])
            data[-1].append(explodelist[8])
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
        output = remote_conn.recv(1000)
        remote_conn.send("term length 0")
        remote_conn.send("\n")
        remote_conn.send("show ip bgp summary")
        remote_conn.send("\n")
        time.sleep(2)
        output = remote_conn.recv(5000)
        x=output.split(',')
        for y in x[4].splitlines():
          z.append(y.split())
        for i in 1,2,3:
          z.pop(0)
        z.pop()
        for explodelist in z:
            data.append([None])
            data[-1].append(None)
            data[-1].append(None)
            data[-1].append(explodelist[0])
            data[-1].append(explodelist[2])
            data[-1].append(explodelist[8])
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

book = xlsxwriter.Workbook('BGP.xlsx')
sheet = book.add_worksheet(column[0])



header_format = book.add_format({'bold':True , 'bg_color':'yellow'})
header = ["Hostname","IPaddress","Peer IP","AS Number","State"]
for col, text in enumerate(header):
    sheet.write(0, col, text, header_format)



for row, data_in_row in enumerate(data):
   for col, text in enumerate(data_in_row):
        sheet.write(row + 1, col, text)


book.close()

print "Data Generated"


