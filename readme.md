# twitter bot using gpt-3
Currently this project will lookup a user by @ on twitter and export a JSONL file composed of three word prompts and resulting tweets to be used to fine tune an OpenAI model.

## Running project to generate training JSONL
First you'll need to create a .secret file emulating .secret-example with your Twitter bearer token and your OpenAI API key. You can obtain keys here:
- [Twitter API](https://developer.twitter.com/en/docs/twitter-api)
- [OpenAI API](https://openai.com/api/)

*Note: requires python3.10 and python3.10-venv*
```bash
chmod +x local-env.sh
. local-env.sh

# run once to initialize project environment
v-init

# to run
v-run
```

## Training Model
Prepare training file
```bash
openai tools fine_tunes.prepare_data -f <LOCAL_FILE>
```

Create a fine-tuned model
```bash
openai api fine_tunes.create -t <TRAIN_FILE_ID_OR_PATH> -m <BASE_MODEL> --suffix <SUFFIX>
# base_model options - davinci, curie, babbage, ada
# suffix is a string to append to beginning of model name

# resume event stream later if training takes a while
openai api fine_tunes.follow -i <YOUR_FINE_TUNE_JOB_ID>
```

List fine tunes
```bash
# List all created fine-tunes
openai api fine_tunes.list

# Retrieve the state of a fine-tune. The resulting object includes
# job status (which can be one of pending, running, succeeded, or failed)
# and other information
openai api fine_tunes.get -i <YOUR_FINE_TUNE_JOB_ID>

# Cancel a job
openai api fine_tunes.cancel -i <YOUR_FINE_TUNE_JOB_ID>
```

## Use a fine-tuned model
```bash
openai api completions.create -m <FINE_TUNED_MODEL> -p <YOUR_PROMPT>
```

## Documentation
[Open Api Project Docs](openai.md)

## Resources:
- [Towards Data Science Tutorial](https://towardsdatascience.com/step-by-step-twitter-sentiment-analysis-in-python-d6f650ade58d)
- [Geeks For Geeks Tutorial](https://www.geeksforgeeks.org/twitter-sentiment-analysis-using-python/)
- [Python Documentation](https://docs.python.org/3/)
- [Twitter API Docs](https://developer.twitter.com/en/docs)
  - [Tweets lookup](https://developer.twitter.com/en/docs/twitter-api/tweets/lookup/introduction)
  - [get tweets python example code - bearer token](https://github.com/twitterdev/Twitter-API-v2-sample-code/blob/main/Tweet-Lookup/get_tweets_with_bearer_token.py)
  - [ get tweets python example code - user context](https://github.com/twitterdev/Twitter-API-v2-sample-code/blob/main/Tweet-Lookup/get_tweets_with_user_context.py)