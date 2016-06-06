from bs4 import BeautifulSoup, Comment
import json   # to use json files
import codecs # to open a text file in utf-8
import urllib # for to internet
import pandas # To extract data from the csv and have robust functionality

# extracting a list of game ids from the csv
colnames = [
    'appid',
    'average_2weeks',
    'players_2weeks',
    'name',
    'ccu',
    'publisher',
    'developer',
    'players_forever',
    'median_forever',
    'median_2weeks',
    'players_forever_variance',
    'owners',
    'average_forever',
    'score_rank',
    'players_2weeks_variance',
    'owners_variance'
]

data = pandas.read_csv('unwrapped-data.csv', names=colnames)

id_list = data.appid.tolist()

for game_id in id_list[1:]:
    # functionality for looking at reviews on the offet of 20. So basically
    # having different values of offset from 0,1,2,3,.. depending on the number
    # of reviews available
    url = (
        "http://store.steampowered.com/appreviews/"
        "" + str(game_id) + ""
        "?start_offset=0&day_range=1&filter=all&language=english"
    )
    print url
    # url = "http://store.steampowered.com/appreviews/400?start_offset=0&day_range=1&filter=all&language=english"

    json_file = urllib.urlopen(url) # This needs to be made so that any file can be loaded thru URL
    json_data = json.load(json_file) # extracts the data

    if ('html' in json_data):
        print 'we got data'
        html = json_data["html"] # extracts the part in the html tag
        with codecs.open("reviews_compiled.txt", "w", "utf-8") as text_file:
            soup = BeautifulSoup(html, 'html.parser')
            text_file.write('\n===\n')
            text_file.write(url)
            for row in soup.find_all('div', attrs={"class" : "content"}):
                text_file.write('\n' + row.text + '\n---\n')

