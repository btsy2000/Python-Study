import functools


def decorator(decorator_func):
    '''Decorator to decorate decorators. Make sure to call the
    func with this decorator attached.
    '''
    decorator_expected_arg_count = decorator_func.__code__.co_argcount - 1
    if decorator_expected_arg_count:
        def decorator_maker(*decorator_args):
            assert len(decorator_args) == decorator_expected_arg_count,\
                "%s expected %d args" % (decorator_func.__name__,
                                         decorator_expected_arg_count)

            def _decorator(func):
                assert callable(func), \
                    "Decorator not given a function. Did you forget to \
                    give %r arguments?" % (decorator_func.__name__)

                def decorated_func(*args, **kwargs):
                    full_args = decorator_args + (func,) + args
                    return decorator_func(*full_args, **kwargs)
                decorated_func.__name__ = func.__name__
                decorated_func.__doc__ = func.__doc__
                return decorated_func
            return _decorator
        return decorator_maker
    else:
        def _decorator(func):
            def decorated_func(*args, **kwargs):
                return decorator_func(func, *args, **kwargs)
            decorated_func.__name__ = func.__name__
            decorated_func.__doc__ = func.__doc__
            return decorated_func
        return _decorator


def notify(email=None,
           email_from='no-reply@youapp.com',
           email_subject='Notification',
           smtp_host='localhost',
           log=None,
           *args, **kwargs):
    '''Decorator to send email notification or log a message to a log file
    or both with the results of running the function.
    Attributes:
        email - List of email addresses to send results to
        email_from - Email address to use for from address
        email_subject - Subject to use for the emails
        smtp_host - SMTP host to connect to for sending emails
        log - Log file location to log notifications to
    Example:
    @notify(email=['myemail@email.com', 'youremail@email.com'])
    def do_something():
       return 'this is what was done'
    Executing the do_something function will then email the email addresses
    with the results of the function.
    '''
    DEFAULT_LOG_FILE = '/tmp/default_log.log'

    def wrap(func):
        name = func.__name__

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logfile = DEFAULT_LOG_FILE
            rtn = func(*args, **kwargs)
            message = "notify: {0}({2}, {3}) -> {1}\n".format(name,
                                                              rtn,
                                                              str(args),
                                                              str(kwargs))
            if log is not None:
                logfile = log
            with open(logfile, 'a') as f:
                f.write(message)

            if email is not None and len(email) > 0:
                import smtplib
                from email.mime.multipart import MIMEMultipart
                msg = MIMEMultipart()
                msg['Subject'] = email_subject
                msg['From'] = email_from
                msg['To'] = ', '.join(email)

                try:
                    s = smtplib.SMTP(smtp_host)
                    s.sendmail(email_from, email, msg.as_string())
                    s.quit()
                except Exception:
                    with open(logfile, 'a') as f:
                        f.write('could not send notification via email\n')
            return rtn
        return wrapper
    return wrap


def memorize(func):
    '''Decorator. Memorizes the results of calling a function with
    specific args and kwargs. If the function is called again with
    those same args and kwargs the previous result is returned. The
    function is no actually executed again.
    '''
    cache = func.cache = {}
    @functools.wraps(func)
    def memorizer(*args, **kwargs):
        print(('cache', cache))
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    return memorizer

@decorator
def deprecated(func, *args, **kwargs):
    '''Decorator which can be used to mark functions as deprecated.
    It will result in a warning being emitted the the function is
    called.
    '''
    import warnings
    #warnings.warn('Call to deprecated function{}.'.format(func.__name__), category=DeprecationWarning)
    s = 'Call to deprecated function {}.'.format(func.__name__)
    warnings.warn(s)
    return func(*args, **kwargs)


def threadify(func, daemon=False):
    '''Decorator adapted from http://stackoverflow.com/a/14331755/18992
    (thanks bj0)
    '''
    import queue
    import threading

    def wrapped_f(q, *args, **kwargs):
        rtn = func(*args, **kwargs)
        q.put(rtn)

    @functools.wraps(func)
    def wrap(*args, **kwargs):
        q = queue.Queue()

        t = threading.Thread(target=wrapped_f, args=(q,) + args, kwargs=kwargs)
        t.daemon = daemon
        t.start()
        t.result = q
        return t

    return wrap

@memorize
# @deprecated
def sub(x, y):
    return x - y

def add(x, y):
    return x + y

def add2(x, y):
    return x + y

if __name__ == '__main__':
    #add(2,3)
    print('sub1', sub(2,3))
    print('sub2', sub(2,3))
    print('sub3', sub(2,3))
    #add2(2,3)