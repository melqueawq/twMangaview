from ._app import app
from flask import render_template, request
from .twmng import twitter_api
import twitter
from .models import Books


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search')
def search_book():
    twurl = request.args.get('twurl')
    content = Books.query.filter_by(url=twurl).all()
    if content is None:
        return render_template('index.html')
    return render_template('search.html', twurl=twurl, content=content)


@app.route('/view')
def view_book():
    tw = twitter_api()
    tw.login_twitter()

    twurl = request.args.get('twurl')[8:].split('/')[-1].split('?')[0]
    print('twid = ' + twurl)
    root_twid = int(twurl)
    # root_twid = 1158573410516996097

    tw.get_api_status()

    tweet_list = tlist = []

    try:
        tweet_list.append(tw.get_tweet(root_twid))
        tlist = tw.get_self_conversation(tweet_list[0]['user']['screen_name'],
                                         root_twid)
    except twitter.api.TwitterHTTPError as e:
        print(e)
        return render_template('index.html')

    tweet_list = tweet_list + tlist

    image_list = []

    for tweet in tweet_list:
        for images in tweet['extended_entities']['media']:
            image_list.append(images['media_url'])

    return render_template('view.html', image_list=image_list)
