"""
Parse all the files an compute the tfidf features. Write the features in tfidf.db

Dependeciy to scikit-learn

TODO: Need to split this into test/validation/TEST
TODO: Files in same test are the same and marked as 1 the rest are 0, we would need to recomand the ones from the same test
"""

import os
import re
import pickle
from random import shuffle, seed
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


##INPUTS TO THE CODE
dataset_dir = "/media/robert/Data/work/papers/dataset"
tfidf_path = dataset_dir + '/tfidf.db'

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
  
def save_features(obj, fname):
    with open(fname, 'wb') as f:
      pickle.dump(obj, f, -1)

# create an iterator object to conserve memory
def make_corpus(paths):
  for p in paths:
    with open(p, 'r') as f:
      txt = f.read()
  yield txt

txt_paths = get_filepaths(dataset_dir)

# compute tfidf vectors with scikits
v = TfidfVectorizer(input='content', 
        encoding='utf-8', decode_error='replace', strip_accents='unicode', 
        lowercase=True, analyzer='word', stop_words='english', 
        token_pattern=r'(?u)\b[a-zA-Z_][a-zA-Z0-9_]+\b',
        ngram_range=(1, 2), max_features = max_features, 
        norm='l2', use_idf=True, smooth_idf=True, sublinear_tf=True,
        max_df=1.0, min_df=1)


train_corpus = make_corpus(txt_paths)
v.fit(train_corpus)

# transform
print("transforming %d documents..." % (len(txt_paths), ))
corpus = make_corpus(txt_paths)
X = v.transform(corpus)
#print(v.vocabulary_)
print(X.shape)

# write full matrix out
out = {}
out['X'] = X # this one is heavy!
print("writing", tfidf_path)
save_features(out, tfidf_path)