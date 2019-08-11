##import sys
##sys.path.insert(0, '/home/capstone/html/resources/pages/wsgi_bin/')
import flask as F
app = F.Flask(__name__)
#@app.route("/query-get/")
#def manacc():
#    arg = F.request.args.get('fuck')
#    return "Hello World! Fuck {}".format(arg)
@app.route("/") #methods=['POST'])
def post():
    ans = F.request.form.get('auth')
    arg = F.request.args.get('fuck')
    return "Hello World! Fuck {}".format(arg)
    if (ans == "powerhub"):
        return "<script>alert(\"tanga amat\");</script>"
    else:
        return "<script>alert(\"tanga male\");</script>"
if __name__ == "__main__":
    app.run()
