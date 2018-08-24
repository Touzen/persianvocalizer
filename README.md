Persian Vocalizer
=================
This is a project I made in the course DD2418 - Language Engineering and that has now also been connected to a really 
basic web interface. It takes text written in the Perso-Arabic script and tries to guess the missing vowels using an HMM
trained on Tajik text (which is written using the Cyrillic script which has all the vowels).

Known issues
------------
The code is basically a bundle of scripts at this moment, and should be refactored into a proper program.

Observed n-grams that aren't part of the training set need to be handled more gracefully. Right now a random known 
observation is chosen.

Decoding can probably be optimized since the number of possible states for an observation is a lot smaller than what is
assumed at the moment. Right now, all states are considered (regardless of the consonant observed) which is pretty
naïve and leads to some weird output sometimes.

Unfortunately, Tajik and Iranian Persian differ in several ways regarding pronounciation which might be mitigated if
more work was put into translating between the dialects.

Setup instructions
-------------------
A transcribed corpus is provided with the code. This is based off the Web to Corpus as described in the project report.
The corpus was processed using the script in process_text.py but further cleanup was done manually. To reproduce the
results described in the report, I recommend skipping step 0 of the process below.

Python 3 is the version used for all the code.

(0. Run process_text.py on the Web to Corpus for Tajik)
1. Run partition.py to divide the data into training and testing sets.
2. Run get_sequences.py to obtain the sequences of states and observations.
3. Run bigram_calculate_matrices.py to obtain the a and b matrices for the HMM.
4. Run HMMVocalizer.py without any arguments to start begin testing the model using the testing data.

Alternatively: run vocalize.sh

Credits
--------
The code is based on an HMM lab in the aforementioned course. That code was written in 2017 by Johan Boye and
Patrik Jonell.