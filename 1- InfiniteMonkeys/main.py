import random

lstChars = list(range(97, 123))
lstChars.append(32)

lstPopulation = []

targetPhrase = "to be or not to be that is the question"


mutationRate = 0.03


def setup(popSize, phraseLength):
    global lstPopulation
    for p in range(popSize):
        strPhrase = ""
        for l in range(phraseLength):
            strPhrase += chr(random.choice(lstChars))
        lstPopulation.append(strPhrase)


def calcFitness(strPhrase):
    global targetPhrase
    score = 0
    for c in range(len(targetPhrase)):
        if strPhrase[c] == targetPhrase[c]:
            score += 1
    return score


def crossover(p1, p2):
    newMember = ""
    for i in range(len(p1)):
        if random.randint(0, 100) % 2 == 0:
            newMember += p1[i]
        else:
            newMember += p2[i]
    return newMember


def mutate(member):
    global mutationRate
    global lstChars
    strRet = ""
    for i in range(len(member)):
        if random.random() < mutationRate:
            strRet += chr(random.choice(lstChars))
        else:
            strRet += member[i]
    return strRet


def run():
    global lstPopulation
    global targetPhrase
    popSize = 1000
    setup(popSize, len(targetPhrase))
    generation = 0

    while targetPhrase not in lstPopulation:
        lstScores = []

        for member in lstPopulation:
            lstScores.append((calcFitness(member), member))

        lstScores.sort(key=lambda p: p[0])
        lstScores.reverse()

        print(
            f"Generation {generation} Best member: {lstScores[0][1]}    Score: {lstScores[0][0]}"
        )

        lstPopulation = []
        member = 0

        lstPopulation.append(lstScores[0][1])
        while len(lstPopulation) < popSize - 1:
            lstPopulation.append(
                mutate(crossover(lstScores[member][1], lstScores[member + 1][1]))
            )
            member += 1

        generation += 1
    if targetPhrase in lstPopulation:
        print(
            f"Generation {generation}: {lstPopulation[lstPopulation.index(targetPhrase)]}"
        )


if __name__ == "__main__":
    run()
