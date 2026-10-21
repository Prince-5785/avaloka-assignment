# Avaloka Assignment

This repository contains implementations for two problems:
1. **Thread-Safe LRU Cache** ([`lru_cache.py`](lru_cache.py))
2. **Event & Meeting Scheduler** ([`scheduler.py`](scheduler.py))

Along with a comprehensive test suite ([`test_all.py`](test_all.py)).

---

## Prerequisites

- **Python 3.8+**
- No external packages or dependencies are required. All implementations rely strictly on Python standard libraries (`threading`, `heapq`, `datetime`, `fractions`, `decimal`, `math`, `random`).

---

## Running the Tests

To run the complete test suite, execute the following command from the project root:

```bash
python3 test_all.py
```

### Expected Output

Upon successful execution, the test suite will exit with code `0` and print:

```text
['Room A', 'Room B', 'Room A']
all ok
zero-duration ok
validation ok
extra edge cases ok
```

---

## Project Structure

```text
├── lru_cache.py     # Thread-safe LRU Cache implementation using HashMap + Doubly Linked List
├── scheduler.py     # Interval scheduling algorithms (can_attend_all, min_rooms_required, assign_rooms)
├── test_all.py      # Unit, edge-case, validation, and multi-threaded stress tests
└── README.md        # Project documentation and run instructions
```

---

## Features & Usage

### 1. LRU Cache (`lru_cache.py`)

A thread-safe Least Recently Used (LRU) Cache supporting $O(1)$ average time complexity for both `get` and `put` operations.

```python
from lru_cache import LRUCache

# Initialize with positive integer capacity
cache = LRUCache(2)

cache.put(1, 100)
cache.put(2, 200)

print(cache.get(1))  # Returns 100
cache.put(3, 300)     # Evicts key 2 (least recently used)
print(cache.get(2))  # Returns -1 (not found)
```

**Key highlights:**
- Backed by a doubly linked list with dummy head and tail nodes.
- Thread-safe using `threading.RLock`.
- Comprehensive input validation for capacity, types, and unhashable keys.

---

### 2. Event Scheduler (`scheduler.py`)

Provides interval scheduling algorithms for meeting rooms and time intervals.

```python
from scheduler import can_attend_all, min_rooms_required, assign_rooms

meetings = [(9, 11), (10, 12), (11, 13)]

# Check if one person can attend all meetings without overlap
print(can_attend_all(meetings))  # False

# Minimum conference rooms required
print(min_rooms_required(meetings))  # 2

# Assign specific room names to each event
print(assign_rooms(meetings))  # ['Room A', 'Room B', 'Room A']
```

**Key highlights:**
- Uses a min-heap (`heapq`) for optimal $O(N \log N)$ room scheduling.
- Reuses freed rooms greedily.
- Supports comparable types such as `int`, `float`, `datetime`, `Decimal`, and `Fraction`.
- Validates intervals against `None`, `NaN`, reversed intervals (`end < start`), and improper structures.
