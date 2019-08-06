import flask as F
app = F.Flask(__name__)
@app.route("/kantutan/")
def manacc():
    return "Hello World!"
if __name__ == "__main__":
    app.run()
