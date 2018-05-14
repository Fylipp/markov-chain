from fire import Fire
from numpy.random import choice


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
        probabilities = self.probabilities(left)
        rights = tuple(probabilities.keys())
        rights_probabilities = tuple(map(lambda r: probabilities[r], rights))

        return choice(rights, p=rights_probabilities)


def generate_markov_chain(text, depth):
    mc = MarkovChain()

    last_fragment = None
    for i in range(len(text) - depth + 1):
        fragment = text[i:i + depth]

        mc.add_occurrence(last_fragment, fragment)
        last_fragment = fragment

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
