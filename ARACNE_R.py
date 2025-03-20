#
# SPDX-FileCopyrightText: 2025 Tian Xiang Du
# SPDX-License-Identifier: CC-BY-NC-SA-4.0
# https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode
# Contact Tian Xiang Du (tdu@ualberta.ca)
# Commercial Licensing Contact: Lisa Stein (stein1@ualberta.ca)

import argparse
import numpy as np
import pandas as pd
import rpy2.robjects as ro
from rpy2.robjects.packages import importr
from rpy2.robjects import numpy2ri
from rpy2.robjects import pandas2ri
numpy2ri.activate()
pandas2ri.activate()
import os

"""
# numpy to rpy2 conversion
from rpy2.robjects import default_converter
from rpy2.robjects.conversion import localconverter

# Create a converter that starts with rpy2's default converter
# to which the numpy conversion rules are added.
np_cv_rules = default_converter + numpy2ri.converter

with localconverter(np_cv_rules) as cv:
    # Anything here and until the `with` block is exited
    # will use our numpy converter whenever objects are
    # passed to R or are returned by R while calling
    # rpy2.robjects functions.
    pass
"""

# implement command-line arguments to specify hyperparameters
parser = argparse.ArgumentParser(description='ARACNE Network inference')
parser.add_argument('--filename', '-F', metavar='Input Matrix', type=str, required=False, default="input_matrix.csv",
                    help='Input data file name (ex: input_matrix.csv)')
parser.add_argument('--regulators', '-R', metavar='Number of Regulators', type=int, required=True,
                    help='Number of regulator genes')
parser.add_argument('--model', metavar='M', type=str, default="a",
                    help='ARACNE model: "a" for additive or "m" for multiplicative')
parser.add_argument('--outfile', '-O', metavar='Output file name', type=str, required=False, default='ARACNE_output_network.csv',
                    help='Name of outfile csv file (default: ARACNE_output_network.csv)')

args = parser.parse_args()
reg_bound = args.regulators
ARACNE_type = args.model
filename = args.filename
outname = args.outfile

# Setup
# load required R library
base = importr('base')
parmigene = importr('parmigene')
aracneModel = parmigene.aracne_a if ARACNE_type == "a" else parmigene.aracne_m

dat = np.genfromtxt(filename, delimiter=',', skip_header=1,dtype=str)
gene_names, gene_dat = np.split(dat,[1],axis=1)
mat = gene_dat.astype(float)
nr,nc = mat.shape
tar_bound = nr
matR = ro.r.matrix(mat, nr, nc)

# Perform ARACNE network inference to get MI adjacency matrix
# R object names can contain a “.” (dot) while in Python the dot means “attribute in a namespace”. 
# Because of this, importr is trying to translate “.” into “_”. 
matMI = parmigene.knnmi_all(matR) 
matMI_filtered = aracneModel(matMI)

# Create pandas dataframe from adjacency matrix
matA = pd.DataFrame(matMI_filtered, columns=gene_names[:,0], index=gene_names[:,0])

# Convert adjacency matrix to edgelist
matE = pd.melt(matA.iloc[0:reg_bound, reg_bound:tar_bound], ignore_index=False)
matE.reset_index(level=0, inplace=True)
matE.rename(columns={"index": "0Regulator", "variable": "0Target", "value": "MI"}, inplace=True)
matE = matE[matE.MI != 0]
# save pd to csv
# os.makedirs('./output/', exist_ok=True)
matE.to_csv(f'./{outname}', index=False)
