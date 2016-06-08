#!/usr/bin/python3

import pickle
import sys
from random import randint

def choose_ngram(ngrams_dict):
    ngrams = sorted(ngrams_dict.items(), key=lambda x: x[1], reverse=True)

    total = sum([ count for (ngram, count) in ngrams ])

    selector = randint(1, total)
    for (ngram, count) in ngrams:
        selector -= count
        if selector <= 0: return ngram

def generate():
    n = 1
    s = []

    next_ngram = '_%START%_'

    while len(s) == 0 or not '_%END%_' in s[-1:][0]:
        print('.', end="")
        try:
            next_dict  = model[n][next_ngram]
        except KeyError:
            # fall back to n-1 grams; couldn't find a successor!
            print('Fallback!')
            print('Failed to find', n, 'gram successor for', next_ngram)
            s.pop()
            next_ngram = ' '.join(next_ngram.split(' ')[:-1])
            s.append(next_ngram)
            n -= 1
            print('Retry for', next_ngram)
            continue

        next_ngram = choose_ngram(next_dict)

        # NOTE(jordan): this is one lookahead method; could also do 2i or
        # try replacing the current ngram if it fails to find an upgrade
        while n < max_n and n + 1 in model:
            last_word = next_ngram.split(' ')[-1]
            lookahead_dict = model[1][last_word]
            lookahead = choose_ngram(lookahead_dict)

            nplus1_gram = next_ngram + ' ' + lookahead
            if nplus1_gram in model[n + 1]:
                #print('Upgrade to', n + 1, 'gram!')
                n += 1
                next_ngram = nplus1_gram

        s.append(next_ngram)

    print(' '.join(s).replace('\\n', '\n'))

if __name__ == '__main__':
    with open(sys.argv[1], 'rb') as handle:
        model = pickle.load(handle)

        max_n = int(sys.argv[2]) if 2 in sys.argv else 100

        generate()

