import jsonlines

class ThreeWordPrompt:
    def __init__(self, output_path, tweets):
        num_tweets = 0
        with jsonlines.open(output_path, 'w') as training_file:
            for tweet in tweets:
                try: 
                    first_three_words = tweet["text"].split()[:3]
                    prompt = "{} {} {} \n\n###\n\n".format(first_three_words[0], first_three_words[1], first_three_words[2])
                    completion = " {} ###".format(tweet["text"])
                    new_jsonl_line = {"prompt": prompt, "completion": " " + completion}
                    training_file.write(new_jsonl_line)
                    num_tweets += 1
                except:
                    continue # less than three words
        self.path = output_path