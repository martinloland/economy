import csv
import operator
from os import path


class Economy(object):
    def __init__(self, csv_file, delimiter=',', months=12, description_pos=2,
                 value_pos=3, date_pos=0):
        if not path.isfile(csv_file):
            raise FileNotFoundError('Could not find file {}'.format(csv_file))
        self.csv_file = csv_file
        self.months = months
        self.categories = {}
        self.category_totals = {}
        self.matches = 0
        self.matched_value = 0
        self.uncat = 0
        self.uncat_value = 0
        self.uncat_items = {}
        self.total_value = 0

        self.desc_pos = description_pos
        self.val_pos = value_pos
        self.date_pos = date_pos
        self.delimiter = delimiter

    def add_cat(self, name, match_list):
        if not isinstance(name, str):
            raise ValueError('Name must be a string')
        if not isinstance(match_list, list):
            raise ValueError('match_list must be a list with strings')
        for i, item in enumerate(match_list):
            if item.find('æ') + item.find('ø') + item.find('å') > -3:
                match_list[i] = self.non_norwegian(item)
        self.categories.update({name: match_list})
        self.category_totals.update({name: 0})

    def non_norwegian(self, text):
        return text.replace('ø', 'o').replace('å', 'aa').replace('æ', 'ae')

    def calculate(self):
        self.csv_total_rows = 0
        with open(self.csv_file, 'r') as csvfile:
            content = csv.reader(csvfile, delimiter=self.delimiter)
            for row in content:
                self.csv_total_rows += 1
                found = False
                description = self.non_norwegian(row[self.desc_pos].lower())
                value = float(row[self.val_pos].replace(',', ''))
                date = row[self.date_pos]
                for key in self.categories:
                    for name in self.categories[key]:
                        if name in description:
                            found = True
                            self.add_match(key, value)
                            break
                if not found:
                    self.uncat += 1
                    self.uncat_value += value
                    self.uncat_items.update(
                        {'{:40} {}'.format(self.non_norwegian(description),
                                        date): value})
                self.total_value += value

        self.coverage = self.matched_value / (
            self.matched_value + self.uncat_value)

    def add_match(self, key, value):
        self.category_totals[key] += value
        self.matched_value += value
        self.matches += 1

    def print_results(self):
        sorted_totals = sorted(self.category_totals.items(),
                               key=operator.itemgetter(1))
        print('')
        print('Money coverage: {:.2f}'.format(self.coverage))
        print('Monthly average:\n')
        for cat in sorted_totals:
            print('{:15} {:.0f}'.format(cat[0],
                                        cat[1] / self.months / self.coverage))
        print('')
        print('{:15} {:.0f}'.format('Total:', self.total_value / self.months))
        print('')

    def print_uncat(self):
        sorted_totals = sorted(self.uncat_items.items(),
                               key=operator.itemgetter(1))
        print('\nUncategorized items:\n')
        for cat in sorted_totals:
            print('{:10.2f}   {}'.format(cat[1], cat[0]))
