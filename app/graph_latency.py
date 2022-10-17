import csv
import os
import random
import timeit
from base64 import b64encode

import BackendApp.MemCache
import app
import random


def main():

    start1 = timeit.default_timer()
    total_time_stamp=[]
    memcache = BackendApp.MemCache.MemCache(128, 'LRU')

    #20 put 80 get
    for i in range (80000):
        fname = open(r'C:\Users\linti\Desktop\ECE1779\app\static\images\abc.jpg', 'rb')

        #with fname as image_file:
        encoded_image = b64encode(fname.read()).decode('utf-8')
        memcache.put(i, encoded_image)
        # add the key and file name to cache as well as database
        stop1 = timeit.default_timer()
        if i % 10 ==0:
            total_time_stamp.append((stop1 - start1)*1000)

    for i in range (20000):
        memcache.get(random.randint(0,79999))
        stop2 = timeit.default_timer()
        if i % 10 == 0:
            total_time_stamp.append((stop2 - start1)*1000)

    print(total_time_stamp)
    print(len(total_time_stamp))

    with open ('total_time_stamp.csv','w') as f:
        writer = csv.writer(f)
        writer.writerow(total_time_stamp)



if __name__ == "__main__":
   main()