import random
import itertools

# MBPD Judge 1
# This function tries to decide if the function f is specifically pathological towards MBPD1.
def MBPD_judge1(f):
    return f.choices[-1] == 'pathological_decider_1'

# MBPD Judge 2
# Similar to MBPD_judge1, but for MBPD2.
def MBPD_judge2(f):
    return f.choices[-1] == 'pathological_decider_2'

# MBPD1 (Maximally Broad Propositional Decider 1)
# This machine tries to decide whether a given function halts.
# If the function is specifically pathological towards MBPD1,
# it gives up and says "Cannot decide".
def MBPD1(f):
    if MBPD_judge1(f):
        return "Cannot decide"
    
    result = f()
    if result == "Halts":
        return "Halts"
    elif result == "Doesn't halt":
        return "Doesn't halt"

# MBPD2 (Maximally Broad Propositional Decider 2)
# Operates similarly to MBPD1, but is sensitive to a different pathological function.
def MBPD2(f):
    if MBPD_judge2(f):
        return "Cannot decide"
    
    result = f()
    if result == "Halts":
        return "Halts"
    elif result == "Doesn't halt":
        return "Doesn't halt"

# PPTM (Partially Probabilistic Turing Machine)
# Randomly chooses either MBPD1 or MBPD2 to decide if a function halts.
# If the chosen MBPD cannot decide, the PPTM continues the loop until a decision is made.
def PPTM(f):
    while True:
        roll = random.choice([MBPD1, MBPD2])
        result = roll(f)
        
        if result != "Cannot decide":
            return result

# Generates all possible pathological configurations up to a given length.
def pathological_simulations(x):
    pathologies = ['pathological_decider_1', 'pathological_decider_2']
    for length in range(1, x+1):
        for choices in itertools.product(pathologies, repeat=length):
            yield list(choices)

# The pathological function.
# Utilizes the list of choices to decide its behavior.
def pathological_decider():
    choices = pathological_decider.choices
    target = choices[-1]
    
    if target == 'pathological_decider_1':
        return "Halts"
    elif target == 'pathological_decider_2':
        return "Doesn't halt"

# Testing the PPTM against various pathological configurations.
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
