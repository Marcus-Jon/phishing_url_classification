import matplotlib.pyplot as plt
import numpy as np
from IPy import IP
from urllib.parse import urlparse
import requests
import datetime
from bs4 import BeautifulSoup as bs4
import tldextract as tlde
from stem import Signal
from stem.control import Controller
from sklearn import *
from sklearn import tree
from sklearn.metrics import accuracy_score
# ------------------------------------------------------------------------------
def url_parse(url):
    if not urlparse(url.strip()).scheme:
        url = 'https://' + url
    scheme, host, path, para, query, fragments = urlparse(url.strip())
    parsed_url = {'url': host + path + para + query + fragments, 'scheme': scheme, 'host': host, 'path': path, 'para': para, 'query': query, 'fragments': fragments}

    return parsed_url

def valid_ip(ip):
    try:
        IP(ip)
        return 1
    except:
        return -1

def length_of_url(url):
    if len(url) > 75:
        return 1
    else:
        return -1

def length_of_domain(domain):
    if len(domain) > 30:
        return 1
    else:
        return -1

def count_character(url, host, character):
    url_char = url.count(character)
    host_char = host.count(character)

    if url_char > 0 and host_char > 0:
        return 1, 1
    elif url_char > 0 and host_char == 0:
        return 1, -1
    elif url_char == 0 and host_char > 0:
        return -1, 1
    else:
        return -1, -1

def count_redirect(url):
    if url.count('//') == 0:
        return -1
    else:
        return 1

def is_redirected(url, proxies):
    try:
        resp = requests.get(url, proxies=proxies, timeout=30)
        if url != resp.url:
            return 1
        else:
            return -1
    except requests.exceptions.ConnectionError:
        return 0
    except requests.exceptions.Timeout:
        print ("     Server connection timed out: no data was received")
        return 0
    except requests.exceptions.InvalidSchema:
        print ("     Invalid Schema")
        return 0
    except requests.exceptions.ContentDecodingError:
        print ("     Decoding Error")
        return 0
    except AttributeError:
        return 0
    except requests.exceptions.TooManyRedirects:
        print ("     To many redirects")
        return 0
    except requests.exceptions.ReadTimeout:
        print ("     Read timed out")
        return 0
    except requests.exceptions.ChunkedEncodingError:
        return 0
    except Exception:
        return 0

def https_token(host):
    if host.count('https') == 0:
        return -1
    else:
        return 1

def shortened_url(url, host, proxies):
    try:
        switch_ip()
        shortened_file = open('known_shorteners.txt', 'r')
        for line in shortened_file:
            if host == line.strip():
                response = requests.get(url, proxies=proxies, timeout=30)
                if response.status_code == 200:
                    full_url = response.url
                    shortened_file.close()
                    return full_url, 1
        shortened_file.close()
        return url, -1

    except requests.exceptions.ConnectionError:
        # Connection to the sever are rejected due to the server not existing or blocking requests.
        return url, 0
    except requests.exceptions.Timeout:
        print ("     Server connection timed out: no data was received")
        return url, 0
    except requests.exceptions.InvalidSchema:
        print ("     Invalid Schema")
        return url, 0
    except requests.exceptions.ContentDecodingError:
        print ("     Decoding Error")
        return url, 0
    except AttributeError:
        return url, 0
    except requests.exceptions.TooManyRedirects:
        print ("     To many redirects")
        return url, 0
    except requests.exceptions.ReadTimeout:
        print ("     Read timed out")
        return 0
    except requests.exceptions.ChunkedEncodingError:
        return 0
    except Exception:
        return url, 0

def check_ssl(url, proxies):
    try:
        switch_ip()
        requests.get(url, verify=True, timeout=30, proxies=proxies)
        return 1
    except requests.exceptions.SSLError:
        print ("     No SSL cert")
        return -1
    except requests.exceptions.ConnectionError:
        # Connection to the sever are rejected due to the server not existing or blocking requests.
        return 0
    except requests.exceptions.Timeout:
        print ("     Server connection timed out: no data was received")
        return 0
    except requests.exceptions.InvalidSchema:
        print ("     Invalid Schema")
        return 0
    except requests.exceptions.ContentDecodingError:
        print ("     Decoding Error")
        return 0
    except AttributeError:
        return 0
    except requests.exceptions.TooManyRedirects:
        print ("     To many redirects")
        return 0
    except requests.exceptions.ReadTimeout:
        print ("     Read timed out")
        return 0
    except requests.exceptions.ChunkedEncodingError:
        return 0
    except Exception:
        return 0

