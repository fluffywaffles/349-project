# from bs4 import BeautifulSoup, Comment
import json #to use json files
import codecs # to open a text file in utf-8
import urllib
import pandas # To extract data from the csv and have robust functionality
import glob

# extracting a list of game ids from the csv
colnames = ['url','reviewerUsername','reviewerDisplayName','reviewerUrl','reviewerProductsCount',\
'reviewText','date','recommended','hoursPlayed','voteText','helpfulPercent','votesHelpful'\
,'votesTotal','votesFunny','commentsCount']

for game in glob.iglob('../data/fewreviews/*.csv'):
	
	data = pandas.read_csv(game, names=colnames)
	reviewsText = data.reviewText.tolist()

	text_file = codecs.open("multiplereviews_compiled.txt", "w", "ascii") #creates a text file for the particular game
	#splitting about the '\n'
	nl = '\n'

	for review in reviewsText[1:2]:

		review = review.decode('ascii', errors = 'ignore')
		review = nl.join(review.split('\\n'))
		#writing to a text file
		text_file.write(review)
		text_file.write('\n\n')

	text_file.close();