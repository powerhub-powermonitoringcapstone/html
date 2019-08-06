#!/usr/bin/python3
# -*- coding: UTF-8 -*-# enable debugging
import cgitb, cgi, hashlib, os, sys
import xml.etree.ElementTree as ET
cgitb.enable()
sys.path.insert(1, '/home/capstone/codebase')
import loginHandler as lh
cwd = os.path.dirname(os.path.realpath(__file__))#take note this doesnt work when os.chdir() is called!
cwdf = '/home/capstone/codebase/'
login = open (cwd + '/login.html', 'r')
sett = open(cwdf + '/pvt.xml', 'r') #element tree stuff
settings = ET.parse(sett)
root = settings.getroot()
found = root.find(".private").attrib['key']
auth = (cgi.FieldStorage()).getvalue('auth') #get value of passphrase
fgt = (cgi.FieldStorage()).getvalue('fgt') #get value of fingerprint
salt = (cgi.FieldStorage()).getvalue('salt') #get value of salt
print("Content-Type: text/html;charset=utf-8\n\n")
print()
def fullAuth():
    global auth, salt
    auth += salt #hash n salt
    auth = hashlib.sha256(auth.encode('utf-8'))
    auth = auth.hexdigest()
    auth = str(auth)
    passh = str(hashlib.sha256((found+salt).encode('utf-8')).hexdigest()) #password hashed
    print("<!DOCTYPE HTML><HTML>")
    if (lh.isLogin(fgt)):
        print("<script>")
        print("window.location.href = \"main.py\";")
        print("</script>")
        print("<\HTML>")
    else:
        if (auth == passh):
            lh.newLogin(fgt)
            print("<script>")
            print("window.location.href = \"main.py\";")
            print("</script>")
            print("<\HTML>")
        else:
            print("<script>")
            print("alert(\"Wrong Password!\");")
            print("window.location.href = \"login.html\";")
            print("</script>")
            print("<\HTML>")
    ##print(auth + "<br>Salt:" + fgt + "<br>Salted" + passh)
if (fgt != None):
    fullAuth()
else:
    for line in login.readlines():
        print (line)
##    print("<script>")
##    print("window.location.href = \"login.html\";")
##    print("</script>")
##    print("<\HTML>")