def domain_count(host):
    no_domains = host.count('.')
    x = tlde.extract(host)
    if no_domains > 3:
        return 1, x[1]
    else:

        return -1, x[1]

def domain_title(url, domain, proxies):
    try:
        switch_ip()
        x = requests.get(url, timeout=60, proxies=proxies)
        if x.status_code == 200:
            resp = requests.get(url, proxies=proxies)
            soup = bs4(resp.text, 'lxml')
            title = str(soup.title.string)
            title = title.lower()
            domain_l = domain.lower()
            if title.count(domain_l) > 0:
                return 1
            else:
                return -1
        elif x.status_code == 401:
            print ("     http 401 error - unauthorised")
            return 0
        elif x.status_code == 403:
            print ("     http 403 error - forbidden")
            return 0
        elif x.status_code == 404:
            print ("     http 404 error - page not found")
            resp = requests.get(url, proxies=proxies)
            if resp.url == url:
                print ("     URL remains on site")
                soup = bs4(x.text, 'lxml')
                title = str(soup.title.string)
                title = title.lower()
                domain_l = domain.lower()
                if title.count(domain_l) > 0:
                    return 1
                else:
                    return -1
            else:
                print ("     URL directed to new site")
                return -1
        elif x.status_code == 405:
            print ("     http 405 error - invalid method")
            return 0
        elif x.status_code == 451:
            print ("     http 451 - unavailable due to legal reasons")
            return 0
        elif x.status_code == 500:
            print ("     http 500 error")
            return 0
        elif x.status_code == 521:
            print ("     http 521 error - server down")
            return 0
        elif x.status_code == 999:
            print ("     Unknown status code")
            if str(x.history) == '[<Response [301]>]':
                 print ("     Redirected to unknown site")
                 return 0
            else:
                print ("     Unknown Action")
                return 0
        else:
            print ("     Unknown")
            return 0

    except requests.exceptions.Timeout:
        print ("     Server connection timed out: no data was received")
        return 0
    except UnicodeEncodeError:
        resp = requests.get(url, timeout=60, proxies=proxies)
        soup = bs4(resp.text, 'lxml')
        title = soup.title.string
        title = title.lower()
        domain_l = domain.lower()
        if title.count(domain_l) > 0:
            return 1
        else:
            return -1
    except requests.exceptions.ConnectionError:
        # Connection to the sever are rejected due to the server not existing or blocking requests.
        return 0
    except requests.exceptions.InvalidSchema:
        print ("     Invalid Schema")
        return 0
    except requests.exceptions.ContentDecodingError:
        print ("     Decoding Error")
        return 0
    except AttributeError:
        return 0
    except requests.exceptions.TooManyRedirects:
        print ("     To many redirects")
        return 0
    except requests.exceptions.ReadTimeout:
        print ("     Read timed out")
        return 0
    except requests.exceptions.ChunkedEncodingError:
        return 0
    except Exception:
        return 0

def set_proxy():
    proxies = {"http": "socks5://proxy_IP:proxy_port",
                "https": "socks5://proxy_IP:proxy_port"}
    return proxies

def switch_ip():
    with Controller.from_port(port=proxy_port) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)

