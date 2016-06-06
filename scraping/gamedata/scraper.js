// NOTE(jordan): requires
var sutils = require('../scrape_common/utils')
  , utils  = require('utils')
  , fs     = require('fs')
  , _      = require('underscore')
  , casper = require('casper').create({
    verbose: true,
    logLevel: "debug"
  })

// NOTE(jordan): defaults
var page = casper.cli.options.page

var headers = [
  'appid',
  'url',
  'name',
  'release',
  'reviewSummary',
  'reviewSentiment',
  'reviewScore',
  'reviewCount'
]

var output_line = function (arr, msg) {
  fs.write('data/gamedata.csv', '"' + arr.join('","') + '"' + '\n', 'a')
  console.log(msg)
}

var output_game = function (game) {
  var gameLine = _.values(game)
  output_line(gameLine, 'wrote game: ' + game.name)
}

function processGames () {
  games = document.getElementById('search_result_container')
                  .children[1]
                  .getElementsByTagName('a')

  return [].map.call(games, function (game) {
    var gamedata = {}

    gamedata.appid   = game.getAttribute('data-ds-appid')
    gamedata.url     = game.href
    gamedata.name    = game.querySelector('.search_name > .title').textContent
    gamedata.release = game.querySelector('.search_released').textContent

    gamedata.reviewSummary = null
    gamedata.reviewScore   = '-1'
    gamedata.reviewSentiment = 'none'
    gamedata.reviewCount   = '0'

    var reviewSummary = game.querySelector('.search_review_summary')

    if (reviewSummary) {
      gamedata.reviewSummary = reviewSummary.getAttribute('data-store-tooltip')

      // NOTE(jordan): get sentiment
      gamedata.reviewSentiment = game.querySelector('.search_review_summary')
                                      .className
                                      .replace('search_review_summary ', '')

      // NOTE(jordan): get review "positivity"
      reviewBrIdx = gamedata.reviewSummary.indexOf('<br>') + 4
      reviewPctIdx = gamedata.reviewSummary.indexOf('%')
      gamedata.reviewScore = gamedata.reviewSummary.slice(reviewBrIdx, reviewPctIdx)

      // NOTE(jordan): get review count
      reviewsStart = gamedata.reviewSummary.indexOf('the') + 4
      reviewsEnd = gamedata.reviewSummary.indexOf('user reviews')
      reviewsStr = gamedata.reviewSummary.slice(reviewsStart, reviewsEnd)
      gamedata.reviewCount = reviewsStr.replace(',', '')
    }

    return gamedata
  })
}

if (!fs.exists('data/gamedata.csv')) {
  console.log('Fresh scrape job!')
  console.log('Writing headers...')
  output_line(headers, 'wrote headers: ' + headers.toString())
} else {
  console.log('Continuing old scrape job...')
}

// NOTE(jordan): begin scraping
console.log('\n================\n\nBegin scraping!\n\n===============\n')
casper.start(sutils.getUrl('games', { page: page }))

// NOTE(jordan): load basic data
casper.then(function processSearchPage () {
  this.echo('Got search page: ' + page + '.')

  games = this.evaluate(processGames)
  games.forEach(output_game)
})

casper.run()

