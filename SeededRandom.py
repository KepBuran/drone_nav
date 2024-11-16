import random

class SeededRandom:
    initial_seed = 0

    def __init__(self):
        self.seed = SeededRandom.initial_seed
        self._random = random.Random(self.seed)

    @staticmethod
    def set_initial_seed(seed):
        SeededRandom.initial_seed = seed

    def __getattr__(self, name):
        def method(*args, **kwargs):
            result = getattr(self._random, name)(*args, **kwargs)
            self.seed += 1
            self._random.seed(self.seed)
            return result
        return method
