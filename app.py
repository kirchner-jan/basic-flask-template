#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template , request
from flask_ngrok import run_with_ngrok
from anytree.importer import JsonImporter
import numpy as np

importer = JsonImporter()
#with open('/content/drive/MyDrive/g_projects/OMEN/stroco/tree_out.json') as f:
with open('tree_out.json') as f:
  root = importer.read(f)

def update_app_data(app_data , splitValue):
  app_data['history'] += splitValue
  return app_data

app_data = {
    "html_title":   "Neuroscience metaverse stroco",
    "root": root,
    "history": root.name + '<br><br>',
    "cnode": root,
    "children_name": [x.name for x in root.children]
}

app = Flask(__name__)
run_with_ngrok(app)  # Start ngrok when app is run

@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == 'POST':
    if not (request.form.get('splitValue') is None):
        # app_data = update_app_value(app_data , request.form.get('splitValue'))
        selectID = np.where([request.form.get('splitValue') == x[:80] for x in app_data['children_name']])[0][0]
        app_data['cnode'] = app_data['cnode'].children[selectID]
        app_data['history'] += app_data['children_name'][selectID] + '<br><br>'
        app_data['children_name'] = [x.name for x in app_data['cnode'].children]
    if not (request.form.get('reset') is None):
        app_data['history'] = root.name + '<br><br>'
        app_data['cnode'] = root
        app_data['children_name'] = [x.name for x in root.children]
  return render_template('index.html', app_data=app_data)

if __name__ == '__main__':
    app.run()