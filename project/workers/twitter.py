import requests
import os
import json

class TweetLookup:
    def __init__(self, authour_id):
        # To set your enviornment variables in your terminal run the following line:
        # export 'BEARER_TOKEN'='<your_bearer_token>'
        bearer_token = os.environ.get("TWITTER_BEARER_TOKEN")

        url = self.create_url(authour_id)
        self.response = self.connect_to_endpoint(url)


    def create_url(self, author_id):
        tweet_fields = "tweet.fields=lang,author_id"
        # Tweet fields are adjustable.
        # Options include:
        # attachments, author_id, context_annotations,
        # conversation_id, created_at, entities, geo, id,
        # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
        # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
        # source, text, and withheld
        ids = "ids={}".format(author_id)
        # You can adjust ids to include a single Tweets.
        # Or you can add to up to 100 comma-separated IDs
        url = "https://api.twitter.com/2/tweets?{}&{}".format(ids, tweet_fields)
        return url


    def bearer_oauth(r):
        """
        Method required by bearer token authentication.
        """

        r.headers["Authorization"] = f"Bearer {bearer_token}"
        r.headers["User-Agent"] = "v2TweetLookupPython"
        return r


    def connect_to_endpoint(url):
        response = requests.request("GET", url, auth=bearer_oauth)
        status_code = response.status_code
        if response.status_code != 200:
            raise Exception(
                "Request returned an error: {} {}".format(
                    response.status_code, response.text
                )
            )
        return [status_code, json.dumps(response.json(), indent=4, sort_keys=True)]


class UserLookup:

    def __init__(self, username_query):
        # To set your enviornment variables in your terminal run the following line:
        # export 'BEARER_TOKEN'='<your_bearer_token>'
        self.bearer_token = os.environ.get("TWITTER_BEARER_TOKEN")
        
        url = self.create_url(username_query)
        self.response = self.connect_to_endpoint(url)


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


    def bearer_oauth(self, r):
        """
        Method required by bearer token authentication.
        """

        r.headers["Authorization"] = f"Bearer {bearer_token}"
        r.headers["User-Agent"] = "v2UserLookupPython"
        return r


    def connect_to_endpoint(self, url):
        response = requests.request("GET", url, auth=bearer_oauth,)
        status_code = response.status_code # do nothing
        if response.status_code != 200:
            raise Exception(
                "Request returned an error: {} {}".format(
                    response.status_code, response.text
                )
            )
        return [status_code, json.dumps(response.json(), indent=4, sort_keys=True)]
