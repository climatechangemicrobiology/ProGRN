#! /bin/bash
# SPDX-FileCopyrightText: 2025 Cerrise Weiblen
# SPDX-License-Identifier: CC-BY-NC-SA-4.0
# https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode
# Commercial Licensing Contact: Lisa Stein (stein1@ualberta.ca)

# Remove columns other than regulator and target IDs, to facilitate diff
cut -d , -f 1,2 -s ARACNE_output_network.csv > ARACNE_comm_input.csv
cut -d , -f 1,2 -s GENIE3_output_network.csv > GENIE3_comm_input.csv

#Sort before compare
sort ARACNE_comm_input.csv > sorted_ARACNE_comm_input.csv
sort GENIE3_comm_input.csv > sorted_GENIE3_comm_input.csv

# Compare regulator-target connections line by line and export matching results to a text file
comm -1 -2 sorted_ARACNE_comm_input.csv sorted_GENIE3_comm_input.csv > consensus_network.csv

# Output comm version information for documentation purposes
#comm --version > comm_version_data.txt
