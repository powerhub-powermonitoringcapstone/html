import flask as F
cwd = '/home/capstone/html/resources/pages'
cwdf = '/home/capstone/codebase'
app = F.Flask(__name__, template_folder=cwd)
@app.route("/main/")
def main():
    return F.render_template('settings_main.html')
@app.route("/security/")
def secu():
    return F.render_template('settings_security.html')
@app.route("/data/", methods=['GET', 'POST'])
def data():
    import sys
    sys.path.insert(1, '/home/capstone/codebase')
    import settingsHandler as sh
    data = {'nodename': sh.readSettings()[4]}
    return F.jsonify(data)
@app.route("/data/write/", methods=['GET', 'POST'])
def write():
##  dito na iveverify yung settings para di cluttered yung internal handler
    return ("yeah")
if __name__ == "__main__":
    app.run()
