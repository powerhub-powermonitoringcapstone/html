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
    if (True):# F.request.json != None or lh.isLogin(str(F.request.json.get('fgt')))):
        files = [cwd_csv + '/' + file for file in os.listdir(cwd_csv)]
        if len(files) > 10: ##checking for extraneous files
            for files_delete in sorted(files, key=os.path.getctime)[:len(files)-10]:
                os.remove(files_delete)
        with open(cwdf+'/measurements.xml', 'r') as sett, open(cwd_csv + '/' + rand + '.csv', mode='w+') as file:
            measurements = ET.parse(sett)
            root = measurements.getroot()
            item = root.findall("./plot")
            file_writer = csv.writer(file, dialect='excel')
            file_writer.writerow(['PowerHub Data Log', "Created " + datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")])
            file_writer.writerow(['',"Hint: Trends in power consumption can be seen easier if you use your favorite spreadsheet program's graphing tools."])
            file_writer.writerow(['Date / Time (UTC)', 'Voltage', 'Current', 'Power Factor', 'Wattage', 'Notification Triggered?'])
            if (True):#F.request.json.get('mode') == None):
                for k in item:
                    file_writer.writerow([k.attrib['date'], k.attrib['voltage'], k.attrib['current'],\
                                          k.attrib['pf'], float(k.attrib['voltage']) * float(k.attrib['current']) * float(k.attrib['pf']),\
                                          k.attrib['notify']])
                    
        return F.send_file(cwd_csv + '/' + rand + '.csv', attachment_filename='PowerHub_dump.csv', as_attachment=True)
            
