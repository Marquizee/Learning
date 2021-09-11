# -*- coding: utf-8 -*-

import os
from collections import defaultdict

# Описание предметной области:
#
# При торгах на бирже совершаются сделки - один купил, второй продал.
# Покупают и продают ценные бумаги (акции, облигации, фьючерсы, етс). Ценные бумаги - это по сути долговые расписки.
# Ценные бумаги выпускаются партиями, от десятка до несколько миллионов штук.
# Каждая такая партия (выпуск) имеет свой торговый код на бирже - тикер - https://goo.gl/MJQ5Lq
# Все бумаги из этой партии (выпуска) одинаковы в цене, поэтому говорят о цене одной бумаги.
# У разных выпусков бумаг - разные цены, которые могут отличаться в сотни и тысячи раз.
# Каждая биржевая сделка характеризуется:
#   тикер ценнной бумаги
#   время сделки
#   цена сделки
#   обьем сделки (сколько ценных бумаг было куплено)
#
# В ходе торгов цены сделок могут со временем расти и понижаться. Величина изменения цен называтея волатильностью.
# Например, если бумага №1 торговалась с ценами 11, 11, 12, 11, 12, 11, 11, 11 - то она мало волатильна.
# А если у бумаги №2 цены сделок были: 20, 15, 23, 56, 100, 50, 3, 10 - то такая бумага имеет большую волатильность.
# Волатильность можно считать разными способами, мы будем считать сильно упрощенным способом -
# отклонение в процентах от полусуммы крайних значений цены за торговую сессию:
#   полусумма = (максимальная цена + минимальная цена) / 2
#   волатильность = ((максимальная цена - минимальная цена) / полусумма) * 100%
# Например для бумаги №1:
#   half_sum = (12 + 11) / 2 = 11.5
#   volatility = ((12 - 11) / half_sum) * 100 = 8.7%
# Для бумаги №2:
#   half_sum = (100 + 3) / 2 = 51.5
#   volatility = ((100 - 3) / half_sum) * 100 = 188.34%
#
# В реальности волатильность рассчитывается так: https://goo.gl/VJNmmY
#
# Задача: вычислить 3 тикера с максимальной и 3 тикера с минимальной волатильностью.
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
# Подготовка исходных данных
# 1. Скачать файл https://drive.google.com/file/d/1l5sia-9c-t91iIPiGyBc1s9mQ8RgTNqb/view?usp=sharing
#       (обратите внимание на значок скачивания в правом верхнем углу,
#       см https://drive.google.com/file/d/1M6mW1jI2RdZhdSCEmlbFi5eoAXOR3u6G/view?usp=sharing)
# 2. Раззиповать средствами операционной системы содержимое архива
#       в папку python_base/lesson_012/trades
# 3. В каждом файле в папке trades содержится данные по сделакам по одному тикеру, разделенные запятыми.
#   Первая строка - название колонок:
#       SECID - тикер
#       TRADETIME - время сделки
#       PRICE - цена сделки
#       QUANTITY - количество бумаг в этой сделке
#   Все последующие строки в файле - данные о сделках
#
# Подсказка: нужно последовательно открывать каждый файл, вычитывать данные, высчитывать волатильность и запоминать.
# Вывод на консоль можно сделать только после обработки всех файлов.
#
# Для плавного перехода к мультипоточности, код оформить в обьектном стиле, используя следующий каркас
#
# class <Название класса>:
#
#     def __init__(self, <параметры>):
#         <сохранение параметров>
#
#     def run(self):
#         <обработка данных>


TRANSACTIONS_PATH = 'lesson_012/trades'
#OUTPUT_FILE = 'lesson_012/OUTPUT.TXT'


class Transaction:
    transactions_table = defaultdict(list)
    sorted_transactions = None
    zero_volatility_table = None
    max_volatility_table = None
    min_volatility_table = None

    def __init__(self):
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

    def readfile(self, file):
        next(file)
        for line in file:
            self.secid, self.tradetime, self.price, self.quantity = line[:-1].split(
                ',')
            self.price = float(self.price)
            if self.price > self.max_price:
                self.max_price = self.price
            if self.min_price == 0 or self.price < self.min_price:
                self.min_price = self.price

    def run(self, file):
        self.readfile(file)
        self.calculate_volatility()


def main():
    transactions = os.listdir(TRANSACTIONS_PATH)

    for _transaction in transactions:
        with open(os.path.join(TRANSACTIONS_PATH, _transaction)) as ts_file:
            ts = Transaction()
            ts.run(ts_file)

    Transaction.get_data()
    Transaction.output()


if __name__ == "__main__":
    exit(main())
