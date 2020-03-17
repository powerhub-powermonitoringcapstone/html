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
@app.route("/data/", methods=['GET', 'POST'])
def data():
##    import sys
    sys.path.insert(1, cwdf)
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
                'carbfpt':sh.readSettings()[8],\
                'refresh':sh.readSettings()[9],\
                'kilowattlimit':sh.readSettings()[10],\
                'kilowattlimitenabled':sh.readSettings()[11],\
                }
        return F.jsonify(data)
    else:
        data = {'nodename': sh.readSettings()[4], \
                'nodetype': sh.readSettings()[6], \
                'isSetup' : sh.readSettings()[0], \
                }
        return F.jsonify(data)
@app.route("/emails/", methods=['GET', 'POST'])
def emails():
    sys.path.insert(1, cwdf)
    import settingsHandler as sh, loginHandler as lh
    if (F.request.json != None and lh.isLogin(str(F.request.json.get('fgt')))):
        data = {'emailaddr1':sh.readSettings()[12],\
                'emailaddr2':sh.readSettings()[13],\
                'emailaddr3':sh.readSettings()[14],\
                'emailaddr4':sh.readSettings()[15],\
                'emailaddr5':sh.readSettings()[16],\
                'emailaddr6':sh.readSettings()[17],\
                'emailaddr7':sh.readSettings()[18],\
                'emailaddr8':sh.readSettings()[19],\
                'emailaddr9':sh.readSettings()[20],\
                'emailaddr10':sh.readSettings()[21],\
                }
        return F.jsonify(data)
    else:
        return "You are not allowed to access this resource."
        
@app.route("/write/", methods=['GET', 'POST'])
def write():
    d = {0:'IsSetup',1:'DataLogging',2:'SensitivityThreshold'\
     ,3:'Debug', 4:'NodeName', 5:'Version', 6:'NodeType',\
     7:'Permanence', 8:'CarbonFootprint', 9:'RefreshRate', 10:'KilowattLimit', 11:'KilowattLimitEnabled'}
    sys.path.insert(1,cwdf)
    import settingsHandler as sh, loginHandler as lh
    if (F.request.json != None and lh.isLogin(str(F.request.json.get('fgt')))):
        for data in range(len(d)):
            if (F.request.json.get(d[data]) != None):
                sh.riteSettings(data, F.request.json.get(d[data]))
    return ("yuh")
if __name__ == "__main__":
    app.run()
