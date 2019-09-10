import twitter
from .config import CONSUMER_KEY, CONSUMER_SECRET


class twitter_api:

    def request_token(self, hosturl, token_filename=None, open_browser=True):
        oc = hosturl + 'oauth_callback'
        print('oc = ' + oc)
        tw = twitter.Twitter(
            auth=twitter.OAuth('', '', CONSUMER_KEY, CONSUMER_SECRET),
            format='', api_version=None)
        a = tw.oauth.request_token(oauth_callback=oc)
        oauth_token, oauth_secret = self.parse_oauth_tokens(
            a)

        oauth_url = ('https://api.twitter.com/oauth/authenticate?'
                     + 'oauth_token=' + oauth_token)
        return oauth_url, oauth_token, oauth_secret

    def get_oauth_token(self, oauth_token, oauth_secret, oauth_verifier):
        tw = twitter.Twitter(
            auth=twitter.OAuth(
                oauth_token, oauth_secret,
                CONSUMER_KEY, CONSUMER_SECRET),
            format='', api_version=None)
        oauth_token, oauth_secret = self.parse_oauth_tokens(
            tw.oauth.access_token(oauth_verifier=oauth_verifier))
        return oauth_token, oauth_secret

    def parse_oauth_tokens(self, result):
        for r in result.split('&'):
            k, v = r.split('=')
            if k == 'oauth_token':
                oauth_token = v
            elif k == 'oauth_token_secret':
                oauth_token_secret = v
        return oauth_token, oauth_token_secret

    def login_twitter_oauth(self, oauth_token, oauth_secret):
        self.api = twitter.Twitter(
            auth=twitter.OAuth(oauth_token, oauth_secret,
                               CONSUMER_KEY, CONSUMER_SECRET))

    def get_account(self):
        status = self.api.account.verify_credentials(skip_status=True)
        return status['screen_name'], status['profile_image_url_https']

    def login_twitter(self):
        # 読み取りだけなのでOAuth2
        bearer_token = twitter.oauth2_dance(
            CONSUMER_KEY, CONSUMER_SECRET)
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
