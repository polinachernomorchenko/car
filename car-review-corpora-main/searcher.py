import sqlite3
import pandas as pd
from pymystem3 import Mystem

ms = Mystem()

s = ''
con = sqlite3.connect('tachka_database.db')


def plus(i, df, ss):
    cr = 0
    for j in range(len(ss)):
        if len(ss[j]) == 2:
            cr += 1
            pos_tag = ss[j][1]
            return cr, pos_tag, j

    return [cr]


def search(s, con, ms):
    ss = s.split()
    df = pd.read_sql("SELECT * from words_table", con)
    tags = ['ADJ',
            'ADP',
            'ADV',
            'AUX',
            'CCONJ',
            'DET',
            'INTJ',
            'NOUN',
            'NUM',
            'PART',
            'PRON',
            'PROPN',
            'SCONJ',
            'SYM',
            'VERB',
            'X']
    cols = ['lemma' for i in range(len(ss))]

    for i in range(len(ss)):
        ss[i] = ss[i].split('+')

    for i in range(len(ss)):
        if ss[i][0][0] == '"':
            cols[i] = 'word'
        else:
            if ss[i][0].isupper() and ss[i][0] in tags:
                cols[i] = 'pos'
            else:
                ss[i][0] = ms.lemmatize(ss[i][0])[0]
                print(ss[i][0])

    pattern = [i[0].replace('"', '') for i in ss]
    print(pattern)
    u = []

    if len(pattern) == 3:
        for i in range(len(df) - len(pattern)):
            if df[cols[0]][i] == pattern[0] and df[cols[1]][i + 1] == pattern[1] and df[cols[2]][i + 2] == pattern[2]:
                cr = plus(i, df, ss)[0]
                if cr == 1:
                    j = plus(i, df, ss)[2]
                    if df['pos'][i + j] == plus(i, df, ss)[1]:
                        if df['sentence_id'][i] == df['sentence_id'][i + 1] == df['sentence_id'][i + 2]:
                            u.append(
                                (df['sentence_id'][i], ' '.join([df['word'][i], df['word'][i + 1], df['word'][i + 2]])))

                if cr == 0:
                    u.append((df['sentence_id'][i], ' '.join([df['word'][i], df['word'][i + 1], df['word'][i + 2]])))

    if len(pattern) == 2:
        for i in range(len(df) - len(pattern)):
            if df[cols[0]][i] == pattern[0] and df[cols[1]][i + 1] == pattern[1]:
                cr = plus(i, df, ss)[0]
                if cr == 1:
                    j = plus(i, df, ss)[2]
                    if df['pos'][i + j] == plus(i, df, ss)[1]:
                        if df['sentence_id'][i] == df['sentence_id'][i + 1]:
                            u.append((df['sentence_id'][i], ' '.join([df['word'][i], df['word'][i + 1]])))

                if cr == 0:
                    if df['sentence_id'][i] == df['sentence_id'][i + 1]:
                        u.append((df['sentence_id'][i], ' '.join([df['word'][i], df['word'][i + 1]])))

    if len(pattern) == 1:
        for i in range(len(df)):
            if df[cols[0]][i] == pattern[0]:
                cr = plus(i, df, ss)[0]
                if cr == 1:
                    j = plus(i, df, ss)[2]
                    if df['pos'][i + j] == plus(i, df, ss)[1]:
                        u.append((df['sentence_id'][i], df['word'][i]))

                if cr == 0:
                    u.append((df['sentence_id'][i], df['word'][i]))

    if u:
        return u
    else:
        return 'нет результатов по вашему запросу'


def sents(u, con):
    ll = []
    if u == 'нет результатов по вашему запросу':
        return 'нет результатов по вашему запросу'
    else:
        for i in range(len(u)):
            df_s = pd.read_sql("SELECT * from sentences_table", con)
            d = {}
            a_i = df_s[df_s['sentence_id'] == u[i][0]]['author_id'].item()
            s = df_s[df_s['sentence_id'] == u[i][0]]['sentence'].item()
            url_p_id = df_s[df_s['sentence_id'] == u[i][0]]['url_id'].item()
            df_u = pd.read_sql("SELECT * from urls", con)
            url = df_u[df_u['url_id'] == url_p_id]['url'].item()
            df_a = pd.read_sql("SELECT * from authors", con)
            a_url = df_a[df_a['author_id'] == a_i]['author'].item()
            d['author'] = a_url
            d['sentence'] = s
            d['url'] = url
            d['ans'] = u[i][1]
            ll.append(d)

        return ll
