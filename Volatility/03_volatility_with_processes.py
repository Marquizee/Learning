# -*- coding: utf-8 -*-

import os
import pandas as pd
from concurrent import futures
from operator import methodcaller


# Задача: вычислить 3 тикера с максимальной и 3 тикера с минимальной волатильностью в МНОГОПРОЦЕССНОМ стиле
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

TRANSACTIONS_PATH = 'trades'


class Transaction:
    """This class is for reading and calculating 'Volatility' from csv files.
    Result of run() function is pd.Dataframe with SECID and VOLATILITY data on single Transaction file. 
    """

    def __init__(self, path_to_file) -> None:
        self.df = pd.DataFrame()
        self.path_to_file = path_to_file
        self.secid = None
        self.volatility = None

    def read_file(self):
        self.df = pd.read_csv(self.path_to_file)

    def calculate_data(self):
        _halfsum = (self.df.PRICE.max() + self.df.PRICE.min())/2
        self.volatility = (self.df.PRICE.max() -
                           self.df.PRICE.min())/_halfsum * 100
        self.secid = self.df.SECID[0]
        return pd.DataFrame({'SECID': [self.secid], 'VOLATILITY': [self.volatility]})

    def run(self):
        self.read_file()
        data = self.calculate_data()
        return data


class Session:
    """This class is for representing data from Transactions
        To use it needs to provide Transactions data to get_session()
        Output will print count times max, min
        and all zero volatility Transactions

    """

    def __init__(self, data) -> None:
        self.data = data
        self.result = pd.DataFrame()

    def get_session(self):
        for data in self.data:
            self.result = self.result.append(data)
            self.result.sort_values(by='VOLATILITY', inplace=True)
        return self.result

    def get_max_vol(self, count):
        return self.result.nlargest(count, 'VOLATILITY')

    def get_zero_vol(self):
        return self.result.loc[self.result.VOLATILITY == 0]['SECID'].tolist()

    def get_min_vol(self, count):
        return self.result.loc[self.result.VOLATILITY != 0].nsmallest(count, 'VOLATILITY')

    def output(self, count):

        print(
            f'Максимальная волатильность: \n{self.get_max_vol(count).to_string(index=False)}')
        print(
            f'Минимальная волатильность: \n{self.get_min_vol(count).to_string(index=False)}')

        print(f'Нулевая волатильность: \n{" ".join(self.get_zero_vol())}')


def main() -> None:
    with futures.ProcessPoolExecutor() as executor:
        transactions_names = os.listdir(TRANSACTIONS_PATH)
        processes = []
        for transaction in transactions_names:
            path_to_transaction = os.path.join(TRANSACTIONS_PATH, transaction)
            processes.append(Transaction(path_to_file=path_to_transaction))

        results = executor.map(methodcaller("run"), processes)

        session = Session(data=results)
        session.get_session()
        session.output(count=3)


if __name__ == "__main__":
    exit(main())
