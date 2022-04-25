from workers.twitter import TweetLookup, UserLookup, GetUserTweets
from workers.openai import CompletionRequest, FineTuneCreationRequest, FileUploadRequest
from workers.training import ThreeWordPrompt
from config import models
from datetime import datetime
import sys, json, jsonlines

default_model_name = 'theonion'

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

def create_model(query=None):
    if query is None:
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
                        new_training_set = ThreeWordPrompt(output_path, GetUserTweets(user_id).tweets)
                        train_model(query, new_training_set.path)
                        custom_path_check = False
                        do_not_export = False
        else:
            new_training_set = ThreeWordPrompt(output_path, GetUserTweets(user_id).tweets)
            train_model(query, new_training_set.path)
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
                            file_upload_request = FileUploadRequest(output_path)
                            fine_tune_creation_request = FineTuneCreationRequest(file_upload_request.file_id, suffix)
                            print(fine_tune_creation_request.request["message"])
                            sys.exit(1)
                        except Exception as e:
                            print("Exception occured creating fine tune request response: {}".format(e))
                            sys.exit(2)
        else:
            try:
                file_upload_request = FileUploadRequest(output_path)
                fine_tune_creation_request = FineTuneCreationRequest(file_upload_request.file_id, suffix)
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