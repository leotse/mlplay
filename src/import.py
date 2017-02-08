# import data from the given csv to the given db

import sys

from data.csv_reader import BatchReader
from data.db import DB
from common.utils import log

BATCH_SIZE = 10000

# read command line args
csvpath = sys.argv[1]
dbpath = sys.argv[2]

# read csv file and insert into db
with DB(dbpath) as prices_db:

    prices_db.reset()

    log('[import] opening file..')
    with BatchReader(csvpath, batchSize=BATCH_SIZE) as reader:

        total = 0

        log('[import] reading in {0} batches.. '.format(BATCH_SIZE))

        for batch in reader:
            total += len(batch)

            # write to db when we have a big enough batch
            prices_db.insert_many(batch)
            log('[import] imported {0} rows'.format(total))
