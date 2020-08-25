"""Code to automatically generate trials for norming study."""

import itertools
import json

import pandas as pd 


### PATHS
DATA_PATH = "data/stims/stimuli.csv"
SAVE_PATH = "experiment/experiment_text.html"

LABELS = ['totally unrelated', 'not very related', 'related', 'same meaning']
PROMPT = "<p>How <b>related</b> are the uses of this word across these two sentences?<p>"
VERSIONS = ['M1_a', 'M1_b', 'M2_a', 'M2_b']


### Read in stims
df_stims = pd.read_csv(DATA_PATH)
### Filter to critical
df_targets = df_stims[~df_stims['M1_b'].isna()]
df_targets = df_targets.reset_index()

doc = ''


"""
DOC: 
This code:
- iterates through each row of the .csv file, then finds all the pairings
of sentences for a given word (6 pairings, 12 total for each order).
- builds a jsPsych trial for each comparison 
- for each word, adds each jsPsych trial to a list corresponding to the possible 12 trials
for that word (m1_ab, m1_ba, ...). call these lists "w_1_trials", "w_2_trials", etc.
- creates an "all_trials" list corresponding to each of these lists, i.e., [w_1_trials, w_2_trials ,...]

Later, in jsPsych, we randomly sample from each of those lists, such that we end up with N (#words)
trials, one for each word. Over many subjects, this should correspond to a roughly even distribution
of each version per word.

"""

## TODO: Redo this so it's more elegantly composed (use itertools.permutations)

for index, row in df_targets.iterrows():

	trials = []
	target_word = row['String']

	for v1, v2 in itertools.permutations(VERSIONS, 2):

		version = '{v1}_{v2}'.format(v1=v1, v2=v2)
		same = v1[0:2] == v2[0:2]

		struct = {
		'type': 'html-slider-response',
		'stimulus': '{ex1}<p>{ex2}'.format(ex1=row[v1], ex2=row[v2]).replace(target_word, "<b>{t}</b>".format(t=target_word)),
		'labels': LABELS,
		'prompt': PROMPT,
		'data': {'word': row['Word'], 'same': same, 'version': version, 'item': index, 
				 'source': row['Source'], 'Class': row['Class'], 
				 'overlap': row['Original Condition']}
		}

		trials.append(struct)


	doc += 'var w_{i}_trials = '.format(i=index) + json.dumps(trials, indent=4) + "\n\n"


### Now create multidimensional array of trials
### TODO: This adds each variable name as a string...we want to add it as a variable
multi_array = []
for i in range(len(df_targets)):
	multi_array.append('w_{i}_trials'.format(i=i))

doc += 'all_trials = ' + json.dumps(multi_array, indent=4) + "\n\n"

	

with open(SAVE_PATH, "w") as f:
 	f.write(doc)

