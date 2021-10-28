"""Construct modified contextualized sensorimotor experiment.

Central goal: present a subset of items to participants, focusing on
those that haven't been observed as many times.

Thus, create several lists:
- sentences with <10 perceptual norms
- sentences with <10 action norms
- sentences with >75% perceptual norms (15)
- sentences with >75% action norms (15)

Then, in JsPsych, we will sample as follows:
-- 26 low-N items
-- 26 high-N items

(That way, we can still assess those new subjects on the basis of their agreement
with high-N items.)
"""

import json

import pandas as pd 
from collections import Counter


# ITEM_PATH
ITEM_PATH = "data/processed/contextualized_sensorimotor_norms.csv"
OG_PATH = "data/stims/stimuli.csv"
SAVE_PATH = "experiment/sensorimotor2_text.html"

# CUTOFFS
CUTOFF_P = 14
CUTOFF_A = 18

# Read in file
df_items = pd.read_csv(ITEM_PATH)
df_og = pd.read_csv(OG_PATH)[['Word', 'String']]
df_og['word'] = df_og['Word']
df_merged = pd.merge(df_items, df_og)

# Create perceptual vs. action frames

print("\n Now compiling perception words")
df_perceptual = df_merged[(df_merged['count_perceptual']>CUTOFF_P)|(df_merged['count_perceptual']<10)]
### Remove high-N words that also appear in low-N 
low_N_perceptual = df_perceptual[df_perceptual['count_perceptual']<10]['word'].values
high_N_perceptual = df_perceptual[df_perceptual['count_perceptual']>CUTOFF_P]['word'].values
print("{X} low-N words.".format(X=len(low_N_perceptual)))
print("{X} high-N words before filtering.".format(X=len(high_N_perceptual)))
df_perceptual = df_perceptual[(df_perceptual['count_perceptual']<10)|(~df_perceptual['word'].isin(low_N_perceptual))]
low_N_perceptual = df_perceptual[df_perceptual['count_perceptual']<10]['word'].values
high_N_perceptual = df_perceptual[df_perceptual['count_perceptual']>CUTOFF_P]['word'].values
print("{X} low-N words.".format(X=len(low_N_perceptual)))
print("{X} high-N words after filtering.".format(X=len(high_N_perceptual)))

## Remove duplicate high-N words
counts = Counter(high_N_perceptual)
high_N_keep = [w for w in counts.keys() if counts[w] == 1]
df_perceptual = df_perceptual[(df_perceptual['count_perceptual']<10)|(df_perceptual['word'].isin(high_N_keep))]
low_N_perceptual = df_perceptual[df_perceptual['count_perceptual']<10]['word'].values
high_N_perceptual = df_perceptual[df_perceptual['count_perceptual']>CUTOFF_P]['word'].values
print("{X} low-N words.".format(X=len(low_N_perceptual)))
print("{X} high-N words after filtering repeats.".format(X=len(high_N_perceptual)))

print("\n Now compiling action words")
### Remove high-N words that also appear in low-N 
df_action = df_merged[(df_merged['count_action']>CUTOFF_A)|(df_merged['count_action']<12)]
low_N_action = df_action[df_action['count_action']<12]['word'].values
high_N_action = df_action[df_action['count_action']>CUTOFF_A]['word'].values
print("{X} low-N words.".format(X=len(low_N_action)))
print("{X} high-N words before filtering.".format(X=len(high_N_action)))
df_action = df_action[(df_action['count_action']<12)|(~df_action['word'].isin(low_N_action))]
df_action = df_action[(df_action['count_action']<12)|(~df_action['word'].isin(low_N_action))]
low_N_action = df_action[df_action['count_action']<12]['word'].values
high_N_action = df_action[df_action['count_action']>CUTOFF_A]['word'].values
print("{X} low-N words.".format(X=len(low_N_action)))
print("{X} high-N words after filtering.".format(X=len(high_N_action)))

## Remove duplicate high-N words
counts = Counter(high_N_action)
high_N_keep = [w for w in counts.keys() if counts[w] == 1]
df_action = df_action[(df_action['count_action']<12)|(df_action['word'].isin(high_N_keep))]
low_N_action = df_action[df_action['count_action']<12]['word'].values
high_N_action = df_action[df_action['count_action']>CUTOFF_P]['word'].values
print("{X} low-N words.".format(X=len(low_N_action)))
print("{X} high-N words after filtering repeats.".format(X=len(high_N_action)))

print(len(df_action))

### Set up output
doc = ''

# Create perception trials
low_N_p = []
high_N_p = []
### TODO: Separate by word? Or do in JsPsych?
for index, row in df_perceptual.iterrows():

	target_word = row['String']
	sentence = row['sentence']

	trial_sentence = sentence.replace(target_word, "<b>{t}</b>".format(t=target_word))
	trial_sentence += "<p>To what extent do you experience the bolded word:"

	struct = {
	'type': 'survey-likert',
	'questions': 'FILLER_PERCEPTION', ## Replace with actual prompts
	'preamble': trial_sentence,
	'data': {'word': row['Word'], 'context': row['context'],
			 'sentence': sentence,
			 'string': row['String']}
	}

	if row['count_perceptual'] > CUTOFF_P:
		struct['data']['N'] = 'high_N'
		high_N_p.append(struct)

	elif row['count_perceptual'] < 10:
		struct['data']['N'] = 'low_N'
		low_N_p.append(struct)


print(len(low_N_p))
print(len(high_N_p))

doc += 'var low_N_trials_perception = ' + json.dumps(low_N_p, indent=4) + "\n\n"
doc += 'var high_N_trials_perception = '+ json.dumps(high_N_p, indent=4) + "\n\n"



# Create action trials
low_N_a = []
high_N_a = []
### TODO: Separate by word? Or do in JsPsych?
for index, row in df_action.iterrows():

	target_word = row['String']
	sentence = row['sentence']

	trial_sentence = sentence.replace(target_word, "<b>{t}</b>".format(t=target_word))
	trial_sentence += "<p>To what extent do you experience the bolded word by performing an action with the:<p><img src='action_norms.png' width = 300 height = 150>"

	struct = {
	'type': 'survey-likert',
	'questions': 'FILLER_ACTION', ## Replace with actual prompts
	'preamble': trial_sentence,
	'data': {'word': row['Word'], 'context': row['context'],
			 'sentence': sentence,
			 'string': row['String']}
	}

	if row['count_action'] > CUTOFF_A:
		struct['data']['N'] = 'high_N'
		high_N_a.append(struct)

	elif row['count_action'] < 12:
		struct['data']['N'] = 'low_N'
		low_N_a.append(struct)

print(len(low_N_a))
print(len(high_N_a))

doc += 'var low_N_trials_action = ' + json.dumps(low_N_a, indent=4) + "\n\n"
doc += 'var high_N_trials_action = '+ json.dumps(high_N_a, indent=4) + "\n\n"


with open(SAVE_PATH, "w") as f:
 	f.write(doc)

