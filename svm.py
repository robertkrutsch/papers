# standard imports
"""
This script trains an svm/user.
"""

import os
import sys
import pickle
# non-standard imports
import numpy as np
from sklearn import svm
from sqlite3 import dbapi2 as sqlite3
# local imports
from utils import Config

"""
This compares the output of the classifier with the reference.
"""
def get_performance(out,ref):
    false_positive = 0
    false_negative = 0
    for i in range(len(out)):
        if (ref[i] == 1) and (out[i] < 0):
            false_negative = false_negative + 1
        if (ref[i] == 0) and (out[i] > 0):
            false_positive = false_positive + 1

    return false_negative,false_positive

"""
check if the database with features exist
"""
def check_file_esist(tfidf_path,filelist_path):
    if not os.path.isfile(tfidf_path):
        print("You need to run tfidf first to produce the features!")
        sys.exit()
    if not os.path.isfile(filelist_path):
        print("You need to run tfidf first to produce the features!")
        sys.exit()

len_usr = []
len_usr.append(0) #first needs to be zero such that we loop properly
for i in range(1, Config.nr_users + 1, 1):
    usr_dir = Config.dataset_dir + "train/usr" + str(i)
    tfidf_path = usr_dir + Config.tfidf_path
    filelist_path = usr_dir + Config.filelist_path
    check_file_esist(tfidf_path, filelist_path)

    # load the file list
    filelist = pickle.load(open(filelist_path, 'rb'))
    #load the features
    out = pickle.load(open(tfidf_path, 'rb'))
    tmp = out['X']
    tmp = tmp.todense()
    len_usr.append(tmp.shape[0]) # keep the number of the files that we have for each user
    if (i==1):
        X = tmp
    else:
        X = np.concatenate((X, tmp), axis=0)

poz = 0
for i in range(1, Config.nr_users + 1, 1):
    y = np.zeros(X.shape[0])
    poz = poz + len_usr[i-1]
    for ix in range(len_usr[i]):
        y[poz + ix] = 1

    clf = svm.LinearSVC(class_weight='balanced', verbose=False, max_iter=10000, tol=1e-6, C=0.1)
    clf.fit(X, y)

    s = clf.decision_function(X) #evaluate on the training dataset

    false_negative, false_positive = get_performance(s, y)
    print("Statistic on usr"+str(i)+":",false_negative,false_positive)

    #TBD - need to compare to the validation set and also against the trainingset, some comparing function would be good to have