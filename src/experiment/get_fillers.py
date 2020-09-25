"""Code to get filler words from CELEX, matched for critical stims."""

import numpy as np
import pandas as pd 

from collections import Counter



### Helper functions
def remove_word(word):
    """Tag word for removal."""
    return " " in word or "-" in word or "'" in word


## Read in critical stims
df_stims = pd.read_csv("data/stims/stimuli.csv")

## Read in CELEX
df_celex = pd.read_csv("data/celex_all.csv", sep="\\")
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

## Merge files
df_merged = pd.merge(df_stims, df_celex, on = ["Word", "Class"])

## Any absent?
df_absent = df_stims[~df_stims['Word'].isin(df_merged['Word'])]
## TODO: Deal with words not in CELEX?



## Duplicates
df_dupes = df_merged[df_merged.duplicated(subset='Word', keep=False)]


## Now filter CELEX to not contain any of our critical stims
df_celex_filtered = df_celex[~df_celex['Word'].isin(df_merged['Word'])]


## Now sample from CELEX---get words within some threshold of the target word frequency, also
## matched for POS ("Class") and length ("SylCnt").
## TODO: Use different frequency measure? This will be frequency of a sense, I think.
samples = []
sampled_words = []
THRESHOLD = .1
for index, row in df_merged.iterrows():
	freq = row['CobLog']
	df_tmp = df_celex_filtered[(df_celex_filtered['CobLog']<freq+THRESHOLD)&(df_celex_filtered['CobLog']>freq-THRESHOLD)]
	df_tmp = df_tmp[(df_tmp['Class']==row['Class'])&(df_tmp['SylCnt']==row['SylCnt'])]
	df_tmp = df_tmp[~df_tmp['Word'].isin(sampled_words)]
	sampled_row = df_tmp.sample(n=1)
	samples.append(sampled_row)

df_concat = pd.concat(samples)





df_concat[['Class', 'SylCnt', 'Word']].groupby(['Class', 'SylCnt']).count()
df_merged[['Class', 'SylCnt', 'Word']].groupby(['Class', 'SylCnt']).count()

df_concat['CobLog'].describe()
df_merged['CobLog'].describe()

df_concat[['Class', 'SylCnt', 'Word', 'CobLog']].groupby(['Class', 'SylCnt']).mean()
df_merged[['Class', 'SylCnt', 'Word', 'CobLog']].groupby(['Class', 'SylCnt']).mean()


import matplotlib.pyplot as plt
plt.hist(df_concat['CobLog'], alpha = .5, label = "filler")
plt.hist(df_merged['CobLog'], alpha = .5, label = "critical")
plt.show()

plt.hist(df_concat['SylCnt'], alpha = .5, label = "filler")
plt.hist(df_merged['SylCnt'], alpha = .5, label = "critical")
plt.show()
