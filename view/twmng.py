import twitter
from .access_token import Token


class twitter_api:
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
