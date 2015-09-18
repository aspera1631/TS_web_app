from flask import render_template, request
from app import app
import MySQLdb
from models import tweet_features, get_tweet_html, validate_tweet

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html",
        title = 'Home', user = { 'nickname': 'Miguel'},
        )

@app.route('/db')
def cities_page():
    db = MySQLdb.connect(host='localhost', user='root', passwd='', db='world', charset='utf8')  # may need to add some other options to connect
    #db = mdb.connect(user="root", host="localhost", passwd="", db="education",  charset='utf8')


    with db:
        cur = db.cursor()
        cur.execute("SELECT Name FROM City LIMIT 15;")
        query_results = cur.fetchall()
    cities = ""
    for result in query_results:
        cities += result[0]
        cities += "<br>"
    return cities

@app.route("/db_fancy")
def cities_page_fancy():
    db = MySQLdb.connect(host='localhost', user='root', passwd='', db='world', charset='utf8')
    with db:
        cur = db.cursor()
        cur.execute("SELECT Name, CountryCode, Population FROM City ORDER BY Population LIMIT 15;")

        query_results = cur.fetchall()
    cities = []
    for result in query_results:
        cities.append(dict(name=result[0], country=result[1], population=result[2]))
    return render_template('cities.html', cities=cities)

@app.route('/input')
def input():
  return render_template("input.html")

@app.route('/output')
def output():
  #pull 'ID' from input field and store it
  tweet_in = request.args.get('tweet_in')
  tweet_coord = tweet_features(tweet_in)
  tweet_html = get_tweet_html(tweet_in)

  invalid_tweet = validate_tweet(tweet_in)


  db = MySQLdb.connect(host='localhost', user='root', passwd='', db='tweetscore', charset='utf8')

  with db:
    cur = db.cursor()
    #just select the city from the world_innodb that the user inputs
    cur.execute("SELECT msg1, msg2, msg3 FROM recommendations3 WHERE desig='%s';" % tweet_coord)
    query_results = cur.fetchall()

  if invalid_tweet is False:
    msg1 = query_results[0][0]
    msg2 = query_results[0][1]
    msg3 = query_results[0][2]

    if msg1 == "":
      msg1 = "You've found a local optimum!"
      msg2 = ""
      msg3 = ""
    return render_template("output.html", tweet_html=tweet_html, tweetText = tweet_in, msg1=msg1, msg2=msg2, msg3=msg3)

  else:
    msg1 = "This does not appear to be a valid tweet!"
    msg2 = ""
    msg3 = ""
    return render_template("output.html", tweet_html=tweet_html, tweetText = tweet_in, msg1=msg1, msg2=msg2, msg3=msg3)

@app.route('/edit_input')
def edit_input():
    tweet_in = request.args.get('tweet_in')

    return render_template("edit_input.html", tweetText = tweet_in)