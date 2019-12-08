import flask as F
cwd = '/home/capstone/html/resources/pages'
cwdf = '/home/capstone/codebase'
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
        with open(cwdf+'/measurements.xml', 'r') as sett:
            measurements = ET.parse(sett) 
            root = measurements.getroot()
            item = root.findall("./plot")
            if (F.request.json.get('mode') == "last"): ## latest 60 readings
                item = item[-60:]
                data = [{'voltage': k.attrib['voltage'], 'current': k.attrib['current'], 'pf': k.attrib['pf']} for k in item]
            if (F.request.json.get('mode') == "start"): ## since last data reset
                data = [{'voltage': k.attrib['voltage'], 'current': k.attrib['current'], 'pf': k.attrib['pf'], 'date': k.attrib['date']} for k in item]
            if (F.request.json.get('mode') == "day"): ##readings throughout a day
                data = [{'voltage': k.attrib['voltage'], 'current': k.attrib['current'], 'pf': k.attrib['pf'], 'date': k.attrib['date']} for k in item \
                        if datetime.datetime.strptime(k.attrib['date'], "%m/%d/%Y %H:%M:%S").date() == datetime.datetime.strptime(F.request.json.get('time'), "%m/%d/%Y").date()]
            if (F.request.json.get('mode') == "week"): ##readings throughout a week
                data = [{'voltage': k.attrib['voltage'], 'current': k.attrib['current'], 'pf': k.attrib['pf'], 'date': k.attrib['date']} for k in item \
                        if datetime.datetime.strptime(k.attrib['date'], "%m/%d/%Y %H:%M:%S").date().strftime("%U") == datetime.datetime.strptime(F.request.json.get('time'), "%m/%d/%Y").date().strftime("%U")]
            return F.jsonify(data)
@app.route("/dates/", methods=['GET', 'POST'])#Dates only, not data
def dates():
    import sys, xml.etree.ElementTree as ET, datetime
    sys.path.insert(1, cwdf)
    import loginHandler as lh, settingsHandler as sh
    if (F.request.json != None and lh.isLogin(str(F.request.json.get('fgt')))):
        data = []
        with open(cwdf+'/measurements.xml', 'r') as sett:
            measurements = ET.parse(sett) 
            root = measurements.getroot()
            item = root.findall("./plot")
            data = []
            if (F.request.json.get('mode') == "months"): ## available months for current year
                for k in item:
                    if datetime.datetime.strptime(k.attrib['date'], "%m/%d/%Y %H:%M:%S").date().year == datetime.datetime.now(datetime.timezone.utc).year and datetime.datetime.strptime(k.attrib['date'], "%m/%d/%Y %H:%M:%S").date().month not in data:
                        data.append(datetime.datetime.strptime(k.attrib['date'], "%m/%d/%Y %H:%M:%S").date().month)
            if (F.request.json.get('mode') == "weeks"): ##mm-dd-yyyy for within a week
                weekr = datetime.datetime.strptime(F.request.get('time'), "%m/%d/%Y %H:%M:%S").date().strftime("%U")## date and time from request
                for k in item:
                    if datetime.datetime.strptime(k.attrib['date'], "%m/%d/%Y %H:%M:%S").date().strftime("%U") == weekr and datetime.datetime.strftime(datetime.datetime.strptime(k.attrib['time'], "%m/%d/%Y %H:%M:%S").date(), "%m/%d/%Y") not in data:
                        data.append(datetime.datetime.strftime(datetime.datetime.strptime(k.attrib['time'], "%m/%d/%Y %H:%M:%S").date(), "%m/%d/%Y"))
            return F.jsonify(data)
if __name__ == "__main__":
    app.run()
