# Trott & Bergen: Polysemy vs. Homonymy

Code for modeling and comparing contextualized word embeddings, generating jsPsych experiments, and analyze data.

The documentation below describes the various data files and processing steps involved.

If you're looking for the RAW-C dataset, more information can be found on the corresponding repository [here](https://github.com/seantrott/raw-c).

# Citing 

If you'd like to use the stimuli or relatedness norms, please cite [Trott & Bergen (2021)](https://arxiv.org/abs/2105.13266):

> Trott, S., & Bergen, B. (2021). RAW-C: Relatedness of Ambiguous Words--in Context (A New Lexical Resource for English). Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th Joint International Conference on Natural Language Processing.

If you'd like to reference the theoretical paper, please cite Trott & Bergen (Under Review):

> Trott, S., & Bergen, B. (Under Review). Word meaning is both categorical and continuous.

# Raw stimuli

The raw stimuli (`data/stims/stimuli.csv`) currently constitute a set of 115 ambiguous words (i.e., items). Each word has two senses, and two *sentences* for each sense. Some of these stimuli were adapted from previous studies (Brown, 2008; Klepousniotou et al, 2008; Klepousniotou, 2002; Klepousniotou & Baum, 2007), and the rest were identified from homonym lists online.

For example the word "lamb" might have two sentences relating to the `Food` sense, and two sentences relating to the `Animal` sense. Similarly, the word `bat` might have two sentences relating to the `Animal` sense, and two sentences relating to the `Instrument` sense.

Crucially, there are two manipulations within and across items:

- Within items, we manipulate whether any given pair of sentences involves crossing a **Sense Boundary** (there are two `Same Sense` combinations, and four `Different Sense` combinations, for each word).  
- Across items, we manipulate the **Ambiguity Type** present (`Homonymy` vs. `Polysemy`). This was identified by consulting both the Merriam-Webster Dictionary and the Oxford English Dictionary, and determining whether the different meanings were represented as different *entries* (Homonymy) or as different *senses* under the same entry (Polysemy). 

# Language model pipeline

Each pair of sentences was then run through two neural language models: ELMo and BERT. We extracted the **contextualized embedding** for the target word (e.g., "lamb") from each context of use, then computed the `cosine distance` between these embeddings (see `src/modeling/get_distances.py`). This is intended to reflect the **distance** between two contexts of use. The resulting data can be found in `data/processed/stims_processed.csv`.

## Analysis of NLM results

Further, an analysis of these results can be found in `src/analysis/norming_analysis.html` (see `src/analysis/norming_analysis.Rmd` for the code to generate this file).

We found that `Same Sense` usages of a word were closer (as measured by `cosine distance`) than `Different Sense` usages. Interestingly, we did *not* find a difference for `Different Sense` usages between `Homonymy` and `Polysemy`; this is in contrast to the results of the norming study below.

# Norming study

