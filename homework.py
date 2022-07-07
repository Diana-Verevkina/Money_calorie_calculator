import datetime as dt
from dataclasses import dataclass


@dataclass()
class Calculator:
    limit: float
    records = []


class Record:
    def __init__(self, amount, comment, date=str(dt.datetime.today().date())):
        self.amount = amount
        self.comment = comment
        self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


class CashCalculator(Calculator):
    """Калькулятор для подсчета денег."""

    USD_RATE = 62.91
    EURO_RATE = 64.33

    def add_record(self, rec: Record):
        """Сохранять новую запись о расходах."""
        self.records.append([rec.amount, rec.comment, rec.date])

    def get_today_stats(self):
        """Считать, сколько денег потрачено сегодня."""
        spent = 0
        for i in range(len(self.records)):
            if self.records[i][2] == dt.datetime.today().date():
                spent = spent + self.records[i][0]
        return spent

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
            return (f"На сегодня осталось {res:.2f} {currency}")
        elif self.get_today_stats() == self.limit:
            return f"Денег нет, держись"
        else:
            return (f"Денег нет, держись: твой долг - "
                    f"{self.get_today_stats() - self.limit:.2f} {currency}")

    def get_week_stats(self):
        """Считать, сколько денег потрачено за последние 7 дней."""
        spent = 0
        for i in range(len(self.records)):
            if (dt.datetime.now() - dt.datetime(self.records[i][2])).days <= 7:
                spent = spent + self.records[i][0]
        return spent




class CaloriesCalculator(Calculator):
    """Калькулятор для подсчета калорий."""

    def add_record(self, rec: Record):
        """Сохранять новую запись о приёме пищи."""
        self.records.append(rec)

    def get_today_stats(self):
        """Считать, сколько калорий уже съедено сегодня."""
        pass

    def get_calories_remained(self):
        """Определять, сколько ещё калорий можно/нужно получить сегодня."""
        if self.amount < self.limit:
            return (f"Сегодня можно съесть что-нибудь ещё,"
                    f"но с общей калорийностью "
                    f"не более {self.limit - self.amount} кКал")
        else:
            return "Хватит есть!"
        pass

    def get_week_stats(self):
        """Считать, сколько калорий получено за последние 7 дней."""

        pass





# создадим калькулятор денег с дневным лимитом 1000
cash_calculator = CashCalculator(1000)

# дата в параметрах не указана,
# так что по умолчанию к записи должна автоматически добавиться сегодняшняя дата
cash_calculator.add_record(Record(amount=145, comment="кофе"))
# и к этой записи тоже дата должна добавиться автоматически
cash_calculator.add_record(Record(amount=300, comment="Серёге за обед"))
# а тут пользователь указал дату, сохраняем её
cash_calculator.add_record(Record(amount=3000, comment="бар в Танин др",
                                  date="07.07.2022"))



print(cash_calculator.records)
print(cash_calculator.get_today_stats())
print(cash_calculator.get_week_stats())
print(cash_calculator.get_today_cash_remained("rub"))
# должно напечататься
# *На сегодня осталось 565 руб*