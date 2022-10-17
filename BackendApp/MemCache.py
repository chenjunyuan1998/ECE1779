import random
import sys
import time

from BackendApp import db

class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


# (O (1) access time)
class MemCache:
    """
    Policy is restricted to LRU and RANDOM
    Cap is capacity in MB
    Cache : a dictionary which value is a Node
    Size : the number of items in the memCache
    Space : memory usage
    """

    def __init__(self, capi, policy):
        self.left = Node(0, 0)
        self.right = Node(0, 0)
        self.cap = capi * 1024 * 1024
        self.cache = {}
        self.right.prev = self.left
        self.left.next = self.right

        self.size = 0
        self.space = 0
        self.policy = policy

        self.hit = 0
        self.missed = 0
        self.total = 0

    """
    Helper function:
    Always inserted to the right most position in Double LinkedList
    To make it most recent
    """

    def insert(self, node):
        node.prev = self.right.prev
        node.next = self.right

        self.right.prev.next = node
        self.right.prev = node

    """
    Helper function:
    Delete the appearance of the node in the Double LinkedList
    """

    def remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    """
    If key not in memcache
    return false
    missed request += 1

    Else for LRU, re-insert the node to last position in Double Linked
    For recent use
    Return the value
    """

    def get(self, key):
        if key not in self.cache:
            self.missed += 1
            self.total += 1
            return -1
        self.remove(self.cache[key])
        self.insert(self.cache[key])

        self.total += 1
        self.hit += 1
        return self.cache[key].value

    """
    If the size of the input val is larger than the cap itself
    return false which means no matter what we cannot put the val into the memcache


    Else if the key is already exist in memcache
    First delete its appearance in the ListList and reduce the size 
    Create a new Node of key, val and insert it into Linkedlist and Cache

    If the space is larger than capacity
    Depends on the policy, we randomly delete/delete LRU in the cache until the space is enough
    """

    def put(self, key, val):
        if sys.getsizeof(val) > self.cap:
            self.missed += 1
            self.total += 1
            return False

        if key in self.cache:
            self.remove(self.cache[key])
            self.space -= sys.getsizeof(self.cache[key].value)
            self.size -= 1

        new_node = Node(key, val)
        self.cache[key] = new_node
        self.insert(self.cache[key])
        self.space += sys.getsizeof(val)
        self.size += 1

        while self.space > self.cap:
            if self.policy == 'LRU':

                lru = self.left.next
                self.invalidateKey(lru.key)

            else:
                random_key = random.choice(list(self.cache))
                self.invalidateKey(random_key)

        return True

    """
    Clear Everything in the Cache
    """

    def clear(self):
        self.space = 0
        self.size = 0
        self.cache.clear()
        self.right.prev = self.left
        self.left.next = self.right

    """
    Remove value from Cache
    Decrease size, space of Cache
    Remove it from the dictionary
    """

    def invalidateKey(self, key):
        self.total += 1
        removed = self.cache[key]
        self.space -= sys.getsizeof(removed.value)
        self.remove(removed)
        del self.cache[removed.key]
        self.size -= 1
        self.hit += 1

    """
    size : nums of items
    space : allocated space in cache
    total : total request
    hit : hitting request
    missed : missed request
    """
    def updateStats(self):
       db.put_stats(self.size, self.space, self.total, self.hit, self.missed)

    """
    update new capacity and policy
    """
    def refreshConfiguration(self):
        conf = db.get_config()
        self.cap = conf[0] * 1024 *1024
        self.policy = conf[1]


    def getMissRate(self):
        return self.missed / self.total if self.total != 0 else 0

    def getHitRate(self):
        return self.hit / self.total if self.total != 0 else 0

    def getItemInCache(self):
        return self.size

    def getCapacityLeft(self):
        return (self.cap - self.space) / (1024 ** 2)

    def getSpace(self):
        return self.space / (1024 ** 2)

    def getCap(self):
        return self.cap / (1024 ** 2)