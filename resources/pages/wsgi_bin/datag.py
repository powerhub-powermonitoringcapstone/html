import flask as F
cwd = '/home/capstone/html/resources/pages'
cwdf = '/home/capstone/codebase'
#sett = open(cwdf + '/pvt.xml', 'r')
#login = open(cwd + '/login.html', 'r')
app = F.Flask(__name__)
@app.route("/", methods=['GET', 'POST']) ##real time data
def post():
    import sys, xml.etree.ElementTree as ET
    sys.path.insert(1, cwdf)
    import loginHandler as lh, settingsHandler as sh
    if (F.request.json != None and lh.isLogin(str(F.request.json.get('fgt')))):
        with open(cwdf+'/measurements.xml', 'r') as sett:
            measurements = ET.parse(sett)
            root = measurements.getroot()
            last = root.findall("./plot")[-1]
        data = {'voltage': last.attrib['voltage'], 'current': last.attrib['current'], 'nodename': sh.readSettings()[4], 'firmware':sh.readSettings()[5]}
        return F.jsonify(data)
    else:
        return F.jsonify({'auth':'false'})
@app.route("/graph/", methods=['GET', 'POST']) #past data array, graphing
def graph():
    import sys, xml.etree.ElementTree as ET
    sys.path.insert(1, cwdf)
    import loginHandler as lh, settingsHandler as sh
    if (F.request.json != None and lh.isLogin(str(F.request.json.get('fgt')))):
        data = []
        with open(cwdf+'/measurements.xml', 'r') as sett:
            measurements = ET.parse(sett) 
            root = measurements.getroot()      
            if (F.request.json.get('mode') == "real"): ## latest 50 readings
                item = root.findall("./plot")[-50:]
                for k in range(len(item)):
                    data.append({'voltage': item[k].attrib['voltage'], 'current': item[k].attrib['current']})
                return F.jsonify(data)
            else:
                if (F.request.json.get('mode') == "start"): ## since program start
                    ## since last start
                    item = root.findall("./plot[@n='1']")[-1]
                    read = root[list(root).index(item):]
                    for k in range(len(read)):
                        data.append({'voltage': read[k].attrib['voltage'], 'current': read[k].attrib['current']})
                    return F.jsonify(data)
if __name__ == "__main__":
    app.run()
