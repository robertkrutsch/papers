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


#prepare paths and check if all data is tehre for us to train
dataset_dir   = Config.dataset_dir
tfidf_path    = Config.tfidf_path
filelist_path = Config.filelist_path

if not os.path.isfile(tfidf_path):
    print("You need to run tfidf first to produce the features!")
    sys.exit()

if not os.path.isfile(filelist_path):
    print("You need to run tfidf first to produce the features!")
    sys.exit()
# -----------------------------------------------------------------------------

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
