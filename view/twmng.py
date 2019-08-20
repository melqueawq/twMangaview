import twitter
from .access_token import Token


class twitter_api:
    def login_twitter(self):

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
            for tweet in tweets:
                if(mode == 'thread'):
                    # スレッド
                    if('extended_entities' not in tweet):
                        continue

                    if(tweet['in_reply_to_status_id'] == twid):
                        tweet_list.append(tweet)
                        twid = tweet['id']
                elif(mode == 'quote'):
                    # 引用
                    if('quoted_status_id' not in tweet):
                        continue

                    if(tweet['quoted_status_id'] == twid):
                        t = self.get_tweet(tweet['in_reply_to_status_id'])
                        tweet_list.append(t)
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
