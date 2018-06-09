from flask import Flask, render_template
app = Flask(__name__)

# Landing page
@app.route('/index.html')
@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/bootstrap')
def bootstrap():
    return render_template('minimal_bootstrap.html')


@app.route('/interactive_plots')
def bootstrap():
    return render_template('interactive_plots.html')

if __name__ == '__main__':
    app.run()