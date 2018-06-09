from flask import Flask, render_template
app = Flask(__name__)
import read_data
import plotting
import calculate_qc_stats

WELLS = ['A', 'AA', 'B_ATZ', 'B_A', 'B', 'D', 'LA', 'XZ7']

# Landing page
@app.route('/index.html')
@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/bootstrap')
def bootstrap():
    return render_template('minimal_bootstrap.html')

@app.route('/qc_stats')
def qc_stats():
    n_files = calculate_qc_stats.count_number_of_files('../../EAGE2018')
    n_las_files = calculate_qc_stats.count_number_of_particular_files('../../EAGE2018', 'las')
    n_pdf_files = calculate_qc_stats.count_number_of_particular_files('../../EAGE2018', 'pdf')
    n_txt_files = calculate_qc_stats.count_number_of_particular_files('../../EAGE2018', 'txt')
    return render_template('qc_stats.html', wells = WELLS,
                           count_number_of_files=calculate_qc_stats.count_number_of_files,
                           count_number_of_particular_files=calculate_qc_stats.count_number_of_particular_files)

@app.route('/bokeh')
def bokeh():
    input_file = "../../EAGE2018/Well-A_finished/HQLD_B_2C1_75-1_Well-A_ISF-BHC-MSFL-GR__COMPOSIT__1.LAS"
    las = read_data.read(input_file)
    df = las.df()
    keys = las.keys()
    script, div, js_resources, css_resources = plotting.plot_bokeh(df, keys[1], keys[2])
    return render_template('bokeh_index.html',
                           plot_script=script,
                           plot_div=div,
                           js_resources=js_resources,
                           css_resources=css_resources )


@app.route('/interactive_plots')
def interactive_plots():

    input_file = "../../EAGE2018/Well-A_finished/HQLD_B_2C1_75-1_Well-A_ISF-BHC-MSFL-GR__COMPOSIT__1.LAS"
    result = read_data.read(input_file)

    result_keys = result.keys()

    mytext = "Hello with my text"

    myimage = plotting.plot_two_columns(result.df(), result_keys[1], result_keys[2])
    print(type(myimage))
    print(myimage)
    return render_template('interactive_plots.html', mytext=mytext, myimage=myimage)

if __name__ == '__main__':
    app.run()