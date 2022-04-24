# vibe-emulator
This program can fine-tune OpenAI models based on a user's tweets and generate tweets based on these models. This project is meant to explore the possibilities of OpenAI's API and model fine-tuning by experimenting with training data and comparing prompted outputs for different models. Check out the [twitter account documenting research progress](https://twitter.com/vibe_emulator).
## Use
1. `create_model` will lookup a user by @ on twitter and export a JSONL file composed of three word prompts and resulting tweets to be used to fine tune an OpenAI model. (intended to create a model - WIP)

2. At this point, you can use OpenAI CLI commands to create a fine-tuned model. Once the model is trained you can append it's name to the `models` dictionary in the `emulate_vibe()` and `compare_vibes()` in `project.py` as you please.

3. Once the model is trained you can use:
  - `emulate_vibe` will return `-n` tweets emulating the user whose model is associated with the key value passed with `-m` flag.

  - `compare_vibes` will return `-n` tweets tweet for each model in the object in the `models` dictionary that is associated with the key value passed by the  `-l` flag.

## Running project
First you'll need to create a .secret file emulating .secret-example with your Twitter bearer token and your OpenAI API key. You can obtain keys here:
- [Twitter API](https://developer.twitter.com/en/docs/twitter-api)
- [OpenAI API](https://openai.com/api/)

*Note: requires python3.10 and python3.10-venv*
```bash
# working dir - ./vibe-emulator
chmod +x local-env.sh
. local-env.sh

# run once to initialize project environment
v-init

vibe-emulator -h
# vibe-emulator -f <function> -n <num_responses> -m <model_name> -M <model_name_array>
#         -f <function> - str- required - function name
#                 options: ["create_model", "emulate_vibe", "compare_vibes"]
#         -n <num_responses> - int - default 1 - number of responses desired
#         -m <model_name> - str - default "theonion" - key value name for model
#         -M <model_array> - arr - default new_models - array of string model names
```
## Training Model
Prepare training file
```bash
openai tools fine_tunes.prepare_data -f <LOCAL_FILE>
```

Create a fine-tuned model
```bash
openai api fine_tunes.create -t <TRAIN_FILE_ID_OR_PATH> -m <BASE_MODEL> --suffix <SUFFIX>
# base_model options - davinci, curie, babbage, ada
# suffix is a string to append to beginning of model name

# resume event stream later if training takes a while
openai api fine_tunes.follow -i <YOUR_FINE_TUNE_JOB_ID>
```

List fine tunes
```bash
# List all created fine-tunes
openai api fine_tunes.list

# Retrieve the state of a fine-tune. The resulting object includes
# job status (which can be one of pending, running, succeeded, or failed)
# and other information
openai api fine_tunes.get -i <YOUR_FINE_TUNE_JOB_ID>

# Cancel a job
openai api fine_tunes.cancel -i <YOUR_FINE_TUNE_JOB_ID>
```

## Use a fine-tuned model
```bash
openai api completions.create -m <FINE_TUNED_MODEL> -p <YOUR_PROMPT>
```

For more useful responses try the `emulate_vibe` and `compare_vibes` functions.

## Example Outputs
[Twitter account documenting research progress](https://twitter.com/vibe_emulator)

Use example - [model comparison](./outputs/use/comparison-political-parties.txt)
```
┌──(venv)(frosty㉿DESKTOP-GLAMV3O)-[/mnt/c/Users/danny/Documents/code/openai/vibe-emulator]
└─$ v-run
----- Compare known reliable model responses -----
Enter desired prompt --> I think Republicans

        Desired prompt: I think Republicans
        Confirm? (y/n) --> y

----------

Output for model curie:ft-personal:elon-2022-04-20-17-13-57:


          I think Republicans should apologize to the American people 
----------
----------

Output for model curie:ft-personal:tuckercarlson-2022-04-21-00-47-52:

          I think Republicans are trying to keep this race out of the hands of Berniecrats. 
          They understand that if they can nominate someone who can win in FL then they won't 
          have to worry about any other state. FL will be the ceiling.
----------
----------

Output for model curie:ft-personal:jordanbpeterson-2022-04-21-01-18-02:


          I think Republicans do this because it seriously works. I understand the appeal. 
          https://t.co/u6UWN72rxJ
----------
----------

Output for model curie:ft-personal:berniesanders-2022-04-21-01-43-04:

          I think Republicans are under such heavy pressure to deliver for the American 
          people by meeting our massive public needs that they may be quite amenable to taking up some of our @JaredPolisi and @JasonHelsov filibuster-proof bill. Let's see what they have to say about it.
----------
----------

Output for model curie:ft-personal:joebiden-2022-04-21-02-34-22:

          I think Republicans believe the best way to get good legislation passed is to 
          pass the best legislation. Democrats believe the best way to get good legislation 
          passed is to pass the best legislation.
----------
----------

Output for model curie:ft-personal:drilv2-2022-04-21-02-55-13:

          I think Republicans would actually have a somewhat easy time creating a 
          national Democratic party if 
          they really wanted to
----------
----------

Output for model curie:ft-personal:dan-fred360-2022-04-21-03-43-25:

          I think Republicans should spend 2018 in observance of Matthew 25:31-46, Morpheus style. smh https://t.co/nbEDxzZ2r3
----------


┌──(venv)(frosty㉿DESKTOP-GLAMV3O)-[/mnt/c/Users/danny/Documents/code/openai/vibe-emulator]
└─$ v-run
----- Compare known reliable model responses -----
Enter desired prompt --> I think Democrats

        Desired prompt: I think Democrats
        Confirm? (y/n) --> y

----------

Output for model curie:ft-personal:elon-2022-04-20-17-13-57:

          I think Democrats should stick to the literal truth
----------
----------

Output for model curie:ft-personal:tuckercarlson-2022-04-21-00-47-52:

          I think Democrats are getting way too smart for the Republican Party. The 
          Republicans are dropping the ball because they don't recognize the long game being 
          played by Democrats.
----------
----------

Output for model curie:ft-personal:jordanbpeterson-2022-04-21-01-18-02:

          I think Democrats should be utterly unequivocal in their condemnation of such a 
          betrayal.
----------
----------

Output for model curie:ft-personal:berniesanders-2022-04-21-01-43-04:

          I think Democrats have got to face the reality that for the foreseeable future, 
          Republicans are going to have a supermajority in the House and Senate — and that means 
          they control the agenda.
----------
----------

Output for model curie:ft-personal:joebiden-2022-04-21-02-34-22:

          I think Democrats are going to be very surprised at how unified we are in 2018. 
          https://t.co/8337vCWEeP
----------
----------

Output for model curie:ft-personal:drilv2-2022-04-21-02-55-13:

          I think Democrats would do well to consider turning the NSC - otherwise known as 
          the Napoleon Complex Council - into some kind of communication tool. Like, a 
          liaison where people could go and complain that they cant figure out if they're a 
          Pilot, a Gunner, or an operator
----------
----------
Output for model curie:ft-personal:dan-fred360-2022-04-21-03-43-25:

          I think Democrats run the same generic shit ads in every single race. 
          it's time to try something new. #DemFightnight
----------
```

Use example - [create completion request](./outputs/use/bernie-bot-league-of-legends.txt)
```
┌──(venv)(frosty㉿DESKTOP-GLAMV3O)-[/mnt/c/Users/danny/Documents/code/openai/vibe-emulator]
└─$ v-run
----- Emulate curie:ft-personal:berniesanders-2022-04-21-01-43-04's Vibe -----
Enter desired prompt --> League of Legends

        Desired prompt: League of Legends
        Confirm? (y/n) --> y

Output for model curie:ft-personal:berniesanders-2022-04-21-01-43-04:
----------
          League of Legends is a global video game that brings trillions of dollars in 
          revenue to its players and developers — it's a game parents give their kids to play, 
          why in the world shouldn’t we be focusing on keeping it SF/F?
----------

----------
          League of Legends is a one-of-a-kind global video game which brings in billions of 
          dollars in revenue for Riot Games based on subscriptions, in-game purchases, ads, 
          and other means.
----------

----------
          The League of Legends World Championship is yet another event that A-list celebrities, 
          super-wealthy 
        
          Mega-Corporations &amp; big media attention use as a way to access political 
          power &amp; make a ton of money for themselves. The World Championship should be 
          viewed for what it is: A global opportunity for gamers from all 
walks
----------

----------
          League of Legends is a big deal.
----------

----------
          League of Legends is a global video game that's estimated to be watched online 
          by over 250 million people. Half of all new gross domestic product is generated by 
          the video game industry. These are earth-shattering figures that point to the fact 
          that we must end this global esports monopoly and allow US-based teams to compete.
----------
```

## Documentation
[OpenAI API Project Docs](openai.md)

## Resources:
- [OpenAI API](https://openai.com/api/)
  - [Sharing outputs policy](https://openai.com/api/policies/sharing-publication/)
- [Python Documentation](https://docs.python.org/3/)
- [Twitter API Docs](https://developer.twitter.com/en/docs)
  - [Tweets lookup](https://developer.twitter.com/en/docs/twitter-api/tweets/lookup/introduction)