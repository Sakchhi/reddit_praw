import pandas as pd
import json
import string
from nltk import pos_tag
from nltk.corpus import wordnet, stopwords
from nltk.tokenize import WhitespaceTokenizer
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import re
from pprint import pprint
import matplotlib.pyplot as plt

with open('credentials.json') as f:
    params = json.load(f)


def clean_text():


if __name__ == '__main__':
    df_raw = pd.read_csv("20191225_saved_comments_{}.csv".format(params['username']))
    df_raw.drop('Unnamed: 0', axis=1, inplace=True)
    df_raw.set_index('id', inplace=True)
