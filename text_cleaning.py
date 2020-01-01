import pandas as pd
import json
import string
import unicodedata
from nltk import pos_tag
from nltk.corpus import wordnet, stopwords
from nltk.tokenize import WhitespaceTokenizer
from nltk.stem import WordNetLemmatizer
import re
from pprint import pprint
import matplotlib.pyplot as plt

with open('credentials.json') as f:
    params = json.load(f)

with open('contraction_map.json') as f:
    contraction_map = json.load(f)


def create_full_text(row):
    if (not row[0]) and (row[-2]):
        return row[-2]
    elif (not row[-2]) and (row[0]):
        return row[0]
    else:
        return str(row[0]) + ' ' + str(row[-2])


def remove_accented_chars(text):
    pattern = r'(&#x\d\d\d\w)'
    text = re.sub(pattern, '', text)
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    return text


def remove_special_characters(text, remove_digits=True):
    text = text.replace('/', ' ')
    pattern = r'[^a-zA-z0-9\s]' if not remove_digits else r'[^a-zA-z\s]'
    text = re.sub(pattern, '', text)
    return text


def get_wordnet_pos(pos_tag):
    if pos_tag.startswith('J'):
        return wordnet.ADJ
    elif pos_tag.startswith('V'):
        return wordnet.VERB
    elif pos_tag.startswith('N'):
        return wordnet.NOUN
    elif pos_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN


def expand_contractions(text, contraction_mapping=contraction_map):
    contractions_pattern = re.compile('({})'.format('|'.join(contraction_mapping.keys())),
                                      flags=re.IGNORECASE | re.DOTALL)

    def expand_match(contraction):
        match = contraction.group(0)
        first_char = match[0]
        expanded_contraction = contraction_mapping.get(match) \
            if contraction_mapping.get(match) \
            else contraction_mapping.get(match.lower())
        expanded_contraction = first_char + expanded_contraction[1:]
        return expanded_contraction

    expanded_text = contractions_pattern.sub(expand_match, text)
    expanded_text = re.sub("'", "", expanded_text)
    return expanded_text


def clean_text(text):
    try:
        text = re.split(r'\s+|[,;.-]\s*', text)
        text = [w.strip(string.punctuation) for w in text]
        text = [w for w in text if not any(c.isdigit() for c in w)]
        text = [w.lower() for w in text]
        stop = stopwords.words("english")
        text = [w for w in text if w not in stop]
        text = [t for t in text if len(t) > 2]
        pos_tags = pos_tag(text)
        text = [WordNetLemmatizer().lemmatize(t[0], get_wordnet_pos(t[1])) for t in pos_tags]
    except:
        text = None
    return text


if __name__ == '__main__':
    df_raw = pd.read_csv("20191225_saved_comments_{}.csv".format(params['username']))
    df_raw.drop('Unnamed: 0', axis=1, inplace=True)
    df_raw.set_index('id', inplace=True)

    df_raw['full_text'] = df_raw.apply(create_full_text, axis=1)

    df_raw.full_text = df_raw.full_text.apply(remove_accented_chars)
    df_raw.full_text = df_raw.full_text.apply(expand_contractions)
    df_raw.full_text = df_raw.full_text.apply(remove_special_characters)

    df_raw['full_text_cleaned'] = df_raw.full_text.apply(clean_text)
    df_raw.to_excel('reddit_saved_comments_cleaned.xlsx')
