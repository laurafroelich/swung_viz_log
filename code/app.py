from flask import Flask, render_template, request
app = Flask(__name__)
import read_data
import plotting
import holoviews as hv
import bokeh
hv.extension('bokeh')

# Landing page
@app.route('/index.html')
@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/bootstrap')
def bootstrap():
    return render_template('minimal_bootstrap.html')


@app.route('/interactive_plots', methods = ['GET', 'POST'])
def interactive_plots():

    print('a')

    current_feature_name = request.args.get("feature_name")
    if current_feature_name == None:
        current_feature_name = "GR"

    input_file = "../data/EAGE2018/Well-A_finished/HQLD_B_2C1_75-1_Well-A_ISF-BHC-MSFL-GR__COMPOSIT__1.LAS"
    result = read_data.read(input_file).df()
    result_small = result[current_feature_name]
    print(result_small.name)



    plot = result_small.plot()
    print(current_feature_name)
    fig = plot.get_figure()
    fname="output{}.png".format(current_feature_name)
    fig.savefig('static/{}'.format(fname))


    mytext = "Hello with my text"

    #myimage = plotting.plot_two_columns(result.df(), result_keys[1], result_keys[2])
    #print(type(myimage))
    #print(myimage)
    print('rendering')
    return render_template('interactive_plots.html', mytext=mytext, myimage=fname,  feature_names=result.columns,  current_feature_name='GR')

@app.route('/handle_data', methods=['POST'])
def handle_data():
    print('hanaadle')
    result = request.form
    #projectpath = request#.form['projectFilepath']
    #print(type(projectpath))
    return 

if __name__ == '__main__':
    app.run()
