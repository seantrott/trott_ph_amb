"""Run each combination of sentences through ELMo."""

import itertools

import pandas as pd
import seaborn as sns

from scipy.spatial.distance import cosine
from tqdm import tqdm



### PATHS
STIMULI_PATH = "data/stims/stimuli.csv"
SAVE_PATH = "data/processed/stims_processed.csv"
VERSIONS = ['M1_a', 'M1_b', 'M2_a', 'M2_b']

### Read in stims
df_stims = pd.read_csv(STIMULI_PATH)
df_stims.head(5)

# Remove rows for which we don't have all versions coded
df_filtered = df_stims[~df_stims['M1_b'].isna()].reset_index()
len(df_filtered)


## Load ELMo
from allennlp.commands.elmo import ElmoEmbedder

elmo = ElmoEmbedder(
    options_file='https://s3-us-west-2.amazonaws.com/allennlp/models/elmo/2x4096_512_2048cnn_2xhighway_5.5B/elmo_2x4096_512_2048cnn_2xhighway_5.5B_options.json', 
    weight_file='https://s3-us-west-2.amazonaws.com/allennlp/models/elmo/2x4096_512_2048cnn_2xhighway_5.5B/elmo_2x4096_512_2048cnn_2xhighway_5.5B_weights.hdf5'
)


# Load BERT
from bert_embedding import BertEmbedding
bert = BertEmbedding()


## Process sentences

## TODO: Make cleaner, like norming study?

distances = []
with tqdm(total=len(df_filtered)) as progress_bar:
    for index, row in df_filtered.iterrows():

        # Extract condition, target word info, and mean relatedness
        condition = row['Original Condition']
        homonymy_label = row['Different_entries_MW']
        target_word = row['String']
        relatedness = row['K_relatedness']
        source = row['Source']
        pos = row['Class']
        
        # Extract and split sentences
        m1_a, m1_b = row['M1_a'].lower().replace(".", "").split(), row['M1_b'].lower().replace(".", "").split()
        m2_a, m2_b = row['M2_a'].lower().replace(".", "").split(), row['M2_b'].lower().replace(".", "").split()

        target_embeddings = {}
        bert_embeddings = {}
        for label, sentence in [('m1_a', m1_a), 
                                ('m1_b', m1_b), 
                                ('m2_a', m2_a),
                                ('m2_b', m2_b)]:
            target_index = sentence.index(target_word)

            # ELMo
            target_embedding = elmo.embed_sentence(sentence)[2][target_index]
            target_embeddings[label] = target_embedding

            # BERT
            bert_embedding = bert
        
        distances.append({
            'same': True,
            'word': target_word,
            'item': index,
            'condition': condition,
            'relatedness': relatedness,
            'version': 'M1',
            'source': source,
            'pos': pos,
            'homonymy_label': homonymy_label,
            'distance': cosine(target_embeddings['m1_a'], target_embeddings['m1_b'])
        })
        distances.append({
            'same': True,
            'word': target_word,
            'condition': condition,
            'relatedness': relatedness,
            'item': index,
            'version': 'M2',
            'source': source,
            'pos': pos,
            'homonymy_label': homonymy_label,
            'distance': cosine(target_embeddings['m2_a'], target_embeddings['m2_b'])
        })
        distances.append({
            'same': False,
            'word': target_word,
            'condition': condition,
            'relatedness': relatedness,
            'item': index,
            'version': 'M1a_M2a',
            'source': source,
            'pos': pos,
            'homonymy_label': homonymy_label,
            'distance': cosine(target_embeddings['m1_a'], target_embeddings['m2_a'])
        })
        distances.append({
            'same': False,
            'word': target_word,
            'condition': condition,
            'relatedness': relatedness,
            'item': index,
            'version': 'M1a_M2b',
            'source': source,
            'pos': pos,
            'homonymy_label': homonymy_label,
            'distance': cosine(target_embeddings['m1_a'], target_embeddings['m2_b'])
        })
        distances.append({
            'same': False,
            'word': target_word,
            'condition': condition,
            'relatedness': relatedness,
            'item': index,
            'source': source,
            'pos': pos,
            'version': 'M1b_M2a',
            'homonymy_label': homonymy_label,
            'distance': cosine(target_embeddings['m1_b'], target_embeddings['m2_a'])
        })
        distances.append({
            'same': False,
            'word': target_word,
            'condition': condition,
            'relatedness': relatedness,
            'item': index,
            'source': source,
            'pos': pos,
            'version': 'M1b_M2b',
            'homonymy_label': homonymy_label,
            'distance': cosine(target_embeddings['m1_b'], target_embeddings['m2_b'])
        })
        progress_bar.update(1)



## Create dataframe
df_distances = pd.DataFrame(distances)

## Save data
df_distances.to_csv(SAVE_PATH)



