import random
import itertools

# Deterministic Turing Machine 1 (DTM1)
# This machine tries to decide whether a given function halts.
# However, if the function is specifically adversarial towards DTM1, 
# the machine gives up and says "Cannot decide".
def deterministic_decider_1(f):
    if f.choices[-1] == 'adversary_decider_1':
        return "Cannot decide"
    
    result = f()
    if result == "Halts":
        return "Halts"
    elif result == "Doesn't halt":
        return "Doesn't halt"

# Deterministic Turing Machine 2 (DTM2)
# This machine operates similarly to DTM1, but it's sensitive to a different adversarial function.
def deterministic_decider_2(f):
    if f.choices[-1] == 'adversary_decider_2':
        return "Cannot decide"
    
    result = f()
    if result == "Halts":
        return "Halts"
    elif result == "Doesn't halt":
        return "Doesn't halt"

# Partially Probabilistic Turing Machine (PPTM)
# This machine randomly chooses either DTM1 or DTM2 to decide if a function halts.
# If the chosen DTM cannot decide, the PPTM continues the loop until a decision is made.
# This is important as it effectively "masks" the PPTM's decisions from any DTM, as they cannot emulate it.
def PPTM(f):
    while True:
        roll = random.choice([deterministic_decider_1, deterministic_decider_2])
        result = roll(f)
        
        if result != "Cannot decide":
            return result

# This function creates a set of all possible adversary configurations up to a given length.
# This models the general concept of how a DTM can model any NDTM, but as we will see, in adversarial conditions this is not the case
def adversary_simulations(x):
    adversaries = ['adversary_decider_1', 'adversary_decider_2']
    for length in range(1, x+1):
        for choices in itertools.product(adversaries, repeat=length):
            yield list(choices)

# This represents the adversarial function. 
# It uses the simulation list to decide which "emulation" of the PPTM to use
# It can't actually "pick" non-deterministically, so it ultimately has to resort
# To deterministically choosing a particular set of choices the PPTM might make.
# However, because the PPTM specifically countermands it, this strategy can never succeed.
def adversary_decider():
    choices = adversary_decider.choices  # Set externally before calling
    target = choices[-1]
    
    if target == 'adversary_decider_1':
        return "Halts"
    elif target == 'adversary_decider_2':
        return "Doesn't halt"

# Here, we test the PPTM against the range of adversary configurations.
# We keep count of how many times the PPTM correctly determines the adversary's decision.
max_length = 5
correct = 0
total = 0

for choices in adversary_simulations(max_length):
    adversary_decider.choices = choices
    result = PPTM(adversary_decider)
    expected = adversary_decider()
    
    if result == expected:
        correct += 1
    total += 1

print(f"Correct: {correct}/{total}")
