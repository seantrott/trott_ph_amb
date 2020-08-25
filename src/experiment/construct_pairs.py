"""Code to automatically generate stims."""

import json
import pandas as pd 


### PATHS
DATA_PATH = "data/stims/stimuli.csv"
SAVE_PATH = "experiment/experiment_text.html"

LABELS = ['totally unrelated', 'not very related', 'related', 'same meaning']
PROMPT = "<p>How <b>related</b> are the uses of this word across these two sentences?<p>"


### Read in stims
df_stims = pd.read_csv(DATA_PATH)
### Filter to critical
df_targets = df_stims[~df_stims['M1_b'].isna()]
df_targets = df_targets.reset_index()

doc = ''

# timeline = []


### Conditions we need
## same: 
##### m1a --> m1b
##### m1b --> m1a
##### m2a --> m2b
##### m2b --> m2a
## not same:
##### m1a --> m2a
##### m2a --> m1a
##### m1a --> m2b
##### m2b --> m1a
##### m1b --> m2a
##### m2a --> m1b
##### m1b --> m2b
##### m2b --> m1b





## Counterbalanced lists: distribute these orderings across different lists

trial_names = ['m1_ab', 'm1_ba',
			   'm2_ab', 'm2_ba',
			   'm1a_m2a', 'm2a_m1a',
			   'm1a_m2b', 'm1a_m2b',
			   'm1b_m2a', 'm2a_m1b',
			   'm1b_m2b', 'm2b_m1b']


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

