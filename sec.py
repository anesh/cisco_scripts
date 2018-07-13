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

book = xlsxwriter.Workbook('audit.xlsx')
sheet = book.add_worksheet("")   

header_format = book.add_format({'bold':True , 'bg_color':'yellow'})
header = ["Hostname","IPaddress","Parameter"]
for col, text in enumerate(header):
    sheet.write(0, col, text, header_format) 
    
f1 = open('devices.txt','r')
f2=open('secconfig.txt','r')

devices = f1.readlines()
configs=f2.read().splitlines()

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
out=[]
x=[]
z=[]
row=0
col=0

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
    column = device.split()
    
    row=row+1
    sheet.write(row, 0,column[0] )
    sheet.write(row, 1,column[1] )
    print column[0]
    try:
        ssh.connect(column[1], username=username, password=password,timeout=5)
        remote_conn = ssh.invoke_shell()
        buff = ''
        while not buff.endswith('>'):
            resp = remote_conn.recv(9999)
            buff+= resp
            print buff
        remote_conn.send("term length 0")
        remote_conn.send("\n")
        buff = ''
        while not buff.endswith('>'):
            resp = remote_conn.recv(9999)
            buff+= resp
            print buff
        for command in configs:
            remote_conn.send("sh start | inc "+command)
            remote_conn.send("\n")
            buff = ''
            while not buff.endswith('>'):
                resp = remote_conn.recv(9999)
                buff+= resp
            #myregex=r'(?<='+re.escape(command)+')(.*)'
            myregex1=r'(?<='+command+')(.*)'
            
            match=re.findall(myregex1,buff,re.DOTALL)
            out=match[0].splitlines()
            
            if command in out[1]:
                print "Configured"
                
            else:
                print "NOt Configured"
                sheet.write(row,2, command)
                
                row=row+1
        #print buff
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
    
    
book.close()
    
    
f1.close()
f2.close()







