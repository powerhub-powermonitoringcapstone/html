#!/usr/bin/python3
# -*- coding: UTF-8 -*-# enable debugging
#powerhub intro authenticator code (c)2019
import cgitb, os, sys
sys.path.insert(1, '/home/capstone/codebase/')
cwd = os.path.dirname(os.path.realpath(__file__))#take note this doesnt work when os.chdir() is called!
import graphingHandler as gh
import settingsHandler as sh
static = open(cwd + "/intro.html", 'r')
cgitb.enable()
v=230
a=10
w=v*a
print("Content-Type: text/html;charset=utf-8\n")
print()
for data in static.readlines():
    print(data.rstrip('\n'))
