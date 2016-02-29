#
# Taylor Wan
# tw476@georgetown.edu
# Platform: OS X
# Language/Environment: python
#
# In accordance with the class policies and Georgetown's Honor Code,
# I certify that, with the exceptions of the class resources and those
# items noted below, I have neither given nor received any assistance
# on this project.
#

import sys
from attribute import *
from attributefactory import *
from attributes import *
from classifier import *
from dataset import *
from example import *
from examples import *
from nominalattribute import *
from numericattribute import *
from traintestsets import *


def test():
    TrainTestSets(sys.argv)


def main():
    # try:
        test()
    # except Exception as e:
        # print e.args[0]

if __name__ == "__main__":
    main()
