##import sys
import flask as F
##sys.path.insert(1, '/home/capstone/codebase')
##import loginHandler as lh
##cwd = '/home/capstone/html/resources/pages'
##cwdf = '/home/capstone/codebase'
#sett = open(cwdf + '/pvt.xml', 'r')
#login = open(cwd + '/login.html', 'r')
app = F.Flask(__name__)
@app.route("/", methods=['POST', 'GET'])
def post():
    ##fgt = F.request.args.get('test')
    fgt = F.request.get_json().get('test')
    return ("Duck {}".format(fgt))
if __name__ == "__main__":
    app.run()
