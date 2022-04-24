import sqlite3

models = {
        "default" : {
            'dril': 'curie:ft-personal:drilv3-2022-04-22-12-26-53',
            'tuckercarlson': 'curie:ft-personal:tuckercarlsonv2-2022-04-22-12-39-43',
            'berniesanders' : 'curie:ft-personal:berniesandersv2-2022-04-22-18-11-20',
            'sensanders' : 'curie:ft-personal:sensanders-2022-04-23-00-28-29',
            'elonmusk' : 'curie:ft-personal:elonv2-2022-04-22-16-44-32',
            'denzelcurry' : 'curie:ft-personal:denzelcurry-2022-04-23-00-03-44',
            'johndiesattheen' : 'curie:ft-personal:johndiesattheen-2022-04-23-00-35-19',
            'mkv-riscy' : 'curie:ft-personal:mkvriscy-2022-04-22-18-43-22',
            'wheezywaiter': 'curie:ft-personal:wheezywaiter-2022-04-23-03-48-03'
        }, # stop="###"
        "old" : {
            'justin-t' : 'curie:ft-personal-2022-04-20-14-53-01',
            'dril-old': 'curie:ft-personal:dril-2022-04-20-15-42-28',
            'elon': 'curie:ft-personal:elon-2022-04-20-17-13-57',
            'libsoftiktok' : 'curie:ft-personal:libsoftiktok-2022-04-20-17-49-25',
            'dojacat' : 'curie:ft-personal:dojacat-2022-04-20-22-06-20',
            'tuckercarlson' : 'curie:ft-personal:tuckercarlson-2022-04-21-00-47-52',
            'h3h3' : 'curie:ft-personal:h3h3productions-2022-04-21-01-06-50',
            'jordanbpeterson' : 'curie:ft-personal:jordanbpeterson-2022-04-21-01-18-02',
            'berniesanders' : 'curie:ft-personal:berniesanders-2022-04-21-01-43-04',
            'joebiden' : 'curie:ft-personal:joebiden-2022-04-21-02-34-22',
            'drilv2' : 'curie:ft-personal:drilv2-2022-04-21-02-55-13',
            'keemstar' : 'curie:ft-personal:keemstar-2022-04-21-03-11-19',
            'kanyewest' : 'curie:ft-personal:kanyewest-2022-04-21-03-31-32',
            'ggreenwald' : 'curie:ft-personal:ggreenwald-2022-04-21-04-20-24',
            'comicdavesmith' : 'curie:ft-personal:comicdavesmith-2022-04-21-04-06-10',
            'bts-twt' : 'curie:ft-personal:bts-twt-2022-04-21-18-36-39',
            'keyon' : 'curie:ft-personal:keyon-2022-04-21-18-47-47',
            'danfred360' : 'curie:ft-personal:dan-fred360-2022-04-21-03-43-25'
        }, # stop="\n"
        "frens" : {
            'GenisWon' : 'curie:ft-personal:geniswon-2022-04-21-19-34-24',
            'fearofsalt' : 'curie:ft-personal:fearofsalt-2022-04-21-20-17-17'
        },
        "sanders" : {
            'berniesanders' : 'curie:ft-personal:berniesandersv2-2022-04-22-18-11-20',
            'sensanders' : 'curie:ft-personal:sensanders-2022-04-23-00-28-29'
        },
        "political" : {
            'tuckercarlson': 'curie:ft-personal:tuckercarlsonv2-2022-04-22-12-39-43',
            'berniesanders' : 'curie:ft-personal:berniesandersv2-2022-04-22-18-11-20',
            'sensanders' : 'curie:ft-personal:sensanders-2022-04-23-00-28-29',
        },
        "fun" : {
            'tuckercarlson': 'curie:ft-personal:tuckercarlsonv2-2022-04-22-12-39-43',
            'johndiesattheen' : 'curie:ft-personal:johndiesattheen-2022-04-23-00-35-19'
        },
        "more" : {
            'theonion': 'curie:ft-personal:theonion-2022-04-21-19-19-28',
            'danpriceseattle' : 'curie:ft-personal:danpriceseattle-2022-04-22-01-11-11',
            'dril': 'curie:ft-personal:drilv3-2022-04-22-12-26-53',
            'tuckercarlson': 'curie:ft-personal:tuckercarlsonv2-2022-04-22-12-39-43',
            'elonmusk' : 'curie:ft-personal:elonv2-2022-04-22-16-44-32',
            'berniesanders' : 'curie:ft-personal:berniesandersv2-2022-04-22-18-11-20'
        }
    }

# con = sqlite3.connect('sqlite/db/vibe-emulator.db')
# db = con.cursor()