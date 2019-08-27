
# The request_token, get_oauth_token, parse_oauth_token are:
#
# uCopyright (c) 2008 Mike Verdone
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files(the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

import twitter

from .access_token import Token


class twitter_api:
    oauth_token = ""
    oauth_token_secret = ""

    def request_token(self, token_filename=None, open_browser=True):
        oc = 'http://127.0.0.1:5000/oauth_callback'

        consumer_key = Token.CONSUMER_KEY
        consumer_secret = Token.CONSUMER_SECRET

        tw = twitter.Twitter(
            auth=twitter.OAuth('', '', consumer_key, consumer_secret),
            format='', api_version=None)
        a = tw.oauth.request_token(oauth_callback=oc)
        twitter_api.oauth_token, twitter_api.oauth_token_secret = self.parse_oauth_tokens(
            a)

        oauth_url = ('https://api.twitter.com/oauth/authenticate?oauth_token=' +
                     twitter_api.oauth_token)
        return oauth_url

    def get_oauth_token(self, oauth_verifier):
        tw = twitter.Twitter(
            auth=twitter.OAuth(
                twitter_api.oauth_token, twitter_api.oauth_token_secret,
                Token.CONSUMER_KEY, Token.CONSUMER_SECRET),
            format='', api_version=None)
        twitter_api.oauth_token, twitter_api.oauth_token_secret = self.parse_oauth_tokens(
            tw.oauth.access_token(oauth_verifier=oauth_verifier))
        return twitter_api.oauth_token, twitter_api.oauth_token_secret

    def parse_oauth_tokens(self, result):
        for r in result.split('&'):
            k, v = r.split('=')
            if k == 'oauth_token':
                oauth_token = v
            elif k == 'oauth_token_secret':
                oauth_token_secret = v
        return oauth_token, oauth_token_secret

    def login_twitter_oauth(self, oauth_token, oauth_token_secret):
        twitter_api.api = twitter.Twitter(
            auth=twitter.OAuth(oauth_token, oauth_token_secret,
                               Token.CONSUMER_KEY, Token.CONSUMER_SECRET))

    def login_twitter(self):
        # 読み取りだけなのでOAuth2
        bearer_token = twitter.oauth2_dance(
            Token.CONSUMER_KEY, Token.CONSUMER_SECRET)
        self.api = twitter.Twitter(
            auth=twitter.OAuth2(bearer_token=bearer_token), retry=True)

    def get_self_conversation(self, name, root_twid, mode='thread'):
        tweets = []

        # ツイート3200件取得
        for i in range(1, 17):
            gets = self.api.statuses.user_timeline(
                id=name, count=200, include_rts=False, page=i)
            if(len(gets) == 0):
                break
            tweets += gets

        twid = root_twid
        tweet_list = []

        while True:
            twid_tmp = twid
            for i, tweet in enumerate(tweets):
                if(mode == 'thread'):
                    # 対象ツイートにリプライを送っているツイートを取得
                    if(tweet['in_reply_to_status_id'] != twid):
                        continue

                    t = tweet
                elif(mode == 'quote'):
                    # 引用でないツイートは無視
                    if('quoted_status_id' not in tweet):
                        continue

                    if(tweet['quoted_status_id'] != twid):
                        continue

                    t = self.get_tweet(tweet['in_reply_to_status_id'])

                # 取得したツイートに画像がない場合は無視
                if('extended_entities' not in t):
                    continue
                if('media' not in t['extended_entities']):
                    continue
                tweet_list.append(t)
                twid = t['id']

            if(twid_tmp == twid):
                break

        return tweet_list

    def get_tweet(self, twid):
        status = self.api.statuses.show(
            id=twid, include_entities=True)
        return status

    def get_api_status(self):
        status = self.api.application.rate_limit_status()
        for s in status['resources'].values():
            for n, lim in s.items():
                if(lim['limit'] != lim['remaining']):
                    print(n, ' - ', lim['limit'], ' : ', lim['remaining'])
# end of class twitter_api
