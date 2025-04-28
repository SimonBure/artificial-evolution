import random
from rules import ALPHABET


class Genome:
    sequence: str
    length: int

    def __init__(self, sequence: str = "", length: int = 0):
        self.sequence = sequence
        self.length = length

    def __str__(self):
        return self.sequence

    def __getitem__(self, position: int) -> str:
        if isinstance(position, slice):
            pass
        else:
            if position < - self.length or position > self.length:
                raise IndexError(f"Index {position} out of genome bounds of length {self.length}")

        return self.sequence[position]

    def __len__(self) -> int:
        return self.length

    def __add__(self, other: 'Genome') -> 'Genome':
        return Genome(self.sequence + other.sequence)

    def random_init(self, length: int):
        self.length = length
        self.sequence = ''.join(random.choice(ALPHABET) for _ in range(length))

    def random_addition_one(self):
        position = random.randint(0, self.length - 1)
        char = random.choice(ALPHABET)

        self.sequence = self.sequence[:position] + char + self.sequence[position:]
        self.length += 1

    def random_addition(self, size: int):
        position = random.randint(0, self.length - 1)
        char = ''.join(random.choice(ALPHABET) for _ in range(size))

        self.sequence = self.sequence[:position] + char + self.sequence[position:]
        self.length += size

    def random_deletion_one(self):
        position = random.randint(0, self.length - 1)
        self.sequence = self.sequence[:position] + self.sequence[position + 1:]
        self.length -= 1

    def random_deletion(self, size: int):
        position = random.randint(0, self.length - size)
        self.sequence = self.sequence[:position] + self.sequence[position + size:]
        self.length -= size

    def random_substitution_one(self):
        position = random.randint(0, self.length - 1)
        char = random.choice(ALPHABET)
        self.sequence = self.sequence[:position] + char + self.sequence[position + 1:]

    def get_fraction(self, fraction: float, begin: bool = True) -> 'Genome':
        index_to_slice = int(fraction * self.length)

        if begin:
            return Genome(self.sequence[:index_to_slice])
        else:
            return Genome(self.sequence[-index_to_slice:])


    def combine_half_genomes(self, other: 'Genome') -> 'Genome':
        """ Combine two genomes by slicing them in half, then mixing them. """

        first_chosen = 0 if random.random() < 0.5 else 1

        if first_chosen == 0:
            new_genome = self.get_fraction(0.5, True) + other.get_fraction(0.5, False)
        else:
            new_genome = other.get_fraction(0.5, True) + self.get_fraction(0.5, False)

        new_genome.length = int(0.5 * (self.length + other.length))

        return new_genome


if __name__ == "__main__":
    random.seed(42)  # For reproducibility
    genome = Genome()
    genome.random_init(10)
    print(f"First Genome: {genome} of length {len(genome)}")
    print(genome.length)
    print(genome[:-5], len(genome[:-5]))
    print(genome.get_fraction(0.5, False))
    
    genome_bis = Genome()
    genome_bis.random_init(10)
    print(f"Second Genome: {genome_bis} of length {len(genome_bis)}")
    
    child_genome = genome.combine_half_genomes(genome_bis)
    print(f"Child Genome: {child_genome} of length {len(child_genome)}")
    
    child_genome.random_addition_one()
    print(f"Mutated child Genome: {child_genome} of length {len(child_genome)}")
    