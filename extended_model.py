from elements import Place, Transition, Numeric
from random_functions import RandomFunctions as rf
from model import Model


class ExtendedModel(Model):
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
        indoors_cashier_delay_time = lambda: 60,
        questioning_time = lambda: rf.uniform(3.5, 1.5),
        refusal_time = lambda: rf.exponential(10),
        issuance_time = lambda: rf.exponential(5),
        obtaining_time = lambda: 1,
        new_clients_percentage = 0.1,
        refusal_percentage = 0.05
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

        # --------------------------------------------------------------------
        p1 = Place('p1', 1)
        indoors_generator = Transition('Надходження до касирів у приміщенні', indoors_generator_time)
        indoors_clients = Place('Клієнти що надходять в приміщення')

        standard_client = Transition('Звичайни клієнт', probability=1 - new_clients_percentage)
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
        indoors_generator.add_outplace(indoors_clients)

        standard_client.add_inplace(indoors_clients)
        standard_client.add_outplace(to_indoors_lines)

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


        new_client = Transition('Новий клієнт', probability=new_clients_percentage)
        manager_line = Place('Черга до управителя')
        manager_free = Place('Управитель вільний', 1)
        questioning = Transition('Опитування', questioning_time)
        questioned = Place('Опитані')
        to_refusal = Transition('На відмову', probability=refusal_percentage)
        to_loan_issuance = Transition('На оформлення', probability=1 - refusal_percentage)
        refusal_line = Place('На відмову')
        loan_issuance_line = Place('На оформлення')
        refusal = Transition('Відмова', refusal_time)
        loan_issuance = Transition('Оформлення кредиту', issuance_time)
        to_card_obtaining = Place('На видачу')
        card_obtaining = Transition('Видача', obtaining_time, priority=1)
        to_returning = Place('На повернення')
        returning = Transition('Поверення', priority=1)


        new_client.add_inplace(indoors_clients)
        new_client.add_outplace(manager_line)

        questioning.add_inplace(manager_line)
        questioning.add_inplace(manager_free)
        questioning.add_outplace(questioned)
        questioning.add_outplace(manager_free)

        to_refusal.add_inplace(questioned)
        to_refusal.add_outplace(refusal_line)

        to_loan_issuance.add_inplace(questioned)
        to_loan_issuance.add_outplace(loan_issuance_line)

        refusal.add_inplace(refusal_line)
        refusal.add_inplace(manager_free)
        refusal.add_outplace(lost)
        refusal.add_outplace(manager_free)

        loan_issuance.add_inplace(loan_issuance_line)
        loan_issuance.add_outplace(to_card_obtaining)

        card_obtaining.add_inplace(to_card_obtaining)
        card_obtaining.add_inplace(manager_free)
        card_obtaining.add_outplace(to_returning)
        card_obtaining.add_outplace(manager_free)

        returning.add_inplace(to_returning)
        returning.add_inplace(indoors_line_free_places)
        returning.add_outplace(indoors_line)

        ts = [
            auto_generator,
            first_auto_line_entry, first_auto_line_exit, first_auto_cashier_serve,
            second_auto_line_entry, second_auto_line_exit, second_auto_cashier_serve,
            indoors_generator,
            indoors_line_entry, indoors_line_exit, indoors_cashier_serve,
            indoors_cashier_delay, transfer_indoors, transfer_lost,
            standard_client, new_client, questioning, to_refusal, to_loan_issuance, refusal, loan_issuance, card_obtaining, returning
        ]

        ps = [
            p0, to_auto_lines,
            first_auto_line_free_places, first_auto_line, first_auto_cashier_free, first_auto_cashier_entry, first_auto_cashier_served,
            second_auto_line_free_places, second_auto_line, second_auto_cashier_free, second_auto_cashier_entry, second_auto_cashier_served,
            p1, to_indoors_lines,
            indoors_line_free_places, indoors_line, indoors_cashier_free, indoors_cashier_entry, indoors_cashier_served,
            p2, lost,
            indoors_clients, manager_line, manager_free, questioned, refusal_line, loan_issuance_line, to_card_obtaining, to_returning

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

    def _warmup(self, warmup_time: Numeric) -> None:
        """Clear probability counters after warmup"""
        self._simulate_part(warmup_time, is_protocol=False, is_stats=False)
        self.n0.n = self.n11.n = self.n12.n = self.n2.n = 0

