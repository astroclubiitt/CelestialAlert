from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Celestial Alert Server Running :)"

if __name__ == "__main__":
    # Do not use app.run() for production
    app.run(host='0.0.0.0', port=8000)
