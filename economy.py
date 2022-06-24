import csv
import enum
import operator
from os import path
from pathlib import Path
import datetime as dt


def csv_to_data_dnb(csv_file, delimiter=';', skiplines=1):
    data = []
    fp = Path(csv_file).resolve()
    if not fp.is_file():
        raise FileNotFoundError(fp)
    with open(fp, 'r') as f:
        content = csv.reader(f, delimiter=delimiter, skipinitialspace=True)
        for i in range(skiplines):
            next(content)
        for row in content:
            outgoing = row[3].replace(' ', '').replace(',', '.')
            ingoing = row[4].replace(' ', '').replace(',', '.')
            v = 0
            if outgoing:
                v = -float(outgoing)
            elif ingoing:
                v = float(ingoing)
            data.append({
                'date': dt.datetime.strptime(row[0], '%d.%m.%Y'),
                'type': row[1].split(' ')[0],
                'description': row[1].lower(),
                'value': v,
            })
    return data


def csv_to_data_nordea(csv_file, delimiter=';', skiplines=7):
    data = []
    fp = Path(csv_file).resolve()
    if not fp.is_file():
        raise FileNotFoundError(fp)
    with open(fp, 'r') as f:
        content = csv.reader(f, delimiter=delimiter, skipinitialspace=True)
        for i in range(skiplines):
            next(content)
        for row in content:
            if 'sum' in row[1].lower():
                break
            outgoing = row[7].replace(' ', '').replace(',', '.')
            ingoing = row[9].replace(' ', '').replace(',', '.')
            v = 0
            if outgoing:
                v = -float(outgoing)
            elif ingoing:
                v = float(ingoing)
            data.append({
                'date': dt.datetime.strptime(row[1], '%Y.%m.%d'),
                'type': row[3],
                'description': row[5],
                'value': v,
            })
    return data



class Economy(object):
    def __init__(self, csv_file, bank, delimiter=';', description_pos=2,
                 value_pos=3, date_pos=0):
        csv_file = Path(csv_file).resolve()
        if not csv_file.is_file():
            raise FileNotFoundError('Could not find file {}'.format(csv_file))
        self.bank = bank
        self.csv_file = csv_file
        self.months = 12
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
        if self.bank == 'nordea':
            data = csv_to_data_nordea(self.csv_file)
        elif self.bank == 'dnb':
            data = csv_to_data_dnb(self.csv_file)
        else:
            raise ValueError('not valid bank')
        dates = []
        for item in data:
            dates.append(item["date"])
            found = False
            skip = False
            description = self.non_norwegian(item['description'].lower())
            value = item['value']
            date = item['date']
            for name in ['kontoregulering', 'overførsel', 'straksutbetaling']:
                if name in item["type"].lower():
                    skip = True
            if value > 0:
                skip = True
            if skip:
                continue
            for key in self.categories:
                for name in self.categories[key]:
                    if name in description:
                        found = True
                        self.add_match(key, value)
                        break
                if found:
                    break
            if not found:
                self.uncat += 1
                self.uncat_value += value
                self.uncat_items.update(
                    {
                        '{:40} {}'.format( description, date): value
                    }
                )

            self.total_value += value
        self.coverage = self.matched_value / (
            self.matched_value + self.uncat_value)
        timedelta = max(dates)-min(dates)
        self.months = timedelta.days/(365/12)

    def add_match(self, key, value):
        self.category_totals[key] += value
        self.matched_value += value
        self.matches += 1

    def categories_from_file(self, filename):
        if not path.isfile(filename):
            raise FileNotFoundError('Could not find file {}'.format(filename))
        with open(filename, 'r') as f:
            for line in f:
                cat_name, li = line.rstrip().split(':')
                match_list = li.split(',')
                self.add_cat(cat_name, match_list)

    def print_status(self):
        print(self.matches)
        print(self.uncat)

    def print_results(self, monthly_average=True):
        sorted_totals = sorted(self.category_totals.items(),
                               key=operator.itemgetter(1))
        print('')
        print('Money coverage: {:.2f}'.format(self.coverage))
        print('Monthly average:\n')
        for cat in sorted_totals:
            if monthly_average:
                val = cat[1] / self.months
            else:
                val = cat[1]
            print('{:20} {:.0f}'.format(cat[0], 0 if self.coverage==0 else  val / self.coverage))
        print('')
        print('{:20} {:.0f}'.format('Total:', self.total_value / self.months))
        print('')

    def print_uncat(self):
        sorted_totals = sorted(self.uncat_items.items(),
                               key=operator.itemgetter(1))
        print('\nUncategorized items:\n')
        for i, cat in enumerate(sorted_totals):
            print('{:10.2f}   {}'.format(cat[1], cat[0]))
            if i > 40:
                return
