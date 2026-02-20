from flask import Flask, render_template, request, jsonify
import pandas as pd
from glob import glob
import re

from pathlib import Path
import os
import shutil
from datetime import datetime

app = Flask(__name__)


@app.route('/file/<filename>')
def file(filename):
    try:
        df = pd.read_csv('files/'+filename+'.csv')
    except FileNotFoundError:
        df = pd.DataFrame(columns=["ID", "Texte", "Tags", "UpdatedAt", "CreatedAt","Thumb"])

    df = df.fillna("")
    allTags = df.Tags.apply(lambda x : x.split(',')).explode('Tags').value_counts().index.to_list()
    autocompTags = '","'.join(allTags)

    filters = request.args.get("q")
    if filters :
        filters = filters.split(',')
        # trouver les qui contient     
        def getItems(li,lf):
            return len(list(set(li) & set(lf)))==len(lf) # qui renvoie vrai si le film contient au moins les genres de la liste
        df = df[df['Tags'].apply(lambda x : x.split(',')).apply(lambda x: getItems(x,filters))]

    relatedTags = df.Tags.apply(lambda x : x.split(',')).explode('Tags').value_counts().index.to_list()
    rows = df.to_dict(orient="records")
    return render_template("file.html", 
        filename=filename, 
        rows=rows, 
        relatedTags=relatedTags, 
        allTags=allTags,
        autocompTags = autocompTags,
        filters=filters)

@app.route("/")
def index():
    files = glob('files/*.csv')
    files = [re.search("files/(.*).csv",file).group(1) for file in files]
    return render_template("index.html", files=files)

@app.route("/save/<filename>", methods=["POST"])
def save(filename):
    rows = request.json
    df = pd.DataFrame(rows)

    if os.path.exists('files/'+filename+'.csv'):
        # keep previous version
        versionPath = 'versions/'+filename+'/'
        # create path if not exist
        Path(versionPath).mkdir(parents=True, exist_ok=True)

        shutil.copyfile('files/'+filename+'.csv', 'versions/'+filename+'/'+filename+'_'+datetime.today().strftime('%Y%m%d_ %H%M%S')+'.csv')

    # 🔹 sauvegarde du nouveau CSV
    df.to_csv('files/'+filename+'.csv', index=False)

    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
