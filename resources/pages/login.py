#!/usr/bin/python3
# -*- coding: UTF-8 -*-# enable debugging
import cgitb, cgi, hashlib
cgitb.enable()
form = cgi.FieldStorage()
form = form.getvalue('auth')
form = form.encode('utf-8')
fgt = cgi.FieldStorage()
fgt = fgt.getvalue('fgt')
fgt = fgt.encode('utf-8') ##fingerprint as salt
form = form + fgt

form = hashlib.sha256(form)
form = form.hexdigest()
form = str(form)
fgt = str(fgt).lstrip('b')
##fgt = hashlib.sha256(fgt)
##fgt = fgt.hexdigest()
print("Content-Type: text/html;charset=utf-8\n\n")
print()
print(form + "<br>" + "Salt:" + fgt)

