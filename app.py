from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('html/index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('html/login.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)