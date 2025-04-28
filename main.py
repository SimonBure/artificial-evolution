import tqdm

from Organism import Organism

if __name__ == "__main__":
    organisms: list[Organism] = []
    iterations_nb: int = 10

    for i in tqdm(range(iterations_nb)):
        fitnesses = [0] * len(organisms)
        for i, o in enumerate(organisms):
            fitnesses[i] = o.compute_fitness()
