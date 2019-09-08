import flask as F
import sys
cwd = '/home/capstone/html/resources/pages'
cwdf = '/home/capstone/codebase'
app = F.Flask(__name__, template_folder=cwd)
@app.route("/main/")
def main(): ## weird rendering shit na ewan ko bat ko ginawa hehe
    return F.render_template('settings_main.html')
@app.route("/security/")
def secu():
    return F.render_template('settings_security.html')
##@app.route("/debug/", methods=['GET', 'POST'])
##def debug():             debug settings: restart server n all that
####    import sys
##    if (F.request.args != None and lh.isLogin(str(F.request.json.get('fgt')))):
@app.route("/data/", methods=['GET', 'POST'])
def data():
##    import sys
    sys.path.insert(1, '/home/capstone/codebase')
    import settingsHandler as sh, loginHandler as lh
    if (F.request.json != None and lh.isLogin(str(F.request.json.get('fgt')))):
        data = {'isSetup':sh.readSettings()[0],\
                'datalogging':sh.readSettings()[1],\
                'threshold':sh.readSettings()[2],\
                'debug':sh.readSettings()[3],\
                'nodename':sh.readSettings()[4],\
                'version':sh.readSettings()[5],\
                'nodetype':sh.readSettings()[6],\
                'permanence':sh.readSettings()[7],\
                }
        return F.jsonify(data)
    else:
        data = {'nodename': sh.readSettings()[4], \
                'nodetype': sh.readSettings()[6], \
                }
        return F.jsonify(data)
            
        
@app.route("/data/write/", methods=['GET', 'POST'])
def write():
##  dito na iveverify yung settings para di cluttered yung internal handler
    return ("yeah")
if __name__ == "__main__":
    app.run()
