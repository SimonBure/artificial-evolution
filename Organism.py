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
        new_genome = self.genome + "Y"
        return Organism(new_genome)
    
    def mutate(self) -> 'Organism':
        # Introduce a mutation in the genome
        mutated_genome = self.genome + "X"
        