from workers.twitter import TweetLookup, UserLookup

def main():
    invalid_query = True
    while invalid_query:
        query = input("Enter the @ of the account you'd like to emulate --> ")
        invalid_query = validate_query(query)

    # get user id
    try:
        user_lookup = UserLookup(query)
        # print("Response code: {}/nResponse: {}".format(user_lookup.response[0], user_lookup.response[1]))
        user_id = user_lookup.response[1][0]["data"]["id"]
        print(user_id)
    except Exception as e:
        print("Exception occurred creating user lookup response: {}".format(e))

    # get tweets
    try:
        pass
    except Exception as e:
        pass

def validate_query(query):
    user_validation = input("\n\tQuery: {}\n\tConfirm? (y/n) --> ".format(query))
    match user_validation:
        case "y":
            return False
        case "n":
            return True
        case _:
            print("\n\tInvalid response for user query validation.")
            validate_query(query)


if __name__ == "__main__":
    main()