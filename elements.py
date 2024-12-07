from typing import Callable, Union

Numeric = Union[int, float]

class Element:
    """Parent class for Petri net elements"""
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.mean: float = 0.

    def update_stats(self, curr_t: float, next_t: float) -> None:
        """Upate the element's statistical data"""
        pass

    def update_mean(self, value: Numeric, curr_t: float, next_t: float) -> None:
        """Update the mean of the given value"""
        self.mean += (value - self.mean) * (next_t - curr_t) / next_t if next_t else 0

    def __repr__(self) -> str:
        return self.name


class Place(Element):
    """Petri place class"""
    def __init__(self, name: str, n: int = 0) -> None:
        super().__init__(name)
        self.n: int = n

    def update_stats(self, curr_t: float, next_t: float) -> None:
        """Update mean marking"""
        self.update_mean(self.n, curr_t, next_t)


class Transition(Element):
    """Petri transition class"""
    def __init__(self,
                 name: str,
                 delay_func: Callable[[], float] = lambda: 0.,
                 priority: int = 0,
                 probability: float = 1.) -> None:
        super().__init__(name)
        self.get_delay: Callable[[], Numeric] = delay_func
        self.priority: int = priority
        self.probability: float = probability

        self.inplaces: dict[Place, int] = {}
        self.outplaces: dict[Place, int] = {}

        self.__next_ts: list[float] = []

    def add_inplace(self, inplace: Place, k: int = 1):
        """Add inplace with given k (default 1) """
        self.inplaces[inplace] = k

    def add_outplace(self, outplace: Place, k: int = 1):
        """Add outplace with given k (default 1) """
        self.outplaces[outplace] = k

    @property
    def enabled(self) -> bool:
        """Check whether is enabled"""
        for p, k in self.inplaces.items():
            if p.n < k:
                return False
        return True

    @property
    def next_t(self) -> float:
        """Get the nearest time of output"""
        match len(self.__next_ts):
            case 0:
                return float('inf')
            case 1:
                return self.__next_ts[0]
            case _:
                return min(self.__next_ts)

    @property
    def next_ts(self) -> list[float]:
        """Get the nearest times of output"""
        return self.__next_ts

    def input(self, curr_t: float) -> None:
        """Input markings according to inplaces once"""
        for p, k in self.inplaces.items():
            p.n -= k
        self.__next_ts += curr_t + self.get_delay(),

    def output(self, next_t: float) -> None:
        """Output markings according to outplaces until next_t is not among times of output"""
        while next_t in self.__next_ts:
            for p, k in self.outplaces.items():
                p.n += k
            self.__next_ts.remove(next_t)

    def update_stats(self, curr_t: float, next_t: float) -> None:
        """Update the mean load"""
        self.update_mean(len(self.__next_ts), curr_t, next_t)

