// NOTE(jordan): requires
var sutils = require('../scrape_common/utils')
  , fs     = require('fs')
  , casper = require('casper').create({
    verbose: true,
    logLevel: "debug"
  })

// help is tracing page's console.log
casper.on('remote.message', function(msg) {
    console.log('[Remote Page] ' + msg);
});

// Print out all the error messages from the web page
casper.on("page.error", function(msg, trace) {
    casper.echo("[Remote Page Error] " + msg, "ERROR");
    casper.echo("[Remote Error trace] " + JSON.stringify(trace, undefined, 4));
});

// NOTE(jordan): defaults
var page   = casper.cli.options.page || 1
  , gameid = casper.cli.options.gameid

var headers = [
  'url',
  'reviewerUsername',
  'reviewerDisplayName',
  'reviewerUrl',
  'reviewerProductsCount',
  'reviewText',
  'date',
  'recommended',
  'hoursPlayed',
  'voteText',
  'helpfulPercent',
  'votesHelpful',
  'votesTotal',
  'votesFunny',
  'commentsCount'
]

var output_line = function (arr, msg) {
  fs.write('data/reviews/' + gameid + '.csv', '"' + arr.join('","') + '"' + '\n', 'a')
  console.log(msg)
}

var output_object = function (object) {
  objectLine = headers.map(function (header) {
    return object[header]
  })
  output_line(objectLine, 'wrote review by: ' + object.reviewerDisplayName)
}

function processReviews (page) {
  pageDiv = document.getElementById('page' + page)
  if (!pageDiv) return []

  console.log('found pageDiv ' + page)

  reviews = pageDiv.getElementsByClassName('apphub_Card')

  return [].map.call(reviews, function (review) {
    var reviewdata = {}

    reviewdata.url = review.getAttribute('data-modal-content-url')

    reviewContent = review.querySelector('.apphub_UserReviewCardContent')

    reviewdata.voteText = reviewContent.querySelector('.found_helpful').innerText.split(/\r?\n|\r/g).map(function (s) { return s.trim() }).join(' ')

    reviewdata.helpfulPercent = '0'
    reviewdata.votesHelpful   = '0'
    reviewdata.votesTotal     = '0'
    reviewdata.votesFunny     = '0'

    if (!/No ratings yet/.test(reviewdata.voteText)) {
      percentMatches = reviewdata.voteText.match(/\((.+)%\)/)
      if (percentMatches) reviewdata.helpfulPercent = percentMatches[1]

      if (/1 person found this review helpful/.test(reviewdata.voteText)) {
        reviewdata.votesHelpful = reviewdata.votesTotal = 1
      } else {
        helpfulnessRatio = reviewdata.voteText.match(/(\w+) of (\w+)/)

        if (helpfulnessRatio) {
          if (helpfulnessRatio[1]) {
            reviewdata.votesHelpful = helpfulnessRatio[1].replace(',', '')
          }
          if (helpfulnessRatio[2]) {
            reviewdata.votesTotal   = helpfulnessRatio[2].replace(',', '')
          }
        }
      }

      votesFunny = reviewdata.voteText.match(/([0-9]+) people found this review funny/)

      if (votesFunny) reviewdata.votesFunny = votesFunny[1].replace(',', '')
    }

    reviewInfo = reviewContent.querySelector('.reviewInfo')

    reviewdata.recommended = reviewInfo.querySelector('.title').innerText.trim() === 'Recommended'

    hours = reviewInfo.querySelector('.hours')
    if (hours) reviewdata.hoursPlayed = reviewInfo.querySelector('.hours').innerText.match(/([0-9.]+) hrs/)[1]

    reviewdata.date = reviewContent.querySelector('.date_posted').innerText.split(':')[1].trim()

    reviewdata.reviewText = reviewContent.querySelector('.apphub_CardTextContent').innerText.split(/\r?\n|\r/g).slice(2).map(function (s) { return s.trim() }).join('\\n')

    reviewAuthor = review.querySelector('.apphub_CardContentAuthorBlock')

    reviewdata.reviewerUrl = reviewAuthor.querySelector('.apphub_friend_block_container > a').href

    // NOTE(jordan): there are two different formats of reviewerUrl
    var matches = reviewdata.reviewerUrl.match(/http:\/\/steamcommunity.com\/id\/(.+)\//)
                || reviewdata.reviewerUrl.match(/http:\/\/steamcommunity.com\/profiles\/(.+)\//)

    reviewdata.reviewerUsername = matches[1]
    reviewdata.reviewerDisplayName = reviewAuthor.querySelector('.apphub_CardContentAuthorName').innerText

    reviewdata.reviewerProductsCount = reviewAuthor.querySelector('.apphub_CardContentMoreLink').innerText.replace(',', '')
    reviewdata.commentsCount = reviewAuthor.querySelector('.apphub_CardCommentCount').innerText

    return reviewdata
  })
}

if (fs.exists('data/reviews/' + gameid + '.csv')) {
  console.log('Clean up the old data...')
  fs.remove('data/reviews/' + gameid + '.csv')
  console.log('All gone!')
}

console.log('Fresh scrape job!')
console.log('Writing headers...')
output_line(headers, 'wrote headers: ' + headers.toString())

// NOTE(jordan): begin scraping
console.log('\n================\n\nBegin scraping!\n\n===============\n')
casper.start(sutils.getUrlForGame('apphub_reviews', gameid))

function processReviewPage () {
  this.echo('Got AppHub Review page: ' + page + '.')

  reviews = this.evaluate(processReviews, page)
  if (reviews.length && page < 100) {
    reviews.forEach(output_object)

    this.thenEvaluate(function (page) {
      document.getElementById('MoreContentForm' + page).submit()
    }, page++)

    return this.wait(100, function () {
      return this.then(processReviewPage)
    })
  }
}

// NOTE(jordan): load basic data
casper.then(processReviewPage)

casper.run()

