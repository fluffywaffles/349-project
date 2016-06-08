import codecs # to open a text file in utf-8
import pandas # To extract data from the csv and have robust functionality
import glob

# extracting a list of game ids from the csv
colnames = ['url','reviewerUsername','reviewerDisplayName','reviewerUrl','reviewerProductsCount',\
'reviewText','date','recommended','hoursPlayed','voteText','helpfulPercent','votesHelpful'\
,'votesTotal','votesFunny','commentsCount']

text_file = codecs.open("../data/top_3.txt", "w", "ascii") #creates a text file for the particular game
for game in glob.iglob('../data/reviews/*.csv'):

	data = pandas.read_csv(game, names=colnames)
	reviewsText = data.reviewText.tolist()

	if len(reviewsText) > 100:
		#splitting about the '\n'
		nl = '\n'
		for review in reviewsText[1:4]:

			review = str(review).decode('ascii', errors = 'ignore')
			review = nl.join(review.split('\\n'))
			#writing to a text file
			text_file.write(review)
			text_file.write('\n\n')

text_file.close();