# YA01 LWVL - This seed grants 3 dimes, a nickel, and a penny within the first 5 uses of wooden nickel as the keeper
# This insane luck had me wondering just how lucky this really was, so here I am to find out
# I would love to use the actual game's RNG to discover seeds with similar or even greater luck, but that may be a bit above my paygrade
# For now, I will just do random trials

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from tqdm import tqdm

def wooden_nickel(n: int = 1) -> int:
    """ 
    Simulate n uses of wodden nickel and return the total value of pennies
    Odds are taken from the binding of isaac wiki: https://bindingofisaacrebirth.fandom.com/wiki/Wooden_Nickel
    Penny: 52%, Nickel: 6%, Dime: 1%, Nothing: 41% 
    """
    return sum(np.random.choice([0, 1, 5, 10], p=[0.41, 0.52, 0.06, 0.01], size=n))

# Run our simulations and collect the data
total_simulations = 10000000
magic_number = 36
data = [wooden_nickel(5) for i in tqdm(range(total_simulations))]
# We will do the expensive sort operation now to save time with getting things like the max of the data
sorted_data = np.sort(np.array(data))

# Do some basic statistical analysis with numpy
mean = np.mean(sorted_data)
std_dev = np.std(sorted_data)
print(f"Number of simulations: {total_simulations}")
print(f"Mean: {mean:.3f}")
print(f"Standard Deviation: {std_dev:.3f}")
print(f"Maximum: {sorted_data[-1]}" )
num_geq_magic_number = 0
for i in reversed(sorted_data): 
    if i >= magic_number:
        num_geq_magic_number += 1
    else:
        break
print(f"Exact number of simulations that tied or beat {magic_number} cents: {num_geq_magic_number}")
print(f"Empirical probability of tying or beating {magic_number} cents: {num_geq_magic_number / total_simulations * 100}%")

# Setup our plot
sns.set_style('whitegrid')
sns.kdeplot(np.array(data), bw_method=0.2)
plt.title(f"Cents from 5 wooden nickel uses ({total_simulations:,} simulations)")
plt.show()