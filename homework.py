import datetime as dt
from dataclasses import dataclass


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if not date:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


@dataclass()
class Calculator:
    limit: float
    records = []

    def add_record(self, rec: Record):
        """Сохранять новую запись о расходах."""
        self.records.append([rec.amount, rec.comment, rec.date])

    def get_today_stats(self):
        """Считать, сколько денег/калорий потрачено/съедено сегодня."""
        res = 0
        for record in self.records:
            if record[2] == dt.date.today():
                res = res + record[0]
        return res

    def get_week_stats(self):
        """Считать, сколько денег/калорий потрачено/получено
        за последние 7 дней."""
        spent = 0
        for record in self.records:
            if (dt.date.today() - record[2]).days <= 7:
                spent = spent + record[0]
        return spent


class CashCalculator(Calculator):
    """Калькулятор для подсчета денег."""

    USD_RATE = 62.91
    EURO_RATE = 64.33

    def get_today_cash_remained(self, currency):
        """Определять, сколько ещё денег можно потратить сегодня в рублях,
        долларах или евро."""
        currency_type = {
            "rub": 1,
            "usd": self.USD_RATE,
            "eur": self.EURO_RATE
        }

        if currency not in currency_type:
            raise KeyError(f"Ключ {currency} не найден "
                           f"в словаре {currency_type}")
        if self.get_today_stats() < self.limit:
            res = self.limit - self.get_today_stats() / currency_type[currency]
            return f"На сегодня осталось {res:.2f} {currency}"
        elif self.get_today_stats() == self.limit:
            return f"Денег нет, держись"
        else:
            return (f"Денег нет, держись: твой долг - "
                    f"{self.get_today_stats() - self.limit:.2f} {currency}")


class CaloriesCalculator(Calculator):
    """Калькулятор для подсчета калорий."""

    def get_calories_remained(self):
        """Определять, сколько ещё калорий можно/нужно получить сегодня."""
        if self.amount < self.limit:
            return (f"Сегодня можно съесть что-нибудь ещё,"
                    f"но с общей калорийностью "
                    f"не более {self.limit - self.amount} кКал")
        else:
            return "Хватит есть!"
        pass


def main():
    """Главная функция."""
    cash_calculator = CashCalculator(1000)

    cash_calculator.add_record(Record(amount=145, comment="кофе"))
    cash_calculator.add_record(Record(amount=300, comment="Серёге за обед"))
    cash_calculator.add_record(Record(amount=3000, comment="бар в Танин др",
                                      date="08.06.2022"))

    print(cash_calculator.get_today_stats())
    print(cash_calculator.get_today_cash_remained("rub"))

    print(cash_calculator.get_week_stats())


if __name__ == '__main__':
    main()

