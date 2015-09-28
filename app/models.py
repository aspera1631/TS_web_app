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
    text1 = text.encode('unicode-escape')
    n = re.findall('(\\\U\w{8}|\\\u\w{4})', text1)
    if n:
        return len(n)
    else:
        return 0


def tweet_features(tweet, img_count):

    # run a tweet through the parser
    p = ttp.Parser()
    result = p.parse(tweet)

    # Use the twitter text py package to validate length
    tweet_tt = tt.TwitterText(tweet + "*"*23*img_count)

    # bin sizes:
    len_bas_max = 140
    len_bas_step = 5
    ht_max = 6
    ht_step = 1
    user_max = 6
    user_step = 1
    url_max = 2
    url_step = 1
    media_max = 2
    media_step = 1
    emo_max = 6
    emo_step = 1


    emo_num = min([emoji_txt(tweet), emo_max])
    ht_num = min([len(result.tags), ht_max])
    media_num = img_count
    url_num = min([len(result.urls), url_max])
    user_num = min([len(result.users), user_max])

    # calculate basic text length
    ht_len = get_len(result.tags)
    user_len = get_len(result.users)
    https_num = count_https(result.urls)
    http_num = url_num - https_num
    url_len = https_num*23 + http_num*22
    media_len = media_num*23

    txt_len_tot = tweet_tt.validation.tweet_length()  # total length of tweet.
    txt_len_basic = min([(txt_len_tot - ht_len - user_len - url_len - media_len - emo_num)//len_bas_step, len_bas_max//len_bas_step])

    if txt_len_basic > 9:
        str_out = "[  %s.   %s.   %s.  %s.   %s.   %s.]" % (emo_num, ht_num, media_num, txt_len_basic, url_num, user_num)
    else:
        str_out = "[ %s.  %s.  %s.  %s.  %s.  %s.]" % (emo_num, ht_num, media_num, txt_len_basic, url_num, user_num)

    return str_out

def validate_tweet(tweet, img_count):
    tweet_tt = tt.TwitterText(tweet + "*"*23*img_count)
    return tweet_tt.validation.tweet_invalid()

def get_tweet_html(tweet):
    p = ttp.Parser()
    result = p.parse(tweet)
    return result.html



def print_lit(text):
    return text.encode('unicode-escape')

test = "blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah @hiya @hiya @hiya blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah @hiya @hiya @hiya"


#print validate_tweet(test, 0)