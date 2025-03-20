# ProGRN
# Version 1.0 (2025)

- SPDX-FileCopyrightText: 2025 Cerrise Weiblen
- SPDX-License-Identifier: CC-BY-NC-SA-4.0
- https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode
- Commercial Licensing Contact: Lisa Stein (stein1@ualberta.ca)

## Welcome to Prokaryote Gene Regulatory Network (ProGRN) Inference Pipeline!

Here you can apply machine learning to infer a gene regulatory network from gene expression data and visualize the network interactively with a .html file.

The machine learning methods implemented here include:

* Mutual Information [(ARACNE)](https://doi.org/10.1186/1471-2105-7-S1-S7) 
* Random Forest [(GENIE3)](https://doi.org/10.1371/journal.pone.0012776)

This is a community-based approach to network inference, comparing the results of the two ML algorithms and removing connections not agreed upon by both ARACNE and GENIE3. This approach increases confidence that the regulatory connections represented in the final, consensus GRN reflect biologically meaningful relationships that were captured in the gene expression data. 

Interactive visualizations of the GRN for the organism <i>Methylomonas denitrificans</i> FJG1 (_ProGRN_FJG1_) can be found at (https://progrn.com).

#### Prepare gene expression data for analysis
Input data should include gene expression changes over at least three sampling points, the more the better.
Data should be in matrix format representing the expression pattern of genes, by row, over chronological sampling times across the columns from left to right. 

Create a .csv file wherein each row contains expression data for one gene.
Any identified regulator genes should be placed in the uppermost rows of the matrix, with target genes occupying the lower rows. Sigma factors are a good choice to begin with. Any transcription factors or other types of regulatory genes can be specified.

Configure the matrix, such that the first column (column A in some editing programs such as LibreOffice Calc and Excel)
contains the gene identifiers (such as GenBank gene_locus). 
Columns to the right should contain the expression data in series, ordered from left to right.

For example, the test model _ProGRN_FJG1_ contains sampling points at 24, 36, 48, 60, 72, and 120 hours. An example of the matrix format can be found in the example_data folder: __gene_expression_matrix_example.csv__. 

Do not use identifiers that begin with zero (0), because this will interfere with the sort functions necessary to create the consensus network.  In addition, appending an identifier tag such as "_SF" to the name or ID of each regulator gene can be useful to differentiate between regulators and targets in the visualization.

#### Set up the code environment and prerequisites
This code has been tested in Linux Ubuntu 22.04.5 LTS and Debian 12. 
Ensure you have installed [Python](https://www.python.org/) (at least version 3.9.12) and [R](https://www.r-project.org/) (at least version 4.2.0).

1. Download this ProGRN_network repository.
1. Use the `cd` command to navigate into this repository folder.
   - `cd path/to/directory/ProGRN`
1. While not technically required, we recommend using a Python [virtual environment](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/).
   - `python3 -m venv venv`
   - `source venv/bin/activate`
   - be aware that misuse of pip can cause catastrophic failure of your operating system, so please read up on virtual environments and proper use of pip before proceeding to the next step
1. Install the Python dependencies:
   - `pip3 install -r requirements.txt`
1. Install the R dependencies:
   - `python3 install_Rpackages.py
   - be aware R libraries may be installed in two locations by default: <br>`/lib/R/site-library` or `/usr/local/lib/R/site-library`

#### Perform ML analysis of gene expression data and generate a consensus network
1. If necessary, use the `cd` command to navigate into this repository folder (Step 2 above).
1. Name your matrix-formatted gene expression data file __input_matrix.csv__ and put it inside the repository directory:
   - `cp ./example_data/gene_expression_matrix_example.csv ./input_matrix.csv`
1. Activate the virtual environment (venv) and run the pipeline, specifying the number of regulator genes.<br>
For the included __gene_expression_matrix_example.csv__ the number of regulators is 5.
   - Open __RUN_PROGRN_PIPELINE.sh__ and set the number of regulators to match your matrix file `NUM_REGULATORS=5`<br>
1. Run the ProGRN Pipeline to generate a consensus network containing only those connections agreed upon by both ML algorithms:<br>
```
RUN_PROGRN_PIPELINE.sh
```
This will produce a consensus network that contains only mutually inclusive connections, __consensus_network.csv__, and an interactive visualization of the network, __index.html__ with a support library. See examples in the ./example_data and ./example_data/lib folders. 

#### Advanced options 

##### ARACNE
An optional argument can be provided to specify the ARACNE model type as either additive or multiplicative. The additive model is used by default if no argument is provided. To modify this argument in __RUN_PROGRN_PIPELINE.sh__, use the --model or -M flag, "a" for additive or "m" for multiplicative <br>`python ARACNE_R.py -M a`

##### GENIE3
An optional argument can be provided to specify the number of random forest trees used in the GENIE3 algorithm. The default is 1,000 trees. To modify this argument in __RUN_PROGRN_PIPELINE.sh__, use --trees or -T followed by the desired tree count as a whole number <br>`python GENIE3_R.py -T 1500`

##### Visualization
The interactive visualizations produced by the ProGRN pipeline are created with Pyvis (https://pyvis.readthedocs.io/en/latest/). Pyvis supports many filtering and visualization features, such as the ability to specify coloured lines and targets based on attributes in a customized input file. If you correlate the __consensus_network.csv__ with your __input_matrix.csv__ and add columns for gene products or other data, modifications can be made to display additional information in the .html visualization by modifying __streamlit_utils.py__. 


