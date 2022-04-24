import requests
import os, sys
import json

class BearerOAuth(requests.auth.AuthBase):
    def __call__(self, r):
        """
        Method required by bearer token authentication.
        """

        r.headers["Authorization"] = f"Bearer {os.environ.get('TWITTER_BEARER_TOKEN')}"
        # r.headers["User-Agent"] = "v2UserLookupPython"
        return r


class GetUserTweets:
    def __init__(self, user_id):
        self.tweets = []
        response_page_limit = 5
        try:
            tweet_lookup = TweetLookup(user_id, 100)
            self.append_tweets(json.loads(tweet_lookup.response))
            try:
                pagination_token = json.loads(tweet_lookup.response)["meta"]["next_token"]
                while response_page_limit >= 0:
                    new_tweet_lookup = TweetLookup(user_id, 100, pagination_token)
                    self.append_tweets(json.loads(new_tweet_lookup.response))
                    try:
                        pagination_token = json.loads(new_tweet_lookup.response)["meta"]["next_token"]
                    except Exception as e:
                        print("Exception occurred gathering tweets (assumed no next page in response - response_page_limit = {}): {}\n".format(response_page_limit, e))
                        break
                    response_page_limit -= 1
            except Exception as e:
                print("Exception occurred gathering tweets (assumed no next page in response - response_page_limit = {}): {}\n".format(response_page_limit, e))
        except Exception as e:
            print("Exception occurred gathering tweets: {}\n".format(e))
            sys.exit(2)

    def append_tweets(self, tweet_lookup_response):
        for tweet in tweet_lookup_response["data"]:
            self.tweets.append(tweet)
            

class TweetLookup:
    def __init__(self, authour_id, max_results, pagination_token=None):
        if pagination_token is None:
            url = self.create_url(authour_id, max_results)
        else:
            url = self.create_url(authour_id, max_results, pagination_token)
        self.response = self.connect_to_endpoint(url)

    def create_url(self, author_id, max_results, pagination_token=None):
        # Tweet fields are adjustable.
        # Options include:
        # attachments, author_id, context_annotations,
        # conversation_id, created_at, entities, geo, id,
        # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
        # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
        # source, text, and withheld
        # ids = "ids={}".format(author_id) # specifying specific tweets instead of all user tweets
        # You can adjust ids to include a single Tweets.
        # Or you can add to up to 100 comma-separated IDs
        max_results_param = "max_results={}".format(max_results)
        exclude = "exclude={}".format("retweets,replies")
        if pagination_token is None:
            url = "https://api.twitter.com/2/users/{}/tweets?{}&{}".format(author_id, exclude, max_results_param)
        else:
            pagination_token_param = "pagination_token={}".format(pagination_token)
            url = "https://api.twitter.com/2/users/{}/tweets?{}&{}&{}".format(author_id, exclude, max_results_param, pagination_token_param)
        return url

    def connect_to_endpoint(self, url):
        response = requests.request("GET", url, auth=self.bearer_oauth)
        status_code = response.status_code
        if response.status_code != 200:
            raise Exception(
                "Request returned an error: {} {}".format(
                    response.status_code, response.text
                )
            )
        return json.dumps(response.json(), indent=4, sort_keys=True)


class UserLookup:
    def __init__(self, username_query):
        url = self.create_url(username_query)
        self.response = self.connect_to_endpoint(url)
        self.user_id = json.loads(self.response)["data"][0]["id"]

    def create_url(self, username_query):
        # Specify the usernames that you want to lookup below
        # You can enter up to 100 comma-separated values.
        usernames = "usernames={}".format(username_query)
        user_fields = "user.fields=description,created_at"
        # User fields are adjustable, options include:
        # created_at, description, entities, id, location, name,
        # pinned_tweet_id, profile_image_url, protected,
        # public_metrics, url, username, verified, and withheld
        url = "https://api.twitter.com/2/users/by?{}&{}".format(usernames, user_fields)
        return url

    def connect_to_endpoint(self, url):
        response = requests.request("GET", url, auth=BearerOAuth())
        status_code = response.status_code # do nothing
        if response.status_code != 200:
            raise Exception(
                "Request returned an error: {} {}".format(
                    response.status_code, response.text
                )
            )
        return json.dumps(response.json(), indent=4, sort_keys=True)
