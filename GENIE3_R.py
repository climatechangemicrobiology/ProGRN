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

# command-line arguments to specify hyperparameters
parser = argparse.ArgumentParser(description='GENIE3 Network inference')
parser.add_argument('--filename', '-F', metavar='Input Matrix', type=str, required=False, default="input_matrix.csv",
                    help='Input data file name (ex: input_matrix.csv)')
parser.add_argument('--regulators', '-R', metavar='Number of Regulators', type=int, required=True,
                    help='Number of regulator genes')
parser.add_argument('--trees', '-T', metavar='Tree Count', type=int, required=False, default=1000,
                    help='Number of trees used in random forest')
parser.add_argument('--filter', '-L', metavar='Score Filter', type=int, required=False, default=0,
                    help='GENIE score filter for network clarity (default: 0.07)')
parser.add_argument('--outfile', '-O', metavar='Output file name', type=str, required=False, default='GENIE3_output_network.csv',
                    help='Name of outfile csv file (default: GENIE3_output_network.csv)')

args = parser.parse_args()
tree_count = args.trees
filename = args.filename
outname = args.outfile
score_filter = args.filter

# Setup
# load required R library
base = importr('base')
stats = importr('stats')
randomForest = importr('randomForest')
ro.r.source('genie3.R')

# load function we have defined in the R file
genie3 = ro.globalenv['get.weight.matrix']

dat = np.genfromtxt(filename, delimiter=',', skip_header=1,dtype=str)
reg_bound = args.regulators # from arguments
gene_names, gene_dat = np.split(dat,[1],axis=1)
mat = gene_dat.astype(float)
matR = pd.DataFrame(mat, index=gene_names[:,0])

# Perform GENIE3 network inference. Check genie3.R for more information on function use
genienet = genie3(ro.conversion.py2rpy(matR), "sqrt", tree_count, ro.r.seq(1,reg_bound), "IncNodePurity", 1, False)
matRF = pd.DataFrame(genienet, columns=gene_names[:,0], index=gene_names[:,0])
matE = pd.melt(matRF.iloc[0:reg_bound, reg_bound:], ignore_index=False)
matE.reset_index(level=0, inplace=True)
matE.rename(columns={"index": "0Regulator", "variable": "0Target", "value": "Score"}, inplace=True)
matE = matE[matE.Score != 0]

# additional filtering
matE = matE[matE.Score >= score_filter]

# save pd to csv
# os.makedirs('./output/', exist_ok=True)
matE.to_csv(f'./{outname}', index=False)
