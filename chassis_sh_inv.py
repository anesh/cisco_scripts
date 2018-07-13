#! /usr/bin/python

import os
import paramiko
import xlsxwriter
import socket
import re
import sys
import textfsm
import telnetlib
import time

username = raw_input('Enter username for device login:')
password = raw_input('Enter the corresponding password:')
print "This might take some time.Extracting information from the following devices: "

# Opens file in read mode
f1 = open('device.txt','r')
f2 = open('ciscocommand.txt','r')

# Creates list based on f1
devices = f1.readlines()
commands = f2.readlines()
template_file = sys.argv[1]
fsm = textfsm.TextFSM(open(template_file))
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
data = []

for device in devices:
    column = device.split()
    data.append([column[0]])
    data[-1].append(column[1])
    print column[0]
    def connectviatelnet():
        try:
            fsm = textfsm.TextFSM(open(template_file))
            output = "Connecting using Telnet"
            print output
            telnet = telnetlib.Telnet(column[1])
            telnet.read_until("Username: ")
            telnet.write(username + '\r')
            telnet.read_until("Password: ")
            telnet.write(password + '\r')
            telnet.write("term length 0"+ "\r\n")
            telnet.write("show inv" + "\r\n")
            telnet.write('exit' '\r\n')
            outx=telnet.read_all()
            fsmx = fsm.ParseText(outx)
            for telx in fsmx:
                tely=''.join(telx)
            data[-1].append(tely)
            telnet.close()
        except Exception as e:
               output = "Telnet Failed"
               data[-1].append(output)
    for command in commands:
        try:
                conn=ssh.connect(column[1], username=username, password=password, timeout=4)
                if conn is None:
                    remote_conn = ssh.invoke_shell()
                    output = remote_conn.recv(1000)
                    remote_conn.send("sh inv")
                    remote_conn.send("\n")
                    time.sleep(2)
                    output = remote_conn.recv(5000)
                    fsm_results = fsm.ParseText(output)
                    for mylist in fsm_results:
                        x=mylist
                    y=x[0]
                    z=y[0]                   
                    data[-1].append(z)
                    ssh.close()
        except  paramiko.AuthenticationException:
                output = "Authentication Failed"
                data[-1].append(output)
        except  paramiko.SSHException:
                output = "Issues with SSH service"
                data[-1].append(output)
        except  socket.error, e:
                connectviatelnet()        
                
                
                       
                       
        
    data[-1] = tuple(data[-1])

f1.close()
f2.close()


#Create Workbook instance
book = xlsxwriter.Workbook('chassis.xlsx')
sheet = book.add_worksheet('SerialNum')


#Define and format header
header_format = book.add_format({'bold':True , 'bg_color':'yellow'})
header = ["Device Name", "IP Address", "Serial Number"]
for col, text in enumerate(header):
    sheet.write(0, col, text, header_format)



# Now, let's write the contents
for row, data_in_row in enumerate(data):
    for col, text in enumerate(data_in_row):
        sheet.write(row + 1, col, text)


book.close()

print "Data Generated"


