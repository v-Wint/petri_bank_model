from elements import Place, Transition
from random_functions import RandomFunctions as rf
from model import Model


class StandardModel(Model):
    def __init__(
        self,
        first_auto_line_capacity = 3,
        second_auto_line_capacity = 4,
        indoors_line_capacity = 7,
        first_cashier_time = lambda: rf.normal(0.5, 0.25),
        second_cashier_time = lambda: rf.uniform(0.6, 0.4),
        indoors_cashier_time = lambda: rf.triang(0.1, 1.2, 0.4),
        indoors_cashiers = 2,
        auto_generator_time = lambda: rf.exponential(0.75),
        indoors_generator_time = lambda: rf.exponential(0.5),
        indoors_cashier_delay_time = lambda: 60
) -> None:
        p0 = Place('p0', 1)
        auto_generator = Transition('Надходження до авт. касирів', auto_generator_time)
        to_auto_lines = Place('До авт. касирів')

        first_auto_line_entry = Transition('Надходження до 1 авт. черги', priority=1, probability=0.5)
        first_auto_line_free_places = Place('Кількість вільних місць у 1 авт. черзі', first_auto_line_capacity)
        first_auto_line = Place('Черга до 1 авт. касира')
        first_auto_line_exit = Transition('Вихід з черги 1 авт. касира')
        first_auto_cashier_free = Place('1 авт. касир вільний', 1)
        first_auto_cashier_entry = Place('Вхід до 1 авт. касира')
        first_auto_cashier_serve = Transition('Обслуговування 1 авт. касиром', first_cashier_time)
        first_auto_cashier_served = Place('Кількість обслугованих 1 авт. касиром')

        second_auto_line_entry = Transition('Надходження до 2 авт. черги', priority=1, probability=0.5)
        second_auto_line_free_places = Place('Кількість вільних місць у 2 авт. черзі', second_auto_line_capacity)
        second_auto_line = Place('Черга до 2 авт. касира')
        second_auto_line_exit = Transition('Вихід з черги 2 авт. касира')
        second_auto_cashier_free = Place('2 авт. касир вільний', 1)
        second_auto_cashier_entry = Place('Вхід до 2 авт. касира')
        second_auto_cashier_serve = Transition('Обслуговування 2 авт. касиром', second_cashier_time)
        second_auto_cashier_served = Place('Кількість обслугованих 2 авт. касиром')

        auto_generator.add_inplace(p0)
        auto_generator.add_outplace(p0)
        auto_generator.add_outplace(to_auto_lines)

        first_auto_line_entry.add_inplace(to_auto_lines)
        first_auto_line_entry.add_inplace(first_auto_line_free_places)
        first_auto_line_entry.add_outplace(first_auto_line)

        first_auto_line_exit.add_inplace(first_auto_line)
        first_auto_line_exit.add_inplace(first_auto_cashier_free)
        first_auto_line_exit.add_outplace(first_auto_line_free_places)
        first_auto_line_exit.add_outplace(first_auto_cashier_entry)

        first_auto_cashier_serve.add_inplace(first_auto_cashier_entry)
        first_auto_cashier_serve.add_outplace(first_auto_cashier_free)
        first_auto_cashier_serve.add_outplace(first_auto_cashier_served)


        second_auto_line_entry.add_inplace(to_auto_lines)
        second_auto_line_entry.add_inplace(second_auto_line_free_places)
        second_auto_line_entry.add_outplace(second_auto_line)

        second_auto_line_exit.add_inplace(second_auto_line)
        second_auto_line_exit.add_inplace(second_auto_cashier_free)
        second_auto_line_exit.add_outplace(second_auto_line_free_places)
        second_auto_line_exit.add_outplace(second_auto_cashier_entry)

        second_auto_cashier_serve.add_inplace(second_auto_cashier_entry)
        second_auto_cashier_serve.add_outplace(second_auto_cashier_free)
        second_auto_cashier_serve.add_outplace(second_auto_cashier_served)

        p1 = Place('p1', 1)
        indoors_generator = Transition('Надходження до касирів у приміщенні', indoors_generator_time)
        to_indoors_lines = Place('До касирів у приміщенні')

        indoors_line_entry = Transition('Надходження до черги в приміщенні', priority=1)
        indoors_line_free_places = Place('Кількість вільних місць у черзі в приміщенні', indoors_line_capacity)
        indoors_line = Place('Черга до касирів у приміщенні')
        indoors_line_exit = Transition('Вихід з черги до касирів у приміщенні')
        indoors_cashier_free = Place('Вільних касирів у приміщенні')
        indoors_cashier_entry = Place('Вхід до касирів у приміщенні')
        indoors_cashier_serve = Transition('Обслуговування касирами у приміщенні', indoors_cashier_time)
        indoors_cashier_served = Place('Кількість обслугованих касирами у приміщенні')

        indoors_generator.add_inplace(p1)
        indoors_generator.add_outplace(p1)
        indoors_generator.add_outplace(to_indoors_lines)

        indoors_line_entry.add_inplace(to_indoors_lines)
        indoors_line_entry.add_inplace(indoors_line_free_places)
        indoors_line_entry.add_outplace(indoors_line)

        indoors_line_exit.add_inplace(indoors_line)
        indoors_line_exit.add_inplace(indoors_cashier_free)
        indoors_line_exit.add_outplace(indoors_line_free_places)
        indoors_line_exit.add_outplace(indoors_cashier_entry)

        indoors_cashier_serve.add_inplace(indoors_cashier_entry)
        indoors_cashier_serve.add_outplace(indoors_cashier_free)
        indoors_cashier_serve.add_outplace(indoors_cashier_served)

        p2 = Place('p2', 1)
        indoors_cashier_delay = Transition('Затримка перед початком роботи', indoors_cashier_delay_time)
        indoors_cashier_delay.add_inplace(p2)
        indoors_cashier_delay.add_outplace(indoors_cashier_free, indoors_cashiers)

        transfer_indoors = Transition('Перехід до приміщення')
        transfer_indoors.add_inplace(to_auto_lines)
        transfer_indoors.add_outplace(to_indoors_lines)

        lost = Place('Втрачено')
        transfer_lost = Transition('Вихід з банку')
        transfer_lost.add_inplace(to_indoors_lines)
        transfer_lost.add_outplace(lost)


        ts = [
            auto_generator,
            first_auto_line_entry, first_auto_line_exit, first_auto_cashier_serve,
            second_auto_line_entry, second_auto_line_exit, second_auto_cashier_serve,
            indoors_generator,
            indoors_line_entry, indoors_line_exit, indoors_cashier_serve,
            indoors_cashier_delay, transfer_indoors, transfer_lost
        ]

        ps = [
            p0, to_auto_lines,
            first_auto_line_free_places, first_auto_line, first_auto_cashier_free, first_auto_cashier_entry, first_auto_cashier_served,
            second_auto_line_free_places, second_auto_line, second_auto_cashier_free, second_auto_cashier_entry, second_auto_cashier_served,
            p1, to_indoors_lines,
            indoors_line_free_places, indoors_line, indoors_cashier_free, indoors_cashier_entry, indoors_cashier_served,
            p2, lost

        ]

        self.m11 = first_auto_cashier_serve
        self.m12 = second_auto_cashier_serve
        self.m2 = indoors_cashier_serve

        self.q11 = first_auto_line
        self.q12 = second_auto_line
        self.q2 = indoors_line

        self.n11 = first_auto_cashier_served
        self.n12 = second_auto_cashier_served
        self.n2 = indoors_cashier_served
        self.n0 = lost

        self.indoors_cashiers = indoors_cashiers

        super().__init__(ps, ts)

    def _calc_stats(self) -> dict[str, float]:
        """Calculate output vars"""
        result = {}
        result["First auto cashier mean load time"] = self.m11.mean
        result["Second auto cashier mean load time"] = self.m12.mean
        result["Indoors cashiers mean load time"] = self.m2.mean / self.indoors_cashiers
        result["First auto line mean size"] = self.q11.mean
        result["Second auto line mean size"] = self.q12.mean
        result["Indoors line mean size"] = self.q2.mean
        result["Lose probability"] = self.n0.n / (self.n0.n + self.n11.n + self.n12.n + self.n2.n)
        return result

