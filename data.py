"""Data getting functions"""
from pymatgen.ext.matproj import MPRester
from monty.serialization import dumpfn, loadfn
import os


def get_data():
    if not os.path.isfile("formulas.json"):
        with MPRester() as mpr:
            data = mpr.query({"icsd_ids.0": {"$exists": True}}, ['pretty_formula', 'icsd_ids'])

        all_formulas = list(set([d['pretty_formula'] for d in data]))
        dumpfn(all_formulas, "formulas.json")
    else:
        all_formulas = loadfn("formulas.json")
    return all_formulas
