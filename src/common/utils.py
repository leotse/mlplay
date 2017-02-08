# utilities

import arrow

def log(msg):
    print '[{0}] {1}'.format(arrow.utcnow(), msg)