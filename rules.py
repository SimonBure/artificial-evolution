import math

MAX_GENOME_LENGTH = 100
MIN_GENOME_LENGTH = 1
MUTATION_PROBA = 0.01
ADDITION_PROBA = 0.01
DELETION_PROBA = 0.01
SUBSTITUTION_PROBA = 0.01
SEXUAL_REPRODUCTION_PROBA = 0.1
SELF_REPRODUCTION_PROBA = 1 - SEXUAL_REPRODUCTION_PROBA
REMOVED_FRACTION = 0.4

ALPHABET = ('0', '1')

def fitness_to_probability(fitnesses: list[int]) -> list[float]:

    # Handle the case where all fitnesses are the same
    if all(f == fitnesses[0] for f in fitnesses):
        return [1.0 / len(fitnesses)] * len(fitnesses)

    # Apply softmax function
    exp_fitnesses = [math.exp(f) for f in fitnesses]
    sum_exp_fitnesses = sum(exp_fitnesses)

    return [ef / sum_exp_fitnesses for ef in exp_fitnesses]


def sliding_symmetry_score(sequence: str, window_size: int = 6) -> float:
    score = 0
    comparisons = 0
    for i in range(len(sequence) - window_size + 1):
        sub_seq = sequence[i:i+window_size]
        half = window_size // 2
        for j in range(half):
            if sub_seq[j] == sub_seq[-(j+1)]:
                score += 1
            comparisons += 1
    return score / comparisons if comparisons else 0


def compute_sequence_fitness(sequence: str) -> int:
    fitness = 0
    penalty = 0

    stored_1 = 0
    ones_in_a_row = 0
    stored_0 = 0
    zeros_in_a_row = 0

    for char in sequence:
        if char == '1':
            stored_1 += 1
            ones_in_a_row += 1
            zeros_in_a_row = 0

            fitness += max(1, ones_in_a_row)
        else:
            stored_0 += 1
            zeros_in_a_row += 1
            ones_in_a_row = 0

            fitness += min(0, - zeros_in_a_row)

    penalty = len(sequence)

    # Big fitness bonus if sequence is a palindrome
    if sequence == sequence[::-1]:
        fitness += 10

    return fitness - penalty
