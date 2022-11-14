import numpy as np
from typing import List, Tuple
import random

def run_matching(scores: List[List], gender_id: List, gender_pref: List) -> List[Tuple]:

    Proposer = [0, 1, 2, 3, 4]
    Acceptor = [5, 6, 7, 8, 9]
    matches = 0

    current_matches = {}
    maybe_matches = {}

    def get_key(val):
        for key, value in current_matches.items():
            if val == value:
                return key

    while matches < 5:

        for single_proposer in Proposer:
            random_acceptor = random.choice(Acceptor) #Choosing random acceptor for each single proposer
            maybe_matches[single_proposer] = random_acceptor #Temporarily matching the random acceptor with the single proposer
            print(maybe_matches)

            if random_acceptor not in current_matches.values(): #if the random acceptor is NOT already in a match
                current_matches.update(maybe_matches)
                maybe_matches.clear()
                matches = len(current_matches)
                print(str(current_matches) + " current")

            else: #if the random acceptor is already in a match

                existing_proposer = get_key(maybe_matches[single_proposer]) #pre-existing proposer already matched with the random acceptor

                if scores[single_proposer][maybe_matches[single_proposer]] > scores[existing_proposer][maybe_matches[single_proposer]]: #comparing scores between hypothetical single proposer + random acceptor match VS pre-existing proposer + random acceptor match
                    del current_matches[existing_proposer]
                    current_matches.update(maybe_matches)
                    print(str(maybe_matches) + " new match")
                    maybe_matches.clear()
                    print(str(current_matches) + " updated")

                else:
                    maybe_matches.clear()
                    #if at least 1 proposer is not matched, the for loop will start again (as seen by the print statements). This will likely occur because it is unlikely for each proposer to be randomly matched with a different acceptor each time.
                    #Repetition of the for loop allows for better matches because each proposer will be assigned a random acceptor again, and the compatibility scores will be compared.
                matches = len(current_matches)

    print(current_matches)

    """
    TODO: Implement Gale-Shapley stable matching!
    :param scores: raw N x N matrix of compatibility scores. Use this to derive a preference rankings.
    :param gender_id: list of N gender identities (Male, Female, Non-binary) corresponding to each user
    :param gender_pref: list of N gender preferences (Men, Women, Bisexual) corresponding to each user
    :return: `matches`, a List of (Proposer, Acceptor) Tuples representing monogamous matches

    Some Guiding Questions/Hints:
        - This is not the standard Men proposing & Women receiving scheme Gale-Shapley is introduced as
        - Instead, to account for various gender identity/preference combinations, it would be better to choose a random half of users to act as "Men" (proposers) and the other half as "Women" (receivers)
            - From there, you can construct your two preferences lists (as seen in the canonical Gale-Shapley algorithm; one for each half of users
        - Before doing so, it is worth addressing incompatible gender identity/preference combinations (e.g. gay men should not be matched with straight men).
            - One easy way of doing this is setting the scores of such combinations to be 0
            - Think carefully of all the various (Proposer-Preference:Receiver-Gender) combinations and whether they make sense as a match
        - How will you keep track of the Proposers who get "freed" up from matches?
        - We know that Receivers never become unmatched in the algorithm.
            - What data structure can you use to take advantage of this fact when forming your matches?
        - This is by no means an exhaustive list, feel free to reach out to us for more help!
    """
    matches = [()]
    return matches

if __name__ == "__main__":
    raw_scores = np.loadtxt('raw_scores.txt').tolist()
    genders = []
    with open('genders.txt', 'r') as file:
        for line in file:
            curr = line[:-1]
            genders.append(curr)

    gender_preferences = []
    with open('gender_preferences.txt', 'r') as file:
        for line in file:
            curr = line[:-1]
            gender_preferences.append(curr)

    gs_matches = run_matching(raw_scores, genders, gender_preferences)



