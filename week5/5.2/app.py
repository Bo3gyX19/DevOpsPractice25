from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the web application!"

@app.route('/version')
def version():
    return "Version: 1.0.0"

@app.route('/health')
def health():
    return "OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
