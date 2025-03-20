import rpy2.robjects.packages as rpackages
from rpy2.robjects.vectors import StrVector

# parmigene installation
packageNames = (['parmigene', 'randomForest'])
utils = rpackages.importr('utils')
utils.chooseCRANmirror(ind=1)

packnames_to_install = [x for x in packageNames if not rpackages.isinstalled(x)]

# Running R in Python example installing packages:
if len(packnames_to_install) > 0:
    utils.install_packages(StrVector(packnames_to_install))