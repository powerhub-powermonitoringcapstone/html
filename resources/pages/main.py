#!/usr/bin/python3
# -*- coding: UTF-8 -*-# enable debugging
import cgitb, os, sys, socket

sys.path.insert(1, '/home/capstone/codebase/')
cwd = os.path.dirname(os.path.realpath(__file__))#take note this doesnt work when os.chdir() is called!
import graphingHandler as gh
import settingsHandler as sh
import voltagegen as vg
static = open(cwd + "/main.html", 'r')
cgitb.enable()
v=230
a=10
w=v*a
print("Content-Type: text/html;charset=utf-8\n\n")
print()
for data in static.readlines():
    print(data.rstrip('\n'))
print("<table id=\"data\">")
print("<tr>")
print("<td>Voltage<br>{}V</td>".format('%.2f'%vg.measure()))
print("<td>Current<br>{}A</td>".format(a))
print("</tr>")
print("<tr>")
print("<td>Wattage<br>{}W</td>".format(w))
print("<td>Graph Here</td>")
print("</tr>")
print("</table> ")
print("<table id=\"nodeshit\">")
print("<tr>")
print(f"<td>Node Name<br>{sh.readSettings()[4]}</td>")
print("<td>IP Address<br>{}</td>".format(socket.gethostbyname(socket.gethostname())))
print("</tr>")
print("<tr>")
print(f"<td>Firmware Version<br>{sh.readSettings()[5]}</td>")
print("<td>Uptime:<br>99999</td>")
print("</tr>")
print("</table>")
print("</BODY>")
print("</HTML>")
