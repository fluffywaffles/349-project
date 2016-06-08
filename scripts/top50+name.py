import codecs # to open a text file in utf-8
import pandas # To extract data from the csv and have robust functionality
import glob # To iterate through files in a directory

colnames = ['url','reviewerUsername','reviewerDisplayName','reviewerUrl','reviewerProductsCount',\
			'reviewText','date','recommended','hoursPlayed','voteText','helpfulPercent','votesHelpful',\
			'votesTotal','votesFunny','commentsCount']

# get game ids and names
gamecols = ['appid','name','release','reviewCount','reviewScore','reviewSentiment',\
			'reviewSummary','url']
gameInfo = pandas.read_csv("../data/gamedata-no-dupes.csv")
gameIDs = gameInfo.appid.tolist()
gameNames = gameInfo.name.tolist()

numgames = 0
text_file = codecs.open("../data/top_3+name-100.txt", "w", "ascii") #creates a text file for the particular game
for game in glob.iglob('../data/reviews/*.csv'):
	numgames += 1
	if numgames == 100:
		break

	data = pandas.read_csv(game, names=colnames)
	reviewsText = data.reviewText.tolist()

	# get the name of the game given the app id
	gameID = int(game[16:-4]) # file name minus the .csv - 16 for ../data/reviews/
	if gameID in gameIDs:
		index = gameIDs.index(gameID)
		name = gameNames[index].decode('ascii', errors='ignore')
	else:
		name = "NoName"

	if len(reviewsText) > 200:
		#splitting about the '\n'
		nl = '\n'
		for review in reviewsText[1:51]:
			# write the game name before each review
			text_file.write(name)
			text_file.write('\n')
			# decode the review
			review = str(review).decode('ascii', errors = 'ignore')
			review = nl.join(review.split('\\n'))
			# write review to a text file
			text_file.write(review)
			text_file.write('\n\n')

text_file.close();