import random
def initial_population():
    return [[ random.randint(0, noOfQueens-1) for _ in range(noOfQueens) ] for _ in range(100)]

###def random_gene(size): #making random genes 
###    return [ random.randint(1, noOfQueens) for _ in range(noOfQueens) ]

def score(gene):
    horizontal_collisions = sum([gene.count(queen)-1 for queen in gene])/2
    diagonal_collisions = 0

    n = len(gene)
    left_diagonal = [0] * 2*n
    right_diagonal = [0] * 2*n
    for i in range(n):
        left_diagonal[i + gene[i] - 1] += 1
        right_diagonal[len(gene) - i + gene[i] - 2] += 1

    diagonal_collisions = 0
    for i in range(2*n-1):
        counter = 0
        if left_diagonal[i] > 1:
            counter += left_diagonal[i]-1
        if right_diagonal[i] > 1:
            counter += right_diagonal[i]-1
        diagonal_collisions += counter / (n-abs(i-n+1))
    
    return int(maxScore - (horizontal_collisions + diagonal_collisions)) #28-(2+3)=23

def probability(gene, score):
    return score(gene) / maxScore

def random_pick(population, probabilities):
    populationWithProbabilty = zip(population, probabilities)
    total = sum(w for c, w in populationWithProbabilty)
    r = random.uniform(0, total)
    upto = 0
    for c, w in zip(population, probabilities):
        if upto + w >= r:
            return c
        upto += w
    assert False, "Shouldn't get here"
    
def reproduce(x, y): #doing cross_over between two genes
    n = len(x)
    c = random.randint(0, n - 1)
    return x[0:c] + y[c:n]

def mutate(x):  #randomly changing the value of a random index of a gene
    n = len(x)
    c = random.randint(0, n - 1)
    m = random.randint(0, n - 1)
    x[c] = m
    return x

def print_gene(pop):
    print("Gene = {},  Score = {}".format(str(pop), score(pop)))

def genetic_queen(population, score):
    mutation_probability = 0.03
    new_population = []
    probabilities = [probability(n, score) for n in population]
    for i in range(len(population)):
        x = random_pick(population, probabilities) #best gene 1
        y = random_pick(population, probabilities) #best gene 2
        child = reproduce(x, y) #creating two new genes from the best 2 genes
        if random.random() < mutation_probability:
            child = mutate(child)
        print_gene(child)
        new_population.append(child)
        if score(child) == maxScore: break
    return new_population

if __name__ == "__main__":
    noOfQueens = 8
    maxScore = (noOfQueens*(noOfQueens-1))/2  # 8*7/2 = 28
    population = initial_population()

    #print(population)
    generation = 1

    while not maxScore in [score(pop) for pop in population]:
        print("=== Generation {} ===".format(generation))
        population = genetic_queen(population, score)
        print("")
        print("Maximum Score = {}".format(max([score(n) for n in population])))
        generation += 1
    valid_sequence = []
    print("Solved in Generation {}!".format(generation-1))
    for pop in population:
        if score(pop) == maxScore:
            print("");
            print("One of the Valid Sequence: ")
            valid_sequence = pop
    
    print(valid_sequence)
                        
               