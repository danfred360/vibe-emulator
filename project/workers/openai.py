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

class FileUploadRequest:
    def __init__(self, training_file_path):
        try:
            self.response = openai.File.create(
                file=open(training_file_path),
                purpose='completion'
            )
        except Exception as e:
            print("Exception occured uploading training file: {}".format(e))
        self.file_id = self.response["id"]

class FineTuneCreationRequest:
    def __init__(self, training_file_id, suffix):
        try:
            self.response = openai.FineTune.create(
                training_file=training_file_id,
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