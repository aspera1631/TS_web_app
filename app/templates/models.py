__author__ = 'bdeutsch'
import twitter_text as tt
from ttp import ttp
import re


def get_len(list):
    len1 = 0
    for item in list:
        len1 += len(item) + 1
    return len1

def count_https(list):
    count = 0
    for item in list:
        if item[:5] =='https':
            count += 1
    return count


def emoji_txt(text):
    # search for retweet
    #print text
    n = re.findall('(\\\U\w{8}|\\\u\w{4})', text)
    if n:
        return len(n)
    else:
        return 0


def tweet_features(df, tweet):
    # run a tweet through the parser
    p = ttp.Parser()
    result = p.parse(tweet)

    # Use the twitter text py package to validate length
    tweet_tt = tt.TwitterText(tweet)


    df["ht_num"] = [len(result.tags)]                   # number of hashtags
    df["user_num"] = [len(result.users)]                # number of user mentions
    df["url_num"] = [len(result.urls)]                  # number of urls
    df["https_num"] = [count_https(result.urls)]        # Number of secure urls
    df["http_num"] = df["url_num"] - df["https_num"]    # number of other urls

    df["ht_len"] = get_len(result.tags)                 # total length of all hashtags
    df["user_len"] = get_len(result.users)              # total length of all user mentions
    df["txt_len_tot"] = [tweet_tt.validation.tweet_length()]    # total length of tweet
    # length of basic text in tweet (no urls, hashtags, user mentions)
    df["txt_len_basic"] = df["txt_len_tot"] - df["user_len"] - df["ht_len"] - df["https_num"]*23 - df["http_num"]*22

    return df

# order: [emo_num, ]

def print_lit(text):
    return text.encode('ascii')

test = "This web app was easy to make! #sarcastic @InsightDataSci"