from standard_model import StandardModel
from extended_model import ExtendedModel
from elements import Numeric
from random_functions import RandomFunctions as rf
from csv_saver import CSVSaver


class Experiment:
    @staticmethod
    def run_standard(time: Numeric) -> dict[str, float]:
        """Run standard model simulation one time"""
        return StandardModel().simulate(time)

    @staticmethod
    def run_extended(time: Numeric) -> dict[str, float]:
        """Run extended model simulation one time"""
        return ExtendedModel().simulate(time)

    @staticmethod
    def verify(time: Numeric) -> None:
        """Perform model verification saving results to verification.csv"""
        PARAMS = [
            3, 4, 7, 0.5, 0.6, 0.4, 2, 0.75, 0.5, 60
        ]
        params = list(PARAMS)
        print("Params", params)
        CSVSaver.save("verification.csv", params + list(Experiment.run_params(time, params).values()))
        for i in range(len(params)):
            params = list(PARAMS)
            if i < 3:
                params[i] = params[i] / 3 if isinstance(params[i], float) else params[i] // 3
            else:
                params[i] = params[i] / 2 if isinstance(params[i], float) else params[i] // 2
            print("Params", params)
            CSVSaver.save("verification.csv", params + list(Experiment.run_params(time, params).values()))

            params = list(PARAMS)
            if i < 3:
                params[i] *= 3
            else:
                params[i] *= 2
            print("Params", params)
            CSVSaver.save("verification.csv", params + list(Experiment.run_params(time, params).values()))

    @staticmethod
    def run_intervals(sim_time: Numeric, warmup_time: Numeric, interval: Numeric, name: str) -> None:
        """Run model outputing and saving stats every interval time"""
        for i in range(21):
            ExtendedModel().simulate_intervals(sim_time, interval, warmup_time, f'{name}-{i}')

    @staticmethod
    def experiment(sim_time: Numeric, warmup_time: Numeric) -> None:
        """Run model simulations 20 times and save the results into standard.csv and extended.csv files"""
        for i in range(1, 21):
            CSVSaver.save("standard.csv", [i] + list(StandardModel().simulate(sim_time, warmup_time, False).values()))
        for i in range(1, 21):
            CSVSaver.save("extended.csv", [i] + list(ExtendedModel().simulate(sim_time, warmup_time, False).values()))

    @staticmethod
    def run_improved_standard(sim_time: Numeric, warmup_time: Numeric = 0):
        StandardModel(indoors_cashier_delay_time=lambda:0, indoors_cashiers=3).simulate(sim_time, warmup_time, False)

    @staticmethod
    def run_improved_extended(sim_time: Numeric, warmup_time: Numeric = 0):
        ExtendedModel(indoors_cashier_delay_time=lambda:0, indoors_cashiers=3).simulate(sim_time, warmup_time, False)

    @staticmethod
    def run_params(time: Numeric, params: list) -> dict[str, float]:
        """Run model with given params list"""
        return StandardModel(
            first_auto_line_capacity = params[0],
            second_auto_line_capacity = params[1],
            indoors_line_capacity = params[2],
            first_cashier_time = lambda: rf.normal(params[3], 0.25),
            second_cashier_time = lambda: rf.uniform(params[4], 0.4),
            indoors_cashier_time = lambda: rf.triang(0.1, 1.2, params[5]),
            indoors_cashiers = params[6],
            auto_generator_time = lambda: rf.exponential(params[7]),
            indoors_generator_time = lambda: rf.exponential(params[8]),
            indoors_cashier_delay_time = lambda: params[9]
        ).simulate(time, is_protocol=False)

    @staticmethod
    def main() -> None:
        Experiment.run_standard(1000)
        Experiment.run_extended(1000)

        Experiment.verify(5000)

        Experiment.run_intervals(50_000, 0, 200, 'basic')
        Experiment.run_intervals(50_000, 2500, 200, 'updated')
        Experiment.experiment(15000, 2500)
        Experiment.run_improved_standard(15_000)
        Experiment.run_improved_extended(15_000)


if __name__ == '__main__':
    Experiment.main()

