#!/usr/bin/python3
# -*- coding: UTF-8 -*-# enable debugging
import cgitb, cgi
cgitb.enable()
form = cgi.FieldStorage()
print("Content-Type: text/html;charset=utf-8\n\n")
print()
print(form.getvalue('auth'))

