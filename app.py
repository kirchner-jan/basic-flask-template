#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template , request
from flask_ngrok import run_with_ngrok
from anytree.importer import JsonImporter

importer = JsonImporter()
with open('/content/drive/MyDrive/g_projects/OMEN/stroco/tree_out.json') as f:
  root = importer.read(f)

app = Flask(__name__)
run_with_ngrok(app)  # Start ngrok when app is run

app_data = {
    "html_title":   "OMEN metaverse stroco",
    "root": root.name
}

@app.route('/')
def index():
  if request.method == 'POST':
    if request.form.get('action1') == 'VALUE1':
        pass # do something
    elif  request.form.get('action2') == 'VALUE2':
        pass # do something else
    else:
        pass # unknown
  return render_template('index.html', app_data=app_data)

if __name__ == '__main__':
    app.run()