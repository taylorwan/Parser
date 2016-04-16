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


### Options

`-t` is an option in TrainTestSets

* Requires one argument: <path>, which specifies the path to a training file

`-T` is an option in TrainTestSets

* Requires one argument: <path>, which specifies the path to a test file

`-x` is an option in Evaluator

* Requires one argument: folds, which specifies the # of folds to partition the training set when evaluating performance

`-p` is an option in Evaluator

* Requires one argument: p, which specifies the ratio of examples to be split into the training set

`-s` is an option in DataSet

* Generates a new seed

`-k` is an option in kNN

* Requires one argument: k, which specifies the # of closest neighbors to be used in making predictions

`-j` is an option in BP

* Requires one argument: j, which specifies the # of nodes in the hidden layer

`-n` is an option in BP

* Requires one argument: n, which specifies the learning rate to be used in adjusting weights

### Testing

You can use `test/votes.mff` and `test/mushroom.mff` as test data

