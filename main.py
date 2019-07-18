from flask import Flask, request, render_template
import pandas as pd
import numpy as np
from PyPDF2 import PdfFileReader
import json
import plotly
import re
from functions import allowed_file, stem_long_list
from classes import MyData
import nltk

# pip install xlrd

app = Flask(__name__)
my_df = MyData()


@app.route('/', methods=['GET', 'POST'])
def home():
    # investigate https://bokeh.pydata.org/en/latest/docs/user_guide/quickstart.html#userguide-quickstart

    if request.method == 'POST':
        if request.form['submit_button'] == 'upload':
            file = request.files['file']
            if file and allowed_file(file.filename):
                my_df.home_file = file.filename
                if file.filename.rsplit('.', 1)[1].lower() == 'csv':
                    my_df.df = pd.read_csv(request.files.get('file'))
                if file.filename.rsplit('.', 1)[1].lower() == 'xlsx' or \
                        file.filename.rsplit('.', 1)[1].lower() == 'xls':
                    my_df.df = pd.read_excel(request.files.get('file'))

        if request.form['submit_button'] == 'update':
            my_df.df = pd.DataFrame(np.reshape(request.values.getlist('df'), (11, 6)))  # fix, not flexible to update dfs
            my_df.df.columns = ['Internal Perspective', 'External Perspective', 'Peer rating', 'Social media',
                                'News reports', 'Survey data']

            x_dim_index = request.values.getlist('x_dim')
            x_dim_index = [int(x) for x in x_dim_index]
            my_df.x_dim = my_df.df.iloc[:, x_dim_index].astype(float).mean(axis=1)

            y_dim_index = request.values.getlist('y_dim')
            y_dim_index = [int(y) for y in y_dim_index]
            my_df.y_dim = my_df.df.iloc[:, y_dim_index].astype(float).mean(axis=1)

    '''nasty piece of temp json to test
    courtesy of https://github.com/plotly/plotlyjs-flask-example/blob/master/app.py'''
    graphs = [
        dict(
            data=[
                dict(
                    x=my_df.x_dim,
                    y=my_df.y_dim,
                    mode='markers',
                    text=my_df.df.index.values
                ),
            ],
            layout=dict(
                title='Materiality matrix',
                hovermode='closest',
                xaxis=dict(
                    title='x-axis',
                    rangemode='tozero'
                ),
                yaxis=dict(
                    title='y-axis',
                    rangemode='tozero'
                )
            )
        )
    ]
    ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)]
    plot = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
    df = my_df.df.style.format('<input type="number" name="df" value="{}" />').hide_index().render()

    return render_template('matrix.html', datadf=df, ids=ids, graphJSON=plot, filename=my_df.home_file)


@app.route('/about')
def about():
    # create some information on this project here
    return render_template('about.html')


@app.route('/data', methods=['GET', 'POST'])
def data():

    text = ''
    # create the document term matrix here
    if request.method == 'POST':
        if request.form['submit_button'] == 'upload':
            my_df.pdf_files = request.files.getlist('pdf_file')

            dict_of_terms = stem_long_list(request.files['long_list'])

            for pdf_file in my_df.pdf_files:
                pdf = PdfFileReader(pdf_file)
                for num_page in range(pdf.getNumPages()):
                    page = pdf.getPage(num_page)
                    page_text = page.extractText().lower()
                    text = text + page_text
                for term in dict_of_terms:
                    words = term.rsplit()
                    pattern = re.compile(r'%s' % "\\s+".join(words), re.IGNORECASE)
                    dict_of_terms[term] = len(pattern.findall(text))
                print(dict_of_terms)

    # now we can adjust the matrix from within the tool as well.

    return render_template("data.html", pdf_text=text, pdf_names=my_df.pdf_files)


if __name__ == '__main__':
    app.run(debug=True)

