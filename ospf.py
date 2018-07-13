#Developed by Anesh Kesavan for SCB

import xlsxwriter
import re
from pysnmp.entity.rfc3413.oneliner import cmdgen
cmdGen = cmdgen.CommandGenerator()

book = xlsxwriter.Workbook('ospf.xlsx')
sheet = book.add_worksheet("report")   

header_format = book.add_format({'bold':True , 'bg_color':'yellow'})
header = ["Hostname","IPaddress","Neighbor","State"]
for col, text in enumerate(header):
    sheet.write(0, col, text, header_format) 

format1 = book.add_format({'bg_color':'green'})
format2 = book.add_format({'bg_color':'red'})
sheet.conditional_format('D2:D65536', {'type': 'text','criteria': 'containing','value':'UP','format':format1})
sheet.conditional_format('D2:D65536', {'type': 'text','criteria': 'containing','value':'DOWN','format':format2})
    
f1 = open('devices.txt','r')
devices = f1.readlines()

row=0
col=0


for device in devices:
  z=[]
  
  row=row+1

  column = device.split()
  sheet.write(row, 0,column[0] )
  sheet.write(row, 1,column[1] )
  
  print column[0]

  

  
  
  varBinds = cmdGen.nextCmd(cmdgen.CommunityData('g0al1e'),cmdgen.UdpTransportTarget((column[1], 161)),'1.3.6.1.2.1.14.10.1.6')
  #print  varBinds[3]
  if not varBinds[3]:
    varBinds = cmdGen.nextCmd(cmdgen.UsmUserData('scbcnim','scb#m0nit@r$'),cmdgen.UdpTransportTarget((column[1], 161)),'1.3.6.1.2.1.14.10.1.6')
    for list in varBinds[3]:
      for y in list:
        regex1=str(y).replace('(ObjectName(\'1.3.6.1.2.1.14.10.1.6.', '')
        regex2=str(regex1).replace('.0\')','')
        x=str(regex2).replace(')','').replace('(','')
        neighbor=x.split(',')[0]
        state=x.split(',')[1]
        if state==" Integer8":
           state="UP"
        else:
           state="DOWN"
      
      
        print "Neighbor: "+neighbor
        sheet.write(row,2,neighbor)
        print "State: "+state
        sheet.write(row,3,state)
        row=row+1
  else:
    for list in varBinds[3]:
      for y in list:
        regex1=str(y).replace('(ObjectName(\'1.3.6.1.2.1.14.10.1.6.', '')
        regex2=str(regex1).replace('.0\')','')
        x=str(regex2).replace(')','').replace('(','')
        neighbor=x.split(',')[0]
        state=x.split(',')[1]
        if state==" Integer8":
           state="UP"
        else:
           state="DOWN"
      
      
        print "Neighbor: "+neighbor
        sheet.write(row,2,neighbor)
        print "State: "+state
        sheet.write(row,3,state)
        row=row+1
    
  
  
book.close()    
f1.close()








      






