import flask as F
cwd = '/home/capstone/html/resources/pages'
cwdf = '/home/capstone/codebase'
app = F.Flask(__name__, template_folder=cwd)
@app.route("/main/", methods=['GET', 'POST'])
def main():
    return F.render_template('settings_main.html')
@app.route("/data/", methods=['GET', 'POST'])
def data():
    import sys
    sys.path.insert(1, '/home/capstone/codebase')
    import settingsHandler as sh
    data = {'nodename': sh.readSettings()[4]}
    return F.jsonify(data)
if __name__ == "__main__":
    app.run()
