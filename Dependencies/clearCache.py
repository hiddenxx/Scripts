import os
import time


def wipe_unused(basedir, limit):
    """
    Remove files in *basedir* not accessed within *limit* minutes

    :param basedir: directory to clean
    :param limit: minutes
    """
    atime_limit = time.time() - limit
    count = 0
    for filename in os.listdir(basedir):
        path = os.path.join(basedir, filename)
        if os.path.getatime(path) < atime_limit:
            os.remove(path)
            count += 1
    print("Removed {} files.".format(count))


if __name__ == '__main__':
    wipe_unused(os.path.join(os.getcwd(), 'cache'), 5)
