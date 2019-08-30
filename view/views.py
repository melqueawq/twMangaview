import twitter
import json
from .twmng import twitter_api

from ._app import app
from flask import render_template, request, redirect, url_for, session
from .models import Books, Users
from ._app import db

# index
@app.route('/')
def index():
    # メッセージがなかったら無視する
    try:
        message = session['message']
        session.pop('message', None)
    except KeyError:
        message = ''
        pass
    return render_template('index.html', message=message)

# 検索
@app.route('/search')
def search_book():
    query = request.args.get('query')
    sbox = request.args.get('sbox')

    # メッセージがなかったら無視する
    try:
        message = session['message']
        session.pop('message', None)
    except KeyError:
        message = ''
        pass

    content = []

    # セレクトボックスの中身に応じて処理を変更
    if (sbox == 'title'):
        content = Books.query.filter(Books.title.like('%'+query+'%')).all()
    elif (sbox == 'url'):
        content = Books.query.filter_by(url=query).all()
    elif (sbox == 'author'):
        # @がなければつける
        if('@' not in query):
            query = '@' + query
        content = Books.query.filter_by(author=query).all()

    # if len(content) == 0:
    #    return redirect(url_for('index'))
    return render_template('search.html', twurl=query, content=content,
                           sbox=sbox, message=message)

# ビューワ
@app.route('/view')
def view_book():
    id = request.args.get('id')
    content = Books.query.filter_by(id=id).first()

    j = open('json/books/'+content.jsonfile, 'r')
    image_list = json.load(j)['image_list']

    return render_template('view.html', imgl=image_list, title=content.title)

# サインイン
@app.route('/signin')
def login_twitter():
    tw = twitter_api()
    oauth_url, oauth_token, oauth_secret = tw.request_token()
    session['oauth_token'] = oauth_token
    session['oauth_secret'] = oauth_secret
    return redirect(oauth_url)

# oauth認証のコールバック
@app.route('/oauth_callback')
def oauth_login():
    oauth_verifier = request.args.get('oauth_verifier')
    tw = twitter_api()

    oauth_token = session['oauth_token']
    oauth_secret = session['oauth_secret']
    oauth_token, oauth_secret = tw.get_oauth_token(
        oauth_token, oauth_secret, oauth_verifier)

    session['oauth_token'] = oauth_token
    session['oauth_secret'] = oauth_secret
    tw.login_twitter_oauth(oauth_token, oauth_secret)

    screen_name, profile_image_url = tw.get_account()
    session['screen_name'] = screen_name
    session['profile_image_url'] = profile_image_url

    # ユーザ登録
    user = Users.query.filter_by(screen_name=screen_name).all()
    if not user:
        data = {"books": []}
        j = open('json/user/' + screen_name + '.json', 'w')
        json.dump(data, j)
        d = Users(screen_name=screen_name,
                  jsonfile=screen_name+'.json')
        db.session.add(d)
        db.session.commit()

    return redirect(url_for('index'))

# サインアウト
@app.route('/signout')
def signout():
    if('oauth_token' in session):
        session.pop('oauth_token', None)
        session.pop('oauth_secret', None)
        session.pop('screen_name', None)
    return redirect(url_for('index'))

# プロフィール
@app.route('/profile/<screen_name>')
def profile(screen_name):
    # DBからリクエストのユーザー名のユーザを探す
    user = Users.query.filter_by(screen_name=screen_name).first()
    screen_id = user.screen_id
    j = open('json/user/'+user.jsonfile, 'r')
    for b in j['books']:
        pass

    if user:
        return render_template('profile.html', screen_id=screen_id)
    else:
        return redirect(url_for('index'))

# Twitterから取得する
@app.route('/fetch')
def fetch_book():
    tw = twitter_api()
    tw.login_twitter()

    # 引用かスレッドか
    sbox = request.args.get('sbox')

    # ツイートID切り出し
    twurl = request.args.get('twurl')[8:].split('/')[-1].split('?')[0]
    root_twid = int(twurl)

    tweet_list = tlist = []

    try:
        # ツイートを持ってくる
        tweet_list.append(tw.get_tweet(root_twid))
        tlist = tw.get_self_conversation(tweet_list[0]['user']['screen_name'],
                                         root_twid, mode=sbox)
    except twitter.api.TwitterHTTPError as e:
        print(e)
        session['message'] = 'tapi'
        return redirect(url_for('/'))

    tweet_list = tweet_list + tlist

    image_data = {"date": tweet_list[0]['created_at'], 'image_list': []}

    # 画像だけ取得
    for tweet in tweet_list:
        for images in tweet['extended_entities']['media']:
            image_data['image_list'].append(images['media_url'])

    # 画像ヒット数が1つ未満だったら登録せずにエラー
    if(len(image_data['image_list']) <= 1):
        session['message'] = 'not_manga'
        return redirect(url_for('search_book', query=request.args.get('twurl'),
                                sbox='url'))

    # json出力
    j = open('json/books/' + twurl + '.json', 'w')
    json.dump(image_data, j)

    # db登録
    d = Books(title=request.args.get('title'),
              author='@'+tweet_list[0]['user']['screen_name'],
              url=request.args.get('twurl'),
              thumbnail=image_data['image_list'][0],
              jsonfile=twurl + '.json',
              user_id=session['screen_name'])
    db.session.add(d)
    db.session.commit()

    session['message'] = 'success'
    return redirect(url_for('search_book', query=request.args.get('twurl'),
                            sbox='url'))
