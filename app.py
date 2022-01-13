#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template
from anytree.importer import JsonImporter

importer = JsonImporter()
with open('/content/drive/MyDrive/g_projects/OMEN/stroco/tree_out.json') as f:
  root = importer.read(f)

DEVELOPMENT_ENV  = True

app = Flask(__name__)

app_data = {
    "html_title":   "OMEN metaverse stroco",
    "root": root.name
}


@app.route('/')
def index():
    return render_template('index.html', app_data=app_data)

if __name__ == '__main__':
    app.run(debug=DEVELOPMENT_ENV)