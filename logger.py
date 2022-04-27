import logging
import functools
import time
# from log_calls import log_calls

logging.basicConfig(filename='log_file', format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG)
logging.debug('This message should appear on the console')
logging.info('So should this')
logging.warning('And this, too')
logging.error('And this, too')


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# utils/decorators.py

def timerun(func):
    """ Calculate the execution time of a method and return it back"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start

        logger = logging.getLogger(__name__)
        logger.debug(f"Duration of {func.__name__} function was {duration}.")
        return result
    return wrapper

# Output:
# 2019-07-21 18:43:25,636 [DEBUG] __main__: Duration of my_func was 0.00023937225341796875.


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# main.py

from utils.debuggers import debugmethod, timerun


@timerun
@debugmethod
def my_func(a, b, c, d):
    return a + b + c + d


if __name__ == "__main__":
    Debugger.enabled = True

    args_dict = dict(
        a=1,
        b=2,
        c=5,
        d=-10
    )

    my_func(**args_dict)

# Output should be like this:
#
# 2019-07-21 18:43:25,635 [DEBUG] __main__: Calling : my_func
# 2019-07-21 18:43:25,635 [DEBUG] __main__: args, kwargs: ((), {'a': 1, 'b': 2, 'c': 5, 'd': -10})
# 2019-07-21 18:43:25,635 [DEBUG] __main__: my_func returned -2
# 2019-07-21 18:43:25,636 [DEBUG] __main__: Duration of my_func was 0.00023937225341796875.
# OK, all done.


def debug(func):
    """Print the function signature and return value"""
    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        args_repr = [repr(a) for a in args]                      # 1
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]  # 2
        signature = ", ".join(args_repr + kwargs_repr)           # 3
        print(f"Calling {func.__name__}({signature})")
        value = func(*args, **kwargs)
        print(f"{func.__name__!r} returned {value!r}")           # 4
        return value
    return wrapper_debug