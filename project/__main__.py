from workers.twitter import TweetLookup, UserLookup
from datetime import datetime
import json

def main():
    # get @ of twitter account
    invalid_query = True
    while invalid_query:
        query = input("Enter the @ of the account you'd like to emulate --> ")
        invalid_query = validate_input("@{}".format(query))

    user_id = get_user_id(query)

    output_path = './outputs/tweets/{}-tweets-for-user-id-{}.json'.format(datetime.now().strftime("%m-%d-%Y_%H-%M-%S"), user_id)
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
                    custom_path = input("Enter custom path (.json) --> ")
                    if validate_input(custom_path):
                        pass
                    else:
                        output_path = custom_path
                        export_tweets(output_path, user_id)
                        custom_path_check = False
                        do_not_export = False
        else:
            export_tweets(output_path, user_id)
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
            tweet_lookup = TweetLookup(user_id, 300)
            outfile.write(tweet_lookup.response)
            # json.dump(tweet_lookup.response, outfile, indent=2)
            print("Successfully outputed to {}...\n".format(output_path))
            print("Response: {}".format(tweet_lookup.response))
    except Exception as e:
        print("Exception occurred exporting tweets to file: {}\n".format(e))

def validate_input(query):
    user_validation = input("\n\t{}\n\tConfirm? (y/n) --> ".format(query))
    match user_validation:
        case "y":
            return False
        case "n":
            return True
        case _:
            print("\n\tInvalid response for user query validation.\n")
            validate_query(query)


if __name__ == "__main__":
    main()