import flask as F
cwd = '/home/capstone/html/resources/pages'
cwdf = '/home/capstone/codebase'
#sett = open(cwdf + '/pvt.xml', 'r')
#login = open(cwd + '/login.html', 'r')
app = F.Flask(__name__)
@app.route("/", methods=['GET', 'POST'])
def post():
    import sys
    sys.path.insert(1, '/home/capstone/codebase')
    import loginHandler as lh
##    return("True")
    if (lh.isLogin(str(F.request.json.get('fgt')))):
        return ("True")
    else:
        return ("False")
@app.route("/auth/", methods=['GET', 'POST'])
def auth():
    import sys
    sys.path.insert(1, '/home/capstone/codebase')
    import os, xml.etree.ElementTree as ET, loginHandler as lh, hashlib
    data = F.request.json
    cwdf = '/home/capstone/codebase'
    sett = open(cwdf + '/pvt.xml', 'r')
    settings = ET.parse(sett)
    root = settings.getroot()
    key = str(root.find(".private").attrib['key']) ##end of loading local files
    auth = str(data.get('auth')) + str(data.get('salt'))
    auth = str(hashlib.sha256(auth.encode('utf-8')).hexdigest())
    passh = str(hashlib.sha256((key+str(data.get('salt'))).encode('utf-8')).hexdigest()) #password hashed
    if (auth == passh):
        lh.newLogin(str(data.get('fgt')))
        return ("True")
    else:
        return ("False")
if __name__ == "__main__":
    app.run()
