import os
import paramiko
import xlsxwriter
import socket
import re
import sys
import time
import telnetlib
import getpass

username = raw_input('Enter username:')
password = getpass.getpass()
deviceip=raw_input('Enter Device IP:')

f1 = open('commands.txt','r')
commands = f1.readlines()
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

for command in commands:
    print "running command:  "+command
    try:
        ssh.connect(deviceip, username=username, password=password,timeout=5)
        stdin, stdout, stderr = ssh.exec_command(command)
        x=stdout.read()
        if "sh process cpu" in command:
            cpulist=x.splitlines()
            print cpulist[19]
        if "show policy-map interface" in command:
            match1=re.findall(r'(?<=Class-map:)(.*)',x) 
            match2=re.findall(r'(?<=drop rate)(.*)',x)
            for y,z in zip(match1,match2):
                print y+z
        if "sh log" in command:
            timex=time.strftime("%b %d")
            match5=re.findall(r'(?<=%s)(.*)' %timex,x) 
            for log in match5:
                print log
        if "show ip protocol" in command:
            match4=re.findall(r'(Routing Information Sources:)(.*?Distance:)',x,re.DOTALL)
            for q in match4:
                for qx in q:
                    print qx
        if "sh interfaces" in command:
            match6=re.findall(r'(.*\d\s)(?=is)',x)
            match7=re.findall(r'(?<=Internet address is)(.*)',x)
            match8=re.findall(r'(reliability.*)',x)
            for intx in match6:
                print intx
            for addr in match7:
                print addr
            for util in match8:
                print util
        if "show ip bgp summary" in command:
            match9=re.findall(r'(Neighbor)(.*)',x,re.DOTALL)
            for bgplist in match9:
                for listoflist in bgplist:
                    print listoflist
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
