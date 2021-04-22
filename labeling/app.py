import os
from itertools import chain

import numpy as np
import pandas as pd
from flask import Flask, render_template, request
from flask_paginate import Pagination, get_page_args, get_page_parameter
from werkzeug.utils import redirect, secure_filename

import module as md

UPLOAD_FOLDER = 'static/files/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# @app.route("/<id>")
@app.route("/")
def index():
    dataset = pd.read_csv('static/files/book1_30.csv').values.tolist()
    output = []
    length = []
    for data in dataset:
        output.append([data[0].split("#")[:-1]])
        length.append(len(data[0].split("#")[:-1]))
    print(output[2])
    output = list(chain.from_iterable(output))
    output = list(chain.from_iterable(output))
    idx = list(range(sum(length)))
    return render_template(
        'index.html',
        idx=idx,
        dataset=output,
    )


@app.route('/data-upload', methods=['POST'])
def get_file():
    md.remove_old_files()
    file = request.files['file']
    file.save(
        os.path.join(app.config['UPLOAD_FOLDER'],
                     secure_filename(file.filename)))
    return redirect("/")


@app.route("/label-data", methods=['POST', "GET"])
def get_form():
    dataset = pd.read_csv('static/files/book1_30.csv').values.tolist()
    output = []
    length = []
    for data in dataset:
        output.append([data[0].split("#")[:-1]])
        length.append(len(data[0].split("#")[:-1]))
    output = list(chain.from_iterable(output))
    output = list(chain.from_iterable(output))
    data = request.form
    label_tmp = list(data.values())
    print(list(data.keys()))
    text = []
    label = []
    pos = 0
    for l in length:
        text.append(output[pos:pos + l])
        label.append(label_tmp[pos:pos + l])
        pos = pos + l
    lll = list(map(lambda x: ','.join(x), label))
    dataset = list(chain.from_iterable(dataset))
    data = pd.DataFrame([dataset, lll]).transpose()
    data.to_csv('test.csv')
    return data.to_html()


app.run(debug=True)
