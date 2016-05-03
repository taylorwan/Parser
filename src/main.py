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

from naivebayes import *
from knn import *
from id3 import *
from bp import *
from forest import *


## initialize and evaluate
def main():
    # try:
        opts = sys.argv
        c = None  # classifier
        cInd = 1

        if 'kNN' == opts[cInd] or 'knn' == opts[cInd]:
            c = kNN()
        elif 'NaiveBayes' == opts[cInd] or 'naivebayes' == opts[cInd]:
            c = NaiveBayes()
        elif 'ID3' == opts[cInd] or 'id3' == opts[cInd]:
            c = ID3()
        elif 'BP' == opts[cInd] or 'bp' == opts[cInd]:
            c = BP()
        elif 'Forest' == opts[cInd] or 'forest' == opts[cInd]:
            c = Forest()
        else:
            loadOptionsError(opts, "Invalid classifier")
        ds = TrainTestSets(opts)
        if len(ds.getTrainingSet().getExamples()) > 0:
            if len(ds.getTestingSet().getExamples()) > 0:
                Evaluator(c).evaluate(ds.getTrainingSet(), ds.getTestingSet())
            else:
                Evaluator(c).evaluate(ds.getTrainingSet())

    # except Exception as e:
    #     if len(e.args) == 1:
    #         print e.args[0]
    #     else:
    #         print e.args[1]


if __name__ == "__main__":
    main()
