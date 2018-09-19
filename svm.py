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


def get_filepaths(directory):
    """
    This function will generate the file names in a directory
    tree by walking the tree either top-down or bottom-up. For each
    directory in the tree rooted at directory top (including top itself),
    it yields a 3-tuple (dirpath, dirnames, filenames).
    Assumption: the files do not have some .png in their name
    """
    file_paths = []  # List which will store all of the full filepaths.

    # Walk the tree.
    for root, directories, files in os.walk(directory):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            if filename.find('.pdf.txt') > 0 : # get only the pdf.txt files
              filepath = os.path.join(root, filename)
              file_paths.append(filepath)  # Add it to the list.

    return file_paths  # Self-explanatory.

def check_file_esist(tfidf_path,filelist_path):
    #check if the database with features exist
    if not os.path.isfile(tfidf_path):
        print("You need to run tfidf first to produce the features!")
        sys.exit()
    if not os.path.isfile(filelist_path):
        print("You need to run tfidf first to produce the features!")
        sys.exit()

for i in range(1, Config.nr_users + 1, 1):
    usr_dir = Config.dataset_dir + "train/usr" + str(i)
    tfidf_path = usr_dir + Config.tfidf_path
    filelist_path = usr_dir + Config.filelist_path
    check_file_esist(tfidf_path, filelist_path)

    # load the file list
    filelist = pickle.load(open(filelist_path, 'rb'))
    #load the features
    out = pickle.load(open(tfidf_path, 'rb'))
    X = out['X']
    X = X.todense()



#TBD Need to split to the users and then assigns 0 for the wrong paper and 1 for the right paper
#TBD might need to change the tfidf to be for each user and to be for training and validation different...
"""
y = np.zeros(X.shape[0])
for ix in posix: y[ix] = 1

clf = svm.LinearSVC(class_weight='balanced', verbose=False, max_iter=10000, tol=1e-6, C=0.1)
clf.fit(X, y)
s = clf.decision_function(X)

sortix = np.argsort(-s)
sortix = sortix[:min(num_recommendations, len(sortix))]  # crop paper recommendations to save space
user_sim[uid] = [strip_version(meta['pids'][ix]) for ix in list(sortix)]
"""
