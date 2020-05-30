from flask import Flask, redirect, url_for, render_template, jsonify
import datetime
import sqlite3

conn = sqlite3.connect('data.db')
c = conn.cursor()
currentDate = datetime.datetime.now()

day = currentDate.strftime("%d/%m/%Y %H:%M:%S")
beamSimulator = True

def createDataTab():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE data
                (date text)''')
    conn.commit()

def dropDataTab():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("DROP TABLE data")
    print("Table dropped...")
    conn.commit()

def insertNewMovement(t):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("INSERT INTO data VALUES (?)", t)
    conn.commit()

def getMovement():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('SELECT * FROM data')
    return c.fetchall()

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('index.html', currentD=day)

@app.route("/simulate/", methods=['POST'])
def newdate():
    beamSimulator = False
    if beamSimulator == False:
        currentDate = datetime.datetime.now()
        day = currentDate.strftime("%d/%m/%Y %H:%M:%S")
        print(day)
        insertNewMovement((day,))
        beamSimulator = True
    return redirect(url_for("home"))

@app.route("/render/", methods=['POST'])
def getdate():
    log = getMovement()
    logParsed = 'n'.join(map(str, log))
    logParsed = logParsed.replace("n", "")
    logParsed = logParsed.replace("(", "")
    logParsed = logParsed.replace("'", "")
    logParsed = logParsed.replace(")", " ")
    print(logParsed)
    return render_template('render.html', movementData=logParsed)

@app.route("/admin/create")
def admin():
    createDataTab()
    # dropDataTab()
    return redirect(url_for("home"))

@app.route("/admin/destroy")
def adminDest():
    dropDataTab()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run()

conn.close()