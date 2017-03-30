import tweepy

ckey = "Fkd21xKJHEC6v9jrOJeesjGPG"
csecret = "tjZQjWPjwbIIZlPjfIN3t1aVFX6JnwUF2BYS3di4V9WhyOw4VJ"
atoken = "807338254202642432-Nzlv8Re6FV19FK621k9T5tjtFr2Knh0"
asecret = "8s5ynqCDSplh6rQTxkp0UETsPfqe4q6SkoPGGhEXVr5A0"

auth = tweepy.OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
api = tweepy.API(auth)

alltweets = []
users = ["UkNatArchives", "WW1TheGreatWar", "19141918online", "smhcentre", "jbanningww1"]
file = open("user tweets.txt", "w")

def IsolateText(inputString, startString, endString):
    if inputString.split(startString)[0] != inputString:
        result = inputString.split(startString)[1]
        result = result.split(endString)[0]
        return result
    else:
        return "\r\n"
    
def ProcessTweet(rawData):
    tweetText = IsolateText(rawData, ", 'text': \"", ", 'truncated':")
    return tweetText

#Code written by GitHub user 'yanofsky' -----------------------

def GetAllTweets(screen_name):

	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name,count=200)
	
	#save most recent tweets
	alltweets.extend(new_tweets)
	
	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1
	
	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		print("getting tweets before %s" % (oldest))
		
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
		
		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		
		print("...%s tweets downloaded so far" % (len(alltweets)))

for user in users:
    GetAllTweets(user)
for tweet in alltweets:
    file.write(str(tweet.text.encode("utf-8")) + "\r\n")
file.close()

# -------------------------------------------------------------------
