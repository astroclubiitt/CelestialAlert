from flask import Flask

# Configure flask server
app = Flask('')

@app.route('/')
def home():
    return "Celestial Alert Server Running :)"

# No need for the keep_alive function if using Gunicorn or another WSGI server
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