for index, row in df_targets.iterrows():

	trials = []

	target_word = row['String']

	struct = {
	'type': 'html-slider-response',
	'stimulus': '{ex1}<p>{ex2}'.format(ex1=row['M1_a'], ex2=row['M1_b']).replace(target_word, "<b>{t}</b>".format(t=target_word)),
	'labels': LABELS,
	'prompt': PROMPT,
	'data': {'word': row['Word'], 'same': 'yes', 'version': 'm1_ab', 'item': index, 'source': row['Source'], 'Class': row['Class'], 'overlap': row['Original Condition']}
	}

	# doc += 'var w_{i}_m1_ab = '.format(i=index) + json.dumps(struct, indent=4) + "\n\n"
	trials.append(struct)

	struct = {
	'type': 'html-slider-response',
	'stimulus': '{ex1}<p>{ex2}'.format(ex1=row['M1_b'], ex2=row['M1_a']).replace(target_word, "<b>{t}</b>".format(t=target_word)),
	'labels': LABELS,
	'prompt': PROMPT,
	'data': {'word': row['Word'], 'same': 'yes', 'version': 'm1_ba', 'item': index, 'source': row['Source'], 'Class': row['Class'], 'overlap': row['Original Condition']}
	}

	# doc += 'var w_{i}_m1_ba = '.format(i=index) + json.dumps(struct, indent=4) + "\n\n"
	trials.append(struct)

	struct = {
	'type': 'html-slider-response',
	'stimulus': '{ex1}<p>{ex2}'.format(ex1=row['M2_a'], ex2=row['M2_b']).replace(target_word, "<b>{t}</b>".format(t=target_word)),
	'labels': LABELS,
	'prompt': PROMPT,
	'data': {'word': row['Word'], 'version': 'm2_ab', 'same': 'yes', 'item': index, 'source': row['Source'], 'Class': row['Class'], 'overlap': row['Original Condition']}
	}

	# doc += 'var w_{i}_m2_ab = '.format(i=index) + json.dumps(struct, indent=4) + "\n\n"
	trials.append(struct)


	struct = {
	'type': 'html-slider-response',
	'stimulus': '{ex1}<p>{ex2}'.format(ex1=row['M2_b'], ex2=row['M2_a']).replace(target_word, "<b>{t}</b>".format(t=target_word)),
	'labels': LABELS,
	'prompt': PROMPT,
	'data': {'word': row['Word'], 'version': 'm2_ba', 'same': 'yes', 'item': index, 'source': row['Source'], 'Class': row['Class'], 'overlap': row['Original Condition']}
	}

	# doc += 'var w_{i}_m2_ba = '.format(i=index) + json.dumps(struct, indent=4) + "\n\n"
	trials.append(struct)


	struct = {
	'type': 'html-slider-response',
	'stimulus': '{ex1}<p>{ex2}'.format(ex1=row['M1_a'], ex2=row['M2_a']).replace(target_word, "<b>{t}</b>".format(t=target_word)),
	'labels': LABELS,
	'prompt': PROMPT,
	'data': {'word': row['Word'], 'version': 'm1a_m2a', 'same': 'no', 'item': index, 'source': row['Source'],'Class': row['Class'],   'overlap': row['Original Condition']}
	}

	# doc += 'var w_{i}_m1a_m2a = '.format(i=index) + json.dumps(struct, indent=4) + "\n\n"
	trials.append(struct)

	struct = {
	'type': 'html-slider-response',
	'stimulus': '{ex1}<p>{ex2}'.format(ex1=row['M2_a'], ex2=row['M1_a']).replace(target_word, "<b>{t}</b>".format(t=target_word)),
	'labels': LABELS,
	'prompt': PROMPT,
	'data': {'word': row['Word'], 'version': 'm2a_m1a', 'same': 'no', 'item': index, 'source': row['Source'],'Class': row['Class'],   'overlap': row['Original Condition']}
	}

	# doc += 'var w_{i}_m2a_m1a = '.format(i=index) + json.dumps(struct, indent=4) + "\n\n"
	trials.append(struct)



	struct = {
	'type': 'html-slider-response',
	'stimulus': '{ex1}<p>{ex2}'.format(ex1=row['M1_a'], ex2=row['M2_b']).replace(target_word, "<b>{t}</b>".format(t=target_word)),
	'labels': LABELS,
	'prompt': PROMPT,
	'data': {'word': row['Word'], 'version': 'm1a_m2b', 'same': 'no', 'item': index, 'source': row['Source'], 'Class': row['Class'],  'overlap': row['Original Condition']}
	}

	# doc += 'var w_{i}_m1a_m2b = '.format(i=index) + json.dumps(struct, indent=4) + "\n\n"
	trials.append(struct)

	struct = {
	'type': 'html-slider-response',
	'stimulus': '{ex1}<p>{ex2}'.format(ex1=row['M2_b'], ex2=row['M1_a']).replace(target_word, "<b>{t}</b>".format(t=target_word)),
	'labels': LABELS,
	'prompt': PROMPT,
	'data': {'word': row['Word'], 'version': 'm2b_m1a', 'same': 'no', 'item': index, 'source': row['Source'], 'Class': row['Class'],  'overlap': row['Original Condition']}
	}

	# doc += 'var w_{i}_m2b_m1a = '.format(i=index) + json.dumps(struct, indent=4) + "\n\n"
	trials.append(struct)


	struct = {
	'type': 'html-slider-response',
	'stimulus': '{ex1}<p>{ex2}'.format(ex1=row['M1_b'], ex2=row['M2_a']).replace(target_word, "<b>{t}</b>".format(t=target_word)),
	'labels': LABELS,
	'prompt': PROMPT,
	'data': {'word': row['Word'], 'version': 'm1b_m2a', 'same': 'no', 'item': index, 'source': row['Source'],'Class': row['Class'],  'overlap': row['Original Condition']}
	}

	# doc += 'var w_{i}_m1b_m2a = '.format(i=index) + json.dumps(struct, indent=4) + "\n\n"
	trials.append(struct)

	struct = {
	'type': 'html-slider-response',
	'stimulus': '{ex1}<p>{ex2}'.format(ex1=row['M2_a'], ex2=row['M1_b']).replace(target_word, "<b>{t}</b>".format(t=target_word)),
	'labels': LABELS,
	'prompt': PROMPT,
	'data': {'word': row['Word'], 'version': 'm2a_m1b', 'same': 'no', 'item': index, 'source': row['Source'],'Class': row['Class'],  'overlap': row['Original Condition']}
	}

	# doc += 'var w_{i}_m2a_m1b = '.format(i=index) + json.dumps(struct, indent=4) + "\n\n"
	trials.append(struct)

	struct = {
	'type': 'html-slider-response',
	'stimulus': '{ex1}<p>{ex2}'.format(ex1=row['M1_b'], ex2=row['M2_b']).replace(target_word, "<b>{t}</b>".format(t=target_word)),
	'labels': LABELS,
	'prompt': PROMPT,
	'data': {'word': row['Word'], 'version': 'm1b_m2b', 'same': 'no', 'item': index, 'source': row['Source'], 'Class': row['Class'], 'overlap': row['Original Condition']}
	}

	# doc += 'var w_{i}_m1b_m2b = '.format(i=index) + json.dumps(struct, indent=4) + "\n\n"
	trials.append(struct)

	struct = {
	'type': 'html-slider-response',
	'stimulus': '{ex1}<p>{ex2}'.format(ex1=row['M2_b'], ex2=row['M1_b']).replace(target_word, "<b>{t}</b>".format(t=target_word)),
	'labels': LABELS,
	'prompt': PROMPT,
	'data': {'word': row['Word'], 'version': 'm2b_m1b', 'same': 'no', 'item': index, 'source': row['Source'], 'Class': row['Class'], 'overlap': row['Original Condition']}
	}

	# doc += 'var w_{i}_m2b_m1b = '.format(i=index) + json.dumps(struct, indent=4) + "\n\n"
	trials.append(struct)




	doc += 'var w_{i}_trials = '.format(i=index) + json.dumps(trials, indent=4) + "\n\n"
	# doc += 'var w_{i}_trials = '.format(i=index) + str(trials) + "\n\n"




### Now create multidimensional array of trials
### TODO: This adds each variable name as a string...we want to add it as a variable
multi_array = []
for i in range(len(df_targets)):
	multi_array.append('w_{i}_trials'.format(i=i))

doc += 'all_trials = ' + json.dumps(multi_array, indent=4) + "\n\n"

	

with open(SAVE_PATH, "w") as f:
 	f.write(doc)

