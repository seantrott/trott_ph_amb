"""Code to get filler words from CELEX, matched for critical stims."""

import math
import numpy as np
import pandas as pd 

from collections import Counter



### paths
BRYSBAERT_PATH = "data/lexical/brysbaert_norms.csv"
CELEX_PATH = "data/lexical/celex_all.csv"
STIMS_PATH = "data/stims/stimuli.csv"
SAVE_PATH = "data/stims/fillers.csv"

### Helper functions
def remove_word(word):
    """Tag word for removal."""
    return " " in word or "-" in word or "'" in word


def preprocess_stims(path):
	"""Preprocess stimuli."""
	df_stims = pd.read_csv(path)
	print("{N} Items.".format(N=len(df_stims)))
	## Remove "Unsure" items
	df_stims = df_stims[df_stims['Ambiguity_Type']!="Unsure"]
	print("{N} Items after removing Unsure types.".format(N=len(df_stims)))
	## Set up dom_pos column
	pos = {'N': 'Noun', 'V': 'Verb'}
	df_stims['POS_tag'] = df_stims['Class'].apply(lambda x: pos[x])
	return df_stims

def preprocess_celex(path):
	"""Preprocess Celex."""
	df_celex = pd.read_csv(path, sep="\\")
	print("{N} Celex items.".format(N=len(df_celex)))
	df_celex = df_celex.dropna()
	# Filter to remove words with hyphens, etc.
	df_celex['remove'] = df_celex['Word'].apply(lambda x: remove_word(x))
	df_celex = df_celex[df_celex['remove']==False]
	# Remove words like "p" or "c" from CELEX
	df_celex['word_length'] = df_celex['Word'].apply(lambda x: len(x))
	df_celex = df_celex[df_celex['word_length']>1]
	# Rremove proper nouns
	df_celex['proper_noun'] = df_celex['Word'].apply(lambda x: (any(l.isupper() for l in x)))
	df_celex = df_celex[df_celex['proper_noun']==False]
	df_celex = df_celex.drop_duplicates(subset=['Word', 'Class'])
	print("{N} Celex items after dropping duplicates, proper nouns, and words of length 0.".format(N=len(df_celex)))
	df_celex = df_celex[['Word', 'SylCnt', 'Class']]
	return df_celex

def preprocess_brysbaert(path):
	"""Preprocess Brysbaert norms."""
	df_brysbaert = pd.read_csv(path)
	print("{N} Brysbaert items.".format(N=len(df_brysbaert)))
	## Log (frequency + 1)
	df_brysbaert['freq_log'] = df_brysbaert['SUBTLEX'].apply(lambda x: math.log10(x+1))
	return df_brysbaert



## Read in critical stims
df_stims = preprocess_stims(STIMS_PATH)

## Read and preprocess Brysbaert /  Celex
df_brysbaert = preprocess_brysbaert(BRYSBAERT_PATH)
df_celex = preprocess_celex(CELEX_PATH)


## Merge Stims, Celex, and Brysbaert
df_merged = pd.merge(df_stims, df_celex, on = ["Word", "Class"])
print("Number of items: {N}".format(N=len(df_merged)))
df_merged = pd.merge(df_merged, df_brysbaert, on = ["Word"])
print("Number of items: {N}".format(N=len(df_merged)))


## Now combine CELEX and Brysbaert
df_source = pd.merge(df_celex, df_brysbaert, on = ['Word'])
## Now filter CELEX to not contain any of our critical stims
df_source = df_source[~df_source['Word'].isin(df_merged['Word'])]
print("{N} items shared across Celex and Brysbaert.".format(N=len(df_brysbaert)))

## Now sample from CELEX---get words within some threshold of the target word frequency, also
## matched for POS ("Class") and length ("SylCnt").
## TODO: Use different frequency measure? This will be frequency of a sense, I think.
samples = []
sampled_words = []
FREQ_THRESHOLD = .1
CONC_THRESHOLD = 1
for index, row in df_merged.iterrows():
	freq = row['freq_log']
	conc = row['Conc.M']

	# Identify words within correct frequency range
	df_tmp = df_source[(df_source['freq_log']<freq+FREQ_THRESHOLD)&(df_source['freq_log']>freq-FREQ_THRESHOLD)]
	# Identify words within correct concreteneess range
	df_tmp = df_tmp[(df_tmp['Conc.M']<conc+CONC_THRESHOLD)&(df_tmp['Conc.M']>conc-CONC_THRESHOLD)]
	# Now identify words with correct grammatical class and length
	df_tmp = df_tmp[(df_tmp['Dom_Pos']==row['POS_tag'])&(df_tmp['Class']==row['Class'])&(df_tmp['SylCnt']==row['SylCnt'])]
	# Remove words we've already identified
	df_tmp = df_tmp[~df_tmp['Word'].isin(sampled_words)]
	# Now sample a row from the set of words that meet the appropriate criteria, and add it to our set of samples

	while True:
		sampled_row = df_tmp.sample(n=1)

		if sampled_row['Word'].values[0] not in sampled_words:
			samples.append(sampled_row)
			sampled_words.append(sampled_row['Word'].values[0])
			break

df_concat = pd.concat(samples)
print("Number of fillers: {N}".format(N=len(df_concat)))


## Now assign each to: 1) NN; 2) NS; 3) SN
# Multiply across
## 38 NN, 37 NS, 37 SN
filler_conditions = ['NN'] * 38 + ['NS'] * 37 + ['SN'] * 37
# Now shuffle
np.random.shuffle(filler_conditions)
# Assign to words
df_concat['filler_condition'] = filler_conditions
# Save
# df_concat.to_csv(SAVE_PATH)





