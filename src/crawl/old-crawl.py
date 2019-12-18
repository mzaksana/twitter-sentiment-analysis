import sys
import tweepy
import json
from textblob import TextBlob


data={}

# Step 1 - Authenticate
consumer_key= 'mx14dcaWnCOFS5UQ0oPq3VbNv'
consumer_secret= 'IJRxUDU1dvYn4PoAUwUB4dHRSpMRYWgT0fgSBP0ZDD2ROFx29B'

access_token='3285650046-JakbVAQdZnFcLOsAVV7bkqUs6AN9IIkUzujujNr'
access_token_secret='d94IrkCqi7GrMIdDOjz8oRxjdmrFpM7ZyKY1mQ2MPwWPU'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


def writeFile(string,dst):
    file=open(dst,"w+")
    file.write(string)
    file.close()

def crawl(target):

    #Step 2 - Retrieve Tweets
    return api.search(q=[target], parser=tweepy.parsers.JSONParser(),count=100000)
     

targets=["garudaindonesia","lionair","citylink","indonesiaairasia","wingsair","sriwijayaair"]
print(targets)
for target in targets:
    print(target)
    data[target]=crawl(target)

print("Save to ")
writeFile(json.dumps(data),sys.argv[1])
