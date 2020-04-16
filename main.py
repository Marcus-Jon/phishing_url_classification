from model import training_func, validation_func, prediction_func
from feature_extraction import feature_extraction
import pickle

# ------------------------------------------------------------------------------
def read_url_list_training():
    url_list_legitimate = []
    url_list_phishing = []

    f = open("url_list_legitimate.txt", "r")
    for i in f:
        i = str(i.strip())
        url_list_legitimate.append(i)
    f.close()

    f = open("url_list_phishing.txt", "r")
    #f = open("errors.txt", "r")
    for i in f:
        i = str(i.strip())
        url_list_phishing.append(i)
    f.close()

    return url_list_legitimate, url_list_phishing

# ------------------------------------------------------------------------------
def main(classifier = None):
    filename = "model_file.sav"
    print ("Select function:")
    print ("1 - Dataset Generation : 2 - Training : 3 - Validation : 4 - Prediction : 5 - Exit")
    function = input()
    function = str(function)
    print ("\n")

    if function == "1":

        url_list_legitimate, url_list_phishing = read_url_list_training()
        for i in url_list_legitimate:
            print (i)
            feature_extraction(i, -1)
        for i in url_list_phishing:
            print (i)
            feature_extraction(i, 1)

        main()

    elif function == "2":
        classifier = training_func()
        main(classifier)
    elif function == "3":
        if classifier != None:
            validation_func(classifier)
            main(classifier)
        else:
            load_model = pickle.load(open(filename, "rb"))
            validation_func(load_model)
            main(load_model)
    elif function == "4":
        if classifier != None:
            prediction_func(classifier)
            main(classifier)
        else:
            load_model = pickle.load(open(filename, "rb"))
            prediction_func(load_model)
            main(load_model)
    elif function == "5":
        pass
    else:
        print ("Not valid option")

# ------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
