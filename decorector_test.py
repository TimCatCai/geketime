import time


def timmer(func):
    def wrapper():
        start_time = time.time()
        func()
        end_time = time.time()
        print("func operates %lf " % (end_time - start_time))
    return wrapper


@timmer
def i_can():
    time.sleep(3)


i_can()


