import flask
from ._app import app
from .twmng import twitter_api


@app.route('/')
def show_entries():
    tw = twitter_api()
    tw.login_twitter()

    root_twid = 1158573410516996097
    tweet_list = []

    tweet_list.append(tw.get_tweet(root_twid))
    tlist = tw.get_timeline(tweet_list[0]['user']['screen_name'],
                            root_twid)
    tweet_list = tweet_list + tlist

    image_list = []

    for tweet in tweet_list:
        for images in tweet['extended_entities']['media']:
            image_list.append(images['media_url'])

    return flask.render_template('index.html', image_list=image_list)
