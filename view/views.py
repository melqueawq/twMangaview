import twitter
import json
from .twmng import twitter_api

from ._app import app
from flask import render_template, request, redirect, url_for
from .models import Books
from ._app import db


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
    pass


@app.route('/fetch')
def fetch_book():
    tw = twitter_api()
    tw.login_twitter()

    twurl = request.args.get('twurl')[8:].split('/')[-1].split('?')[0]
    root_twid = int(twurl)
    # root_twid = 1158573410516996097

    tw.get_api_status()

    tweet_list = tlist = []

    try:
        # ツイートを持ってくる
        tweet_list.append(tw.get_tweet(root_twid))
        tlist = tw.get_self_conversation(tweet_list[0]['user']['screen_name'],
                                         root_twid)
    except twitter.api.TwitterHTTPError as e:
        print(e)
        return render_template('index.html')

    tweet_list = tweet_list + tlist

    image_data = {"date": tweet_list[0]['created_at'], 'image_list': []}

    # 画像だけ取得
    for tweet in tweet_list:
        for images in tweet['extended_entities']['media']:
            image_data['image_list'].append(images['media_url'])

    # json出力
    j = open('json/' + twurl + '.json', 'w')
    json.dump(image_data, j)

    # db登録
    d = Books(title=request.args.get('title'),
              author='@'+tweet_list[0]['user']['screen_name'],
              url=request.args.get('twurl'),
              jsonfile=twurl + '.json')
    db.session.add(d)
    db.session.commit()

    return redirect(url_for('search_book', twurl=request.args.get('twurl')))
