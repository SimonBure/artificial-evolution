import random
import tqdm
import os

from Organism import Organism
from Genome import Genome
from rules import fitness_to_probability, REMOVED_FRACTION, SEXUAL_REPRODUCTION_PROBA


def compute_organisms_fitnesses(organisms: list[Organism]) -> list[int]:
    fitnesses = [0] * len(organisms)
    for i, o in enumerate(organisms):
        fitnesses[i] = o.compute_fitness()
    return fitnesses


def choose_mate(organism: Organism, organisms: list[Organism], probabilities: list[float]) -> Organism:
    chosen_mate = random.choices(organisms, probabilities)

    # Auto-sexual reproduction is not allowed
    while chosen_mate is organism:
        chosen_mate = random.choices(organisms, probabilities)

    return chosen_mate

def remove_organisms_from_fitnesses(organisms: list[Organism], fitnesses: list[int], fraction_removed: float) -> tuple[list[Organism], list[int]]:
    # Pair organisms with their fitness values
    organism_fitness_pairs = list(zip(organisms, fitnesses))

    # Sort pairs by fitness (ascending order)
    sorted_pairs = sorted(organism_fitness_pairs, key=lambda pair: pair[1])

    # Calculate how many organisms to remove
    num_to_remove = int(len(organisms) * fraction_removed)

    # Return only the organisms with higher fitness values
    return [org for org, _ in sorted_pairs[num_to_remove:]], [fit for _, fit in sorted_pairs[num_to_remove:]]


def display_and_save_best_sequences(organisms: list[Organism], fitnesses: list[int], percentage: float,
                                    filename: str = "best_sequences.txt") -> None:
    organism_fitness_pairs = list(zip(organisms, fitnesses))

    # Sort pairs by fitness (descending order)
    sorted_pairs = sorted(organism_fitness_pairs, key=lambda pair: pair[1], reverse=True)

    # Calculate how many organisms to display and save
    num_to_display = max(1, int(len(organisms) * percentage))

    # Get the best organisms
    best_pairs = sorted_pairs[:num_to_display]

    # Display the best sequences
    print(f"\nTop {percentage*100:.0f}% best sequences:")
    for i, (org, fitness) in enumerate(best_pairs):
        print(f"  Rank {i+1}: Genome={org.genome}, Fitness={fitness}")

    # Save the best sequences to a file
    with open(filename, 'w') as f:
        f.write(f"Rank, Genome, Length, Fitness\n")
        for i, (org, fitness) in enumerate(best_pairs):
            f.write(f"{i+1}, {org.genome}, {org.genome.length}, {fitness}\n")

    print(f"\nBest sequences saved to {os.path.abspath(filename)}")


if __name__ == "__main__":
    # Initialize a population of organisms
    population_size = 10
    organisms: list[Organism] = []

    env_variance = 0.2

    for _ in range(population_size):
        genome = Genome()
        genome.random_init(random.randint(5, 20))  # Random genome length between 5 and 20
        organisms.append(Organism(genome))

    iterations_nb: int = 10

    for i in tqdm.tqdm(range(iterations_nb)):
        # Compute fitness for each organism
        fitnesses = compute_organisms_fitnesses(organisms)

        # Simulate a varying environment
        fraction_removed = random.gauss(REMOVED_FRACTION, env_variance)

        # Remove organisms with lowest fitness
        organisms, fitnesses = remove_organisms_from_fitnesses(organisms, fitnesses, fraction_removed)
        mating_probabilities = fitness_to_probability(fitnesses)

        # Reproduce the remaining organisms
        for org in organisms:
            # Decide on reproduction method based on probabilities from rules.py
            # If there is only one organism remaining, don't allow sexual reproduction
            if len(organisms) != 1 and random.random() < SEXUAL_REPRODUCTION_PROBA:
                mate = choose_mate(org, organisms, mating_probabilities)
                offspring = org.sexual_reproduction(mate)
            else:
                offspring = org.self_reproduction()
                # Always mutate offspring from asexual reproduction
                # Randomly choose between addition, deletion, or substitution
                offspring = offspring.mutate()

            organisms.append(offspring)

            print(f"Iteration {i}:")
            for j, (org, fit) in enumerate(zip(organisms, fitnesses)):
                print(f"  Organism {j}: Genome={org.genome}, Fitness={fit}")

    # After all iterations, compute final fitness values
    final_fitnesses = compute_organisms_fitnesses(organisms)

    # Display and save the best sequences (top 20%)
    display_and_save_best_sequences(organisms, final_fitnesses, 0.2)
