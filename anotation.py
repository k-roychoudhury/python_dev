import functools
import time

def timer(func):
    """Print the runtime of the decorated function"""
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()    # 1
        value = func(*args, **kwargs)
        end_time = time.perf_counter()      # 2
        run_time = end_time - start_time    # 3
        print(f"Finished {func.__name__!r} in {run_time:.4f} secs")
        return value
    return wrapper_timer


def do_twice(func):
    @functools.wraps(func)
    def wrapper_do_twice(*args, **kwargs):
        func(*args, **kwargs)
        return func(*args, **kwargs)
    return wrapper_do_twice


def decorator(func):
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        # Do something before
        value = func(*args, **kwargs)
        # Do something after
        return value
    return wrapper_decorator


@do_twice
@timer
def greet(name):
    print(f"Hello {name}")


greet("kunal")


def log(func):
    def logging_task_wrapper(*args, **kwargs):
        _args: str = ",".join(["[{}]".format(str(item)) for item in args] + list(kwargs.items()))
        print("{} - {}".format(func.__name__, _args))
        return_value = func(*args, **kwargs)
        return return_value
    return logging_task_wrapper


@log
def do_shit(a1, a2):
    return a1 ** a2

print(do_shit(4, 3))
