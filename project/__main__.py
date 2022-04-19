from workers.twitter import TweetLookup, UserLookup

def main():
    invalid_query = True
    while invalid_query:
        query = input("Enter the @ of the account you'd like to emulate --> ")
        invalid_query = validate_query(query)

    try:
        user_lookup_response = UserLookup(query)
        print("Response code: {}/nResponse: {}".format(user_lookup_response[0], user_lookup_response[1]))
    except Exception as e:
        print("Exception occurred creating user lookup response: {}".format(e))

    try:
        pass
    except Exception as e:
        pass

def validate_query(query):
    user_validation = input("\n\tQuery: {}\n\tConfirm? (y/n) --> ").format(query)
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