from flask import Flask, render_template, request, g
from wtforms import Form, IntegerField, validators, StringField
import sqlite3
from flask_flatpages import FlatPages
from flask_frozen import Freezer

# from compute import compute

app = Flask(__name__)
app.config.from_pyfile('settings.py')
pages = FlatPages(app)
freezer = Freezer(app)
# Model
class InputForm(Form):
  # E = StringField(
  #     label='element', default='H',
  #     validators=[validators.InputRequired(), validators.Length(min=1, max=2), validators.regexp("[a-zA-Z]+$", message="Only letters")])
  A = IntegerField(
      label='atomic mass', default=1,
      validators=[validators.InputRequired()])
  Z = IntegerField(
      label='atomic number', default=1,
      validators=[validators.InputRequired()])

def get_element(A, Z, cur):
  cur.execute(f"select * from elements where Z='{Z}' and A='{A}'")

@app.route('/', methods=['GET', 'POST'])
def get_input():
  # Get form
  form = InputForm(request.form)
  con = sqlite3.connect("database.db")
  # Validate the form
  if request.method == 'POST' and form.validate():
    # Get into the database and query
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(
        f"select * from elements where Z='{form.Z.data}' and A='{form.A.data}'")
    mH = 1.00782
    mn = 1.00866
    # Fetch the data
    elements = cur.fetchall()
    elements[0]['A']
    return render_template('index.html', form=form, elements=elements, mn=mn, mH=mH)
  else:
    return render_template('index.html', form=form, elements=[])


# @app.route('/list')
# def list():
#   con = sqlite3.connect("database.db")
#   con.row_factory = sqlite3.Row

#   cur = con.cursor()
#   cur.execute("select * from elements where Z='1' and A='5'")

#   rows = cur.fetchall()
#   if rows == []:

#   else:
#     return render_template("list.html", rows=rows)


if __name__ == '__main__':
  app.run(debug=True)
