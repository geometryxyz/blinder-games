# G1 stans MSM outside of the circuit and A wins if it knows discrete log of all Bi. 
# G2 stands for proving knowledge for system of X + sum ciBi and
# A wins if it doesn't know discrete log of all Bis since that's the only way how it can cancel X

from scipy.stats import nhypergeom

# nhypergeom.pmf(k, M, n, r) means that (k + r)th sample must be a failure 

# Cheating prover fails to win a G1/G2 when one of the events happen
# f 
# s f 
# s s f 
# s s s f 
# s .. f
def win_game(needed_s_samples: int, num_of_s: int, M: int):
    if num_of_s < needed_s_samples: 
        return (False, 0.0)
    fail_prob = 0.0
    for ki in range(0, needed_s_samples): 
        fail_prob += nhypergeom.pmf(k=ki, M=M, n=num_of_s, r=1)

    return (True, 1.0 - fail_prob)

# k_dl = number of blinders for which A knows discrete log
def win_both_games(M: int, k_dl: int, n1: int, n2: int): 
    # number of blinders for which A doesn't know discrete log
    dk_dl = M - k_dl 

    (is_g1_possible, win_g1) = win_game(n1, k_dl, M)
    if not is_g1_possible: 
        return None

    # if A won game 1, there are M - n1 more indices to be queried 
    (is_g2_possible, win_g2) = win_game(n2, dk_dl, M - n1)
    if not is_g2_possible: 
        return None

    return win_g1 * win_g2


M = 32
n1 = 14
n2 = 6

probs = [(k_dl, win_both_games(M, k_dl, n1, n2)) for k_dl in range(n1, M)]

max_prob = float('-inf')
max_k_dl = -1

for k_dl, prob in probs:
    if prob is None: 
        continue

    if prob > max_prob:
        max_prob = prob
        max_k_dl = k_dl

print(f"The maximum probability is {max_prob} and it is achieved for k_dl={max_k_dl}")