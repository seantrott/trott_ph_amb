# Trott & Bergen: Polysemy vs. Homonymy

Code for modeling and comparing contextualized word embeddings, generating jsPsych experiments, and analyze data.

The documentation below describes the various data files and processing steps involved.

# Raw stimuli

The raw stimuli (`data/stims/stimuli.csv`) currently constitute a set of 115 ambiguous words (i.e., items). Each word has two senses, and two *sentences* for each sense. Some of these stimuli were adapted from previous studies (Brown, 2008; Klepousniotou et al, 2008; Klepousniotou, 2002; Klepousniotou & Baum, 2007), and the rest were identified from homonym lists online.

For example the word "lamb" might have two sentences relating to the `Food` sense, and two sentences relating to the `Animal` sense. Similarly, the word `bat` might have two sentences relating to the `Animal` sense, and two sentences relating to the `Instrument` sense.

Crucially, there are two manipulations within and across items:

- Within items, we manipulate whether any given pair of sentences involves crossing a **Sense Boundary** (there are two `Same Sense` combinations, and four `Different Sense` combinations, for each word).  
- Across items, we manipulate the **Ambiguity Type** present (`Homonymy` vs. `Polysemy`). This was identified by consulting both the Merriam-Webster Dictionary and the Oxford English Dictionary, and determining whether the different meanings were represented as different *entries* (Homonymy) or as different *senses* under the same entry (Polysemy). 

**Note 1**: The question of whether to label two distinct *usages* of a word as Homonymy vs. Polysemy is by no means theoretically settled, and has been discussed extensively in the literature (see Valera (2020) for a recent review); it is usually based on "relatedness", either historical (e.g., shared etymology), psychological (e.g., degree of association), or both. We used a lexicographically derived annotation scheme to maximally align our labels with the methodology (and results) of lexicographers; these labels were further validated in the Norming Study (see below). Notably, investigating this posited theoretical distinction (along with the distinction between `Same` vs. `Different` senses) is at root the motivation for the current set of studies.

**Note 2**: There were three items for which we could not identify whether the `Different Sense` usage was truly a different sense, according to either MW or the OED, and each seemed to involve some form of **metonymy**: *novel* (e.g., "paperback" vs. "best-selling"), *magazine* (e.g., "weekly" vs. "glossy"), and *oil* (e.g., "crude" vs. "canola"). These were included in the norming study (see below) but ultimately excluded from the final experiment.

# Language model pipeline

Each pair of sentences was then run through two neural language models: ELMo and BERT. We extracted the **contextualized embedding** for the target word (e.g., "lamb") from each context of use, then computed the `cosine distance` between these embeddings (see `src/modeling/get_distances.py`). This is intended to reflect the **distance** between two contexts of use. The resulting data can be found in `data/processed/stims_processed.csv`.

## Analysis of NLM results

Further, an analysis of these results can be found in `src/analysis/norming_analysis.html` (see `src/analysis/norming_analysis.Rmd` for the code to generate this file).

We found that `Same Sense` usages of a word were closer (as measured by `cosine distance`) than `Different Sense` usages. Interestingly, we did *not* find a difference for `Different Sense` usages between `Homonymy` and `Polysemy`; this is in contrast to the results of the norming study below.

# Norming study

These 115 words (corresponding to 460 sentences, 690 sentence pairs, and 1380 unique sentence *orderings*) were used in a norming study. 

The code to generate the items for the norming study automatically (using `data/stims/stimuli.csv`) can be found in `src/experiment/construct_norming_study.py`). This compiles a set of JsPsych trials (De Leeuw, 2015) that can in turn be copy/pasted into the appropriate .html file (in this case: `experiment/np_sona.html`).

81 participants were recruited via the UCSD SONA participant pool. They were asked to indicate how related two usages of a word were, from 0 ("not at all related") to 4 ("same meaning"). Their raw data files were compiled (see `data/processed/polysemy_norming.csv`) using `src/preprocessing/concat_norming.py`. The analysis script (`src/analysis/norming_analysis.Rmd`) includes several exclusion criteria (including bot checks and catch trials), resulting in a total of 77 participants.

