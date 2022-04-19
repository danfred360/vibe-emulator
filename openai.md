# openapi
collection of useful stuff from the docs

# endpoints
## completions
create completion
```python
POST https://api.openai.com/v1/engines/{engine_id}/completions
```

Path parameters
engine_id
string
Required
The ID of the engine to use for this request

```python
import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.Completion.create(
  engine="text-davinci-002",
  prompt="Say this is a test",
  max_tokens=5
)

# parameters
{
  "prompt": "Say this is a test",
  "suffix": "-- this comes after -- davinci",
  "max_tokens": 5, # davinci max - 4096, all other models max - 2048 tokens
  "temperature": 1, # sampling temp - higher values mean the model will take more risks (more creative)
  "top_p": 1, # alternative to sampling with temp - nucleus sampling
  "n": 1, # number of results to generate for each prompt
  "stream": false, # option to stream back partial progress
  "echo": false, # echo back prompt in addition to completion, default false
  "presence_penalty": 0, # default 0, -2 < x > 2, pos. values penalize new tokens based on whether they appear in the text so far - increase likelihood to talk about new topics
  "frequence_penalty": 0, # default 0, -2 < x > 2, pos. values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat tge same line verbatim
  "logprobs": null,
  "stop": "\n"
}

# response
{
  "id": "cmpl-uqkvlQyYK7bGYrRHQ0eXlWi7",
  "object": "text_completion",
  "created": 1589478378,
  "model": "text-davinci-002",
  "choices": [
    {
      "text": "\n\nThis is a test",
      "index": 0,
      "logprobs": null,
      "finish_reason": "length"
    }
  ]
}

```

## classifications
create classification
```python
POST https://api.openai.com/v1/classifications

import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.Classification.create(
  search_model="ada",
  model="curie",
  examples=[
    ["A happy moment", "Positive"],
    ["I am sad.", "Negative"],
    ["I am feeling awesome", "Positive"]
  ],
  query="It is a raining day :(",
  labels=["Positive", "Negative", "Neutral"],
)

# parameters
{
  "examples": [
    ["A happy moment", "Positive"],
    ["I am sad.", "Negative"],
    ["I am feeling awesome", "Positive"]
  ],
  "labels": ["Positive", "Negative", "Neutral"],
  "query": "It is a raining day :(",
  "search_model": "ada",
  "model": "curie"
}

# response
{
  "completion": "cmpl-2euN7lUVZ0d4RKbQqRV79IiiE6M1f",
  "label": "Negative",
  "model": "curie:2020-05-03",
  "object": "classification",
  "search_model": "ada",
  "selected_examples": [
    {
      "document": 1,
      "label": "Negative",
      "text": "I am sad."
    },
    {
      "document": 0,
      "label": "Positive",
      "text": "A happy moment"
    },
    {
      "document": 2,
      "label": "Positive",
      "text": "I am feeling awesome"
    }
  ]
}
```

## answers
create answer
```python
POST https://api.openai.com/v1/answers

import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.Answer.create(
  search_model="ada",
  model="curie",
  question="which puppy is happy?",
  documents=["Puppy A is happy.", "Puppy B is sad."],
  examples_context="In 2017, U.S. life expectancy was 78.6 years.",
  examples=[["What is human life expectancy in the United States?","78 years."]],
  max_tokens=5,
  stop=["\n", "<|endoftext|>"],
)

# parameters
{
  "documents": ["Puppy A is happy.", "Puppy B is sad."],
  "question": "which puppy is happy?",
  "search_model": "ada",
  "model": "curie",
  "examples_context": "In 2017, U.S. life expectancy was 78.6 years.",
  "examples": [["What is human life expectancy in the United States?","78 years."]],
  "max_tokens": 5,
  "stop": ["\n", "<|endoftext|>"]
}

# response
{
  "answers": [
    "puppy A."
  ],
  "completion": "cmpl-2euVa1kmKUuLpSX600M41125Mo9NI",
  "model": "curie:2020-05-03",
  "object": "answer",
  "search_model": "ada",
  "selected_documents": [
    {
      "document": 0,
      "text": "Puppy A is happy. "
    },
    {
      "document": 1,
      "text": "Puppy B is sad. "
    }
  ]
}
```

