"""
Parse all the files an compute the tfidf features. First train on the training dataset and then produce the features.

Write the features in tfidf.db and the file list in file_list.db with pickle. This files will be writen for each user
in the respective user directories.

Dependeciy to scikit-learn

"""

import os
import re
import pickle
from random import shuffle, seed
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from utils import Config

##INPUTS TO THE CODE
txt_paths = []
max_features = 5000


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
            if filename.find('.pdf.txt') > 0 : # get only the png files
              filepath = os.path.join(root, filename)
              file_paths.append(filepath)  # Add it to the list.

    return file_paths  # Self-explanatory.
  
def save_data(features,file_list,fname_features,fname_filelist):
    with open(fname_features, 'wb') as f:
      pickle.dump(features, f, -1)

    with open(fname_filelist, 'wb') as f:
      pickle.dump(file_list, f, -1)


# create an iterator object to conserve memory
def make_corpus(paths):
  for p in paths:
    with open(p, 'r') as f:
      txt = f.read()
    yield txt


#learn how to build the tfidf features from the training data
txt_paths = get_filepaths(Config.dataset_dir + "train/")

# compute tfidf vectors with scikits
v = TfidfVectorizer(input='content',
                    encoding='utf-8', decode_error='replace', strip_accents='unicode',
                    lowercase=True, analyzer='word', stop_words='english',
                    token_pattern=r'(?u)\b[a-zA-Z_][a-zA-Z0-9_]+\b',
                    ngram_range=(1, 2), max_features=max_features,
                    norm='l2', use_idf=True, smooth_idf=True, sublinear_tf=True,
                    max_df=1.0, min_df=1)

train_corpus = make_corpus(txt_paths)
v.fit(train_corpus)

#for all users parse the files and generate the tfidf features and write them in that directory
for i in range(1, Config.nr_users + 1, 1):
    """
        First generate the features for the training data.
    """
    print("Training dataset...")
    usr_dir = Config.dataset_dir + "train/usr" + str(i)
    tfidf_path = usr_dir + Config.tfidf_path
    filelist_path = usr_dir + Config.filelist_path
    txt_paths = []
    txt_paths = get_filepaths(usr_dir)

    # transform
    print("transforming %d documents..." % (len(txt_paths), ))
    corpus = make_corpus(txt_paths)
    X = v.transform(corpus)
    print(X.shape)

    # write full matrix out and write also the file list
    out = {}
    out['X'] = X # this one is heavy!
    print("writing", tfidf_path,filelist_path)
    save_data(out,txt_paths, tfidf_path,filelist_path)
    """
        Second generate the features for the validation data.
    """
    print("Validation dataset...")
    usr_dir = Config.dataset_dir + "valid/usr" + str(i)
    tfidf_path = usr_dir + Config.tfidf_path
    filelist_path = usr_dir + Config.filelist_path
    txt_paths = []
    txt_paths = get_filepaths(usr_dir)

    # transform
    print("transforming %d documents..." % (len(txt_paths), ))
    corpus = make_corpus(txt_paths)
    X = v.transform(corpus)
    print(X.shape)

    # write full matrix out and write also the file list
    out = {}
    out['X'] = X # this one is heavy!
    print("writing", tfidf_path,filelist_path)
    save_data(out,txt_paths, tfidf_path,filelist_path)