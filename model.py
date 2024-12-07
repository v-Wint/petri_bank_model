from typing import Optional
from elements import Place, Transition, Numeric
import random
from csv_saver import CSVSaver


class Model:
    """Petri net model"""
    def __init__(self, places: list[Place], transitions: list[Transition]) -> None:
        self.ps = places
        self.ts = transitions
        self.curr_t, self.next_t = 0., 0.

    def simulate(self,
                 sim_time: Numeric,
                 warmup_time: Numeric = 0,
                 is_protocol: bool = True,
                 is_result: bool = True) -> dict[str, float]:
        """
        Perform Petri net simulation with given warmup and simulation time

        Parameters
        ----------
        sim_time : Numeric
            time of simulation after warmup if specified
        warmup_time: Numeric
            time of warmup, no warmup is performed when 0
        is_protocol: bool
            whether to output protocol
        is_result: bool
            whether to output simulation results

        Returns
        -------
        dict[str, float]
            simulation results in the form of ditionary with keys the names
            of output variables and values the output variables values
        """

        if warmup_time:
            self._warmup(warmup_time)

        self._simulate_part(sim_time + warmup_time, warmup_time, is_protocol)

        result = self._calc_stats()

        if is_result: self._print_stats(result)

        return result


    def simulate_intervals(self,
                           sim_time: Numeric,
                           interval: Numeric,
                           warmup_time: Numeric = 0,
                           name: Optional[str] = None) -> None:
        """
        Perform Petri net simulation saving the statistical data after each interval time pass into csv

        Parameters
        __________
        sim_time : Numeric
            time of experiment after warmup if specified
        interval : Numeric
            time of the intervals between statistical data calculations
        warmup_time: Numeric
            warmup time to adjust statistical information gathering
        """

        filename = f"{name if name else self.__class__.__name__}-result.csv"
        CSVSaver.create_clear_file(filename)

        if warmup_time:
            self._warmup(warmup_time)

        current = warmup_time + interval

        while current <= sim_time + warmup_time:
            print(current - warmup_time)
            self._simulate_part(current, warmup_time, False, True)
            stats = self._calc_stats()
            CSVSaver.save(filename, [current - warmup_time] + list(stats.values()))
            self._print_stats(self._calc_stats())
            current += interval

    def _warmup(self, warmup_time: Numeric) -> None:
        """Perform warmup before gathering stats of the model"""
        self._simulate_part(warmup_time, is_protocol=False, is_stats=False)

    def _simulate_part(self,
                       max_time: Numeric,
                       warmup_adjustment: Numeric = 0,
                       is_protocol: bool = True,
                       is_stats: bool = True) -> None:
        """
        Change the state of the model by performing simulation from current state up to max_time

        Parameters
        ----------
        max_time: Numeric
            time to which change the state of the model
        warmup_adjustment: Numeric
            warmup time to adjust statistical information gathering
        is_protocol: bool
            whether to output protocol
        is_result: bool
            whether to gather statistical information
        """
        while self.curr_t < max_time:
            self._input(is_protocol)
            self.next_t = self._find_next_t(is_protocol)
            if is_stats: self._update_stats(warmup_adjustment)
            self.curr_t = self.next_t
            self._output(is_protocol)

    def _input(self, is_protocol: bool = False) -> None:
        """Perform repetative input of model's transitions solving conflicts until no transition is enabled"""
        enabled = [t for t in self.ts if t.enabled]

        if is_protocol: self._print_enabled(enabled)

        while enabled:
            maximum = max(f.priority for f in enabled)
            enabled = [f for f in enabled if f.priority == maximum]
            t = random.choices(enabled, weights=[f.probability for f in enabled])[0]
            if is_protocol: print("Chose", t)
            t.input(self.curr_t)
            enabled = [t for t in self.ts if t.enabled]

        if is_protocol: self._print_state("\nInput result")

    def _find_next_t(self, is_protocol) -> float:
        """Find the nearest otuput time among model's transitions"""
        next_el = min(self.ts, key=lambda e: e.next_t)
        next_t = next_el.next_t

        if is_protocol: print(f"It's time for event in {next_el}, time = {next_t}")

        return next_t

    def _update_stats(self, warmup_adjustment: Numeric) -> None:
        """Update statistical information of the model's elements"""
        for e in self.ts + self.ps:
            e.update_stats(self.curr_t - warmup_adjustment, self.next_t - warmup_adjustment)

    def _output(self, is_protocol: bool = False) -> None:
        """Perform repetative output of model's transitions"""
        for t in self.ts:
            if t.next_t == self.curr_t:
                t.output(self.curr_t)

        if is_protocol: self._print_state("\nOutput result")

    def _calc_stats(self) -> dict[str, float]:
        """Calculate current statistical data of elements"""
        stats = {}
        for t in self.ts:
            stats[f"Transition {t.name} mean load"] = t.mean
        for p in self.ps:
            stats[f"Place {p.name} mean marking"] = p.mean
            stats[f"Place {p.name} current marking"] = p.n
        return stats

    def _print_state(self, heading: Optional[str] = None) -> None:
        """Print current state of the model"""
        if heading: print(heading)
        print("\n".join(f"{p} n = {p.n}" for p in self.ps))
        print("\n".join(f"{t} next_ts = {t.next_ts}" for t in self.ts))
        print()

    def _print_enabled(self, enabled: list[Transition]) -> None:
        """Print current state of enabled transitions"""
        if enabled:
            print("Enabled transitions:")
            print("\n".join(f"{t} {t.priority} {t.probability}" for t in enabled))
        else:
            print("No enabled transitions")

    def _print_stats(self, result: dict[str, float]) -> None:
        """Print the statistical data of eleents"""
        print("-------------RESULT---------------")
        for k, v in result.items():
            print(k, '=', v)

