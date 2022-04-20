from workers.twitter import TweetLookup, UserLookup
from datetime import datetime
import json, jsonlines

def main():
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
        if validate_input(output_path):
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
                        custom_path_check = False
                        do_not_export = False
        else:
            export_training_set(output_path, user_id)
            do_not_export = False

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
        pagination_token = json.loads(tweet_lookup.response)["meta"]["next_token"]

        while x >= 0:
            new_tweet_lookup = TweetLookup(user_id, 100, pagination_token) # 100
            tweet_lookup_responses.append(new_tweet_lookup.response)
            pagination_token = json.loads(new_tweet_lookup.response)["meta"]["next_token"]
            x -= 1

    except Exception as e:
        print("Exception occurred gathering tweets: {}\n".format(e))
        exit()

    try:
        with jsonlines.open(output_path, 'w') as outfile:
            for response in tweet_lookup_responses:
                for tweet in json.loads(response)["data"]:
                    prompt = ""
                    for word in tweet["text"].split()[:3]:
                        prompt += " " + word
                    new_jsonl_line = {"prompt": prompt, "completion": " " + tweet["text"] + " END"}
                    outfile.write(new_jsonl_line)
            print("\nSuccessfully outputed to {}...\n".format(output_path))
    except Exception as e:
        print("Exception occurred exporting tweets to JSONL trianing set: {}\n".format(e))
        exit()

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


if __name__ == "__main__":
    main()