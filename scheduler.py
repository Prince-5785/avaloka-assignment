import heapq


def _validate(events):
    """Return a clean list of (start, end) tuples or raise a clear error.

    Times can be any values that compare with each other (ints, floats,
    datetimes, ...). Strings, None, bools and NaN are rejected.
    """
    if events is None:
        return []                                   # no events -> nothing to schedule
    cleaned = []
    for ev in events:
        if isinstance(ev, (str, bytes)):
            raise ValueError(f"event must be a (start, end) pair, got {ev!r}")
        try:
            start, end = ev
        except (TypeError, ValueError):
            raise ValueError(f"event must be a (start, end) pair, got {ev!r}") from None
        for t in (start, end):
            if t is None or isinstance(t, (str, bytes, bool)):
                raise TypeError(f"start and end must be numbers or datetimes, got {ev!r}")
            if t != t:                              # NaN is the only value not equal to itself
                raise ValueError(f"time value is NaN in {ev!r}")
        try:
            reversed_times = end < start
        except TypeError:
            raise TypeError(f"start and end cannot be compared in {ev!r}") from None
        if reversed_times:
            raise ValueError(f"end time is before start time in {ev!r}")
        cleaned.append((start, end))
    return cleaned


def can_attend_all(events):
    events = sorted(_validate(events))
    for i in range(1, len(events)):
        if events[i][0] < events[i - 1][1]:      # strict: touching is OK
            return False
    return True


def min_rooms_required(events):
    """Min-heap of end times of meetings currently occupying a room."""
    heap = []
    peak = 0
    for s, e in sorted(_validate(events)):
        while heap and heap[0] <= s:     # earliest meeting already over -> reuse its room
            heapq.heappop(heap)
        heapq.heappush(heap, e)
        peak = max(peak, len(heap))
    return peak


def assign_rooms(events):
    """Returns a list of room names, one per event, in the original order."""
    events = _validate(events)
    order = sorted(range(len(events)), key=lambda i: events[i])
    busy, free, result, count = [], [], [None] * len(events), 0
    for i in order:
        s, e = events[i]
        while busy and busy[0][0] <= s:
            heapq.heappush(free, heapq.heappop(busy)[1])
        if free:
            r = heapq.heappop(free)
        else:
            r = count
            count += 1
        result[i] = f"Room {chr(65 + r) if r < 26 else r + 1}"
        heapq.heappush(busy, (e, r))
    return result
