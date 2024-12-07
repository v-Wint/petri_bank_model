import random, math

class RandomFunctions:
    @staticmethod
    def exponential(mean_t: float | int) -> float:
        return - mean_t * math.log(random.random())

    @staticmethod
    def uniform(mean_t: float | int, deviation_t: float | int) -> float:
        return mean_t + 2 * (random.random() - 0.5) * deviation_t

    @staticmethod
    def normal(mean_t: float | int, deviation_t: float | int) -> float:
        r = random.gauss(mean_t, deviation_t)
        return r if r >= 0 else RandomFunctions.normal(mean_t, deviation_t)

    @staticmethod
    def triang(low_t: float | int, high_t: float | int, mode_t: float | int) -> float:
        return random.triangular(low_t, high_t, mode_t)

