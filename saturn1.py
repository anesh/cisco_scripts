#! /usr/bin/python

import os
import paramiko
import xlsxwriter
import socket
import re
import sys
import telnetlib
import time
import textfsm
from compiler.ast import flatten

username = raw_input('Enter username for device login:')
password = raw_input('Enter the corresponding password:')
print "Ahhhh ......"

# Opens file in read mode
f1 = open('device.txt','r')


# Creates list based on f1
devices = f1.readlines()
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
    ssh.connect(column[1], username=username, password=password)
    remote_conn = ssh.invoke_shell()
    output = remote_conn.recv(1000)
    if 'HKG_MEG_WS03' in column:
        remote_conn.send("sh clock")
        remote_conn.send("\n")
        remote_conn.send("sh int Po2 | i drop")
        remote_conn.send("\n")
        remote_conn.send("sh int Po1 | i drop")
        remote_conn.send("\n")
        remote_conn.send("sh int Gi1/0/1 | i drop")
        remote_conn.send("\n")
        remote_conn.send("sh int Gi1/0/2 | i drop")
        remote_conn.send("\n")
        remote_conn.send("sh int Gi2/0/1 | i drop")
        remote_conn.send("\n")
        remote_conn.send("sh int Gi2/0/2 | i drop")
        remote_conn.send("\n")
    elif 'HKG_MEG_WAE03' in column:
        remote_conn.send("sh clock")
        remote_conn.send("\n")
        remote_conn.send("sh interface GigabitEthernet 0/0")
        remote_conn.send("\n")
        remote_conn.send("sh interface GigabitEthernet 0/1")
        remote_conn.send("\n")
    elif 'HKG_MEG_WAE04' in column:
        remote_conn.send("sh clock")
        remote_conn.send("\n")
        remote_conn.send("sh interface GigabitEthernet 0/0")
        remote_conn.send("\n")
        remote_conn.send("sh interface GigabitEthernet 0/1")
        remote_conn.send("\n")
        
    time.sleep(2)
    output = remote_conn.recv(5000)
    print output
    fsm_results = fsm.ParseText(output)
    for list1 in fsm_results:
        x=flatten(list1)       #flatten out irregualr list
        for z in x:
            data[-1].append(z)        #convert a list to string and append data to old list
    
        
   
 #data is of datastructure List of List to serve as input for xlsxwriter
    
f1.close()
ssh.close()

#Create Workbook instance
book = xlsxwriter.Workbook('saturn.xlsx')
sheet = book.add_worksheet(column[0])


#Define and format header
header_format = book.add_format({'bold':True , 'bg_color':'yellow'})
header = ["Hostname","IPaddress","Time", "Po2", "Po1","Gi1/0/1","Gi1/0/2","Gi2/0/1","Gi2/0/2"]
for col, text in enumerate(header):
    sheet.write(0, col, text, header_format)



# Now, let's write the contents
for row, data_in_row in enumerate(data):
    for col, text in enumerate(data_in_row):
        sheet.write(row + 1, col, text)


book.close()

print "Data Generated"


