import flask as F
cwd = '/home/capstone/html/resources/pages'
cwdf = '/home/capstone/codebase'
cwd_csv = '/home/capstone/codebase/csv'
app = F.Flask(__name__)
@app.route("/", methods=['GET', 'POST']) 
def dump():
    import sys, xml.etree.ElementTree as ET, csv, uuid, datetime, os
    rand = str(uuid.uuid4())
    sys.path.insert(1, cwdf)
    import loginHandler as lh, settingsHandler as sh
    if (F.request.args != None or lh.isLogin(str(F.request.args.get('fgt')))):
        files = [cwd_csv + '/' + file for file in os.listdir(cwd_csv)]
        if len(files) > 10: ##checking for extraneous files
            for files_delete in sorted(files, key=os.path.getctime)[:len(files)-10]:
                os.remove(files_delete)
        with open(cwdf+'/measurements.xml', 'r') as sett, open(cwd_csv + '/' + rand + '.csv', mode='w+') as file:
            measurements = ET.parse(sett)
            root = measurements.getroot()
            item = root.findall("./plot")
            timeoffset = int(F.request.args.get('timeoffset'))
            file_writer = csv.writer(file, dialect='excel')
            file_writer.writerow(['PowerHub Data Log', "Created " + datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")]) 
            file_writer.writerow(['',"Hint: Trends in power consumption can be seen easier if you use your favorite spreadsheet program's graphing tools."])
            file_writer.writerow(['Date / Time (according to Local Time)', 'Voltage', 'Current', 'Power Factor', 'Wattage', 'Notification Triggered?'])
            if (F.request.args.get('mode') == "entire"):
                for k in item:
                    if timeoffset < 0:
                        timeoffset = -timeoffset
                        time = datetime.datetime.strptime(k.attrib['date'], "%m/%d/%Y %H:%M:%S") - datetime.timedelta(hours=int(timeoffset/60), minutes=timeoffset%60)
                    else:
                        time = datetime.datetime.strptime(k.attrib['date'], "%m/%d/%Y %H:%M:%S") + datetime.timedelta(hours=int(timeoffset/60), minutes=timeoffset%60)
                    file_writer.writerow([time.strftime("%m/%d/%Y %H:%M:%S"),\
                                          k.attrib['voltage'], k.attrib['current'],\
                                          k.attrib['pf'], float(k.attrib['voltage']) * float(k.attrib['current']) * float(k.attrib['pf']),\
                                          k.attrib['notify']])
            if (F.request.args.get('mode') == "month"):
                date = [datetime.datetime.strptime(F.request.args.get('time'), "%m/%Y").month, datetime.datetime.strptime(F.request.args.get('time'), "%m/%Y").year]
                for k in item:
                    datadate = [datetime.datetime.strptime(k.attrib['date'], "%m/%d/%Y %H:%M:%S").month, datetime.datetime.strptime(k.attrib['date'], "%m/%d/%Y %H:%M:%S").year]
                    if datadate == date:
                        if timeoffset < 0:
                            timeoffset =- timeoffset
                            time = datetime.datetime.strptime(k.attrib['date'], "%m/%d/%Y %H:%M:%S") - datetime.timedelta(hours=int(timeoffset/60), minutes=timeoffset%60)
                        else:
                            time = datetime.datetime.strptime(k.attrib['date'], "%m/%d/%Y %H:%M:%S") + datetime.timedelta(hours=int(timeoffset/60), minutes=timeoffset%60)
                        file_writer.writerow([time.strftime("%m/%d/%Y %H:%M:%S"),\
                                          k.attrib['voltage'], k.attrib['current'],\
                                          k.attrib['pf'], float(k.attrib['voltage']) * float(k.attrib['current']) * float(k.attrib['pf']),\
                                          k.attrib['notify']])
            if (F.request.args.get('mode') == "week"):
                date = [datetime.datetime.strptime(F.request.args.get('time'), "%m/%d/%Y").strftime("%U"), datetime.datetime.strptime(F.request.args.get('time'), "%m/%d/%Y").year]
                for k in item:
                    datadate = [datetime.datetime.strptime(k.attrib['date'], "%m/%d/%Y %H:%M:%S").strftime("%U"), datetime.datetime.strptime(k.attrib['date'], "%m/%d/%Y %H:%M:%S").year]
                    if datadate == date:
                        if timeoffset < 0:
                            timeoffset =- timeoffset
                            time = datetime.datetime.strptime(k.attrib['date'], "%m/%d/%Y %H:%M:%S") - datetime.timedelta(hours=int(timeoffset/60), minutes=timeoffset%60)
                        else:
                            time = datetime.datetime.strptime(k.attrib['date'], "%m/%d/%Y %H:%M:%S") + datetime.timedelta(hours=int(timeoffset/60), minutes=timeoffset%60)
                        file_writer.writerow([time.strftime("%m/%d/%Y %H:%M:%S"),\
                                          k.attrib['voltage'], k.attrib['current'],\
                                          k.attrib['pf'], float(k.attrib['voltage']) * float(k.attrib['current']) * float(k.attrib['pf']),\
                                          k.attrib['notify']])
            if (F.request.args.get('mode') == "day"):
                for k in item:
                    if datetime.datetime.strptime(F.request.args.get('time'), "%m/%d/%Y").date() == datetime.datetime.strptime(k.attrib['date'], "%m/%d/%Y %H:%M:%S").date():
                        if timeoffset < 0:
                            timeoffset =- timeoffset
                            time = datetime.datetime.strptime(k.attrib['date'], "%m/%d/%Y %H:%M:%S") - datetime.timedelta(hours=int(timeoffset/60), minutes=timeoffset%60)
                        else:
                            time = datetime.datetime.strptime(k.attrib['date'], "%m/%d/%Y %H:%M:%S") + datetime.timedelta(hours=int(timeoffset/60), minutes=timeoffset%60)
                        file_writer.writerow([time.strftime("%m/%d/%Y %H:%M:%S"),\
                                          k.attrib['voltage'], k.attrib['current'],\
                                          k.attrib['pf'], float(k.attrib['voltage']) * float(k.attrib['current']) * float(k.attrib['pf']),\
                                          k.attrib['notify']])
        return F.send_file(cwd_csv + '/' + rand + '.csv', attachment_filename='PowerHub_dump.csv', as_attachment=True)
            