## Results of norming study

The results of the norming analysis can be found in `src/analysis/norming_analysis.html`. We validated both manipulations: `Same Sense` pairs were judged to be much more related than `Different Sense` pairs; further, for `Different Sense` pairs, `Homonyms` were typically judged to be entirely unrelated, while words annotated as `Polysemous` spanned a more uniform distribution, i.e., some were very related and some were very unrelated. 

Additionally, `cosine distance` (from both ELMo and BERT) was negatively associated with `relatedness` for a given pair of sentences, as expected. Notably, it also appears that `cosine distance` (a measure of **contextual distance**), while itself correlated with `Same/Different Sense`, does not perfectly capture the variance in `Relatedness` explained by `Same/Different Sense`. That is, `cosine distance` *underestimates* how related participants judge `Same Sense` pairs to be; further, for `Homonyms`, `cosine distance` *underestimates* how *dissimilar* participants judge `Different Sense` pairs to be.

We ultimately excluded the three `Unsure` items from the final set of critical stimuli, given that participants usually judged the `Different Sense` usages to be the same meaning (e.g., "paperback novel" vs. "best-selling novel"). This, along with the fact that neither MW nor OED listed the meanings under separate senses or entries, made us too uncertain about the ability of these items to elicit `Different Sense` judgments.

# Fillers 

After running the norming study, we identified a set of **filler** words, from which we would generate nonsense (and some sensible) filler sentences for the primary rexperiment. Each of the 112 critical items were matched for Length (number of syllables), part of speech (as used in the critical sentence, e.g., Verb vs. Noun), and frequency (based on the SUBTLEX frequency data).

# Primary experiment

The primary experiments were registered on OSF ([Experiment 1](https://osf.io/gj48a/), [Experiment 2](https://osf.io/4ej6t)).

Participants performed a **primed sensibility judgment** task. The dependent variables were `log(RT)` and `Accuracy` (i.e., whether their response to the target trial was correct or incorrect).

## Data

The processed data for the primary experiments, *before removing outliers*, can be found here:

- Experiment 1: `data/processed/polysemy_s1_main.csv`  
- Experiment 2: `data/processed/polysemyu_s2_main.csv`

These files are necessary for running the pre-registered analysis scripts (see below).

Additionally, we have saved another version of the data files, *after removing outliers* and merging with the norming data:

- Experiment 1: `data/processed/polysemy_s1_final.csv`  
- Experiment 2: `data/processed/polysemyu_s2_final.csv`

## Analysis scripts

The pre-registered analyses can be found here:

- Experiment 1: `src/analysis/exp1_prereg.Rmd`  
- Experiment 2: `data/processed/exp2_prereg.Rmd`

There are also *knit* `.html` files from both of these `.Rmd` files with the same filepath.



# References

Brown, S. W. (2008). Polysemy in the mental lexicon. Colorado Research in Linguistics, 21.

De Leeuw, J. R. (2015). jsPsych: A JavaScript library for creating behavioral experiments in a Web browser. Behavior research methods, 47(1), 1-12.

Klepousniotou, E., Titone, D., & Romero, C. (2008). Making sense of word senses: The comprehension of polysemy depends on sense overlap. Journal of Experimental Psychology: Learning, Memory, and Cognition, 34(6), 1534.

Klepousniotou, E. (2002). The processing of lexical ambiguity: Homonymy and polysemy in the mental lexicon. Brain and language, 81(1-3), 205-223.

Klepousniotou, E., & Baum, S. R. (2007). Disambiguating the ambiguity advantage effect in word recognition: An advantage for polysemous but not homonymous words. Journal of Neurolinguistics, 20(1), 1-24.

Valera, S. (2020). Polysemy Versus Homonymy. In Oxford Research Encyclopedia of Linguistics.

