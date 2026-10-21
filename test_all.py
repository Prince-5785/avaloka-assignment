from lru_cache import LRUCache
from scheduler import *
import threading
c = LRUCache(2)
c.put(1, 1); c.put(2, 2); assert c.get(1) == 1
c.put(3, 3); assert c.get(2) == -1
c.put(4, 4); assert c.get(1) == -1 and c.get(3) == 3 and c.get(4) == 4
c.put(3, 30); assert c.get(3) == 30
assert can_attend_all([(9,10),(10,11),(11,12)]) is True
assert can_attend_all([(9,11),(10,12)]) is False
assert can_attend_all([]) is True
assert min_rooms_required([(9,10),(10,11),(11,12)]) == 1
assert min_rooms_required([(9,11),(10,12),(10,13)]) == 3
assert min_rooms_required([(0,30),(5,10),(15,20)]) == 2
assert min_rooms_required([]) == 0
print(assign_rooms([(9,11),(10,12),(11,13)]))
c = LRUCache(50)
def w(k):
    for i in range(5000): c.put(i % 100 + k, i); c.get(i % 100)
ts = [threading.Thread(target=w, args=(k,)) for k in range(8)]
[t.start() for t in ts]; [t.join() for t in ts]
assert len(c.map) <= 50
print("all ok")
# zero-duration events (start == end) are valid and still need a room
assert can_attend_all([(9,9),(9,10)]) is True
assert can_attend_all([(8,10),(9,9)]) is False
assert min_rooms_required([(9,9)]) == 1
assert min_rooms_required([(9,9),(9,10)]) == 1
assert min_rooms_required([(9,9),(9,9)]) == 1
assert min_rooms_required([(8,10),(9,9)]) == 2
print("zero-duration ok")

def raises(exc, f, *a):
    try: f(*a)
    except exc: return True
    return False

# input validation
assert raises(ValueError, can_attend_all, [(10, 9)])
assert raises(ValueError, min_rooms_required, [(1, 2, 3)])
assert raises(TypeError, assign_rooms, [(1, "a")])
assert can_attend_all(None) is True and min_rooms_required(None) == 0 and assign_rooms(None) == []
assert assign_rooms(iter([(1, 2), (2, 3)])) == ["Room A", "Room A"]
assert min_rooms_required([[1, 2], [2, 3]]) == 1                 # lists work too
assert min_rooms_required([(1.5, 2.5), (2.0, 3)]) == 2           # floats work
assert min_rooms_required([(9, 10), (9, 10), (9, 10)]) == 3      # identical events
assert can_attend_all([(9, 10)]) is True                         # single event
events = [(9, 11), (10, 12)]
min_rooms_required(events); assert events == [(9, 11), (10, 12)] # input not mutated
for bad in (0, -1, 1.5, True, None, "3"):
    assert raises((ValueError, TypeError), LRUCache, bad)
one = LRUCache(1)
one.put(1, 1); one.put(2, 2)
assert one.get(1) == -1 and one.get(2) == 2 and len(one) == 1
one.put(2, 3); assert one.get(2) == 3 and len(one) == 1          # update at full capacity, no eviction
print("validation ok")

# NaN, datetimes and other number types
import datetime as dt, fractions, decimal, math
nan = float("nan")
assert raises(ValueError, min_rooms_required, [(nan, 5)])
assert raises(ValueError, can_attend_all, [(1, nan)])
assert raises(TypeError, min_rooms_required, [("9", "10")])
assert raises(TypeError, min_rooms_required, [(None, 5)])
assert raises(ValueError, min_rooms_required, ["ab"])
assert raises(TypeError, min_rooms_required, [(1, 2), (dt.datetime(2026, 1, 1), dt.datetime(2026, 1, 2))])
d = dt.datetime(2026, 1, 1, 9)
h = dt.timedelta(hours=1)
assert min_rooms_required([(d, d + h), (d + h, d + 2 * h)]) == 1
assert min_rooms_required([(d, d + 2 * h), (d + h, d + 3 * h)]) == 2
assert assign_rooms([(d, d + h), (d + h, d + 2 * h)]) == ["Room A", "Room A"]
assert min_rooms_required([(fractions.Fraction(1, 2), 1), (1, 2)]) == 1
assert min_rooms_required([(decimal.Decimal("1"), decimal.Decimal("3")), (2, 4)]) == 2
assert min_rooms_required([(0, math.inf), (5, math.inf)]) == 2
big = [(i, i + 1) for i in range(100000)]                        # 100k back-to-back events
assert min_rooms_required(big) == 1 and can_attend_all(big)
assert len(set(assign_rooms([(0, 10)] * 30))) == 30              # more than 26 rooms get unique names

# LRU: unhashable key fails cleanly and leaves cache untouched
c = LRUCache(2); c.put(1, 1)
assert raises(TypeError, c.put, [1], 1) and raises(TypeError, c.get, [1])
assert len(c) == 1 and c.get(1) == 1

# threaded run: structure must stay consistent (map and list agree, never above capacity)
c = LRUCache(20)
def worker(seed):
    import random
    r = random.Random(seed)
    for _ in range(20000):
        k = r.randint(0, 60)
        c.put(k, k) if r.random() < .5 else c.get(k)
ts = [threading.Thread(target=worker, args=(i,)) for i in range(8)]
[x.start() for x in ts]; [x.join() for x in ts]
keys, n = [], c.head.next
while n is not c.tail: keys.append(n.key); n = n.next
assert len(keys) == len(set(keys)) == len(c.map) <= 20 and set(keys) == set(c.map)
print("extra edge cases ok")
