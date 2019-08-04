#!/usr/bin/python3
# -*- coding: UTF-8 -*-# enable debugging
import cgitb, cgi, hashlib, os, sys
import xml.etree.ElementTree as ET
cgitb.enable()
sys.path.insert(1, '/home/capstone/codebase/')
cwdf = '/home/capstone/codebase/'
sett = open(cwdf + 'pvt.xml', 'r') #element tree stuff
settings = ET.parse(sett)
root = settings.getroot()
found = root.find(".private").attrib['key']
auth = (cgi.FieldStorage()).getvalue('auth') #get value
fgt = (cgi.FieldStorage()).getvalue('fgt') #get value of fingerprint
auth = auth + fgt #hash n salt
auth = hashlib.sha256(auth.encode('utf-8'))
auth = auth.hexdigest()
auth = str(auth)
passh = str(hashlib.sha256((found+fgt).encode('utf-8')).hexdigest()) #password hashed
print("Content-Type: text/html;charset=utf-8\n\n")
print()
print(auth + "<br>Salt:" + fgt + "<br>Salted" + passh)

