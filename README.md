# [Parser](https://github.com/taylorwan/Parser)
Read, parse, store, and output examples in Mark's File Format (mff).

Project for COSC 288: Introduction to Machine Learning

## Running k-NN

```python
main.py kNN [-t <path> [-T <path>]] [-k neighbors] [-x folds]
```

## Running Naive Bayes

```python
main.py NaiveBayes [-t <path> [-T <path>]] [-x folds]
```

## Running ID3

```python
main.py ID3 [-t <path> [-T <path>]] [-p proportion]
```

## Running Neural Network with Back Propagation

```python
main.py BP [-t <path> [-T <path>]] [-j hiddenNodes] [-p proportion] [-n learningRate]
```

## Running Random Forest

```python
main.py Forest [-t <path> [-T <path>]] [-m trees] [-n maxSetSize]
```

### Options

`-t` is an option in TrainTestSets ** required

* Requires one argument: <path>, which specifies the path to a training file

`-T` is an option in TrainTestSets

* Requires one argument: <path>, which specifies the path to a test file

`-x` is an option in Evaluator

* Requires one argument: folds, which specifies the # of folds to partition the training set when evaluating performance. Default is 10.

`-p` is an option in Evaluator

* Requires one argument: p, which specifies the ratio of examples to be split into the training set. Default is 0.3.

`-s` is an option in DataSet

* Generates a new seed

`-k` is an option in kNN

* Requires one argument: k, which specifies the # of closest neighbors to be used in making predictions. Default is 3.

`-j` is an option in BP

* Requires one argument: j, which specifies the # of nodes in the hidden layer. Default is 2.

`-n` is an option in BP

* Requires one argument: n, which specifies the learning rate to be used in adjusting weights. Default is 0.9.

`-m` is an option in Forest

* Requires one argument: m, which specifies the number of trees in our forest. Default is 3.

`-n` is an option in Forest

* Requires one argument: n, which specifies the max size of a subset of examples for any particlar tree in our forest. Default is 100.

### Testing

You can use `test/votes.mff` and `test/mushroom.mff` as test data

