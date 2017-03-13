import tweepy
from normalizr import Normalizr


numTweetsToSave = input("Tweets to download: " + "\r\n")
numTweetsToSave = int(numTweetsToSave)
phraseToTrack = input("Phrase to track: " + "\r\n")
fileName = phraseToTrack + ".txt"
tweetList = [] #Stores each tweet
stringList = [] #Stores each word from each tweet (2D)

normalizr = Normalizr(language='en')

#Consumer key & secret, access token & secret
ckey = "Fkd21xKJHEC6v9jrOJeesjGPG"
csecret = "tjZQjWPjwbIIZlPjfIN3t1aVFX6JnwUF2BYS3di4V9WhyOw4VJ"
atoken = "807338254202642432-Nzlv8Re6FV19FK621k9T5tjtFr2Knh0"
asecret = "8s5ynqCDSplh6rQTxkp0UETsPfqe4q6SkoPGGhEXVr5A0"


'''
The following code is based closely on code written by:

Harrison Kinsley
PythonProgramming.net

It is used with his permission and can be found in the following YouTube
playlist:

Twitter API v1.1, uploaded by sentdex (Harrison Kinsley's YouTube channel)

https://www.youtube.com/watch?v=pUUxmvvl2FE&list=PLQVvvaa0QuDdlcEkEtW64jmeFlLZ_XgmT
'''     
def IsolateText(inputString, startString, endString):
    if inputString.split(startString)[0] != inputString:
        result = inputString.split(startString)[1]
        result = result.split(endString)[0]
        return result
    else:
        return "\r\n"
    
def ProcessTweet(rawData):
    tweetID = IsolateText(rawData, '","id":', ',"id_str":')
    tweetText = IsolateText(rawData, '","text":', ',"source":')
    tweetText = tweetText.split(',"display_text_range":')[0]
    return tweetText

def SaveTweetToFile(tweet, fileName):
    saveFile = open(fileName, 'a')
    saveFile.write(tweet)
    saveFile.write('\n')
    saveFile.close()

class TrimmedListener(tweepy.streaming.StreamListener):
    def on_data(self, data):
        tweetText = ProcessTweet(data)
        tweetText = normalizr.normalize(tweetText)
        SaveTweetToFile(tweetText, fileName)
        tweetList.append(tweetText)
        if len(tweetList) < numTweetsToSave:
            return True
        else:
            return False
    def on_error(self, status):
        print(status)

auth = tweepy.OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

trimmedStream = tweepy.Stream(auth, TrimmedListener())
trimmedStream.filter(track=[phraseToTrack], languages=["en"], async = False)
''' This concludes the section based on Harrison Kinsley's code '''

print("Done")
