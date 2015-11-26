import random
import time
import sys

if __name__ == "__main__":
    while (True):
        duration = random.randint(5000,30000)
        print "{t}".format(t=duration)
        sys.stdout.flush()
        time.sleep(duration/1000.)