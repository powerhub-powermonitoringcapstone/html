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
    import settingsHandler as sh
    data = {'voltage': 230, 'current': 5, 'nodename': sh.readSettings()[4], 'firmware':sh.readSettings()[5]}
    return F.jsonify(data)

if __name__ == "__main__":
    app.run()
