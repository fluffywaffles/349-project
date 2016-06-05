import csv
import json
#from pprint import pprint

def run ():
    with open("./unwrapped-data.json") as json_file:
        json_data = json.load(json_file)

    with open("./unwrapped-data.csv", "w") as csv_file:
        headers = json_data[0].keys()

        writer = csv.writer(csv_file, delimiter=",", quotechar="|")

        writer.writerow(headers)

        for game in json_data:
            writer.writerow(game.values())

if __name__ == '__main__':
    run()

