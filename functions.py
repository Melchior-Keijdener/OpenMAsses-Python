import pandas as pd
import nltk
import re
import numpy as np


def allowed_file(filename):
    """checks for the types of files that are uploaded, for now, only csv is accepted, but more can be added"""
    allowed_extensions = ['csv', 'xlsx', 'xls']
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


def stem_long_list(long_list):
    stem_maker = nltk.PorterStemmer()
    long_list = pd.read_excel(long_list)
    flat_list = []
    for term in long_list['Description']:
        terms = term.split(';')
        clean_terms = []
        for clean_term in terms:
            print(clean_term)
            clean_terms = clean_term.split(' ')

            print(clean_terms)

            print(clean_term)
            clean_term = clean_term.strip()
            clean_terms.append(clean_term)
        flat_list.extend(clean_terms)
    dict_of_terms = {i: 0 for i in np.unique(flat_list)}
    print(np.unique(flat_list))
    print(dict_of_terms)
