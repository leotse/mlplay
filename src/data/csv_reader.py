# prices csv file reader

import os
import csv
import arrow

DATE_FORMAT = 'YYYY-MM-DD'


class BatchReader:

    def __init__(self, path, batchSize=5):
        self.csvpath = os.path.realpath(path)
        self.batchSize = batchSize
        self.done = False

    def __enter__(self):
        self.file = open(self.csvpath, 'r')
        self.reader = csv.reader(self.file)
        self.fields = self.reader.next()
        return self

    def __exit__(self, ex_type, ex_value, traceback):
        self.file.close()

    def __iter__(self):
        return self

    def next(self):
        if self.done:
            raise StopIteration()

        batch = []
        try:
            for i in xrange(self.batchSize):
                line = self.reader.next()
                price = self.parse(line)
                batch.append(price)

        except StopIteration:
            self.done = True

        return batch

    # parses a line item in the csv file
    def parse(self, line):
        item = {field: None for field in self.fields}
        for [field, val] in zip(self.fields, line):
            if(field == 'ex-dividend'):
                item['dividend'] = self.parse_field('dividend', val)
            else:
                item[field] = self.parse_field(field, val)
        return item

    # parses a field into the proper type
    def parse_field(self, field, val):
        if val is None or val == '':
            return None
        elif field == 'ticker':
            return val
        elif field == 'date':
            return (arrow.get(val, DATE_FORMAT)
                         .replace(tzinfo='US/Eastern'))
        else:
            return float(val)
