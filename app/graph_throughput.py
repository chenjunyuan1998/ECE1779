import csv
import os
import random
import timeit
from base64 import b64encode

import BackendApp.MemCache
import app
import random

def main():
    #cache = MemCache.MemCache(1, 'LRU')
    cache = BackendApp.MemCache.MemCache(128, 'LRU')
    start = timeit.default_timer()
    end = timeit.default_timer()
    count = 0
    while end - start < 5:
        for i in range(8):
            fname = open(r'/app/static/images/abc.jpg', 'rb')

            # with fname as image_file:
            encoded_image = b64encode(fname.read()).decode('utf-8')
            cache.put(count + i, encoded_image)
            cache.clear()
            end = timeit.default_timer()
            if end - start > 5:
                break
            count += 1
        for i in range(2):
            cache.get(random.randint(0,count-1))
            cache.clear()
            end = timeit.default_timer()
            if end - start > 5:
                break
            count += 1
        end = timeit.default_timer()

    print(count)



if __name__ == "__main__":
   main()