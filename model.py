import matplotlib.pyplot as plt
import numpy as np
import pickle
from sklearn import *
from sklearn import tree
from sklearn.metrics import accuracy_score

# ------------------------------------------------------------------------------
def training_func():
    training_data = np.genfromtxt('dataset.arff', delimiter=',', dtype=np.int32)
    inputs = training_data[:,:-1]
    outputs = training_data[:, -1]

    training_inputs = inputs[:6400]
    training_outputs = outputs[:6400]

    testing_inputs = inputs[800:]
    testing_outputs = outputs[800:]

    classifier = tree.DecisionTreeClassifier(max_depth=5, min_samples_leaf=1)
    classifier.fit(training_inputs, training_outputs)
    predictions = classifier.predict(testing_inputs)

    accuracy = 100.0 * accuracy_score(testing_outputs, predictions)

    print ("The accuracy of your decision tree on testing data is: " + str(accuracy))
    print ("\n")

    fig = plt.figure(figsize=(16, 9))
    ax = plt.subplot()
    x = ["is_valid_ip", "length_url", "length_domain", "host_at", "host_hyp", "contains_redirects", "redirect", "https_token_check", "shortened", "ssl", "no_domains", "title", "url_at"]
    _ = tree.plot_tree(classifier, feature_names=x, class_names=["0", "1"], ax=ax)
    plt.show()

    filename = "model_file.sav"
    pickle.dump(classifier, open(filename, "wb"))

    return classifier

def validation_func(classifier):
    validation_data = np.genfromtxt('dataset_validation.arff', delimiter=',', dtype=np.int32)
    validation_inputs = validation_data[:,:-1]
    validation_outputs = validation_data[:, -1]

    predictions = classifier.predict(validation_inputs)

    accuracy = 100.0 * accuracy_score(validation_outputs, predictions)

    print ("The accuracy of your decision tree on validation data is: " + str(accuracy))
    print ("\n")

def prediction_func(classifier):
    url = input("Enter URL: ")
    url = str(url)

    results = feature_extraction(url, 0, 1)
    results = np.array(results)
    results = results.reshape(1, -1)
    prediction = classifier.predict(results)

    print (prediction)
