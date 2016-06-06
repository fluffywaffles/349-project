var urls        = require('./urls')
  , extend      = require('extend')
  , querystring = require('querystring')

exports.getUrl = function getUrl (endpoint, params) {
  params   = params || {}
  endpoint = (endpoint instanceof Object && endpoint) || urls[endpoint]

  return urls[endpoint.base]
    + endpoint.path
    + '?' + querystring.stringify(extend(endpoint.params, params))
}

exports.getUrlForGame = function getUrlForGame (endpoint, name, params) {
  endpoint = urls[endpoint]
  endpoint.path = endpoint.path.replace(/\{gameid\}/, name)

  return exports.getUrl(endpoint, params)
}

