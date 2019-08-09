import twitter
from .access_token import Token


class twitter_api:
    def login_twitter(self):
        self.api = twitter.Twitter(
            auth=twitter.OAuth(Token.ACCESS_TOKEN, Token.ACCESS_TOKEN_SECRET,
                               Token.CONSUMER_KEY, Token.CONSUMER_SECRET))

    def get_self_conversation(self, name, root_twid):
        tweets = []

        # ツイート600件取得
        for i in range(1, 17):
            gets = self.api.statuses.user_timeline(
                id=name, count=200, include_rts=False, page=i)
            if(len(gets) == 0):
                print(i)
                break
            tweets += gets

        twid = root_twid
        tweet_list = []

        # スレッド取得
        while True:
            twid_tmp = twid
            for tweet in tweets:
                if(tweet['in_reply_to_status_id'] == twid):
                    tweet_list.append(tweet)
                    twid = tweet['id']

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