# ------------------------------------------------------------------------------
def feature_extraction(url, label, function=0):
    proxies = set_proxy()
    switch_ip()

    parsed_url = url_parse(url)

    if not urlparse(url.strip()).scheme:
        full_url, shortened = shortened_url(parsed_url['scheme'] + '://' + url, parsed_url['host'], proxies)
    else:
        full_url, shortened = shortened_url(url, parsed_url['host'], proxies)
    if full_url != url:
        parsed_url = url_parse(url)

    is_valid_ip = valid_ip(parsed_url['host'])
    length_url = length_of_url(parsed_url['url'])
    url_at, host_at = count_character(parsed_url['url'], parsed_url['host'], '@')
    url_hyp, host_hyp = count_character(parsed_url['url'], parsed_url['host'], '-')
    no_domains, domain_name = domain_count(parsed_url['host'])
    contains_redirects = count_redirect(parsed_url['url'])
    https_token_check = https_token(parsed_url['host'])
    length_domain = length_of_domain(domain_name)

    if not urlparse(url.strip()).scheme:
        ssl = check_ssl("https://" + url, proxies)
    else:
        ssl = check_ssl(url, proxies)

    if not urlparse(url.strip()).scheme:
        redirect = is_redirected("https://" + url, proxies)
    else:
        redirect = is_redirected(url, proxies)

    if not urlparse(url.strip()).scheme:
        title = domain_title(('https://' + url), domain_name, proxies)
    else:
        title = domain_title(url, domain_name, proxies)

    if function == 0:
        write_dataset(is_valid_ip, length_url, length_domain, host_at, host_hyp, contains_redirects, redirect, https_token_check, shortened, ssl, no_domains, title, url_at, label, url)
    elif function == 1:
        results = [is_valid_ip, length_url, length_domain, host_at, host_hyp, contains_redirects, redirect, https_token_check, shortened, ssl, no_domains, title, url_at]
        return results
# ------------------------------------------------------------------------------
def write_dataset(is_valid_ip, length_url, length_domain, host_at, host_hyp, contains_redirects, redirect, https_token_check, shortened, ssl, no_domains, title, url_at, label, url):
    try:

        f = open("dataset.arff", 'a')
        f.write("'{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}'".format(int(is_valid_ip), int(length_url),
        int(length_domain), int(host_at), int(host_hyp), int(contains_redirects), int(redirect), int(https_token_check), int(shortened), int(ssl),
        int(no_domains), int(title), int(url_at), int(label)))
        f.write("\n")
        f.close()

    except TypeError:
        print ("     Type error")

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
def training_func():
    training_data = np.genfromtxt('dataset.txt', delimiter=',', dtype=np.int32)
    inputs = training_data[:,:-1]
    outputs = training_data[:, -1]

    training_inputs = inputs[:6400]
    training_outputs = outputs[:6400]

    validation_inputs = inputs[800:]
    validation_outputs = outputs[800:]

    classifier = tree.DecisionTreeClassifier(max_depth=5, min_samples_leaf=1)
    classifier.fit(training_inputs, training_outputs)
    predictions = classifier.predict(validation_inputs)

    accuracy = 100.0 * accuracy_score(validation_outputs, predictions)

    print ("The accuracy of your decision tree on validation data is: " + str(accuracy))
    print ("\n")

    fig = plt.figure(figsize=(16, 9))
    ax = plt.subplot()
    x = ["is_valid_ip", "length_url", "length_domain", "host_at", "host_hyp", "contains_redirects", "redirect", "https_token_check", "shortened", "ssl", "no_domains", "title", "url_at"]
    _ = tree.plot_tree(classifier, feature_names=x, class_names=["0", "1"], ax=ax)
    plt.show()

    return classifier

def testing_func(classifier):
    testing_data = np.genfromtxt('dataset_testing.txt', delimiter=',', dtype=np.int32)
    testing_inputs = testing_data[:,:-1]
    testing_outputs = testing_data[:, -1]

    predictions = classifier.predict(testing_inputs)

    accuracy = 100.0 * accuracy_score(testing_outputs, predictions)

    print ("The accuracy of your decision tree on testing data is: " + str(accuracy))
    print ("\n")

def prediction_func(classifier):
    url = input("Enter URL: ")
    url = str(url)

    results = feature_extraction(url, 0, 1)
    results = np.array(results)
    results = results.reshape(1, -1)
    prediction = classifier.predict(results)

    print (prediction)

# ------------------------------------------------------------------------------
def main(classifier = None):
    print ("Select function:")
    print ("1 - Dataset Generation : 2 - Training : 3 - Testing : 4 - Prediction : 5 - Exit")
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
            testing_func(classifier)
            main(classifier)
        else:
            print ("Needs to be trained first.")
    elif function == "4":
        if classifier != None:
            prediction_func(classifier)
            main(classifier)
        else:
            print ("Needs to be trained first.")
    elif function == "5":
        pass
    else:
        print ("Not valid option")

# ------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
