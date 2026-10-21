import threading


class _Node:
    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key=0, value=0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, capacity: int):
        if isinstance(capacity, bool) or not isinstance(capacity, int):
            raise TypeError("capacity must be an integer")
        if capacity <= 0:
            raise ValueError("capacity must be a positive integer")
        self.capacity = capacity
        self.map = {}                      # key -> node
        self.head = _Node()                # dummy head (most recent side)
        self.tail = _Node()                # dummy tail (least recent side)
        self.head.next = self.tail
        self.tail.prev = self.head
        self._lock = threading.RLock()     # makes it thread-safe

    def _remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_front(self, node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def __len__(self):
        with self._lock:
            return len(self.map)

    def get(self, key):
        with self._lock:
            node = self.map.get(key)
            if node is None:
                return -1
            self._remove(node)
            self._add_front(node)
            return node.value

    def put(self, key, value):
        with self._lock:
            node = self.map.get(key)
            if node:
                node.value = value
                self._remove(node)
                self._add_front(node)
                return
            if len(self.map) >= self.capacity:
                lru = self.tail.prev
                self._remove(lru)
                del self.map[lru.key]
            node = _Node(key, value)
            self.map[key] = node
            self._add_front(node)
