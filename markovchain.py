from fire import Fire
from numpy.random import choice as np_choice
from random import choice as r_choice


class MarkovChain:
    def __init__(self):
        self._fragments = {}

    def add_occurrence(self, left, right):
        left_dict = self._fragments.get(left)

        if left_dict is None:
            left_dict = self._fragments[left] = {}

        occurrences = left_dict.get(right, 0)
        left_dict[right] = occurrences + 1

    def occurrences(self, left):
        return self._fragments[left] or {}

    def probabilities(self, left):
        occurrences = self.occurrences(left)
        total_occurrences = sum(occurrences.values())

        return {right: occurrences[right] / total_occurrences for right in occurrences.keys()}

    def next(self, left):
        if left is None:
            return r_choice(tuple(self._fragments.keys()))

        probabilities = self.probabilities(left)
        rights = tuple(probabilities.keys())
        rights_probabilities = tuple(map(lambda r: probabilities[r], rights))

        return np_choice(rights, p=rights_probabilities)


def generate_markov_chain(text, depth):
    mc = MarkovChain()

    for i in range(len(text) - depth - depth + 1):
        left = text[i:i + depth]
        right = text[i + depth:i + depth + depth]

        mc.add_occurrence(left, right)

    return mc


def generate(input_file, iterations=100, depth=5):
    with open(input_file) as file:
        src = file.read()

    mc = generate_markov_chain(src, depth)

    fragments = []
    last = None

    for i in range(iterations):
        last = mc.next(last)

        fragments.append(last)

    return ''.join(fragments)


if __name__ == '__main__':
    Fire(generate)
