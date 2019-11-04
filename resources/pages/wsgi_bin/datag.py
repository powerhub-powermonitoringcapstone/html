import flask as F
cwd = '/home/capstone/html/resources/pages'
cwdf = '/home/capstone/codebase'
#sett = open(cwdf + '/pvt.xml', 'r')
#login = open(cwd + '/login.html', 'r')
app = F.Flask(__name__)
@app.route("/real/", methods=['GET', 'POST']) ##real time data
def realtimeGraph():
    import sys, xml.etree.ElementTree as ET
    sys.path.insert(1, cwdf)
    import loginHandler as lh, settingsHandler as sh
    if (F.request.json != None and lh.isLogin(str(F.request.json.get('fgt')))):
        with open(cwdf+'/measurements.xml', 'r') as sett:
            measurements = ET.parse(sett)
            root = measurements.getroot()
            item = root.findall("./plot")
            kilowatts = 0
            for entries in item:
                kilowatts += float(entries.attrib['voltage']) * float(entries.attrib['current']) * float(entries.attrib['pf'])
            kilowatts = kilowatts/3600/1000
        data = {'voltage': item[-1].attrib['voltage'], 'current': item[-1].attrib['current'], \
                'variation':item[-1].attrib['variation'], 'notify':item[-1].attrib['notify'], \
                'nodename': sh.readSettings()[4], 'firmware':sh.readSettings()[5],\
                'wattage': float(item[-1].attrib['voltage']) * float(item[-1].attrib['current']) * float(item[-1].attrib['pf']), 'kwh': kilowatts, 'pf': item[-1].attrib['pf']}
        return F.jsonify(data)
    else:
        return F.jsonify({'auth':'false'})
@app.route("/past/", methods=['GET', 'POST']) #past data array, graphing
def pastData():
    import sys, xml.etree.ElementTree as ET, datetime
    sys.path.insert(1, cwdf)
    import loginHandler as lh, settingsHandler as sh
    if (F.request.json != None and lh.isLogin(str(F.request.json.get('fgt')))):
        data = []
        with open(cwdf+'/measurements.xml', 'r') as sett:
            measurements = ET.parse(sett) 
            root = measurements.getroot()
            item = root.findall("./plot")
            if (F.request.json.get('mode') == "last"): ## latest 60 readings
                item = item[-60:]
                for k in range(len(item)):
                    data.append({'voltage': item[k].attrib['voltage'], 'current': item[k].attrib['current'], 'pf': item[k].attrib['pf']})
                return F.jsonify(data)
            else:
                if (F.request.json.get('mode') == "start"): ## since program start
                    item = root.findall("./plot[@n='1']")[-1]
                    read = root[list(root).index(item):]
                    for k in range(len(read)):
                        data.append({'voltage': read[k].attrib['voltage'], 'current': read[k].attrib['current'], 'pf': item[k].attrib['pf']})
                    return F.jsonify(data)
                else:
                    if (F.request.json.get('mode') == "day"): ##readings throughout a day
                        for stuff in item:
                            if (datetime.datetime.strptime(item[k].attrib['date'], "%m/%d/%Y %H:%M:%S").date() == datetime.datetime.strptime(F.request.get('time'), "%m/%d/%Y").date()):
                                data.append({'voltage': item[k].attrib['voltage'], 'current': item[k].attrib['current'], 'pf': item[k].attrib['pf']})
                        return F.jsonify(data)
                    else:
                        if (F.request.json.get('mode') == "datescurr"): ## available months for current year
                            months = []
                            for k in range(len(item)):
                                if (datetime.datetime.strptime(item[k].attrib['date'], "%m/%d/%Y %H:%M:%S").date().year == datetime.datetime.now(datetime.timezone.utc).year):
                                    if (months.count(datetime.datetime.strptime(item[k].attrib['date'], "%m/%d/%Y %H:%M:%S").date().month) == 0):
                                        months.append(datetime.datetime.strptime(item[k].attrib['date'], "%m/%d/%Y %H:%M:%S").date().month)
                            return F.jsonify(months)
                        else:
                            if (F.request.json.get('mode') == "week"): ##readings throughout a week
                                for k in range(len(item)):
                                    if (datetime.datetime.strptime(item[k].attrib['date'], "%m/%d/%Y %H:%M:%S").date().strftime("%U") == datetime.datetime.strptime(F.request.get('time'), "%m/%d/%Y").date().strftime("%U")):
                                        data.append({'voltage': item[k].attrib['voltage'], 'current': item[k].attrib['current'], 'pf': item[k].attrib['pf']})
                                return F.jsonify(data)
                            
                        
if __name__ == "__main__":
    app.run()