These 115 words (corresponding to 460 sentences, 690 sentence pairs, and 1380 unique sentence *orderings*) were used in a norming study ([Trott & Bergen, 2021)](https://arxiv.org/abs/2105.13266):

> Trott, S., & Bergen, B. (2021). RAW-C: Relatedness of Ambiguous Words--in Context (A New Lexical Resource for English). Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th Joint International Conference on Natural Language Processing.

The analysis script ([`src/analysis/norming_analysis.Rmd`](https://github.com/seantrott/trott_ph_amb/blob/master/src/analysis/norming_analysis.Rmd)) includes several exclusion criteria (including bot checks and catch trials), resulting in a total of 77 participants.

## Results of norming study

The results of the norming analysis can be found in [`src/analysis/norming_analysis.html`](https://github.com/seantrott/trott_ph_amb/blob/master/src/analysis/norming_analysis.html). They are described in considerably more detail in [Trott & Bergen (2021)](https://arxiv.org/abs/2105.13266).

# Fillers 

After running the norming study, we identified a set of **filler** words, from which we would generate nonsense (and some sensible) filler sentences for the primary rexperiment. Each of the 112 critical items were matched for Length (number of syllables), part of speech (as used in the critical sentence, e.g., Verb vs. Noun), and frequency (based on the SUBTLEX frequency data).

# Primary experiment

The primary experiments were registered on OSF ([Experiment 1](https://osf.io/gj48a/), [Experiment 2](https://osf.io/4ej6t)).

Participants performed a **primed sensibility judgment** task. The dependent variables were `log(RT)` and `Accuracy` (i.e., whether their response to the target trial was correct or incorrect).

## Data

The processed data for the primary experiments, *before removing outliers*, can be found here:

- Experiment 1: [`data/processed/polysemy_s1_main.csv`](https://github.com/seantrott/trott_ph_amb/blob/master/data/processed/polysemy_s1_main.csv)  
- Experiment 2: [`data/processed/polysemyu_s2_main.csv`](https://github.com/seantrott/trott_ph_amb/blob/master/data/processed/polysemy_s2_main.csv)

These files are necessary for running the pre-registered analysis scripts (see below).

Additionally, we have saved another version of the data files, *after removing outliers* and merging with the norming data:

- Experiment 1: `data/processed/polysemy_s1_final.csv`  
- Experiment 2: `data/processed/polysemyu_s2_final.csv`

## Analysis scripts

### Primary (pre-registered) analyses

The pre-registered analyses can be found here:

- Experiment 1: [`src/analysis/exp1_prereg.Rmd`](https://github.com/seantrott/trott_ph_amb/blob/master/src/analysis/exp1_prereg.Rmd)
- Experiment 2: [`data/processed/exp2_prereg.Rmd`](https://github.com/seantrott/trott_ph_amb/blob/master/src/analysis/exp2_prereg.Rmd)

There are also *knit* `.html` files from both of these `.Rmd` files with the same filepath.

### Analyses with transformed distance

The analyses involving **transformations** to `cosine distance` can be found at [`src/analysis/transformations.Rmd`](https://github.com/seantrott/trott_ph_amb/blob/master/src/analysis/transformations.Rmd) (along with a knit `.html` file [here](https://github.com/seantrott/trott_ph_amb/blob/master/src/analysis/transformations.html)).

### Supplementary Analysis with Dominance

The supplementary analysis with **dominance** can be found at: [`src/analysis/dominance.Rmd`](https://github.com/seantrott/trott_ph_amb/blob/master/src/analysis/dominance.Rmd).

The norms themselves can be found [here](https://github.com/seantrott/trott_ph_amb/blob/master/data/processed/dominance_norms_with_order.csv).

###3 Supplementary Analysis with Surprisal

The supplementary analysis with **surprisal** can be found at: [`src/analysis/surprisal_exploratory.Rmd`](https://github.com/seantrott/trott_ph_amb/blob/master/src/analysis/surprisal_exploratory.Rmd).

The surprisal estimates can be found [here](https://github.com/seantrott/trott_ph_amb/blob/master/data/processed/bert-large_surprisals.csv).



# References

Brown, S. W. (2008). Polysemy in the mental lexicon. Colorado Research in Linguistics, 21.

De Leeuw, J. R. (2015). jsPsych: A JavaScript library for creating behavioral experiments in a Web browser. Behavior research methods, 47(1), 1-12.

Klepousniotou, E., Titone, D., & Romero, C. (2008). Making sense of word senses: The comprehension of polysemy depends on sense overlap. Journal of Experimental Psychology: Learning, Memory, and Cognition, 34(6), 1534.

Klepousniotou, E. (2002). The processing of lexical ambiguity: Homonymy and polysemy in the mental lexicon. Brain and language, 81(1-3), 205-223.

Klepousniotou, E., & Baum, S. R. (2007). Disambiguating the ambiguity advantage effect in word recognition: An advantage for polysemous but not homonymous words. Journal of Neurolinguistics, 20(1), 1-24.

Valera, S. (2020). Polysemy Versus Homonymy. In Oxford Research Encyclopedia of Linguistics.

