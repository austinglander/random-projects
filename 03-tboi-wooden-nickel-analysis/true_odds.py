# After a statistics lecture this week, I realized I could calculate the EXACT odds of getting >= 36 cents in the first five uses of wooden nickel
# Axiom 3 of probability: P(A U B) = P(A) + P(B) if A and B are disjoint
# Note that simple events (events with only one outcome) are disjoint
# Therefore, I can simply calculate the exact odds of every possibility, and sum the desired events (>= 36 cents)
# There are only 4^5 events, as we have 5 independent events (wooden nickel uses) with 4 possibilities each (0, 1, 5, 10)

import numpy as np
import json

# Start by generating our sample space
# I would love to implement this with a general algorithm that could apply to n repetitions of wooden nickel. Not sure how yet.
OUTCOMES = {
    0: 0.41,
    1: 0.52,
    5: 0.06,
    10: 0.01
}
sample_space = []
for i in OUTCOMES:
    for j in OUTCOMES:
        for k in OUTCOMES:
            for l in OUTCOMES:
                for m in OUTCOMES:
                    sample_space.append([i, j, k, l, m])

# Let's approach the next step by generating some parallel lists, one storing probabilities of event i in sample_space, and the other storing the sum of event i in sample_space
event_probabilities = []
event_sums = []
for event in sample_space:
    event_sums.append(sum(event))
    # Multiplication rule for independent events: P(A ∩ B) = P(A) * P(B)
    # Goal: For each event, calculate P(S ∩ A ∩ B ∩ C ∩ D ∩ E) = P(S) * P(A) * P(B) * P(C) * P(D) * P(E)
    # Axiom 2 of probability: P(S) = 1, which is why we initialize probability to 1.
    probability = 1
    for outcome in event:
        probability *= OUTCOMES[outcome]
    event_probabilities.append(probability)

# Sanity check: The sum of all event_probabilities should be 1 (give or take cause floating point stuff)
print(sum(event_probabilities))

# Might as well find the exact odds of getting >= n cents for every value of n since we have this nice list
# Generate dictionary of keys 0-50 with values 0
n_cent_probabilty = {i:0 for i in range(51)}
# For every event of n-cents in event_sums, add the probability of that event occuring to every dictionary entry <= n
# This turns the dictionary into a map of n-cent events -> probability of >= n-cents
for index, val in enumerate(event_sums):
    for dict_key in range(0, val + 1):
        n_cent_probabilty[dict_key] += event_probabilities[index]

# Let's see the results!
print(json.dumps(n_cent_probabilty, indent=4))
with open("wooden_nickel_probabilities.json", "w") as out_file:
    out_file.write(json.dumps(n_cent_probabilty, indent=4))



