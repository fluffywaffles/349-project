#!/usr/bin/python3

import csv
import argparse
import pickle

parser = argparse.ArgumentParser(description="Desperate HMM just wants to please")

parser.add_argument('corpusfile', metavar='CF', type=str,
                    help='the corpus file')
parser.add_argument('--ngram', dest='ngram', default=2, type=int,
                    help='max ngram size (default: 2, bigrams)')
parser.add_argument('-o', dest='outfile', default=None, type=str,
                    help='where to output the pickled model')

args = parser.parse_args()

with open(args.corpusfile, encoding='utf-8') as corpus:
    reader = csv.reader(corpus)

    # NOTE(jordan): this is a hack that won't work after the data is re-scraped
    # but ack whatever
    _url=0
    _reviewerUsername=1
    _reviewerDisplayName=2
    _reviewerUrl=3
    _reviewerProductCount=4
    _reviewText=5
    _date=6
    _recommended=7
    _hoursPlayed=8
    _voteText=9
    _helpfulPercent=10
    _votesHelpful=11
    _votesTotal=12
    _votesFunny=13
    _commentsCount=14

    model = {}

    ngram = args.ngram

    out = args.outfile or args.corpusfile.split('/')[-1:][0].split('.')[0]

    print('Generating model...')

    count = 0

    for review in reader:
        count += 1
        print('\n- On review #%s' % count)

        reviewText = review[_reviewText]
        #paragraphs = reviewText.split('\n')

        reviewText = '_%START%_ ' + reviewText + ' _%END%_'

        words = list(filter(None, reviewText.split(' ')))
        # now let's add them to the model
        print('\tCreating ngrams...', end='\n\t')

        textcount = 0

        for i in range(len(words)):
            textcount += 1

            print('.', end='')
            if (textcount % 50 == 0): print('\n\t', end='')

            for n in range(1, ngram + 1):
                grams  = words[i : (i + n)]
                next_grams = words[(i + n) : (i + 2*n)]
                stringg = ' '.join(grams)
                stringn = ' '.join(next_grams)
                # Let's allow imbalanced successors so that _%END%_s don't get lost
                if len(grams) is n:# and len(next_grams) is n:
                    try:
                        model[n][stringg][stringn] = model[n][stringg][stringn] + 1
                    except KeyError:
                        if not n in model:
                            model[n] = {}
                        if not stringg in model[n]:
                            model[n][stringg] = {}
                        model[n][stringg][stringn] = 1

        print()

with open('hmm-%s-%s_grams.pickle' % (out, ngram), 'wb') as handle:
    pickle.dump(model, handle)

