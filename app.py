# -*- coding: utf-8 -*-
import os

from flask import Flask
from flask import render_template
from flask_wtf import Form
from wtforms import TextAreaField
from wtforms.validators import DataRequired

import pconverter


class ConfigError(Exception):
    pass


SECRET_KEY = os.environ.get('SECRET_KEY')

if not SECRET_KEY:
    raise ConfigError


app = Flask(__name__)
app.config.from_object(__name__)


class InputForm(Form):
    text = TextAreaField('テキストを入力', validators=[DataRequired()])


def preprocess_input(istr):
    istr = istr.replace('\r', '')
    return istr


@app.route('/', methods=('GET', 'POST'))
def pconv():
    form = InputForm()

    if form.validate_on_submit():
        try:
            rstr = pconverter.main(preprocess_input(form.text.data))
        except:
            rstr = 'Error!'
        return render_template('index.html', form=form, rstr=rstr)

    return render_template('index.html', form=form)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
