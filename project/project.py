from workers.twitter import TweetLookup, UserLookup
from workers.openai import CompletionRequest, FineTuneCreationRequest
from datetime import datetime
import sys, json, jsonlines

default_model_name = 'theonion'

models = {
        "default" : {
            'dril': 'curie:ft-personal:drilv3-2022-04-22-12-26-53',
            'tuckercarlson': 'curie:ft-personal:tuckercarlsonv2-2022-04-22-12-39-43',
            'berniesanders' : 'curie:ft-personal:berniesandersv2-2022-04-22-18-11-20',
            'sensanders' : 'curie:ft-personal:sensanders-2022-04-23-00-28-29',
            'elonmusk' : 'curie:ft-personal:elonv2-2022-04-22-16-44-32',
            'denzelcurry' : 'curie:ft-personal:denzelcurry-2022-04-23-00-03-44',
            'johndiesattheen' : 'curie:ft-personal:johndiesattheen-2022-04-23-00-35-19',
            'mkv-riscy' : 'curie:ft-personal:mkvriscy-2022-04-22-18-43-22',
            'wheezywaiter': 'curie:ft-personal:wheezywaiter-2022-04-23-03-48-03'
        }, # stop="###"
        "old" : {
            'justin-t' : 'curie:ft-personal-2022-04-20-14-53-01',
            'dril-old': 'curie:ft-personal:dril-2022-04-20-15-42-28',
            'elon': 'curie:ft-personal:elon-2022-04-20-17-13-57',
            'libsoftiktok' : 'curie:ft-personal:libsoftiktok-2022-04-20-17-49-25',
            'dojacat' : 'curie:ft-personal:dojacat-2022-04-20-22-06-20',
            'tuckercarlson' : 'curie:ft-personal:tuckercarlson-2022-04-21-00-47-52',
            'h3h3' : 'curie:ft-personal:h3h3productions-2022-04-21-01-06-50',
            'jordanbpeterson' : 'curie:ft-personal:jordanbpeterson-2022-04-21-01-18-02',
            'berniesanders' : 'curie:ft-personal:berniesanders-2022-04-21-01-43-04',
            'joebiden' : 'curie:ft-personal:joebiden-2022-04-21-02-34-22',
            'drilv2' : 'curie:ft-personal:drilv2-2022-04-21-02-55-13',
            'keemstar' : 'curie:ft-personal:keemstar-2022-04-21-03-11-19',
            'kanyewest' : 'curie:ft-personal:kanyewest-2022-04-21-03-31-32',
            'ggreenwald' : 'curie:ft-personal:ggreenwald-2022-04-21-04-20-24',
            'comicdavesmith' : 'curie:ft-personal:comicdavesmith-2022-04-21-04-06-10',
            'bts-twt' : 'curie:ft-personal:bts-twt-2022-04-21-18-36-39',
            'keyon' : 'curie:ft-personal:keyon-2022-04-21-18-47-47',
            'danfred360' : 'curie:ft-personal:dan-fred360-2022-04-21-03-43-25'
        }, # stop="\n"
        "frens" : {
            'GenisWon' : 'curie:ft-personal:geniswon-2022-04-21-19-34-24',
            'fearofsalt' : 'curie:ft-personal:fearofsalt-2022-04-21-20-17-17'
        },
        "sanders" : {
            'berniesanders' : 'curie:ft-personal:berniesandersv2-2022-04-22-18-11-20',
            'sensanders' : 'curie:ft-personal:sensanders-2022-04-23-00-28-29'
        },
        "political" : {
            'tuckercarlson': 'curie:ft-personal:tuckercarlsonv2-2022-04-22-12-39-43',
            'berniesanders' : 'curie:ft-personal:berniesandersv2-2022-04-22-18-11-20',
            'sensanders' : 'curie:ft-personal:sensanders-2022-04-23-00-28-29',
        },
        "fun" : {
            'tuckercarlson': 'curie:ft-personal:tuckercarlsonv2-2022-04-22-12-39-43',
            'johndiesattheen' : 'curie:ft-personal:johndiesattheen-2022-04-23-00-35-19'
        },
        "more" : {
            'theonion': 'curie:ft-personal:theonion-2022-04-21-19-19-28',
            'danpriceseattle' : 'curie:ft-personal:danpriceseattle-2022-04-22-01-11-11',
            'dril': 'curie:ft-personal:drilv3-2022-04-22-12-26-53',
            'tuckercarlson': 'curie:ft-personal:tuckercarlsonv2-2022-04-22-12-39-43',
            'elonmusk' : 'curie:ft-personal:elonv2-2022-04-22-16-44-32',
            'berniesanders' : 'curie:ft-personal:berniesandersv2-2022-04-22-18-11-20'
        }
    }

def emulate_vibe(num_responses=1, model_list_input="default", model_name_input=default_model_name):
    model = models[model_list_input][model_name_input]# models[8]

    print("----- Emulate {}'s Vibe ----".format(model_name_input))

    prompt = get_prompt()

    completion_request = CompletionRequest(model=model, prompt=prompt, stop_phrase="###", n=num_responses) # "\n" or "###"
    print("\nOutput for model\n\t{}:".format(model))
    for tweet in completion_request.response["choices"]:
        print("-------------------------------")
        print("\t{}".format(tweet.text))
        print("-------------------------------")

def compare_vibes(n, models_input="default"):
    models_list = models[models_input]

    print("---- Compare model responses for list {} ----".format(models_input))

    prompt = get_prompt()

    for model_key in models_list:
        completion_request = CompletionRequest(model=models_list[model_key], prompt=prompt, stop_phrase="###", n=n) # "\n"
        print("Output for model {}:".format(models_list[model_key]))
        for tweet in completion_request.response["choices"]:
            # tweet_words = tweet.text.split(" ")
            print("---------------------")
            print("\t{}".format(tweet.text))
            print("---------------------")

