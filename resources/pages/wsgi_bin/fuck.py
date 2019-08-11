import flask as F
cwd = '/home/capstone/html/resources/pages'
cwdf = '/home/capstone/codebase'
#sett = open(cwdf + '/pvt.xml', 'r')
#login = open(cwd + '/login.html', 'r')
app = F.Flask(__name__)
@app.route("/", methods=['POST', 'GET'])
def post():
    import sys
    sys.path.insert(1, '/home/capstone/codebase')
    import loginHandler as lh
    fgt = F.request.get_json().get('fgt')
    if (lh.isLogin(fgt)):
        return ("True")
    else:
        return ("False")
if __name__ == "__main__":
    app.run()
