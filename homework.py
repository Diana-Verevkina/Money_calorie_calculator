import datetime as dt


class Record:
    def __init__(self, amount: float, comment: str, date: dt = None) -> None:
        self.amount = amount
        self.comment = comment
        if not date:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


class Calculator:
    def __init__(self, limit: float):
        self.limit = limit
        self.records = []

    def add_record(self, rec: Record) -> None:
        """Сохранять новую запись о расходах."""
        self.records.append(rec)

    def get_today_stats(self) -> float:
        """Считать, сколько денег/калорий потрачено/съедено сегодня."""
        today_stats = sum(record.amount for record in self.records
                          if record.date == dt.date.today())
        return today_stats

    def get_week_stats(self) -> float:
        """Считать, сколько денег/калорий потрачено/получено
        за последние 7 дней."""
        today = dt.date.today()
        week_ago = today - dt.timedelta(7)
        week_stats = sum(record.amount for record in self.records
                         if week_ago <= record.date <= today)
        return week_stats

    def check_limit(self):
        if self.get_today_stats() < self.limit:
            return True
        return False


class CashCalculator(Calculator):
    """Калькулятор для подсчета денег."""

    USD_RATE: float = 62.91
    EURO_RATE: float = 64.33

    def get_today_cash_remained(self, currency: str) -> str:
        """Определять, сколько ещё денег можно потратить сегодня в рублях,
        долларах или евро."""
        currency_type = {
            "rub": [1, "руб"],
            "usd": [self.USD_RATE, "USD"],
            "eur": [self.EURO_RATE, "Euro"]
        }

        if currency not in currency_type:
            raise KeyError(f"Ключ {currency} не найден "
                           f"в словаре {currency_type}")

        const, name = currency_type[currency]

        if self.check_limit():
            res = (self.limit - self.get_today_stats()
                   / const)
            return f"На сегодня осталось {res:.2f} {name}"
        elif self.get_today_stats() == self.limit:
            return f"Денег нет, держись"
        else:
            cash_remained = self.get_today_stats() - self.limit
            return (f"Денег нет, держись: твой долг - "
                    f"{cash_remained:.2f} {name}")


class CaloriesCalculator(Calculator):
    """Калькулятор для подсчета калорий."""

    def get_calories_remained(self) -> str:
        """Определять, сколько ещё калорий можно/нужно получить сегодня."""
        if self.check_limit():
            calories_remained = self.limit - self.get_today_stats()
            return (f"Сегодня можно съесть что-нибудь ещё,"
                    f"но с общей калорийностью "
                    f"не более {calories_remained} кКал")
        else:
            return "Хватит есть!"


def main() -> None:
    """Главная функция."""
    cash_calculator = CashCalculator(1000)
    calories_calculator = CaloriesCalculator(1000)

    cash_calculator.add_record(Record(200, "Безудержный шопинг"))
    cash_calculator.add_record(Record(300, "Наполнение потребительской "
                                           "корзины"))
    cash_calculator.add_record(Record(691, "Катание на такси", "05.07.2022"))
    # _________________________________________________________________________
    calories_calculator.add_record(Record(1186, "Кусок тортика. И ещё один."))
    calories_calculator.add_record(Record(84, "Йогурт.", "08.07.2022"))
    calories_calculator.add_record(Record(1140, "Баночка чипсов.",
                                          "24.02.2019"))
    # _________________________________________________________________________
    print("Денег потрачено сегодня:")
    print(cash_calculator.get_today_stats())
    print("Калорий получено сегодня:")
    print(calories_calculator.get_today_stats())

    print("Денег потрачено за неделю:")
    print(cash_calculator.get_week_stats())
    print("Калорий получено за неделю:")
    print(calories_calculator.get_week_stats())

    print("Сегодня можно еще потратить:")
    print(cash_calculator.get_today_cash_remained("rub"))
    print("Сегодня можно еще съесть:")
    print(calories_calculator.get_calories_remained())


if __name__ == '__main__':
    main()

