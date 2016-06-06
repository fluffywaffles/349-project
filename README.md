# EECS 349 Project
Jordan Timmerman
Agam Gupta
Upasna Madhok
Michael Horst

## What you need to do (Agam, Upasna, and Michael)

Make sure you already have node and npm installed.

Run the following commands:

```
npm i -g phantomjs casperjs
npm install
./scrape-part gameid-splits/gameid-split-{your name here}
```

so for instance I would run

```
./scrape-part gameid-splits/gameid-split-jordan
```

THEN, very importantly, run all of the following:

```
git add --all
git commit -am "{Your name here} game reviews scraped."
git push origin master
```

Thanks!

## How to run the scraper (in general)

First, you need to install all the dependencies. (There aren't many.)

You must **already** have nodejs and npm installed.

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

