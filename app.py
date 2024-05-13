from flask import Flask
from threading import Thread

# Configure flask server
app = Flask('')

@app.route('/')
def home() :
    return "Celestial Alert Server Running"

def run():
    app.run(host='0.0.0.0', port=8000)

# Keep the server alive
def keep_alive(): 
    t = Thread(target=run)
    t.start()
