#! /bin/bash
# SPDX-FileCopyrightText: 2025 Cerrise Weiblen
# SPDX-License-Identifier: CC-BY-NC-SA-4.0
# https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode
# Commercial Licensing Contact: Lisa Stein (stein1@ualberta.ca)


PYTHON=python

NUM_REGULATORS=5

echo "Running ARACNE..."
$PYTHON ./ARACNE_R.py --regulators $NUM_REGULATORS

echo "Running GENIE3..."
$PYTHON ./GENIE3_R.py  --regulators $NUM_REGULATORS

echo "Finding consensus..."
./ARACNE_GENIE3_consensus.sh
echo "The result is in 'consensus_network.csv'"

$PYTHON visualization_app.py
echo "Visualization is in 'index.html'"

#eof
