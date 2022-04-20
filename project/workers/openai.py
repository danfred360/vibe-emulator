import os
import openai

class CompletionRequest:
    def __init__(self, model, prompt, n=1):
        try:
            self.response = openai.Completion.create(
                model=model,
                prompt=prompt,
                max_tokens=70,
                n=n,
                stop="\n"
            )
        except Exception as e:
            print("Exception occured while attempting completion request: {}".format(e))


# Note: this doesn't do anything yet

class FineTunedModelCreator:
    def __init__(self, training_file_path, model):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        openai.FineTune.create(
            training_file=training_file_path,
            model=model,
            suffix="suffix"
            )

        self.bearer_token = os.environ.get("OPENAI_API_KEY")

        url = self.create_url(training_file_path, model)
        self.response = self.connect_to_endpoint(url)


    # TODO use pagination_token parameter to load results until max_result
    def create_url(self, training_file_path, model):
        training_file_path_param = "training_file={}".format(training_file_path)
        model_param = "model={}".format(model)
        url = "https://api.openai.com/v1/fine-tunes?{}&{}".format(training_file_path_param, model_param)
        return url


    def bearer_oauth(self, r):
        """
        Method required by bearer token authentication.
        """

        r.headers["Authorization"] = f"Bearer {self.bearer_token}"
        r.headers["User-Agent"] = "v2TweetLookupPython"
        return r


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