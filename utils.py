"""
Provides some helping functions and some variables to be used accroas multiple scripts
"""

import os

class Config(object):
    dataset_dir = "dataset/" #path of the dataset
    xplorer_save_dir = "dataset_ieee/"  # here we save all the papers from xplore

    tfidf_path = dataset_dir + '/tfidf.db' #tfidf features are writen here
    filelist_path = dataset_dir + 'file_list.db'

    max_features = 5000 #this is the max number of features we want to creat with scikit
    overwrite_txt = 1 #overwrite the text files already existing when transforming pdf2txt (1,0)


def get_pdf_filepaths(directory):
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
            if filename.find('.pdf') > 0 : # get only the png files
	      if filename.find('.txt') < 1:
                filepath = os.path.join(root, filename)
                file_paths.append(filepath)  # Add it to the list.

    return file_paths  # Self-explanatory.

def get_txt_filepaths(directory):
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
