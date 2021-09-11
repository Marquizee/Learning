# -*- coding: utf-8 -*-


# Задача: вычислить 3 тикера с максимальной и 3 тикера с минимальной волатильностью в МНОГОПОТОЧНОМ стиле
#
# Бумаги с нулевой волатильностью вывести отдельно.
# Результаты вывести на консоль в виде:
#   Максимальная волатильность:
#       ТИКЕР1 - ХХХ.ХХ %
#       ТИКЕР2 - ХХХ.ХХ %
#       ТИКЕР3 - ХХХ.ХХ %
#   Минимальная волатильность:
#       ТИКЕР4 - ХХХ.ХХ %
#       ТИКЕР5 - ХХХ.ХХ %
#       ТИКЕР6 - ХХХ.ХХ %
#   Нулевая волатильность:
#       ТИКЕР7, ТИКЕР8, ТИКЕР9, ТИКЕР10, ТИКЕР11, ТИКЕР12
# Волатильности указывать в порядке убывания. Тикеры с нулевой волатильностью упорядочить по имени.
#

# -*- coding: utf-8 -*-

import os
from collections import defaultdict
from threading import Thread

TRANSACTIONS_PATH = 'lesson_012/trades'
#OUTPUT_FILE = 'lesson_012/OUTPUT.TXT'


class Transaction(Thread):
    transactions_table = defaultdict(list)
    sorted_transactions = None
    zero_volatility_table = None
    max_volatility_table = None
    min_volatility_table = None

    def __init__(self, path,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path_to_file = path
        self.secid = None
        self.tradetime = None
        self.price = None
        self.quantity = None
        self.min_price = 0
        self.max_price = 0
        self.half_sum = 0
        self.volatility = 0

    @staticmethod
    def get_data():
        Transaction.sorted_transactions = sorted(
            Transaction.transactions_table.items(), key=lambda item: item[1][3])
        Transaction.zero_volatility_table = [
            (y[0], y[1][3]) for y in Transaction.sorted_transactions if y[1][3] == 0.0]
        Transaction.min_volatility_table = [
            (y[0], y[1][3]) for y in Transaction.sorted_transactions if y[1][3] != 0.0][:3]
        Transaction.max_volatility_table = [
            (y[0], y[1][3]) for y in Transaction.sorted_transactions if y[1][3] != 0.0][-3:]

    @staticmethod
    def output():
        print('Максимальная волатильность:')
        for tiker, value in reversed(Transaction.max_volatility_table):
            print(f'{tiker} - {round(value,2)}%')

        print('Минимальная волатильность:')
        for tiker, value in reversed(Transaction.min_volatility_table):
            print(f'{tiker} - {round(value,2)}%')

        print('Нулевая волатильность:')
        for tiker, value in Transaction.zero_volatility_table:
            print(tiker, end=' ')

    def calculate_volatility(self):
        self.half_sum = (self.max_price + self.min_price)/2
        self.volatility = (self.max_price - self.min_price)/self.half_sum * 100
        Transaction.transactions_table[self.secid] = [
            self.min_price, self.max_price, self.half_sum, self.volatility]

    def read_file(self):
        with open(self.path_to_file, 'r') as file:
            next(file)
            for line in file:
                self.secid, self.tradetime, self.price, self.quantity = line[:-1].split(
                    ',')
                self.price = float(self.price)
                if self.price > self.max_price:
                    self.max_price = self.price
                if self.min_price == 0 or self.price < self.min_price:
                    self.min_price = self.price

    def run(self):
        self.read_file()
        self.calculate_volatility()


def main():
    transactions = os.listdir(TRANSACTIONS_PATH)
    for transaction in transactions:
        path_to_transaction = os.path.join(TRANSACTIONS_PATH, transaction)
        ts = Transaction(path=path_to_transaction)
        ts.start()
    Transaction.get_data()
    Transaction.output()


if __name__ == "__main__":
    exit(main())
