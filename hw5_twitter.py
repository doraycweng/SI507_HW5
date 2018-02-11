from requests_oauthlib import OAuth1
import string
import json
import sys
import requests
import secret_data # file that contains OAuth credentials
import nltk # uncomment line after you install nltk

## SI 206 - HW
## COMMENT WITH:
## Your section day/time: Monday/13:00 
## Any names of people you worked with on this assignment:

#usage should be python3 hw5_twitter.py <username> <num_tweets>
username = sys.argv[1]
num_tweets = sys.argv[2]

consumer_key = secret_data.CONSUMER_KEY
consumer_secret = secret_data.CONSUMER_SECRET
access_token = secret_data.ACCESS_KEY
access_secret = secret_data.ACCESS_SECRET

#Code for OAuth starts
url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
auth = OAuth1(consumer_key, consumer_secret, access_token, access_secret)
requests.get(url, auth=auth)
#Code for OAuth ends

#Write your code below:
#Code for Part 3:Caching
#Finish parts 1 and 2 and then come back to this

CACHE_FNAME = 'twitter_cache.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

except:
    CACHE_DICTION = {}


def params_unique_combination(baseurl, params):
    alphabetized_keys = sorted(params.keys())
    res = []
    for k in alphabetized_keys:
        res.append("{}-{}".format(k, params[k]))
    return baseurl + "_".join(res)


def make_request_using_cache(baseurl, params):
    unique_ident = params_unique_combination(baseurl,params)

    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    else:
        print("Making a request for new data...")
        resp = requests.get(baseurl, auth=auth, params=params)
        CACHE_DICTION[unique_ident] = json.loads(resp.text)
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]


#Code for Part 1:Get Tweets
baseurl = "https://api.twitter.com/1.1/statuses/user_timeline.json"
params = {"screen_name": username, "count": num_tweets}
results_list = make_request_using_cache(baseurl, params)
file = open('tweet.json', 'w')
file.write(json.dumps(results_list, indent=4))


#Code for Part 2:Analyze Tweets
word_list = []
stop_word_list = ["http", "https", "RT"]
for tweet in results_list:
    tokens = nltk.word_tokenize(tweet["text"])
    for token in tokens:
        if token[0] in list(string.ascii_letters) and token not in stop_word_list:
            word_list.append(token)

wordCount_diction = {}
for word in word_list:
	if word.lower() in wordCount_diction.keys():
		wordCount_diction[word.lower()] += 1 
	else:
		wordCount_diction[word.lower()] = 1


print("USER: " + username + "  TWEETS ANALYZED: " + num_tweets)
print("5 MOST FREQUENT WORDS: ")
sort_list=sorted(wordCount_diction, key=wordCount_diction.__getitem__ , reverse = True)
for word in sort_list[:5]:
	print(word + "(" + str(wordCount_diction[word]) + ")")



if __name__ == "__main__":
    if not consumer_key or not consumer_secret:
        print("You need to fill in client_key and client_secret in the secret_data.py file.")
        exit()
    if not access_token or not access_secret:
        print("You need to fill in this API's specific OAuth URLs in this file.")
        exit()
