import time


def timer(f):
    def wrapper(*args, **kwargs):
        start = time.time()
        print("Function invoke started")
        rv = f(*args, **kwargs)
        print(f"Func invoke ended, and total time is {time.time() - start}")
        return rv
    return wrapper


@timer
def test():
    for _ in range(1000000):
        pass


test()
