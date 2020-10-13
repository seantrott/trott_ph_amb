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
print("{N} Items.".format(N=len(df_stims)))
## Remove "Unsure" items
df_stims = df_stims[df_stims['Ambiguity_Type']!="Unsure"]
print("{N} Items after removing Unsure types.".format(N=len(df_stims)))


## Read in CELEX
df_celex = pd.read_csv("data/lexical/celex_all.csv", sep="\\")
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
df_celex = df_celex.drop_duplicates(subset='Word')
print(len(df_celex))
df_celex = df_celex[['Word', 'SylCnt', 'CompCnt']]


### TODO: Deal with missing CELEX word ("mold")

## Read in SUBTLEX
df_subtlex = pd.read_csv("data/lexical/subtlex.csv")
print(len(df_subtlex))

## Merge files
df_merged = pd.merge(df_stims, df_celex, on = ["Word"])
print(len(df_merged))
df_merged = pd.merge(df_merged, df_subtlex, on = ["Word"])
print(len(df_merged))

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
