import flask as F
cwd = '/home/capstone/html/resources/pages'
cwdf = '/home/capstone/codebase'
app = F.Flask(__name__)
@app.route("/", methods=['GET', 'POST'])
def post():
    import sys
    sys.path.insert(1, '/home/capstone/codebase')
    import loginHandler as lh, settingsHandler as sh
    if (lh.isLogin(str(F.request.json.get('fgt'))) and sh.readSettings()[0] == "True"):
        return ("True")
    else:
        if (sh.readSettings()[0] == "True"):
            return ("False")
        else:
            return ("Setup")
@app.route("/auth/", methods=['GET', 'POST'])
def auth():
    import sys
    sys.path.insert(1, '/home/capstone/codebase')
    import loginHandler as lh
    data = F.request.json
    return (lh.authenticate(data.get('auth'), data.get('fgt')))
@app.route("/change/", methods=['GET', 'POST'])
def change():
    import sys
    sys.path.insert(1, '/home/capstone/codebase')
    import loginHandler as lh
    data = F.request.json
    return (lh.changeKey(data.get('auth'), data.get('fgt')))
 
if __name__ == "__main__":
    app.run()
