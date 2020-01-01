from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import json

with open('credentials.json') as f:
    params = json.load(f)

if __name__ == '__main__':
    df_raw = pd.read_csv("20191225_saved_comments_{}.csv".format(params['username']))
    df_raw.drop('Unnamed: 0', axis=1, inplace=True)
    df_raw.set_index('id', inplace=True)

    df_raw['full_text'] = df_raw.apply(create_full_text, axis=1)
    df_raw.full_text = df_raw.full_text.apply(remove_accented_chars)
    print(df_raw.head().full_text)
