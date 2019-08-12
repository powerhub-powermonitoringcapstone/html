import flask as F
cwd = '/home/capstone/html/resources/pages'
cwdf = '/home/capstone/codebase'
#sett = open(cwdf + '/pvt.xml', 'r')
#login = open(cwd + '/login.html', 'r')
app = F.Flask(__name__)
@app.route("/", methods=['GET', 'POST'])
def post():
    return "230"##F.jsonify(voltage='230')

if __name__ == "__main__":
    app.run()
