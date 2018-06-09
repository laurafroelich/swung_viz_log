from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/bootstrap')
def bootstrap():
    #return 'Hello again'
    return render_template('minimal_bootstrap.html')

if __name__ == '__main__':
    app.run()