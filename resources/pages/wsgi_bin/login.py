import flask as F
cwd = '/home/capstone/html/resources/pages'
cwdf = '/home/capstone/codebase'
app = F.Flask(__name__)
@app.route("/", methods=['GET', 'POST'])
def post():
    import sys
    sys.path.insert(1, '/home/capstone/codebase')
    import loginHandler as lh
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
    sett = open(cwdf + '/pvt.xml', 'r')
    settings = ET.parse(sett)
    root = settings.getroot()
    key = str(root.find(".private").attrib['key'])
    salt = str(root.find(".private").attrib['salt'])##end of loading local files
    auth = str(data.get('auth')) + salt
    auth = str(hashlib.sha256(auth.encode('utf-8')).hexdigest())
    if (auth == key):
        lh.newLogin(str(data.get('fgt')))
        return ("True")
    else:
        return ("False")
@app.route("/change/", methods=['GET', 'POST'])
def change():
    import sys, uuid, os, xml.etree.ElementTree as ET, hashlib
    sys.path.insert(1, '/home/capstone/codebase')
    import loginHandler as lh
    lh.clear()
    data = F.request.json
    salt = str(uuid.uuid4())
    auth = str(hashlib.sha256((data.get('auth') + salt).encode('utf-8')).hexdigest())
    with open(cwdf + '/pvt.xml', 'r') as sett:
        settings = ET.parse(sett)
        root = settings.getroot()
        found = root.find("./private")
        if (found == None and lh.isLogin(data.get('fgt'))):
            root.append(ET.Element("private", {'key': auth, 'salt': salt}))
        else:
            found.set('key', auth)
            found.set('salt', salt)
        with open (cwdf + '/pvt.xml', 'wb') as settw:
            settings.write(settw)
            settw.close()
    return ("True") ## success
if __name__ == "__main__":
    app.run()
