#!/usr/bin/python3
# -*- coding: UTF-8 -*-# enable debugging
import cgitb, os, sys
sys.path.insert(1, '/home/capstone/codebase/')
cwd = os.path.dirname(os.path.realpath(__file__))#take note this doesnt work when os.chdir() is called!
import graphingHandler as gh
import settingsHandler as sh
static = open(cwd + "/settings.html", 'r')
cgitb.enable()
v=230
a=10
w=v*a
print("Content-Type: text/html;charset=utf-8\n")
print()
for data in static.readlines():
    print(data.rstrip('\n'))
print("<body>")
print("<div style=\"height:96px\"></div><!--placeholder-->")
print("<img id=\"intro_logo\" class=\"main\" src=\"../logo1.png\">")
print("<div class=\"navbuttons\" onClick=\"security()\">Security Controls<span class=\"navarrow\">&#x3009;</span></div><br>")
print("<div class=\"navbuttons\">Firmware Update<span class=\"navarrow\">&#x3009;</span></div><br>")
print(f"<div class=\"navbuttons\">Node Name...<span class=\"navparm\">{sh.readSettings()[4]}</span><span class=\"navarrow\">&#x3009;</span></div><br>")
print("<div class=\"navbuttons\">About<span class=\"navarrow\">&#x3009;</span></div><br>")
print("<!--security-->")
print("<div class=\"security\">MAC Address<span class=\"security\" style=\"position:fixed; left:210px\">Status</span></div><br>")
print("<div class=\"security\">Client Info<span class=\"security\" style=\"position:fixed; left:332px\">&#x3009;</span></div>")
print("<iframe id=\"nav\" class=\"main\"src=\"nav.html?from=settings\"></iframe>")
print("</body>")
print("</HTML>")