## files
files are used to upload documents that can be used accross features like Answers, Search, and Classifications

list files
```python
GET https://api.openai.com/v1/files

import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.File.list()

# response
{
  "data": [
    {
      "id": "file-ccdDZrC3iZVNiQVeEA6Z66wf",
      "object": "file",
      "bytes": 175,
      "created_at": 1613677385,
      "filename": "train.jsonl",
      "purpose": "search"
    },
    {
      "id": "file-XjGxS3KTG0uNmNOK362iJua3",
      "object": "file",
      "bytes": 140,
      "created_at": 1613779121,
      "filename": "puppy.jsonl",
      "purpose": "search"
    }
  ],
  "object": "list"
}
```

upload file

```python
POST https://api.openai.com/v1/files

import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.File.create(
  file=open("puppy.jsonl"),
  purpose='answers'
)

# response
{
  "id": "file-XjGxS3KTG0uNmNOK362iJua3",
  "object": "file",
  "bytes": 140,
  "created_at": 1613779121,
  "filename": "puppy.jsonl",
  "purpose": "answers"
}
```

delete file
```python
DELETE https://api.openai.com/v1/files/{file_id}

import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.File.delete("file-XjGxS3KTG0uNmNOK362iJua3")

# response
{
  "id": "file-XjGxS3KTG0uNmNOK362iJua3",
  "object": "file",
  "deleted": true
}
```

retrieve file
```python
GET https://api.openai.com/v1/files/{file_id}

import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.File.retrieve("file-XjGxS3KTG0uNmNOK362iJua3")

# response
{
  "id": "file-XjGxS3KTG0uNmNOK362iJua3",
  "object": "file",
  "bytes": 140,
  "created_at": 1613779657,
  "filename": "puppy.jsonl",
  "purpose": "answers"
}
```

