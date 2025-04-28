import random

from Genome import Genome
from rules import ADDITION_PROBA, DELETION_PROBA, SUBSTITUTION_PROBA, compute_sequence_fitness

class Organism:
    genome: Genome
    fitness: int

    def __init__(self, genome: Genome):
        self.genome = genome

    def __str__(self):
        return self.genome

    def compute_fitness(self) -> int:
        return compute_sequence_fitness(self.genome.sequence)

    def sexual_reproduction(self, other: 'Organism') -> 'Organism':
        combined_genome = self.genome.combine_half_genomes(other.genome)
        return Organism(combined_genome)

    def self_reproduction(self) -> 'Organism':
        new_genome = Genome(self.genome.sequence, self.genome.length)
        return Organism(new_genome)

    def mutate(self) -> 'Organism':
        # Create a copy of the genome
        mutated_genome = Genome(self.genome.sequence, self.genome.length)

        # Randomly choose mutation type with equal probability
        mutation_type = random.random()

        if mutation_type < 1/3:
            # Add a random character
            mutated_genome.random_addition_one()
        elif mutation_type < 2/3 and mutated_genome.length > 1:
            # Delete a random character (only if genome length > 1)
            mutated_genome.random_deletion_one()
        else:
            # Substitute a random character
            mutated_genome.random_substitution_one()

        return Organism(mutated_genome)
