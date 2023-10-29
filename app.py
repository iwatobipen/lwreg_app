from flask import Flask
from flask import request
from flask import url_for, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import Form
from wtforms.validators import DataRequired
from wtforms import StringField

import lwreg
from lwreg.utils import register, retrieve, query
from lwreg.utils import defaultConfig
from rdkit import Chem
from rdkit.Chem.Draw import rdMolDraw2D
from rdkit.Chem.Draw import rdDepictor
import checker

app = Flask(__name__)
bootstrap = Bootstrap5(app)

class Smiles(Form):
    smi = StringField("mol2smi", validators=[DataRequired()])

cfg = checker.checkdb()

def smi2svg(smi):
    mol = Chem.MolFromSmiles(smi)
    rdDepictor.Compute2DCoords(mol)
    d2d = rdMolDraw2D.MolDraw2DSVG(200, 100)
    d2d.DrawMolecule(mol)
    d2d.FinishDrawing()
    return d2d.GetDrawingText()

@app.route("/top")
def top():
    return render_template("top.html")

@app.route("/chempage", methods=["GET", "POST"])
def chempage():
    if request.method == "POST":
        smiles = request.form['smiles']
        svg = smi2svg(smiles)
        res = query(config=cfg, smiles=smiles)
        if len(res) == 0:
            molid = register(config=cfg, smiles=smiles)
            return render_template("registered.html",molid=molid, svg=svg)
        else:
            return render_template("exists.html", molid=res[0], svg=svg)
    return render_template("chem.html")



if __name__=="__main__":
    app.run(debug=True)


