from lwreg.utils import defaultConfig
from lwreg.utils import initdb
import os
import sys

cfg = defaultConfig()
dbname = "./static/ideamol.sqlt"
cfg["dbname"] = dbname

def checkdb():
    if not os.path.exists(dbname):
        initdb(config=cfg, confirm=True)
    return cfg