def get_prompt():
    invalid_prompt = True
    while invalid_prompt:
        query = input("Enter desired prompt --> ")
        invalid_prompt = validate_input("Desired prompt: {}".format(query))
    return query + " \n\n###\n\n"

def validate_input(query):
    user_validation = input("\n\t{}\n\tConfirm? (y/n) --> ".format(query))
    match user_validation:
        case "y":
            return False
        case "n":
            return True
        case _:
            print("\n\tInvalid response for user query validation.\n")
            validate_input(query)

def create_model():
    # get @ of twitter account
    invalid_query = True
    while invalid_query:
        query = input("Enter the @ of the account you'd like to emulate --> ")
        invalid_query = validate_input("@{}".format(query))

    user_id = get_user_id(query)

    output_path = './outputs/training-sets/user-{}-{}.jsonl'.format(query, datetime.now().strftime("%m-%d-%Y_%H-%M-%S"))
    do_not_export = True
    while do_not_export:
        # query = input(" --> ")
        # output to custom path?
        if validate_input("Output path: {}".format(output_path)):
            if validate_input("Enter custom path?"):
                print("Exiting...")
                exit()
            else:
                custom_path_check = True
                while custom_path_check:
                    custom_path = input("Enter custom path (.jsonl) --> ")
                    if validate_input(custom_path):
                        pass
                    else:
                        output_path = custom_path
                        export_training_set(output_path, user_id)
                        train_model(query, output_path)
                        custom_path_check = False
                        do_not_export = False
        else:
            export_training_set(output_path, user_id)
            train_model(query, output_path)
            do_not_export = False

def train_model(query, output_path):
    do_not_train = True
    suffix = query
    while do_not_train:
        if validate_input("Train model with suffix: {}".format(suffix)):
            if validate_input("Enter custom suffix?"):
                print("Exiting...")
                exit()
            else:
                custom_suffix_check = True
                while custom_suffix_check:
                    custom_suffix = input("Enter custom suffix --> ")
                    if validate_input(custom_suffix):
                        pass
                    else:
                        suffix = custom_suffix
                        try:
                            fine_tune_creation_request = FineTuneCreationRequest(output_path, suffix)
                            print(fine_tune_creation_request.result["message"])
                            sys.exit(1)
                        except Exception as e:
                            print("Exception occured creating fine tune request response: {}".format(e))
                            sys.exit(2)
        else:
            try:
                fine_tune_creation_request = FineTuneCreationRequest(output_path, suffix)
                print(fine_tune_creation_request.result["message"])
                sys.exit(1)
            except Exception as e:
                print("Exception occured creating fine tune request response: {}".format(e))
                sys.exit(2)

def get_user_id(query):
    # get user id
    try:
        user_lookup = UserLookup(query)
        print("\nUser Lookup Response: {}\n".format(user_lookup.response))
        user_id = json.loads(user_lookup.response)["data"][0]["id"]
        return user_id
    except Exception as e:
        print("Exception occurred parsing user lookup response: {}\n".format(e))
        exit()
    
# TODO edit twitter worker to enforce max_results to gather enough tweets to train a model
# TODO handle nonexistant path
def export_tweets(output_path, user_id):
    # get tweets
    try:
        with open(output_path, 'w') as outfile:
            tweet_lookup = TweetLookup(user_id, 100)
            outfile.write(tweet_lookup.response)
            # json.dump(tweet_lookup.response, outfile, indent=2)
            print("Successfully outputed to {}...\n".format(output_path))
            print("Response: {}".format(tweet_lookup.response))
    except Exception as e:
        print("Exception occurred exporting tweets to file: {}\n".format(e))

def export_training_set(output_path, user_id):
    x = 5
    try:
        tweet_lookup = TweetLookup(user_id, 100) # 100
        tweet_lookup_responses = [tweet_lookup.response]
        try:
            pagination_token = json.loads(tweet_lookup.response)["meta"]["next_token"]
            while x >= 0:
                new_tweet_lookup = TweetLookup(user_id, 100, pagination_token) # 100
                tweet_lookup_responses.append(new_tweet_lookup.response)
                try:
                    pagination_token = json.loads(new_tweet_lookup.response)["meta"]["next_token"]
                except Exception as e:
                    print("Exception occurred gathering tweets (assumed no next page in response - x = {}): {}\n".format(x, e))
                    break
                x -= 1
        except Exception as e:
            print("Exception occurred gathering tweets (assumed no next page in response - x = {}): {}\n".format(x, e))

    except Exception as e:
        print("Exception occurred gathering tweets: {}\n".format(e))
        exit()

    try:
        num_tweets = 0
        with jsonlines.open(output_path, 'w') as outfile:
            for response in tweet_lookup_responses:
                for tweet in json.loads(response)["data"]:
                    try: 
                        first_three_words = tweet["text"].split()[:3]
                        prompt = "{} {} {} \n\n###\n\n".format(first_three_words[0], first_three_words[1], first_three_words[2])
                        completion = " {} ###".format(tweet["text"])
                        new_jsonl_line = {"prompt": prompt, "completion": " " + completion}
                        outfile.write(new_jsonl_line)
                        num_tweets += 1
                    except:
                        continue
            print("\nSuccessfully outputed {} tweets to {}...\n".format(num_tweets, output_path))
    except Exception as e:
        print("Exception occurred exporting tweets to JSONL training set: {}\n".format(e))
        print(tweet_lookup_responses)
        exit()