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
# This is to represent all possible deterministic representations of
# Our PPTM, since this exhaustive method is typically what is used
# To demonstrate equivalence (in adversarial cases, this does not hold).

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

#########################Another Example of Assymetry############################

# Deterministic Turing Machine (DTM)
# Note: The DTM can't call the PTM but can only emulate it. Here, the emulation is simplistic and deterministic.
def DTM(emulated_opponent_behavior, mode):
    def self_output(x):
        return x

    if mode == "Offense":
        # Tries to predict the number the opponent will output while on defense
        # Note: emulated_opponent_behavior should be a deterministic representation of the PTM's behavior
        return emulated_opponent_behavior("Defense")
    else:
        for x in range(1, 101):
            # Checks if the emulated opponent would correctly guess x
            if emulated_opponent_behavior("Offense") == x:
                continue
            else:
                return x

# Probabilistic Turing Machine (PTM)
def PTM(opponent_func, mode):
    def self_output(x):
        return x

    if mode == "Offense":
        while True:
            # Randomly selects a number and checks if it matches the opponent's defense output
            x = random.randint(1, 100)
            if opponent_func(self_output, "Defense") == x:
                return x
    else:
        while True:
            x = random.randint(1, 100)
            if opponent_func(lambda: x, "Offense") == x:
                continue
            else:
                return x

# Emulated behavior of PTM as understood by DTM
# This function needs to be deterministic
def emulated_PTM_behavior(mode):
    # Simplified deterministic behavior; in reality, this would be far more complex
    return 42 if mode == "Defense" else 84

# Example usage
DTM_result = DTM(emulated_PTM_behavior, "Offense")
PTM_result = PTM(DTM, "Offense")

print("DTM on Offense:", DTM_result)
print("PTM on Offense:", PTM_result)
