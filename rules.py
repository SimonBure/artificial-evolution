MAX_GENOME_LENGTH = 100
MIN_GENOME_LENGTH = 1
MUTATION_PROBA = 0.01
ADDITION_PROBA = 0.01
DELETION_PROBA = 0.01
SUBSTITUTION_PROBA = 0.01
SEXUAL_REPRODUCTION_RATE = 0.5
SELF_REPRODUCTION_RATE = 0.5

ALPHABET = ('0', '1')

def compute_sequence_fitness(sequence: str) -> int:
    fitness = 0
    stored_1 = 0
    ones_in_a_row = 0
    stored_0 = 0
    zeros_in_a_row = 0
    
    for char in sequence:
        if char == '1':
            fitness += 1
            
            stored_1 += 1
            ones_in_a_row += 1
            zeros_in_a_row = 0
        else:
            
            
            stored_0 += 1
            zeros_in_a_row += 1
            ones_in_a_row = 0
            
    return fitness