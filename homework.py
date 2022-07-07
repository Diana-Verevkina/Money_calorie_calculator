import datetime as dt
from dataclasses import dataclass


class Record:
    def __init__(self, amount: float, comment: str, date: dt = None) -> None:
        self.amount = amount
        self.comment = comment
        if not date:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


@dataclass()
class Calculator:
    limit: float
    cash_records = []
    calories_records = []

    def add_record(self, rec: Record) -> None:
        """Сохранять новую запись о расходах."""
        if type(self).__name__ == "CashCalculator":
            self.cash_records.append([rec.amount, rec.comment, rec.date])
        else:
            self.calories_records.append([rec.amount, rec.comment, rec.date])

    def get_today_stats(self) -> float:
        """Считать, сколько денег/калорий потрачено/съедено сегодня."""
        res = 0
        if type(self).__name__ == "CashCalculator":
            records = self.cash_records
        else:
            records = self.calories_records
        for record in records:
            if record[2] == dt.date.today():
                res = res + record[0]
        return res

    def get_week_stats(self) -> float:
        """Считать, сколько денег/калорий потрачено/получено
        за последние 7 дней."""
        res = 0
        if type(self).__name__ == "CashCalculator":
            records = self.cash_records
        else:
            records = self.calories_records
        for record in records:
            if (dt.date.today() - record[2]).days <= 7:
                res = res + record[0]
        return res


class CashCalculator(Calculator):
    """Калькулятор для подсчета денег."""

    USD_RATE: float = 62.91
    EURO_RATE: float = 64.33

    def get_today_cash_remained(self, currency: str) -> str:
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

    def get_calories_remained(self) -> str:
        """Определять, сколько ещё калорий можно/нужно получить сегодня."""
        if self.get_today_stats() < self.limit:
            return (f"Сегодня можно съесть что-нибудь ещё,"
                    f"но с общей калорийностью "
                    f"не более {self.limit - self.get_today_stats()} кКал")
        else:
            return "Хватит есть!"
        pass


def main() -> None:
    """Главная функция."""
    cash_calculator = CashCalculator(1000)
    calories_calculator = CaloriesCalculator(1000)

    cash_calculator.add_record(Record(200, "Безудержный шопинг"))
    cash_calculator.add_record(Record(300, "Наполнение потребительской "
                                           "корзины"))
    cash_calculator.add_record(Record(691, "Катание на такси", "01.07.2022"))
    # _________________________________________________________________________
    calories_calculator.add_record(Record(1186, "Кусок тортика. И ещё один.",
                                          "08.07.2022"))
    calories_calculator.add_record(Record(84, "Йогурт.", "08.07.2022"))
    calories_calculator.add_record(Record(1140, "Баночка чипсов.",
                                          "24.02.2019"))
    # _________________________________________________________________________

    print(cash_calculator.get_today_stats())
    print(calories_calculator.get_today_stats())

    print(cash_calculator.get_week_stats())
    print(calories_calculator.get_week_stats())

    print(cash_calculator.get_today_cash_remained("rub"))
    print(calories_calculator.get_calories_remained())


if __name__ == '__main__':
    main()

