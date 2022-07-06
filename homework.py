import datetime as dt


class Record:
    """Калькулятор для подсчета денег."""

    def add_record(self):
        """Сохранять новую запись о расходах."""
        pass

    def get_today_stats(self):
        """Считать, сколько денег потрачено сегодня."""
        pass

    def get_today_cash_remained(self, currency):
        """Определять, сколько ещё денег можно потратить сегодня в рублях,
        долларах или евро."""
        pass

    def get_week_stats(self):
        """Считать, сколько денег потрачено за последние 7 дней."""
        pass


class Calculator:
    """Калькулятор для подсчета калорий."""

    def add_record(self):
        """Сохранять новую запись о приёме пищи."""
        pass

    def get_today_stats(self):
        """Считать, сколько калорий уже съедено сегодня."""
        pass

    def get_calories_remained(self):
        """Определять, сколько ещё калорий можно/нужно получить сегодня."""
        pass

    def get_week_stats(self):
        """Считать, сколько калорий получено за последние 7 дней."""
        pass
