import base64
import random

pop_size = 100
ec = 20
mr = 0.3  # Mutation rate is fairly large in this case, but works well

dic = {}
for i in range(1, 17):
    s = "a" * i
    for _ in range(i):
        s = base64.b64encode(s.encode()).decode()
    dic[len(s)] = i


with open("4 - DecodeGA/encoded_flag.txt", "r") as f:
    enc = f.read()

choices = list(dic.keys())
# Keys: [4, 8, 12, 24, 32, 44, 80, 108, 144, 256, 344, 460, 800, 1068, 1424, 1960]
# Values: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]


run = True


def init():
    pop = []
    for i in range(pop_size):
        individual = [random.choice(choices) for _ in range(8)]
        pop.append(individual)

    return pop


def mutate(individual):
    for i in range(len(individual)):
        if random.random() <= mr:
            individual[i] = random.choice(choices)


def crossover(population):
    new_gen = []
    for s in range(ec):
        new_gen.append(population[s][1])

    index = 0
    while len(new_gen) != pop_size:
        p1 = population[index][1]
        index += 1

        p2 = population[index][1]
        k_point = random.randint(1, len(p1) - 1)  # one point crossover

        off1 = p1[:k_point] + p2[k_point:]
        off2 = p2[:k_point] + p1[k_point:]

        mutate(off1)
        mutate(off2)

        new_gen.append(off1)
        new_gen.append(off2)

    return new_gen


population = init()
while run:

    score_count = (
        []
    )  # this is just a quick and dirty way to keep score associated with individuals
    max_score = 0
    max_flag = ""
    for individual in population:
        flag = b""
        try:
            # try to decode the password
            index = 0
            for i in range(len(individual)):
                l = individual[i]
                seg = enc[index : index + l]
                for _ in range(dic[l]):
                    seg = base64.b64decode(seg)
                flag += seg
                index += l

            # Evaluate the fitness of the individual by comparing the decoded flag to known criteria
            score = 0
            flag = flag.decode()
            if flag[0] == "C":  # starts with C
                score += 1
            if flag[1] == "T":  # second letter is T
                score += 1
            if flag[2] == "F":  # third letter F
                score += 1
            if flag[3] == "{":  # 4th character {
                score += 1
            if flag.endswith("}"):  # ends wih }
                score += 1
            if flag.startswith(
                "CTF{"
            ):  # bonus points if it matches all of the known criteria
                score += 5
            if len(flag) == 21:  # points for being the right length
                score += 1

            if score == 11:
                print(flag)
                run = False
            if score > max_score:
                print(f"new high score: {score}| {flag}")
                max_score = score
                max_flag = flag
        except:
            score = -10

        score_count.append((score, individual))
    score_count.sort(key=lambda s: s[0], reverse=True)

    population = crossover(score_count)


# Given info
# Starts with CTF{
# Ends with }
# len(lengths) = 8
# len(flag) = 21
