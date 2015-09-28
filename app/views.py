from flask import render_template, request
from app import app
import MySQLdb
from models import tweet_features, get_tweet_html, validate_tweet


@app.route('/')
@app.route('/input')
def landing():
    return render_template("input.html", img_count=0)
    # input template -> score. Carries image info.


@app.route('/score', methods=['GET', 'POST'])
def score():
    img_count = int(request.form['img_count'])
    tweet_in = request.form['tweetText']
    try:
        file1 = request.form["file"]
    except:
        file1 = None
    if file1:
        img_count += 1

    tweet_coord = tweet_features(tweet_in, img_count) # input image count
    tweet_html = get_tweet_html(tweet_in)
    invalid_tweet = validate_tweet(tweet_in, img_count)

    db = MySQLdb.connect(host='localhost', user='root', passwd='CFT^vgy7', db='tweetscore', charset='utf8')

    with db:
        cur = db.cursor()
        #just select the city from the world_innodb that the user inputs
        cur.execute("SELECT msg1, msg2, msg3 FROM recommendations_RF2 WHERE desig='%s';" % tweet_coord)
        query_results = cur.fetchall()

    if invalid_tweet is False:
        msg1 = query_results[0][0]
        msg2 = query_results[0][1]
        msg3 = query_results[0][2]

        if msg1 == "":
            msg1 = "This tweet is the best it can be! If you want to improve, try something completely different."
            msg2 = ""
            msg3 = ""

        return render_template("score.html", tweet_html=tweet_html, img_count=img_count, tweetText=tweet_in, msg1=msg1,
                               msg2=msg2, msg3=msg3)

    elif invalid_tweet == "Too long":
        msg1 = "This tweet is more than 140 characters."
        msg2 = ""
        msg3 = ""
        return render_template("score.html", tweet_html=tweet_html, img_count=img_count, tweetText=tweet_in, msg1=msg1,
                               msg2=msg2, msg3=msg3)
    else:
        msg1 = "This does not appear to be a valid tweet!"
        msg2 = ""
        msg3 = ""
        return render_template("score.html", tweet_html=tweet_html, img_count=img_count, tweetText=tweet_in, msg1=msg1,
                               msg2=msg2, msg3=msg3)


@app.route('/upload', methods=['GET', 'POST'])
# Upload an image. For now, just point to input.
def upload():
    img_count = int(request.form['img_count'])
    tweet_in = request.form['tweetText']
    return render_template("score.html", img_count=img_count, tweetText=tweet_in)


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    img_count = int(request.form['img_count'])
    tweet_in = request.form['tweetText']
    return render_template("edit.html", tweetText=tweet_in, img_count=img_count)