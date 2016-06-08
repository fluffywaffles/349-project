# EECS 349 Project
Jordan Timmerman
Agam Gupta
Upasna Madhok
Michael Horst

## How to run the scraper (in general)

You must **already** have nodejs and npm installed.

Then, you need to install the dependencies. (There aren't many.)

```
npm i -g phantomjs casperjs
npm install
```

Then you can run the scrapers.

**NOTE** The review scraper depends on the game data scraper's output. You
cannot run them in parallel, nor can you run the review scraper at all until the
game scraper has been run.

The scrapers are in the root directory of the project. You can run them by
opening your terminal and typing

```
$ ./scrape-gamedata
... (some time passes)
$ ./scrape-reviews
```

`./scrape-gamedata` will scrape the Steam API for every game in its database.

`./scrape-reviews` will scrape the Steam API for every review of every game that
was previously scraped.

You'll probably see some error messages. These can be ignored so long as they do
not interfere with output looking like "wrote {review|game} ..." and so long as
phantomjs does not crash.

All scraped output will go to the `data` directory.

## Getting Started (faster)

For convenience's sake, a pre-scraped gamedata file is stashed in the data
directory. The `./scrape-reviews` script is pre-set to look for this file
instead of the usual file output by the `./scrape-gamedata` script.

So you can skip running `./scrape-gamedata`.

## What is happening?

We're using NodeJS to drive a headless version of the webkit rendering engine.
More specifically, we're using the CasperJS wrapper API on the PhantomJS
headless browser task-runner. Which is a bunch of gibberish, but basically we
can run javascript inside of an invisible browser to scrape content from the DOM
without parsing strings or anything else. Check out the `scraping` folder if you
want to see the code, but it's not super pretty.

## How to process the data

### Dependencies

A lot of the data processing is dependent on common unix utilities, so you won't
be able to run them on Windows.

You'll also need to install GNU Parallel, which is used in a few of the scripts
to speed up their execution and give a live ETA on their progress.

There are data processing scripts all over the place, but most of them are
centralized in data/reviews-aggregators/scripts. After scraping the reviews and
general gamedata from steam, you can use the `gen-top-n` script to generate
lists of the top n reviews for some number of games.

eg

```
$ pwd
data/reviews-aggregators
$ scripts/gen-top-n 10 ../reviews/* > top10.csv
$ scripts/gen-top-n 50 ../reviews/10270.csv > 10270-top10.csv
```

There's also a `scripts/gen-more-than-100-list` for generating a file of all the
games with more than 100 user reviews, which narrows the field and increases the
overall quality quite a bit if you then use that list as the input to gen-top-n
script calls.

## How to use the Hidden Markov Model

The HMM is written in python3, and it's in the hmm/ directory.

There are two components: create-model.py (for creating a model and dumping a
pickled version of it for later) and generate.py (for loading the pickle dump
and using the model to generate reviews).

Here's how to use them:

```
$ python3 create-model.py {csv to use for input}
```

create-model has help text and all kinds of stuff. There are only two options,
though: `--ngram=X` for generating up to X-grams from the input data (default is
2), and `-o outputname` for setting the name portion of the output pickle file
to something memorable if you want. Otherwise it'll default to the name of the
file you're loading. Eg, if you call it on top10.csv, it's going to create a
pickle file hmm-top10-X_grams.pickle.

```
$ python3 generate.py {pickle file to use for input} {optional max n-gram size}
```

This one doesn't have much to it. It'll just churn for a bit and then spit out a
bunch of text.