retrieve file content
```python
GET https://api.openai.com/v1/files/{file_id}/content

import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")
content = openai.File.download("file-XjGxS3KTG0uNmNOK362iJua3")

```
## fine tuning a model
Training data must be a [JSONL](https://jsonlines.org/) document
```python
{"prompt": "<prompt text>", "completion": "<ideal generated text>"}
{"prompt": "<prompt text>", "completion": "<ideal generated text>"}
{"prompt": "<prompt text>", "completion": "<ideal generated text>"}
...
```

Use CLI tool fo validate, give suggestions, and reformat your data:
```bash
openai tools fine_tunes.prepare_data -f <LOCAL_FILE>
```

To create a fine tuned model:
*Note: Models may only be created using CLI tool. All other operations may be preformed using python. Or not??*
python
```python
import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.FineTune.create(training_file="file-XGinujblHPwGLSztz8cPS8XY")

# response
{
  "id": "ft-AF1WoRqd3aJAHsqc9NY7iL8F",
  "object": "fine-tune",
  "model": "curie",
  "created_at": 1614807352,
  "events": [
    {
      "object": "fine-tune-event",
      "created_at": 1614807352,
      "level": "info",
      "message": "Job enqueued. Waiting for jobs ahead to complete. Queue number: 0."
    }
  ],
  "fine_tuned_model": null,
  "hyperparams": {
    "batch_size": 4,
    "learning_rate_multiplier": 0.1,
    "n_epochs": 4,
    "prompt_loss_weight": 0.1,
  },
  "organization_id": "org-...",
  "result_files": [],
  "status": "pending",
  "validation_files": [],
  "training_files": [
    {
      "id": "file-XGinujblHPwGLSztz8cPS8XY",
      "object": "file",
      "bytes": 1547276,
      "created_at": 1610062281,
      "filename": "my-data-train.jsonl",
      "purpose": "fine-tune-train"
    }
  ],
  "updated_at": 1614807352,
}

# list fine tunes
import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.FineTune.list()

# response
{
  "object": "list",
  "data": [
    {
      "id": "ft-AF1WoRqd3aJAHsqc9NY7iL8F",
      "object": "fine-tune",
      "model": "curie",
      "created_at": 1614807352,
      "fine_tuned_model": null,
      "hyperparams": { ... },
      "organization_id": "org-...",
      "result_files": [],
      "status": "pending",
      "validation_files": [],
      "training_files": [ { ... } ],
      "updated_at": 1614807352,
    },
    { ... },
    { ... }
  ]
}

# get fine tune
import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.FineTune.retrieve(id="ft-AF1WoRqd3aJAHsqc9NY7iL8F")

# response
{
  "id": "ft-AF1WoRqd3aJAHsqc9NY7iL8F",
  "object": "fine-tune",
  "model": "curie",
  "created_at": 1614807352,
  "events": [
    {
      "object": "fine-tune-event",
      "created_at": 1614807352,
      "level": "info",
      "message": "Job enqueued. Waiting for jobs ahead to complete. Queue number: 0."
    },
    {
      "object": "fine-tune-event",
      "created_at": 1614807356,
      "level": "info",
      "message": "Job started."
    },
    {
      "object": "fine-tune-event",
      "created_at": 1614807861,
      "level": "info",
      "message": "Uploaded snapshot: curie:ft-acmeco-2021-03-03-21-44-20."
    },
    {
      "object": "fine-tune-event",
      "created_at": 1614807864,
      "level": "info",
      "message": "Uploaded result files: file-QQm6ZpqdNwAaVC3aSz5sWwLT."
    },
    {
      "object": "fine-tune-event",
      "created_at": 1614807864,
      "level": "info",
      "message": "Job succeeded."
    }
  ],
  "fine_tuned_model": "curie:ft-acmeco-2021-03-03-21-44-20",
  "hyperparams": {
    "batch_size": 4,
    "learning_rate_multiplier": 0.1,
    "n_epochs": 4,
    "prompt_loss_weight": 0.1,
  },
  "organization_id": "org-...",
  "result_files": [
    {
      "id": "file-QQm6ZpqdNwAaVC3aSz5sWwLT",
      "object": "file",
      "bytes": 81509,
      "created_at": 1614807863,
      "filename": "compiled_results.csv",
      "purpose": "fine-tune-results"
    }
  ],
  "status": "succeeded",
  "validation_files": [],
  "training_files": [
    {
      "id": "file-XGinujblHPwGLSztz8cPS8XY",
      "object": "file",
      "bytes": 1547276,
      "created_at": 1610062281,
      "filename": "my-data-train.jsonl",
      "purpose": "fine-tune-train"
    }
  ],
  "updated_at": 1614807865,
}
```

bash
```bash
openai api fine_tunes.create -t <TRAIN_FILE_ID_OR_PATH> -m <BASE_MODEL> # ada, babbage, curie, or davinci

# to resume event stream in cli (training can take a while)
openai api fine_tunes.follow -i <YOUR_FINE_TUNE_JOB_ID>

# List all created fine-tunes
openai api fine_tunes.list

# Retrieve the state of a fine-tune. The resulting object includes
# job status (which can be one of pending, running, succeeded, or failed)
# and other information
openai api fine_tunes.get -i <YOUR_FINE_TUNE_JOB_ID>

# Cancel a job
openai api fine_tunes.cancel -i <YOUR_FINE_TUNE_JOB_ID>
```
The documentation recommends providing "at least a few hundred hihg-quality examples." - [Source](https://beta.openai.com/docs/guides/fine-tuning/general-best-practices)
[Customize model name documentation](https://beta.openai.com/docs/guides/fine-tuning/customize-your-model-name)

To use fine tuned model (example using completions endpoint):
bash
```bash
openai api completions.create -m <FINE_TUNED_MODEL> -p <YOUR_PROMPT>
```
python
```python
import openai
openai.Completion.create(
    model=FINE_TUNED_MODEL,
    prompt=YOUR_PROMPT)
```

delete a fine-tuned model
bash
```bash
openai api models.delete -i <FINE_TUNED_MODEL>
```

python
```python
import openai
openai.Model.delete(FINE_TUNED_MODEL)
```
- [fine tuning docs](https://beta.openai.com/docs/guides/fine-tuning)

# reference links
- [documentation](https://beta.openai.com/docs/api-reference/completions/create?lang=python)
- [openai models breakdown](https://beta.openai.com/docs/engines/overview)
- [model comparison tool](https://gpttools.com/comparisontool)
- [openapi usage page](https://beta.openai.com/account/usage)
- [application review guidlines](https://beta.openai.com/docs/usage-guidelines/app-review)