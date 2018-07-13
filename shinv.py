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
        telnet.write("show inv" + "\r\n")
        telnet.write('exit' '\r\n')
        outx=telnet.read_all()
        match=re.findall(r'(?<=PID:\s)(.*)',outx)
        for matchlist in match:
            listoflist.append(matchlist.split(','))
        for explodelist in listoflist:
            data.append([None])
            data[-1].append(None)
            data[-1].append(explodelist[0])
            data[-1].append(explodelist[2])
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
        remote_conn.send("sh inv")
        remote_conn.send("\n")
        time.sleep(2)
        output = remote_conn.recv(5000)
        match=re.findall(r'(?<=PID:\s)(.*)',output)
        for matchlist in match:
            listoflist.append(matchlist.split(','))
        for explodelist in listoflist:
            data.append([None])
            data[-1].append(None)
            data[-1].append(explodelist[0])
            data[-1].append(explodelist[2])
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

book = xlsxwriter.Workbook('shinv.xlsx')
sheet = book.add_worksheet(column[0])



header_format = book.add_format({'bold':True , 'bg_color':'yellow'})
header = ["Hostname","IPaddress","PID","Serial Number"]
for col, text in enumerate(header):
    sheet.write(0, col, text, header_format)



for row, data_in_row in enumerate(data):
   for col, text in enumerate(data_in_row):
        sheet.write(row + 1, col, text)


book.close()

print "Data Generated"


