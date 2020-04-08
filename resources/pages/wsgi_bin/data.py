import flask as F
cwd = '/home/capstone/html/resources/pages'
cwdf = '/home/capstone/codebase'
app = F.Flask(__name__)
@app.route("/real/", methods=('GET', 'POST')) ##real time data
def realtimeGraph():
    import sys, lxml.etree as ET, portalocker
    sys.path.insert(1, cwdf)
    import loginHandler as lh, settingsHandler as sh
    refreshrate = int(sh.readSettings()[9])
    if (F.request.json != None and lh.isLogin(str(F.request.json.get('fgt')))):
        datafile = open(cwdf + '/measurements.xml', 'r+')
        lock = False
        while lock == False:
            try:
                lock = True
                with portalocker.Lock(cwdf + '/measurements.xml', 'r+') as datafile:
                    root = ET.parse(datafile)
                    item = root.findall("plot")
                    kilowatts = 0            
                    for entries in item:
                        kilowatts += float(entries.get('voltage')) * float(entries.get('current')) * float(entries.get('pf'))
                    kilowatts = kilowatts/refreshrate/1000
                    data = {'voltage': item[-1].get('voltage'), 'current': item[-1].get('current'), \
                            'variation': item[-1].get('variation'), 'notify':item[-1].get('notify'), \
                            'nodename': sh.readSettings()[4], 'firmware':sh.readSettings()[5],\
                            'wattage': float(item[-1].get('voltage')) * float(item[-1].get('current')) * float(item[-1].get('pf')), 'kwh': kilowatts, 'pf': item[-1].get('pf')}                    
            except portalocker.exceptions.LockException:
                pass
        return F.jsonify(data)
    else:
        return("Not logged in yet.")
@app.route("/past/", methods=('GET', 'POST')) #past data array, graphing
def pastData():
    import sys, lxml.etree as ET, datetime, portalocker
    sys.path.insert(1, cwdf)
    import loginHandler as lh, settingsHandler as sh
    if (F.request.json != None and lh.isLogin(str(F.request.json.get('fgt')))):
        data = []
        lock = False
        while lock == False:
            try:
                with portalocker.Lock(cwdf + '/measurements.xml', 'r+') as datafile:
                    lock = True
                    root = ET.parse(datafile)
                    if (F.request.json.get('mode') == "start"): ## since last data reset
                        data = [{'voltage': k.get('voltage'), 'current': k.get('current'), 'pf': k.get('pf'), 'date': k.get('date')} for k in root.iter("plot")]
                    if (F.request.json.get('mode') == "lastmin"): ## readings from the last n minute
                        item = root.findall("plot")
                        mins = int(F.request.json.get('time'))
                        for k in item:
                            if (datetime.datetime.strptime(k.get('date'), "%m/%d/%Y %H:%M:%S") >= datetime.datetime.strptime(item[-1].get('date'), "%m/%d/%Y %H:%M:%S") - datetime.timedelta(minutes=mins, seconds=-1)):
                                data.append({'voltage': k.get('voltage'), 'current': k.get('current'), 'pf': k.get('pf'), 'date': k.get('date')})
                    if (F.request.json.get('mode') == "day"): ##readings throughout a day
                        for k in root.iter("plot"):
                            if (datetime.datetime.strptime(k.get('date'), "%m/%d/%Y %H:%M:%S").date() == datetime.datetime.strptime(F.request.json.get('time'), "%m/%d/%Y")):
                                data.append({'voltage': k.get('voltage'), 'current': k.get('current'), 'pf': k.get('pf'), 'date': k.get('date')})
                    if (F.request.json.get('mode') == "week"): ##readings throughout a week
                        for k in root.iter("plot"):
                            if (datetime.datetime.strptime(k.get('date'), "%m/%d/%Y %H:%M:%S").date().strftime("%U") == datetime.datetime.strptime(F.request.json.get('time'), "%m/%d/%Y").date().strftime("%U")):
                                data.append({'voltage': k.get('voltage'), 'current': k.get('current'), 'pf': k.get('pf'), 'date': k.get('date')})
                    if (F.request.json.get('mode') == "month"): ##readings throughout a month
                        for k in root.iter("plot"):
                            if (datetime.datetime.strptime(k.get('date'), "%m/%d/%Y %H:%M:%S").month == datetime.datetime.strptime(F.request.json.get('time'), "%m/%Y").month):
                                data.append({'voltage': k.get('voltage'), 'current': k.get('current'), 'pf': k.get('pf'), 'date': k.get('date')})                    
            except portalocker.exceptions.LockException:
                pass
        return F.jsonify(data)
    else:
        return("Not logged in yet.")
@app.route("/dates/", methods=('GET', 'POST'))#Dates only, not data
def dates():
    import sys, xml.etree.ElementTree as ET, datetime, portalocker
    sys.path.insert(1, cwdf)
    import loginHandler as lh, settingsHandler as sh
    if (F.request.json != None and lh.isLogin(str(F.request.json.get('fgt')))):
        data = []
        lock = False
        while lock == False:
            try:
                with portalocker.Lock(cwdf + '/measurements.xml', 'r+') as datafile:
                    lock = True
                    item = ET.parse(datafile).iter("plot")
                    if (F.request.json.get('mode') == "months"): ## available months for year
                        year = datetime.datetime.strptime(F.request.json.get('time'), "%Y").year
                        for k in item:
                            if datetime.datetime.strptime(k.get('date'), "%m/%d/%Y %H:%M:%S").year == year and datetime.datetime.strptime(k.get('date'), "%m/%d/%Y %H:%M:%S").month not in data:
                                data.append(datetime.datetime.strptime(k.get('date'), "%m/%d/%Y %H:%M:%S").month)
                    if (F.request.json.get('mode') == "weeks"): ##mm-dd-yyyy for within a week
                        weekr = datetime.datetime.strptime(F.request.json.get('time'), "%m/%d/%Y %H:%M:%S").strftime("%U")## date and time from request
                        for k in item:
                            if datetime.datetime.strptime(k.get('date'), "%m/%d/%Y %H:%M:%S").strftime("%U") == weekr and datetime.datetime.strftime(datetime.datetime.strptime(k.get('time'), "%m/%d/%Y %H:%M:%S"), "%m/%d/%Y") not in data:
                                data.append(datetime.datetime.strftime(datetime.datetime.strptime(k.get('time'), "%m/%d/%Y %H:%M:%S"), "%m/%d/%Y"))
                    if (F.request.json.get('mode') == "days"): ##available days within a month
                        request = [datetime.datetime.strptime(F.request.json.get('time'), "%m/%Y").month, datetime.datetime.strptime(F.request.json.get('time'), "%m/%Y").year]
                        for k in item:
                            datefile = datetime.datetime.strptime(k.get('date'), "%m/%d/%Y %H:%M:%S")
                            if datefile.month == request[0] and datefile.year == request[1] and datetime.datetime.strftime(datefile, "%d") not in data:
                                data.append(datetime.datetime.strftime(datefile, "%d"))
                    if (F.request.json.get('mode') == "years"): ## available years
                        for k in item:
                            if datetime.datetime.strptime(k.get('date'), "%m/%d/%Y %H:%M:%S").year not in data:
                                data.append(datetime.datetime.strptime(k.get('date'), "%m/%d/%Y %H:%M:%S").year)
            except portalocker.exceptions.LockException:
                pass
        return F.jsonify(data)
    else:
        return("Not logged in yet.")        
if __name__ == "__main__":
    app.run()
