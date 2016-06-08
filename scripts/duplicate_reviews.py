import codecs # to open a text file in utf-8
import pandas # To extract data from the csv and have robust functionality
import glob # To iterate through files in a directory

colnames = ['url','reviewerUsername','reviewerDisplayName','reviewerUrl','reviewerProductsCount',\
			'reviewText','date','recommended','hoursPlayed','voteText','helpfulPercent','votesHelpful',\
			'votesTotal','votesFunny','commentsCount']

for game in glob.iglob('../data/reviews/730.csv'):
	
	data = pandas.read_csv(game, names=colnames)
	reviewsText = data.reviewText.tolist()

	if len(reviewsText) > 100:
		gameID = game[16:-4] # file name minus the .csv: start from 16 for ../data/reviews/
		saveloc = '../data/cs-go-' + gameID + '.txt'

		text_file = codecs.open(saveloc, "w", "ascii")
		#splitting about the '\n'
		nl = '\n'
		reviewNum = 0
		for review in reviewsText[1:990]:
			# decode the review
			review = str(review).decode('ascii', errors = 'ignore')
			review = nl.join(review.split('\\n'))
			if reviewNum > 500:
				review = review * int(20-(reviewNum/50))
			# write review to a text file
			text_file.write(review)
			text_file.write('\n\n')
			reviewNum += 1
	text_file.close()