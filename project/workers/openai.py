import os, sys, openai

class CompletionRequest:
    def __init__(self, model, prompt, stop_phrase, n=1):
        try:
            self.response = openai.Completion.create(
                model=model,
                prompt=prompt,
                max_tokens=70,
                n=n,
                stop=stop_phrase
            )
        except Exception as e:
            print("Exception occured while attempting completion request: {}".format(e))
            sys.exit(2)

class FineTuneCreationRequest:
    def __init__(self, training_file_path, suffix):
        try:
            self.response = openai.FineTune.create(
                training_file=training_file_path,
                suffix=suffix
            )
        except Exception as e:
            print("Exception occured while attempting fine tune creation request: {}".format(e))
            sys.exit(2) 


class FineTuneListRequest:
    def __init__(self):
        try:
            self.response = openai.FineTune.list()
        except Exception as e:
            print("Exception occured while attempting fine list request: {}".format(e))
            sys.exit(2)