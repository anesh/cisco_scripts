#Developed by Anesh Kesavan for SCB

import xlsxwriter
import re
from pysnmp.entity.rfc3413.oneliner import cmdgen
cmdGen = cmdgen.CommandGenerator()

f1 = open('devices.txt','r')
devices = f1.readlines()
data = []




for device in devices:
  a=[]
  z=[]
  e=[]

  listoflist=[]
  column = device.split()
  data.append([column[0]])
  ip=column[1]
  data[-1].append(column[1])
  print column[0]
  xls=[]
  
  #For BGP peer State
  varBinds = cmdGen.nextCmd(cmdgen.CommunityData('g0al1e'),cmdgen.UdpTransportTarget((column[1], 161)),'1.3.6.1.2.1.15.3.1.2')
  #for Remote AS number
  varBinds1 = cmdGen.nextCmd(cmdgen.CommunityData('g0al1e'),cmdgen.UdpTransportTarget((column[1], 161)),'1.3.6.1.2.1.15.3.1.9') 

  

  for list in varBinds[3]:
    for y in list:
      h=str(y).replace('(', '').replace(')', '')
      g=str(h).replace('ObjectName1.3.6.1.2.1.15.3.1.2.','')
      z.append(g)
      
  for list1 in varBinds1[3]:
    for b in list1:
      c=str(b).replace('(', '').replace(')', '')
      d=str(c).replace('ObjectName1.3.6.1.2.1.15.3.1.9.','')
      m=str(d).replace('Integer','')
      e.append(m)
      
      
  #gives peer IP and state and Remote AS
  for i,g in zip(z,e):
    peer=i.split(',')[0]
    peerip=re.search(r'(?<=ObjectName\'1\.3\.6\.1\.2\.1\.15\.3\.1\.2\.)(.*)',peer)
    ipval= peerip.group()
    state=i.split(',')[1]
    if state==" Integer6":
      state="UP"
    else:
      state="DOWN"
    remoteas=g.split(',')[1]
    data.append([None])
    data[-1].append(None)
    data[-1].append(ipval)
    data[-1].append(state)
    data[-1].append(remoteas)
    
    
#data is of datastructure List of List to serve as input for xlsxwriter
    
f1.close()

book = xlsxwriter.Workbook('BGP.xlsx')
sheet = book.add_worksheet(column[0])

format1 = book.add_format({'bg_color':'green'})
format2 = book.add_format({'bg_color':'red'})
sheet.conditional_format('D3:D65536', {'type': 'text','criteria': 'containing','value':'UP','format':format1})
sheet.conditional_format('D3:D65536', {'type': 'text','criteria': 'containing','value':'DOWN','format':format2})

header_format = book.add_format({'bold':True , 'bg_color':'yellow'})
header = ["Hostname","IPaddress","Peer IP","State","AS Number"]
for col, text in enumerate(header):
    sheet.write(0, col, text, header_format)



for row, data_in_row in enumerate(data):
   for col, text in enumerate(data_in_row):
        sheet.write(row + 1, col, text)

        
book.close()

print "Data Generated"





      






