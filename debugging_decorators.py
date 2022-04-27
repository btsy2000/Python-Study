import time


def timeit(function):
    '''Decorator used for debugging. Prints the call and how long it took.'''
    def timed(*args, **kwargs):
        ts = time.time()
        result = function(*args, **kwargs)
        te = time.time()
        print("{0} ({1}, {2}) {3:.2} sec"
              .format(function.__name__, args, kwargs, te - ts))
        return result
    return timed


def debug(function):
    '''Decorator that places a break point right before calling the function.'''
    def wrapped(*args, **kwargs):
        import pdb; pdb.set_trace()  # XXX BREAKPOINT
        return function(*args, **kwargs)
    return wrapped