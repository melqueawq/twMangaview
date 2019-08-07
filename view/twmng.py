import twitter
from .access_token import Token


class twitter_api:
    def login_twitter(self):
        self.api = twitter.Twitter(
            auth=twitter.OAuth(Token.ACCESS_TOKEN, Token.ACCESS_TOKEN_SECRET,
                               Token.CONSUMER_KEY, Token.CONSUMER_SECRET),
            retry=True)

    def get_timeline(self, name, root_twid):
        tweets = []
        for i in range(1, 3):
            tweets += self.api.statuses.user_timeline(
                id=name, count=200, include_rts=False, page=i)

        twid = root_twid
        tweet_list = []
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

    def search_responce(self, word, root_twid):
        tweets = self.api.search.tweets(
            q=word, count=200, since_id=root_twid,
            include_entities=True)["statuses"]

        twid = root_twid
        tweet_list = []
        while True:
            twid_tmp = twid
            for tweet in tweets:
                if(tweet['in_reply_to_status_id'] == twid):
                    tweet_list.append(tweet)
                    twid = tweet['id']

            if(twid_tmp == twid):
                break

        return tweet_list
# end of class twitter_api
