import random
import itertools

# Optimal Halting Decider 1 (OHD1)
# This machine tries to decide whether a given function halts.
# However, if the function is specifically pathological towards OHD1, 
# the machine gives up and says "Cannot decide".
def OHD1(f):
    if f.choices[-1] == 'pathological_decider_1':
        return "Cannot decide"
    
    result = f()
    if result == "Halts":
        return "Halts"
    elif result == "Doesn't halt":
        return "Doesn't halt"

# Optimal Halting Decider 2 (OHD2)
# This machine operates similarly to OHD1, but it's sensitive to a different pathological function.
def OHD2(f):
    if f.choices[-1] == 'pathological_decider_2':
        return "Cannot decide"
    
    result = f()
    if result == "Halts":
        return "Halts"
    elif result == "Doesn't halt":
        return "Doesn't halt"

# Partially Probabilistic Turing Machine (PPTM)
# This machine randomly chooses either OHD1 or OHD2 to decide if a function halts.
# If the chosen OHD cannot decide, the PPTM continues the loop until a decision is made.
# This is important as it effectively "masks" the PPTM's decisions from any OHD, as they cannot emulate it.
def PPTM(f):
    while True:
        roll = random.choice([OHD1, OHD2])
        result = roll(f)
        
        if result != "Cannot decide":
            return result

# This function creates a set of all possible pathological configurations up to a given length.
# This models the general concept of how a DTM can model any NDTM, but as we will see, in pathological conditions this is not the case
def pathological_simulations(x):
    pathologies = ['pathological_decider_1', 'pathological_decider_2']
    for length in range(1, x+1):
        for choices in itertools.product(pathologies, repeat=length):
            yield list(choices)

# This represents the pathological function. 
# It uses the simulation list to decide which "emulation" of the PPTM to use.
# It can't actually "pick" non-deterministically, so it ultimately has to resort
# To deterministically choosing a particular set of choices the PPTM might make.
# However, because the PPTM specifically countermands it, this strategy can never succeed.
def pathological_decider():
    choices = pathological_decider.choices  # Set externally before calling
    target = choices[-1]
    
    if target == 'pathological_decider_1':
        return "Halts"
    elif target == 'pathological_decider_2':
        return "Doesn't halt"

# Here, we test the PPTM against the range of pathological configurations.
# We keep count of how many times the PPTM correctly determines the pathological's decision.
max_length = 5
correct = 0
total = 0

for choices in pathological_simulations(max_length):
    pathological_decider.choices = choices
    result = PPTM(pathological_decider)
    expected = pathological_decider()
    
    if result == expected:
        correct += 1
    total += 1

print(f"Correct: {correct}/{total}")
